"""
BTC_1m_UltraScalp 戦略
======================
1分足 FVG（Fair Value Gap） + Order Block によるBTCウルトラスキャルピング。

ロジック:
1. 1分足キャンドルを取得
2. FVG検知: Bullish = high[i-2] < low[i], Bearish = low[i-2] > high[i]
3. Order Block: 直近Swing High/Lowの直前キャンドルボディをOBゾーンとして認識
4. EMA9/21でトレンドバイアス確認
5. FVGゾーン + OBゾーン + EMAバイアスが一致した場合エントリー
6. SL = ATR × 倍率（動的SL - ボラティリティ適応）
7. TP = SLの2倍以上（R:R 1:2保証）
8. トレーリングストップ
9. レバレッジ3x
"""

import time
import logging
import pandas as pd
import numpy as np
from typing import Optional, Tuple
from utils import validate_order_result, place_exchange_sl, update_exchange_sl, cancel_exchange_sl

logger = logging.getLogger(__name__)


class BTC1mFVGStrategy:
    """BTC 1分足 FVG + Order Block スキャルピング戦略"""

    STRATEGY_NAME = "BTC_1m_UltraScalp"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram):
        """
        Args:
            info: Hyperliquid Info インスタンス
            exchange: Hyperliquid Exchange インスタンス
            config: config.json の btc_1m_fvg セクション
            risk_manager: RiskManager インスタンス
            telegram: TelegramAlert インスタンス
        """
        self.info = info
        self.exchange = exchange
        self.cfg = config["btc_1m_fvg"]
        self.risk_manager = risk_manager
        self.telegram = telegram

        self.coin = self.cfg["coin"]
        self.leverage = self.cfg["leverage"]
        self.ema_fast = self.cfg["ema_fast"]
        self.ema_slow = self.cfg["ema_slow"]
        self.tp_min = self.cfg["tp_min_pct"]
        self.tp_max = self.cfg["tp_max_pct"]
        self.sl_pct = self.cfg["sl_pct"]              # フォールバック固定SL
        self.atr_period = self.cfg.get("atr_period", 14)
        self.atr_sl_multiplier = self.cfg.get("atr_sl_multiplier", 1.5)
        self.min_rr_ratio = self.cfg.get("min_rr_ratio", 2.0)  # 最低R:R比
        self.trailing_activation = self.cfg["trailing_activation_pct"]
        self.trailing_step = self.cfg["trailing_step_pct"]
        self.candle_count = self.cfg["candle_count"]
        self.interval = self.cfg["interval"]
        self.loop_interval = self.cfg["loop_interval_sec"]

        # アカウントアドレス（取引所SL注文用）
        self.account_address = config["account_address"]

        # ポジション状態
        self.position: Optional[dict] = None  # {side, size, entry_price, sl, tp, highest/lowest}
        self._sl_oid: Optional[int] = None  # 取引所SL注文のorder ID
        self.running = True

    def run(self):
        """メインループ（threadingから呼ばれる）"""
        logger.info(f"[{self.STRATEGY_NAME}] 戦略開始 - {self.coin} {self.interval}")

        # レバレッジ設定
        try:
            self.exchange.update_leverage(self.leverage, self.coin)
            logger.info(f"[{self.STRATEGY_NAME}] レバレッジ設定: {self.leverage}x")
        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] レバレッジ設定失敗: {e}")

        while self.running:
            try:
                self._tick()
            except Exception as e:
                logger.error(f"[{self.STRATEGY_NAME}] ティックエラー: {e}", exc_info=True)
            time.sleep(self.loop_interval)

    def stop(self):
        """戦略停止"""
        self.running = False
        logger.info(f"[{self.STRATEGY_NAME}] 停止シグナル受信")

    def _tick(self):
        """1ティック処理"""
        # 日次DDチェック
        if self.risk_manager.check_daily_drawdown():
            if self.position:
                self._close_position("日次DD制限")
            return

        # キャンドルデータ取得
        df = self._get_candles()
        if df is None or len(df) < self.candle_count:
            return

        # BTC価格をリスクマネージャーに通知（相関監視用）
        current_price = df["close"].iloc[-1]
        self.risk_manager.update_btc_price(current_price)

        # ポジション保有中 → トレーリング/TP/SL管理
        if self.position:
            self._manage_position(current_price)
            return

        # ポジションなし → エントリーシグナル探索
        signal = self._check_entry_signal(df)
        if signal:
            side = "buy" if signal == "long" else "sell"
            if not self.risk_manager.can_open_position(self.STRATEGY_NAME, self.coin, side):
                return
            self._open_position(signal, current_price, df)

    def _get_candles(self) -> Optional[pd.DataFrame]:
        """1分足キャンドルを取得してDataFrameに変換"""
        try:
            # SDK v0.22+ では startTime, endTime が必須
            import time
            end_time = int(time.time() * 1000)
            start_time = end_time - self.candle_count * 60 * 1000  # 1m = 60s
            candles = self.info.candles_snapshot(self.coin, self.interval, start_time, end_time)
            if not candles:
                return None

            df = pd.DataFrame(candles)
            # カラム名をSDKの出力に合わせて調整
            df = df.rename(columns={
                "o": "open", "h": "high", "l": "low", "c": "close",
                "v": "volume", "t": "timestamp"
            })
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    df[col] = df[col].astype(float)

            # EMA計算
            df["ema_fast"] = df["close"].ewm(span=self.ema_fast, adjust=False).mean()
            df["ema_slow"] = df["close"].ewm(span=self.ema_slow, adjust=False).mean()

            # ATR計算（動的SL用）
            df["tr"] = np.maximum(
                df["high"] - df["low"],
                np.maximum(
                    abs(df["high"] - df["close"].shift(1)),
                    abs(df["low"] - df["close"].shift(1))
                )
            )
            df["atr"] = df["tr"].rolling(window=self.atr_period).mean()

            return df
        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] キャンドル取得エラー: {e}")
            return None

    def _detect_fvg(self, df: pd.DataFrame) -> list:
        """
        FVG（Fair Value Gap）検出。
        Bullish FVG: high[i-2] < low[i] → 間にギャップ
        Bearish FVG: low[i-2] > high[i] → 間にギャップ

        Returns:
            FVGリスト [{type, top, bottom, index}]
        """
        fvgs = []
        for i in range(2, len(df)):
            # Bullish FVG: i-2本目のhighがi本目のlowより低い
            if df["high"].iloc[i - 2] < df["low"].iloc[i]:
                fvgs.append({
                    "type": "bullish",
                    "top": df["low"].iloc[i],
                    "bottom": df["high"].iloc[i - 2],
                    "index": i
                })
            # Bearish FVG: i-2本目のlowがi本目のhighより高い
            elif df["low"].iloc[i - 2] > df["high"].iloc[i]:
                fvgs.append({
                    "type": "bearish",
                    "top": df["low"].iloc[i - 2],
                    "bottom": df["high"].iloc[i],
                    "index": i
                })
        return fvgs

    def _detect_order_blocks(self, df: pd.DataFrame) -> list:
        """
        Order Block検出。
        Swing High直前の陽線ボディ = Bearish OB（供給ゾーン）
        Swing Low直前の陰線ボディ = Bullish OB（需要ゾーン）

        直近5本を見てSwingポイントを特定。
        """
        obs = []
        lookback = 5

        for i in range(lookback, len(df) - lookback):
            # Swing High: i番目のhighが前後lookback本より高い
            is_swing_high = all(
                df["high"].iloc[i] > df["high"].iloc[i - j]
                and df["high"].iloc[i] > df["high"].iloc[i + j]
                for j in range(1, min(lookback, len(df) - i))
                if i + j < len(df)
            )

            if is_swing_high and i > 0:
                # 直前のキャンドルがOB
                ob_candle = df.iloc[i - 1]
                obs.append({
                    "type": "bearish_ob",
                    "top": max(ob_candle["open"], ob_candle["close"]),
                    "bottom": min(ob_candle["open"], ob_candle["close"]),
                    "index": i - 1
                })

            # Swing Low: i番目のlowが前後lookback本より低い
            is_swing_low = all(
                df["low"].iloc[i] < df["low"].iloc[i - j]
                and df["low"].iloc[i] < df["low"].iloc[i + j]
                for j in range(1, min(lookback, len(df) - i))
                if i + j < len(df)
            )

            if is_swing_low and i > 0:
                ob_candle = df.iloc[i - 1]
                obs.append({
                    "type": "bullish_ob",
                    "top": max(ob_candle["open"], ob_candle["close"]),
                    "bottom": min(ob_candle["open"], ob_candle["close"]),
                    "index": i - 1
                })

        return obs

    def _check_entry_signal(self, df: pd.DataFrame) -> Optional[str]:
        """
        エントリーシグナル判定。
        FVG + Order Block + EMAバイアスが一致する場合のみ。

        Returns:
            "long", "short", または None
        """
        current_price = df["close"].iloc[-1]
        ema_fast_val = df["ema_fast"].iloc[-1]
        ema_slow_val = df["ema_slow"].iloc[-1]

        # EMAバイアス
        bullish_bias = ema_fast_val > ema_slow_val
        bearish_bias = ema_fast_val < ema_slow_val

        # FVG検出（直近10本以内のみ有効）
        fvgs = self._detect_fvg(df)
        recent_fvgs = [f for f in fvgs if f["index"] >= len(df) - 10]

        # Order Block検出（直近20本以内のみ有効）
        obs = self._detect_order_blocks(df)
        recent_obs = [o for o in obs if o["index"] >= len(df) - 20]

        # ロングシグナル: Bullish FVGゾーンに価格が入り + Bullish OBと重なる + EMA上向き
        if bullish_bias:
            for fvg in recent_fvgs:
                if fvg["type"] == "bullish" and fvg["bottom"] <= current_price <= fvg["top"]:
                    # Bullish OBと重なるか確認
                    for ob in recent_obs:
                        if ob["type"] == "bullish_ob":
                            # OBゾーンとFVGゾーンがオーバーラップ
                            if ob["bottom"] <= fvg["top"] and ob["top"] >= fvg["bottom"]:
                                logger.info(
                                    f"[{self.STRATEGY_NAME}] ロングシグナル検出: "
                                    f"FVG={fvg}, OB={ob}, EMA=Bullish"
                                )
                                return "long"

        # ショートシグナル: Bearish FVGゾーン + Bearish OB + EMA下向き
        if bearish_bias:
            for fvg in recent_fvgs:
                if fvg["type"] == "bearish" and fvg["bottom"] <= current_price <= fvg["top"]:
                    for ob in recent_obs:
                        if ob["type"] == "bearish_ob":
                            if ob["bottom"] <= fvg["top"] and ob["top"] >= fvg["bottom"]:
                                logger.info(
                                    f"[{self.STRATEGY_NAME}] ショートシグナル検出: "
                                    f"FVG={fvg}, OB={ob}, EMA=Bearish"
                                )
                                return "short"

        return None

    def _open_position(self, signal: str, current_price: float, df: pd.DataFrame = None):
        """ポジションを開く（ATRベース動的SL）"""
        is_buy = signal == "long"
        side = "buy" if is_buy else "sell"

        # ATRベースのSL幅を計算
        atr_sl_pct = self.sl_pct  # フォールバック
        if df is not None and "atr" in df.columns:
            current_atr = df["atr"].iloc[-1]
            if not pd.isna(current_atr) and current_atr > 0:
                atr_sl_pct = (current_atr * self.atr_sl_multiplier / current_price) * 100
                # 最低SL: 0.15%, 最大SL: 1.0%（暴走防止）
                atr_sl_pct = max(0.15, min(atr_sl_pct, 1.0))

        # R:R比チェック: TPがSLのmin_rr_ratio倍以上あるか
        tp_pct = self.tp_min
        if tp_pct < atr_sl_pct * self.min_rr_ratio:
            tp_pct = atr_sl_pct * self.min_rr_ratio
            if tp_pct > self.tp_max:
                logger.info(
                    f"[{self.STRATEGY_NAME}] R:R不足でスキップ: "
                    f"SL={atr_sl_pct:.3f}%, 必要TP={tp_pct:.3f}% > 上限{self.tp_max}%"
                )
                return

        # ポジションサイズ計算（ATRベースSLで計算）
        size = self.risk_manager.calculate_position_size(
            strategy_name=self.STRATEGY_NAME,
            leverage=self.leverage,
            entry_price=current_price,
            sl_pct=atr_sl_pct,
            is_btc=True
        )

        if size <= 0:
            return

        sz_decimals = self.exchange.info.asset_to_sz_decimals.get(self.coin, 5)
        size = round(size, sz_decimals)
        if size <= 0:
            return

        try:
            result = self.exchange.market_open(
                self.coin, is_buy, size, None, 0.01
            )
            logger.info(f"[{self.STRATEGY_NAME}] 注文結果: {result}")

            success, err_msg = validate_order_result(result)
            if not success:
                logger.error(f"[{self.STRATEGY_NAME}] 注文失敗: {err_msg}")
                return

            # ATRベース動的SL/TP設定
            if is_buy:
                sl_price = current_price * (1 - atr_sl_pct / 100)
                tp_price = current_price * (1 + tp_pct / 100)
            else:
                sl_price = current_price * (1 + atr_sl_pct / 100)
                tp_price = current_price * (1 - tp_pct / 100)

            logger.info(
                f"[{self.STRATEGY_NAME}] ATR動的SL: {atr_sl_pct:.3f}%, "
                f"TP: {tp_pct:.3f}%, R:R=1:{tp_pct/atr_sl_pct:.1f}"
            )

            self.position = {
                "side": side,
                "size": size,
                "entry_price": current_price,
                "sl": sl_price,
                "tp": tp_price,
                "highest": current_price if is_buy else None,
                "lowest": current_price if not is_buy else None,
                "trailing_active": False
            }

            # 取引所SL注文を配置
            self._sl_oid = place_exchange_sl(
                self.exchange, self.info, self.account_address,
                self.coin, is_buy, size, sl_price, self.STRATEGY_NAME
            )

            # リスクマネージャーに登録
            self.risk_manager.register_position(
                self.STRATEGY_NAME, self.coin, side, size, current_price
            )

            # Telegram通知
            self.telegram.notify_entry(
                self.STRATEGY_NAME, self.coin, side, size, current_price, self.leverage
            )

        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] 注文エラー: {e}", exc_info=True)

    def _manage_position(self, current_price: float):
        """ポジション管理: トレーリング、TP、SL"""
        if not self.position:
            return

        is_long = self.position["side"] == "buy"
        entry = self.position["entry_price"]

        # 現在のP&L%
        if is_long:
            pnl_pct = ((current_price - entry) / entry) * 100
            if self.position["highest"] is None or current_price > self.position["highest"]:
                self.position["highest"] = current_price
        else:
            pnl_pct = ((entry - current_price) / entry) * 100
            if self.position["lowest"] is None or current_price < self.position["lowest"]:
                self.position["lowest"] = current_price

        # SLヒット判定（ソフトウェアSL - 取引所SLのバックアップ）
        if is_long and current_price <= self.position["sl"]:
            self._close_position("SLヒット")
            return
        elif not is_long and current_price >= self.position["sl"]:
            self._close_position("SLヒット")
            return

        # TP到達判定
        if is_long and current_price >= self.position["tp"]:
            self._close_position("TP到達")
            return
        elif not is_long and current_price <= self.position["tp"]:
            self._close_position("TP到達")
            return

        # トレーリングストップ更新
        if pnl_pct >= self.trailing_activation:
            self.position["trailing_active"] = True

        if self.position["trailing_active"]:
            old_sl = self.position["sl"]
            if is_long:
                new_sl = self.position["highest"] * (1 - self.trailing_step / 100)
                if new_sl > self.position["sl"]:
                    self.position["sl"] = new_sl
            else:
                new_sl = self.position["lowest"] * (1 + self.trailing_step / 100)
                if new_sl < self.position["sl"]:
                    self.position["sl"] = new_sl

            # SL更新があれば取引所SL注文も更新
            if self.position["sl"] != old_sl:
                logger.debug(f"[{self.STRATEGY_NAME}] トレーリングSL更新: {self.position['sl']:.2f}")
                self._sl_oid = update_exchange_sl(
                    self.exchange, self.info, self.account_address,
                    self.coin, is_long, self.position["size"],
                    self.position["sl"], self._sl_oid, self.STRATEGY_NAME
                )

    def _close_position(self, reason: str):
        """ポジションクローズ"""
        if not self.position:
            return

        # 取引所SL注文をキャンセル
        if self._sl_oid:
            cancel_exchange_sl(self.exchange, self.coin, self._sl_oid, self.STRATEGY_NAME)
            self._sl_oid = None

        try:
            is_buy = self.position["side"] == "buy"
            result = self.exchange.market_close(self.coin)
            logger.info(f"[{self.STRATEGY_NAME}] 決済: {reason}, 結果: {result}")

            # P&L計算（概算）
            entry = self.position["entry_price"]
            # 現在価格を取得
            mid = self._get_mid_price()
            if mid and entry > 0:
                if is_buy:
                    pnl_pct = ((mid - entry) / entry) * 100
                else:
                    pnl_pct = ((entry - mid) / entry) * 100
                pnl = pnl_pct / 100 * entry * self.position["size"]
            else:
                pnl = 0.0
                pnl_pct = 0.0

            # Telegram通知
            self.telegram.notify_exit(
                self.STRATEGY_NAME, self.coin, self.position["side"],
                entry, mid or entry, pnl, pnl_pct
            )

            # リスクマネージャーから解除
            self.risk_manager.unregister_position(self.STRATEGY_NAME)
            self.position = None

        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] 決済エラー: {e}", exc_info=True)

    def _get_mid_price(self) -> Optional[float]:
        """現在のミッド価格を取得"""
        try:
            all_mids = self.info.all_mids()
            return float(all_mids.get(self.coin, 0))
        except Exception:
            return None
