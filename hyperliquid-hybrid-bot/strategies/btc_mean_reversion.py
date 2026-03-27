"""
BTC_MeanReversion 戦略
========================
逆張り: 下がったら買う、上がったら売る。

ロジック:
1. RSI(14) + ボリンジャーバンド(20, 2σ) で過熱/過売を検出
2. RSI ≤ 30 + 価格がBB下限タッチ → LONG（売られすぎ → 反発狙い）
3. RSI ≥ 70 + 価格がBB上限タッチ → SHORT（買われすぎ → 反落狙い）
4. TP = BBミドル（移動平均への回帰）
5. SL = ATRベース動的SL
6. 出来高スパイクで確認（セリクラ/バイクラ検出）
"""

import time
import logging
import pandas as pd
import numpy as np
from typing import Optional
from utils import (
    validate_order_result,
    place_exchange_sl, update_exchange_sl, cancel_exchange_sl
)

logger = logging.getLogger(__name__)


class BTCMeanReversionStrategy:
    """BTC 逆張りミーンリバージョン戦略"""

    STRATEGY_NAME = "BTC_MeanReversion"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram):
        self.info = info
        self.exchange = exchange
        self.cfg = config["btc_mean_reversion"]
        self.risk_manager = risk_manager
        self.telegram = telegram

        self.coin = self.cfg["coin"]
        self.leverage = self.cfg["leverage"]
        self.rsi_period = self.cfg["rsi_period"]
        self.rsi_oversold = self.cfg["rsi_oversold"]
        self.rsi_overbought = self.cfg["rsi_overbought"]
        self.bb_period = self.cfg["bb_period"]
        self.bb_std = self.cfg["bb_std"]
        self.atr_period = self.cfg["atr_period"]
        self.atr_sl_multiplier = self.cfg["atr_sl_multiplier"]
        self.vol_spike_mult = self.cfg["volume_spike_multiplier"]
        self.tp_bb_middle = self.cfg["tp_to_bb_middle"]
        self.sl_pct_max = self.cfg["sl_pct_max"]
        self.trailing_activation_pct = self.cfg["trailing_activation_pct"]
        self.trailing_step_pct = self.cfg["trailing_step_pct"]
        self.candle_count = self.cfg["candle_count"]
        self.interval = self.cfg["interval"]
        self.loop_interval = self.cfg["loop_interval_sec"]

        self.account_address = config["account_address"]
        self.position: Optional[dict] = None
        self.running = True
        self._sl_oid: Optional[int] = None

    def run(self):
        logger.info(f"[{self.STRATEGY_NAME}] 戦略開始 - {self.coin} {self.interval} MeanReversion")
        try:
            self.exchange.update_leverage(self.leverage, self.coin)
        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] レバレッジ設定失敗: {e}")

        while self.running:
            try:
                self._tick()
            except Exception as e:
                logger.error(f"[{self.STRATEGY_NAME}] ティックエラー: {e}", exc_info=True)
            time.sleep(self.loop_interval)

    def stop(self):
        self.running = False

    def _tick(self):
        if self.risk_manager.check_daily_drawdown():
            if self.position:
                self._close_position("日次DD制限")
            return

        df = self._get_candles()
        if df is None or len(df) < max(self.bb_period, self.rsi_period, self.atr_period) + 5:
            return

        current_price = df["close"].iloc[-1]
        self.risk_manager.update_btc_price(current_price)

        if self.position:
            self._manage_position(current_price, df)
            return

        signal = self._check_entry_signal(df)
        if signal:
            side = "buy" if signal == "long" else "sell"
            if not self.risk_manager.can_open_position(self.STRATEGY_NAME, self.coin, side):
                return
            self._open_position(signal, current_price, df)

    # ================================================================
    # データ取得 + インジケータ計算
    # ================================================================
    def _get_candles(self) -> Optional[pd.DataFrame]:
        try:
            end_time = int(time.time() * 1000)
            interval_sec = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600}.get(self.interval, 300)
            start_time = end_time - self.candle_count * interval_sec * 1000

            candles = self.info.candles_snapshot(self.coin, self.interval, start_time, end_time)
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

            # RSI
            df["rsi"] = self._calc_rsi(df["close"], self.rsi_period)

            # ボリンジャーバンド
            df["bb_mid"] = df["close"].rolling(window=self.bb_period).mean()
            bb_std = df["close"].rolling(window=self.bb_period).std()
            df["bb_upper"] = df["bb_mid"] + (bb_std * self.bb_std)
            df["bb_lower"] = df["bb_mid"] - (bb_std * self.bb_std)

            # ATR
            df["tr"] = np.maximum(
                df["high"] - df["low"],
                np.maximum(
                    abs(df["high"] - df["close"].shift(1)),
                    abs(df["low"] - df["close"].shift(1))
                )
            )
            df["atr"] = df["tr"].rolling(window=self.atr_period).mean()

            # 出来高MA
            df["vol_ma"] = df["volume"].rolling(window=20).mean()

            return df
        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] キャンドル取得エラー: {e}")
            return None

    @staticmethod
    def _calc_rsi(series: pd.Series, period: int) -> pd.Series:
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=period, min_periods=period).mean()
        avg_loss = loss.rolling(window=period, min_periods=period).mean()
        rs = avg_gain / avg_loss.replace(0, np.inf)
        return 100 - (100 / (1 + rs))

    # ================================================================
    # エントリーシグナル（逆張り）
    # ================================================================
    def _check_entry_signal(self, df: pd.DataFrame) -> Optional[str]:
        curr = df.iloc[-1]
        prev = df.iloc[-2]

        rsi = curr["rsi"]
        close = curr["close"]
        low = curr["low"]
        high = curr["high"]
        bb_lower = curr["bb_lower"]
        bb_upper = curr["bb_upper"]
        vol = curr["volume"]
        vol_ma = curr["vol_ma"]

        if pd.isna(rsi) or pd.isna(bb_lower) or pd.isna(vol_ma) or vol_ma == 0:
            return None

        vol_ratio = vol / vol_ma

        # === LONG: 売られすぎ → 反発狙い ===
        # RSI過売 + 安値がBB下限にタッチ + 陽線（反発開始）
        if (rsi <= self.rsi_oversold
                and low <= bb_lower
                and close > curr["open"]
                and vol_ratio >= self.vol_spike_mult):
            logger.info(
                f"[{self.STRATEGY_NAME}] LONG シグナル: "
                f"RSI={rsi:.1f}, BB下限={bb_lower:.2f}, "
                f"安値={low:.2f}, Vol比={vol_ratio:.1f}x"
            )
            return "long"

        # === SHORT: 買われすぎ → 反落狙い ===
        # RSI過熱 + 高値がBB上限にタッチ + 陰線（反落開始）
        if (rsi >= self.rsi_overbought
                and high >= bb_upper
                and close < curr["open"]
                and vol_ratio >= self.vol_spike_mult):
            logger.info(
                f"[{self.STRATEGY_NAME}] SHORT シグナル: "
                f"RSI={rsi:.1f}, BB上限={bb_upper:.2f}, "
                f"高値={high:.2f}, Vol比={vol_ratio:.1f}x"
            )
            return "short"

        return None

    # ================================================================
    # ポジション開閉
    # ================================================================
    def _open_position(self, signal: str, current_price: float, df: pd.DataFrame):
        is_buy = signal == "long"
        side = "buy" if is_buy else "sell"

        # ATRベースSL
        current_atr = df["atr"].iloc[-1]
        if pd.isna(current_atr) or current_atr <= 0:
            return

        atr_sl_pct = (current_atr * self.atr_sl_multiplier / current_price) * 100
        atr_sl_pct = min(atr_sl_pct, self.sl_pct_max)

        # TP = BBミドルまでの距離
        bb_mid = df["bb_mid"].iloc[-1]
        if pd.isna(bb_mid):
            return

        if is_buy:
            tp_pct = ((bb_mid - current_price) / current_price) * 100
        else:
            tp_pct = ((current_price - bb_mid) / current_price) * 100

        # TPが小さすぎる（すでにミドル付近）場合はスキップ
        if tp_pct < atr_sl_pct * 1.5:
            logger.info(
                f"[{self.STRATEGY_NAME}] R:R不足でスキップ: "
                f"TP={tp_pct:.3f}%, SL={atr_sl_pct:.3f}%"
            )
            return

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
            result = self.exchange.market_open(self.coin, is_buy, size, None, 0.01)
            logger.info(f"[{self.STRATEGY_NAME}] 注文結果: {result}")

            success, err_msg = validate_order_result(result)
            if not success:
                logger.error(f"[{self.STRATEGY_NAME}] 注文失敗: {err_msg}")
                return

            if is_buy:
                sl_price = current_price * (1 - atr_sl_pct / 100)
                tp_price = bb_mid if self.tp_bb_middle else current_price * (1 + tp_pct / 100)
            else:
                sl_price = current_price * (1 + atr_sl_pct / 100)
                tp_price = bb_mid if self.tp_bb_middle else current_price * (1 - tp_pct / 100)

            logger.info(
                f"[{self.STRATEGY_NAME}] 逆張りエントリー: {side} @ {current_price:.2f}, "
                f"SL={sl_price:.2f}({atr_sl_pct:.2f}%), TP={tp_price:.2f}(BB中央), "
                f"R:R=1:{tp_pct/atr_sl_pct:.1f}"
            )

            self.position = {
                "side": side,
                "size": size,
                "entry_price": current_price,
                "sl": sl_price,
                "tp": tp_price,
                "highest": current_price if is_buy else None,
                "lowest": current_price if not is_buy else None,
                "trailing_active": False,
            }

            self._sl_oid = place_exchange_sl(
                self.exchange, self.info, self.account_address,
                self.coin, is_buy, size, sl_price, self.STRATEGY_NAME
            )

            self.risk_manager.register_position(
                self.STRATEGY_NAME, self.coin, side, size, current_price
            )
            self.telegram.notify_entry(
                self.STRATEGY_NAME, self.coin, side, size, current_price, self.leverage
            )

        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] 注文エラー: {e}", exc_info=True)

    def _manage_position(self, current_price: float, df: pd.DataFrame):
        if not self.position:
            return

        is_long = self.position["side"] == "buy"
        entry = self.position["entry_price"]

        if is_long:
            pnl_pct = ((current_price - entry) / entry) * 100
            if self.position["highest"] is None or current_price > self.position["highest"]:
                self.position["highest"] = current_price
        else:
            pnl_pct = ((entry - current_price) / entry) * 100
            if self.position["lowest"] is None or current_price < self.position["lowest"]:
                self.position["lowest"] = current_price

        # SLチェック
        if is_long and current_price <= self.position["sl"]:
            self._close_position("SLヒット")
            return
        elif not is_long and current_price >= self.position["sl"]:
            self._close_position("SLヒット")
            return

        # TP = BBミドルに到達（動的TP）
        bb_mid = df["bb_mid"].iloc[-1] if "bb_mid" in df.columns else self.position["tp"]
        if not pd.isna(bb_mid) and self.tp_bb_middle:
            self.position["tp"] = bb_mid

        if is_long and current_price >= self.position["tp"]:
            self._close_position("TP到達(BB中央)")
            return
        elif not is_long and current_price <= self.position["tp"]:
            self._close_position("TP到達(BB中央)")
            return

        # トレーリング（TP付近を超えた場合のボーナス利益確保）
        if pnl_pct >= self.trailing_activation_pct:
            self.position["trailing_active"] = True

        if self.position["trailing_active"]:
            old_sl = self.position["sl"]
            if is_long:
                new_sl = self.position["highest"] * (1 - self.trailing_step_pct / 100)
                if new_sl > self.position["sl"]:
                    self.position["sl"] = new_sl
            else:
                new_sl = self.position["lowest"] * (1 + self.trailing_step_pct / 100)
                if new_sl < self.position["sl"]:
                    self.position["sl"] = new_sl

            if self.position["sl"] != old_sl:
                self._sl_oid = update_exchange_sl(
                    self.exchange, self.info, self.account_address,
                    self.coin, is_long, self.position["size"],
                    self.position["sl"], self._sl_oid, self.STRATEGY_NAME
                )

    def _close_position(self, reason: str):
        if not self.position:
            return

        if self._sl_oid:
            cancel_exchange_sl(self.exchange, self.coin, self._sl_oid, self.STRATEGY_NAME)
            self._sl_oid = None

        try:
            result = self.exchange.market_close(self.coin)
            logger.info(f"[{self.STRATEGY_NAME}] 決済: {reason}, 結果: {result}")

            entry = self.position["entry_price"]
            is_buy = self.position["side"] == "buy"
            mid = self._get_mid_price()
            if mid and entry > 0:
                pnl_pct = ((mid - entry) / entry * 100) if is_buy else ((entry - mid) / entry * 100)
                pnl = pnl_pct / 100 * entry * self.position["size"]
            else:
                pnl, pnl_pct = 0.0, 0.0

            self.telegram.notify_exit(
                self.STRATEGY_NAME, self.coin, self.position["side"],
                entry, mid or entry, pnl, pnl_pct
            )
            self.risk_manager.unregister_position(self.STRATEGY_NAME)
            self.position = None

        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] 決済エラー: {e}", exc_info=True)

    def _get_mid_price(self) -> Optional[float]:
        try:
            all_mids = self.info.all_mids()
            return float(all_mids.get(self.coin, 0))
        except Exception:
            return None
