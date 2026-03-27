"""
Alts_MeanReversion 戦略
========================
アルト逆張り: 下がったら買う、上がったら売る。複数銘柄対応。

ロジック:
1. RSI(14) + ボリンジャーバンド(20, 2σ) で過熱/過売を検出
2. RSI ≤ 25 + BB下限タッチ + 陽線 → LONG
3. RSI ≥ 75 + BB上限タッチ + 陰線 → SHORT
4. TP1 = 50%をBBミドルで利確、残りはATRトレーリング
5. SL = ATRベース動的SL
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


class AltsMeanReversionStrategy:
    """アルト 逆張りミーンリバージョン戦略（複数銘柄対応）"""

    STRATEGY_NAME_PREFIX = "Alts_MeanRev"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram, coin: str):
        self.info = info
        self.exchange = exchange
        self.cfg = config["alts_mean_reversion"]
        self.risk_manager = risk_manager
        self.telegram = telegram
        self.coin = coin
        self.strategy_name = f"{self.STRATEGY_NAME_PREFIX}_{coin}"

        self.leverage = self.cfg["leverage"]
        self.rsi_period = self.cfg["rsi_period"]
        self.rsi_oversold = self.cfg["rsi_oversold"]
        self.rsi_overbought = self.cfg["rsi_overbought"]
        self.bb_period = self.cfg["bb_period"]
        self.bb_std = self.cfg["bb_std"]
        self.atr_period = self.cfg["atr_period"]
        self.atr_sl_multiplier = self.cfg["atr_sl_multiplier"]
        self.vol_spike_mult = self.cfg["volume_spike_multiplier"]
        self.tp1_pct_of_bb = self.cfg["tp1_close_ratio"]
        self.atr_trailing_mult = self.cfg["atr_trailing_multiplier"]
        self.sl_pct_max = self.cfg["sl_pct_max"]
        self.candle_count = self.cfg["candle_count"]
        self.interval = self.cfg["interval"]
        self.loop_interval = self.cfg["loop_interval_sec"]

        self.account_address = config["account_address"]
        self.position: Optional[dict] = None
        self.running = True
        self._sl_oid: Optional[int] = None

    def run(self):
        logger.info(f"[{self.strategy_name}] 戦略開始 - {self.coin} {self.interval} MeanReversion")
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
        if self.risk_manager.check_daily_drawdown():
            if self.position:
                self._close_position("日次DD制限")
            return

        df = self._get_candles()
        if df is None or len(df) < max(self.bb_period, self.rsi_period, self.atr_period) + 5:
            return

        current_price = df["close"].iloc[-1]

        if self.position:
            self._manage_position(current_price, df)
            return

        signal = self._check_entry_signal(df)
        if signal:
            side = "buy" if signal == "long" else "sell"
            if not self.risk_manager.can_open_position(self.strategy_name, self.coin, side):
                return
            self._open_position(signal, current_price, df)

    def _get_candles(self) -> Optional[pd.DataFrame]:
        try:
            end_time = int(time.time() * 1000)
            interval_sec = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600}.get(self.interval, 900)
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

            df["rsi"] = self._calc_rsi(df["close"], self.rsi_period)
            df["bb_mid"] = df["close"].rolling(window=self.bb_period).mean()
            bb_std = df["close"].rolling(window=self.bb_period).std()
            df["bb_upper"] = df["bb_mid"] + (bb_std * self.bb_std)
            df["bb_lower"] = df["bb_mid"] - (bb_std * self.bb_std)

            df["tr"] = np.maximum(
                df["high"] - df["low"],
                np.maximum(
                    abs(df["high"] - df["close"].shift(1)),
                    abs(df["low"] - df["close"].shift(1))
                )
            )
            df["atr"] = df["tr"].rolling(window=self.atr_period).mean()
            df["vol_ma"] = df["volume"].rolling(window=20).mean()

            return df
        except Exception as e:
            logger.error(f"[{self.strategy_name}] キャンドル取得エラー: {e}")
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

    def _check_entry_signal(self, df: pd.DataFrame) -> Optional[str]:
        curr = df.iloc[-1]
        rsi = curr["rsi"]
        close = curr["close"]
        vol = curr["volume"]
        vol_ma = curr["vol_ma"]

        if pd.isna(rsi) or pd.isna(curr["bb_lower"]) or pd.isna(vol_ma) or vol_ma == 0:
            return None

        vol_ratio = vol / vol_ma

        # LONG: 売られすぎ
        if (rsi <= self.rsi_oversold
                and curr["low"] <= curr["bb_lower"]
                and close > curr["open"]
                and vol_ratio >= self.vol_spike_mult):
            logger.info(
                f"[{self.strategy_name}] LONG: RSI={rsi:.1f}, "
                f"BB下限={curr['bb_lower']:.4f}, Vol比={vol_ratio:.1f}x"
            )
            return "long"

        # SHORT: 買われすぎ
        if (rsi >= self.rsi_overbought
                and curr["high"] >= curr["bb_upper"]
                and close < curr["open"]
                and vol_ratio >= self.vol_spike_mult):
            logger.info(
                f"[{self.strategy_name}] SHORT: RSI={rsi:.1f}, "
                f"BB上限={curr['bb_upper']:.4f}, Vol比={vol_ratio:.1f}x"
            )
            return "short"

        return None

    def _open_position(self, signal: str, current_price: float, df: pd.DataFrame):
        is_buy = signal == "long"
        side = "buy" if is_buy else "sell"

        current_atr = df["atr"].iloc[-1]
        if pd.isna(current_atr) or current_atr <= 0:
            return

        atr_sl_pct = (current_atr * self.atr_sl_multiplier / current_price) * 100
        atr_sl_pct = min(atr_sl_pct, self.sl_pct_max)

        bb_mid = df["bb_mid"].iloc[-1]
        if pd.isna(bb_mid):
            return

        size = self.risk_manager.calculate_position_size(
            strategy_name=self.strategy_name,
            leverage=self.leverage,
            entry_price=current_price,
            sl_pct=atr_sl_pct,
            is_btc=False
        )
        if size <= 0:
            return

        sz_decimals = self.exchange.info.asset_to_sz_decimals.get(self.coin, 2)
        size = round(size, sz_decimals)
        if size <= 0:
            return

        try:
            result = self.exchange.market_open(self.coin, is_buy, size, None, 0.01)
            logger.info(f"[{self.strategy_name}] 注文結果: {result}")

            success, err_msg = validate_order_result(result)
            if not success:
                logger.error(f"[{self.strategy_name}] 注文失敗: {err_msg}")
                return

            if is_buy:
                sl_price = current_price * (1 - atr_sl_pct / 100)
            else:
                sl_price = current_price * (1 + atr_sl_pct / 100)

            self.position = {
                "side": side,
                "size": size,
                "original_size": size,
                "entry_price": current_price,
                "sl": sl_price,
                "tp1": bb_mid,
                "tp1_hit": False,
                "atr": current_atr,
                "highest": current_price if is_buy else None,
                "lowest": current_price if not is_buy else None,
            }

            self._sl_oid = place_exchange_sl(
                self.exchange, self.info, self.account_address,
                self.coin, is_buy, size, sl_price, self.strategy_name
            )

            self.risk_manager.register_position(
                self.strategy_name, self.coin, side, size, current_price
            )
            self.telegram.notify_entry(
                self.strategy_name, self.coin, side, size, current_price, self.leverage
            )

        except Exception as e:
            logger.error(f"[{self.strategy_name}] 注文エラー: {e}", exc_info=True)

    def _manage_position(self, current_price: float, df: pd.DataFrame):
        if not self.position:
            return

        is_long = self.position["side"] == "buy"

        if is_long:
            if self.position["highest"] is None or current_price > self.position["highest"]:
                self.position["highest"] = current_price
        else:
            if self.position["lowest"] is None or current_price < self.position["lowest"]:
                self.position["lowest"] = current_price

        # SLチェック
        if is_long and current_price <= self.position["sl"]:
            self._close_position("SLヒット")
            return
        elif not is_long and current_price >= self.position["sl"]:
            self._close_position("SLヒット")
            return

        # 動的TP1 = BBミドル（毎ティック更新）
        bb_mid = df["bb_mid"].iloc[-1] if "bb_mid" in df.columns else self.position["tp1"]
        if not pd.isna(bb_mid):
            self.position["tp1"] = bb_mid

        # TP1: 半分利確
        if not self.position["tp1_hit"]:
            if is_long and current_price >= self.position["tp1"]:
                self._partial_close("TP1(BB中央)")
            elif not is_long and current_price <= self.position["tp1"]:
                self._partial_close("TP1(BB中央)")
            return

        # TP1後: ATRトレーリング
        atr = self.position["atr"]
        if atr > 0:
            old_sl = self.position["sl"]
            trailing_distance = atr * self.atr_trailing_mult
            if is_long:
                new_sl = self.position["highest"] - trailing_distance
                if new_sl > self.position["sl"]:
                    self.position["sl"] = new_sl
            else:
                new_sl = self.position["lowest"] + trailing_distance
                if new_sl < self.position["sl"]:
                    self.position["sl"] = new_sl

            if self.position["sl"] != old_sl:
                self._sl_oid = update_exchange_sl(
                    self.exchange, self.info, self.account_address,
                    self.coin, is_long, self.position["size"],
                    self.position["sl"], self._sl_oid, self.strategy_name
                )

    def _partial_close(self, reason: str):
        if not self.position:
            return

        close_size = self.position["original_size"] * self.tp1_pct_of_bb
        sz_decimals = self.exchange.info.asset_to_sz_decimals.get(self.coin, 2)
        close_size = round(close_size, sz_decimals)
        if close_size <= 0:
            return

        try:
            is_buy = self.position["side"] == "buy"
            result = self.exchange.market_open(self.coin, not is_buy, close_size, None, 0.01)
            logger.info(f"[{self.strategy_name}] 半分利確: {reason}, 結果: {result}")

            success, err_msg = validate_order_result(result)
            if not success:
                logger.error(f"[{self.strategy_name}] 半分利確失敗: {err_msg}")
                return

            self.position["size"] -= close_size
            self.position["tp1_hit"] = True
            self.position["sl"] = self.position["entry_price"]  # 建値ストップ

            # 取引所SLを建値に更新
            self._sl_oid = update_exchange_sl(
                self.exchange, self.info, self.account_address,
                self.coin, is_buy, self.position["size"],
                self.position["sl"], self._sl_oid, self.strategy_name
            )

            self.telegram.notify_exit(
                self.strategy_name, self.coin, self.position["side"],
                self.position["entry_price"],
                self._get_mid_price() or self.position["entry_price"],
                0, 0
            )
        except Exception as e:
            logger.error(f"[{self.strategy_name}] 半分利確エラー: {e}", exc_info=True)

    def _close_position(self, reason: str):
        if not self.position:
            return

        if self._sl_oid:
            cancel_exchange_sl(self.exchange, self.coin, self._sl_oid, self.strategy_name)
            self._sl_oid = None

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
