"""
Alts_ShortBreak_15m 戦略
=========================
15分足 レンジブレイク × 複数アルト銘柄（SOL, HYPE, WIF等）。

ロジック:
1. 15分足で直近20本の高値/安値レンジを算出
2. ブレイク + 出来高2.5倍以上でエントリー
3. 偽ブレイク回避: エントリー後5分以内に逆行 → 即損切り
4. TP1 1.5%で半分利確、残りはATR×2.5トレーリング
5. レバレッジ15x
"""

import time
import logging
import pandas as pd
import numpy as np
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class Alts15mBreakStrategy:
    """アルト 15分足 ショートブレイク戦略（複数銘柄対応）"""

    STRATEGY_NAME_PREFIX = "Alts_15m_Break"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram, coin: str):
        """
        Args:
            coin: 対象銘柄（SOL, HYPE, WIF等）
        """
        self.info = info
        self.exchange = exchange
        self.cfg = config["alts_15m_break"]
        self.risk_manager = risk_manager
        self.telegram = telegram
        self.coin = coin
        self.strategy_name = f"{self.STRATEGY_NAME_PREFIX}_{coin}"

        self.leverage = self.cfg["leverage"]
        self.range_period = self.cfg["range_period"]
        self.vol_multiplier = self.cfg["volume_multiplier"]
        self.fake_break_timeout = self.cfg["fake_break_timeout_sec"]
        self.fake_break_revert_pct = self.cfg["fake_break_revert_pct"]
        self.tp1_pct = self.cfg["tp1_pct"]
        self.tp1_close_ratio = self.cfg["tp1_close_ratio"]
        self.atr_period = self.cfg["atr_period"]
        self.atr_trailing_mult = self.cfg["atr_trailing_multiplier"]
        self.sl_pct = self.cfg["sl_pct"]
        self.candle_count = self.cfg["candle_count"]
        self.interval = self.cfg["interval"]
        self.loop_interval = self.cfg["loop_interval_sec"]

        self.position: Optional[dict] = None
        self.running = True

    def run(self):
        """メインループ"""
        logger.info(f"[{self.strategy_name}] 戦略開始 - {self.coin} {self.interval}")
        try:
            self.exchange.update_leverage(self.leverage, self.coin)
        except Exception as e:
            logger.error(f"[{self.strategy_name}] レバレッジ設定失敗: {e}")

        while self.running:
            try:
                self._tick()
            except Exception as e:
                logger.error(f"[{self.strategy_name}] ティックエラー: {e}", exc_info=True)
            time.sleep(self.loop_interval)

    def stop(self):
        self.running = False

    def _tick(self):
        """1ティック処理"""
        if self.risk_manager.check_daily_drawdown():
            if self.position:
                self._close_position("日次DD制限", close_all=True)
            return

        df = self._get_candles()
        if df is None or len(df) < max(self.range_period, self.atr_period) + 5:
            return

        current_price = df["close"].iloc[-1]

        if self.position:
            self._manage_position(current_price, df)
            return

        if not self.risk_manager.can_open_position(self.strategy_name):
            return

        signal = self._check_entry_signal(df)
        if signal:
            self._open_position(signal, current_price, df)

    def _get_candles(self) -> Optional[pd.DataFrame]:
        """15分足キャンドルを取得"""
        try:
            candles = self.info.candles_snapshot(self.coin, self.interval, self.candle_count)
            if not candles:
                return None

            df = pd.DataFrame(candles)
            df = df.rename(columns={
                "o": "open", "h": "high", "l": "low", "c": "close",
                "v": "volume", "t": "timestamp"
            })
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    df[col] = df[col].astype(float)

            # ATR計算
            df["tr"] = np.maximum(
                df["high"] - df["low"],
                np.maximum(
                    abs(df["high"] - df["close"].shift(1)),
                    abs(df["low"] - df["close"].shift(1))
                )
            )
            df["atr"] = df["tr"].rolling(window=self.atr_period).mean()

            # 出来高MA
            df["vol_ma"] = df["volume"].rolling(window=self.range_period).mean()

            return df
        except Exception as e:
            logger.error(f"[{self.strategy_name}] キャンドル取得エラー: {e}")
            return None

    def _check_entry_signal(self, df: pd.DataFrame) -> Optional[str]:
        """
        レンジブレイクシグナル判定。
        直近range_period本の高値/安値を突破 + 出来高確認。
        """
        curr = df.iloc[-1]
        current_price = curr["close"]
        current_volume = curr["volume"]
        vol_ma = curr["vol_ma"]

        if pd.isna(vol_ma) or vol_ma == 0:
            return None

        # 直近range_period本のレンジ（現在足を除く）
        lookback = df.iloc[-(self.range_period + 1):-1]
        range_high = lookback["high"].max()
        range_low = lookback["low"].min()

        vol_ratio = current_volume / vol_ma

        # ブレイクアウト上方: 高値ブレイク + 出来高条件
        if current_price > range_high and vol_ratio >= self.vol_multiplier:
            logger.info(
                f"[{self.strategy_name}] 上方ブレイク検出: "
                f"価格={current_price:.4f} > レンジ高値={range_high:.4f}, "
                f"出来高比={vol_ratio:.1f}x"
            )
            return "long"

        # ブレイクアウト下方: 安値ブレイク + 出来高条件
        if current_price < range_low and vol_ratio >= self.vol_multiplier:
            logger.info(
                f"[{self.strategy_name}] 下方ブレイク検出: "
                f"価格={current_price:.4f} < レンジ安値={range_low:.4f}, "
                f"出来高比={vol_ratio:.1f}x"
            )
            return "short"

        return None

    def _open_position(self, signal: str, current_price: float, df: pd.DataFrame):
        """ポジションを開く"""
        is_buy = signal == "long"
        side = "buy" if is_buy else "sell"

        size = self.risk_manager.calculate_position_size(
            strategy_name=self.strategy_name,
            leverage=self.leverage,
            entry_price=current_price,
            sl_pct=self.sl_pct,
            is_btc=False  # アルト戦略
        )

        if size <= 0:
            return

        try:
            result = self.exchange.market_open(self.coin, is_buy, size, None, 0.01)
            logger.info(f"[{self.strategy_name}] 注文結果: {result}")

            # ATR取得（トレーリング用）
            current_atr = df["atr"].iloc[-1] if not pd.isna(df["atr"].iloc[-1]) else 0

            if is_buy:
                sl_price = current_price * (1 - self.sl_pct / 100)
                tp1_price = current_price * (1 + self.tp1_pct / 100)
            else:
                sl_price = current_price * (1 + self.sl_pct / 100)
                tp1_price = current_price * (1 - self.tp1_pct / 100)

            self.position = {
                "side": side,
                "size": size,
                "original_size": size,
                "entry_price": current_price,
                "entry_time": time.time(),
                "sl": sl_price,
                "tp1": tp1_price,
                "tp1_hit": False,
                "atr": current_atr,
                "highest": current_price if is_buy else None,
                "lowest": current_price if not is_buy else None,
            }

            self.risk_manager.register_position(
                self.strategy_name, self.coin, side, size, current_price
            )
            self.telegram.notify_entry(
                self.strategy_name, self.coin, side, size, current_price, self.leverage
            )

        except Exception as e:
            logger.error(f"[{self.strategy_name}] 注文エラー: {e}", exc_info=True)

    def _manage_position(self, current_price: float, df: pd.DataFrame):
        """ポジション管理: 偽ブレイク回避 + TP1分割利確 + ATRトレーリング"""
        if not self.position:
            return

        is_long = self.position["side"] == "buy"
        entry = self.position["entry_price"]
        elapsed = time.time() - self.position["entry_time"]

        # === 偽ブレイク回避 ===
        # エントリー後5分以内に逆行（fake_break_revert_pct以上）したら即損切り
        if elapsed <= self.fake_break_timeout:
            if is_long:
                revert_pct = ((entry - current_price) / entry) * 100
            else:
                revert_pct = ((current_price - entry) / entry) * 100

            if revert_pct >= self.fake_break_revert_pct:
                logger.warning(
                    f"[{self.strategy_name}] 偽ブレイク検出: "
                    f"逆行{revert_pct:.2f}% ({elapsed:.0f}秒経過)"
                )
                self._close_position("偽ブレイク損切り", close_all=True)
                return

        # 最高値/最安値更新
        if is_long:
            if self.position["highest"] is None or current_price > self.position["highest"]:
                self.position["highest"] = current_price
        else:
            if self.position["lowest"] is None or current_price < self.position["lowest"]:
                self.position["lowest"] = current_price

        # SLチェック
        if is_long and current_price <= self.position["sl"]:
            self._close_position("SLヒット", close_all=True)
            return
        elif not is_long and current_price >= self.position["sl"]:
            self._close_position("SLヒット", close_all=True)
            return

        # === TP1: 1.5%で半分利確 ===
        if not self.position["tp1_hit"]:
            if is_long and current_price >= self.position["tp1"]:
                self._partial_close("TP1到達")
            elif not is_long and current_price <= self.position["tp1"]:
                self._partial_close("TP1到達")
            return

        # === TP1後: ATRトレーリングストップ ===
        atr = self.position["atr"]
        if atr > 0:
            trailing_distance = atr * self.atr_trailing_mult
            if is_long:
                new_sl = self.position["highest"] - trailing_distance
                if new_sl > self.position["sl"]:
                    self.position["sl"] = new_sl
                    logger.debug(f"[{self.strategy_name}] ATRトレーリングSL: {new_sl:.4f}")
            else:
                new_sl = self.position["lowest"] + trailing_distance
                if new_sl < self.position["sl"]:
                    self.position["sl"] = new_sl
                    logger.debug(f"[{self.strategy_name}] ATRトレーリングSL: {new_sl:.4f}")

    def _partial_close(self, reason: str):
        """TP1で半分利確"""
        if not self.position:
            return

        close_size = self.position["original_size"] * self.tp1_close_ratio

        try:
            is_buy = self.position["side"] == "buy"
            # 半分を反対売買
            result = self.exchange.market_open(
                self.coin, not is_buy, close_size, None, 0.01
            )
            logger.info(f"[{self.strategy_name}] 半分利確: {reason}, 結果: {result}")

            self.position["size"] -= close_size
            self.position["tp1_hit"] = True

            # SLをエントリー価格に引き上げ（建値ストップ）
            self.position["sl"] = self.position["entry_price"]

            self.telegram.notify_exit(
                self.strategy_name, self.coin, self.position["side"],
                self.position["entry_price"],
                self._get_mid_price() or self.position["entry_price"],
                0, 0  # 部分決済なので概算は省略
            )

        except Exception as e:
            logger.error(f"[{self.strategy_name}] 半分利確エラー: {e}", exc_info=True)

    def _close_position(self, reason: str, close_all: bool = True):
        """ポジション全決済"""
        if not self.position:
            return

        try:
            result = self.exchange.market_close(self.coin)
            logger.info(f"[{self.strategy_name}] 決済: {reason}, 結果: {result}")

            entry = self.position["entry_price"]
            is_buy = self.position["side"] == "buy"
            mid = self._get_mid_price()
            if mid and entry > 0:
                pnl_pct = ((mid - entry) / entry * 100) if is_buy else ((entry - mid) / entry * 100)
                pnl = pnl_pct / 100 * entry * self.position["size"]
            else:
                pnl, pnl_pct = 0.0, 0.0

            self.telegram.notify_exit(
                self.strategy_name, self.coin, self.position["side"],
                entry, mid or entry, pnl, pnl_pct
            )
            self.risk_manager.unregister_position(self.strategy_name)
            self.position = None

        except Exception as e:
            logger.error(f"[{self.strategy_name}] 決済エラー: {e}", exc_info=True)

    def _get_mid_price(self) -> Optional[float]:
        try:
            all_mids = self.info.all_mids()
            return float(all_mids.get(self.coin, 0))
        except Exception:
            return None
