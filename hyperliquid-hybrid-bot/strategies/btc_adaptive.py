"""
BTC_Adaptive 戦略
========================
相場レジーム自動判定により逆張り/順張りを自動切り替え。

- レンジ相場（ADX低い）→ 逆張り（RSI + BB ミーンリバージョン）
- トレンド相場（ADX高い）→ 順張り（RSI + MACD モメンタムリトレース）

RegimeDetectorが毎ティック判定し、最適な戦略ロジックを選択する。
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
from utils.regime_detector import RegimeDetector, MarketRegime

logger = logging.getLogger(__name__)


class BTCAdaptiveStrategy:
    """BTC アダプティブ戦略（レジーム自動切替）"""

    STRATEGY_NAME = "BTC_Adaptive"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram):
        self.info = info
        self.exchange = exchange
        self.cfg = config["btc_adaptive"]
        self.risk_manager = risk_manager
        self.telegram = telegram

        self.coin = self.cfg["coin"]
        self.leverage = self.cfg["leverage"]
        self.interval = self.cfg["interval"]
        self.candle_count = self.cfg["candle_count"]
        self.loop_interval = self.cfg["loop_interval_sec"]

        # 共通インジケータパラメータ
        self.rsi_period = self.cfg["rsi_period"]
        self.atr_period = self.cfg["atr_period"]
        self.bb_period = self.cfg["bb_period"]
        self.bb_std = self.cfg["bb_std"]

        # 逆張り（レンジ相場）パラメータ
        self.mr_rsi_oversold = self.cfg["mr_rsi_oversold"]
        self.mr_rsi_overbought = self.cfg["mr_rsi_overbought"]
        self.mr_atr_sl_mult = self.cfg["mr_atr_sl_multiplier"]
        self.mr_vol_spike = self.cfg["mr_volume_spike_multiplier"]
        self.mr_tp_bb_middle = self.cfg["mr_tp_to_bb_middle"]
        self.mr_min_rr = self.cfg["mr_min_rr"]

        # 順張り（トレンド相場）パラメータ
        self.tf_rsi_oversold = self.cfg["tf_rsi_oversold"]
        self.tf_rsi_overbought = self.cfg["tf_rsi_overbought"]
        self.tf_macd_fast = self.cfg["tf_macd_fast"]
        self.tf_macd_slow = self.cfg["tf_macd_slow"]
        self.tf_macd_signal = self.cfg["tf_macd_signal"]
        self.tf_vol_threshold = self.cfg["tf_volume_threshold"]
        self.tf_tp_pct = self.cfg["tf_tp_pct"]
        self.tf_atr_sl_mult = self.cfg["tf_atr_sl_multiplier"]

        # 共通
        self.sl_pct_max = self.cfg["sl_pct_max"]
        self.trailing_activation = self.cfg["trailing_activation_pct"]
        self.trailing_step = self.cfg["trailing_step_pct"]

        # レジーム判定
        self.regime_detector = RegimeDetector(
            adx_period=self.cfg.get("adx_period", 14),
            adx_range_threshold=self.cfg.get("adx_range_threshold", 20.0),
            adx_trend_threshold=self.cfg.get("adx_trend_threshold", 25.0),
            bb_period=self.bb_period,
            bb_std=self.bb_std,
            bb_width_lookback=self.cfg.get("bb_width_lookback", 20)
        )

        self.account_address = config["account_address"]
        self.position: Optional[dict] = None
        self.running = True
        self._sl_oid: Optional[int] = None
        self._current_regime: MarketRegime = MarketRegime.UNKNOWN
        self._momentum_direction: Optional[str] = None
        self._momentum_confirmed_at: float = 0

    def run(self):
        logger.info(f"[{self.STRATEGY_NAME}] 戦略開始 - {self.coin} {self.interval} Adaptive")
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
        if df is None or len(df) < self.candle_count // 2:
            return

        current_price = df["close"].iloc[-1]
        self.risk_manager.update_btc_price(current_price)

        # レジーム判定
        new_regime = self.regime_detector.detect(df)
        if new_regime != MarketRegime.UNKNOWN:
            if new_regime != self._current_regime:
                logger.info(
                    f"[{self.STRATEGY_NAME}] レジーム変更: "
                    f"{self._current_regime.value} → {new_regime.value}"
                )
                self._current_regime = new_regime
                # レジーム変更時、モメンタム方向をリセット
                self._momentum_direction = None

        if self.position:
            self._manage_position(current_price, df)
            return

        # レジームに応じたシグナル判定
        signal = None
        if self._current_regime == MarketRegime.RANGING:
            signal = self._check_mean_reversion_signal(df)
        elif self._current_regime == MarketRegime.TRENDING:
            signal = self._check_trend_following_signal(df)

        if signal:
            side = "buy" if signal["direction"] == "long" else "sell"
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

            # BB
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

            # MACD（順張り用）
            ema_fast = df["close"].ewm(span=self.tf_macd_fast, adjust=False).mean()
            ema_slow = df["close"].ewm(span=self.tf_macd_slow, adjust=False).mean()
            df["macd"] = ema_fast - ema_slow
            df["macd_signal"] = df["macd"].ewm(span=self.tf_macd_signal, adjust=False).mean()
            df["macd_hist"] = df["macd"] - df["macd_signal"]

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
    # 逆張りシグナル（レンジ相場用）
    # ================================================================
    def _check_mean_reversion_signal(self, df: pd.DataFrame) -> Optional[dict]:
        curr = df.iloc[-1]
        rsi = curr["rsi"]
        close = curr["close"]
        low = curr["low"]
        high = curr["high"]
        bb_lower = curr["bb_lower"]
        bb_upper = curr["bb_upper"]
        bb_mid = curr["bb_mid"]
        vol = curr["volume"]
        vol_ma = curr["vol_ma"]

        if pd.isna(rsi) or pd.isna(bb_lower) or pd.isna(vol_ma) or vol_ma == 0:
            return None

        vol_ratio = vol / vol_ma

        # LONG: RSI過売 + BB下限タッチ + 陽線 + 出来高スパイク
        if (rsi <= self.mr_rsi_oversold
                and low <= bb_lower
                and close > curr["open"]
                and vol_ratio >= self.mr_vol_spike):
            logger.info(
                f"[{self.STRATEGY_NAME}] [逆張り] LONG: "
                f"RSI={rsi:.1f}, BB下限={bb_lower:.2f}, Vol比={vol_ratio:.1f}x"
            )
            return {"direction": "long", "mode": "mean_reversion", "tp_target": bb_mid}

        # SHORT: RSI過熱 + BB上限タッチ + 陰線 + 出来高スパイク
        if (rsi >= self.mr_rsi_overbought
                and high >= bb_upper
                and close < curr["open"]
                and vol_ratio >= self.mr_vol_spike):
            logger.info(
                f"[{self.STRATEGY_NAME}] [逆張り] SHORT: "
                f"RSI={rsi:.1f}, BB上限={bb_upper:.2f}, Vol比={vol_ratio:.1f}x"
            )
            return {"direction": "short", "mode": "mean_reversion", "tp_target": bb_mid}

        return None

    # ================================================================
    # 順張りシグナル（トレンド相場用）
    # ================================================================
    def _check_trend_following_signal(self, df: pd.DataFrame) -> Optional[dict]:
        if len(df) < 3:
            return None

        curr = df.iloc[-1]
        prev = df.iloc[-2]

        rsi = curr["rsi"]
        macd_hist = curr["macd_hist"]
        prev_macd_hist = prev["macd_hist"]
        vol = curr["volume"]
        vol_ma = curr["vol_ma"]

        if pd.isna(rsi) or pd.isna(macd_hist) or pd.isna(vol_ma) or vol_ma == 0:
            return None

        vol_ratio = vol / vol_ma

        # フェーズ1: モメンタム確認
        if (rsi > 50 and rsi < self.tf_rsi_overbought
                and macd_hist > 0 and prev_macd_hist <= 0
                and vol_ratio >= self.tf_vol_threshold):
            self._momentum_direction = "bullish"
            self._momentum_confirmed_at = time.time()
            logger.info(
                f"[{self.STRATEGY_NAME}] [順張り] Bullishモメンタム確認: "
                f"RSI={rsi:.1f}, MACD_hist={macd_hist:.4f}"
            )

        elif (rsi < 50 and rsi > self.tf_rsi_oversold
              and macd_hist < 0 and prev_macd_hist >= 0
              and vol_ratio >= self.tf_vol_threshold):
            self._momentum_direction = "bearish"
            self._momentum_confirmed_at = time.time()
            logger.info(
                f"[{self.STRATEGY_NAME}] [順張り] Bearishモメンタム確認: "
                f"RSI={rsi:.1f}, MACD_hist={macd_hist:.4f}"
            )

        # モメンタム有効期限: 15分
        if self._momentum_direction and time.time() - self._momentum_confirmed_at > 900:
            self._momentum_direction = None

        # フェーズ2: リトレースメント検出
        if self._momentum_direction == "bullish":
            if 45 < rsi < 60 and curr["close"] > prev["close"] and curr["close"] > curr["open"]:
                self._momentum_direction = None
                return {"direction": "long", "mode": "trend_following", "tp_target": None}

        elif self._momentum_direction == "bearish":
            if 40 < rsi < 55 and curr["close"] < prev["close"] and curr["close"] < curr["open"]:
                self._momentum_direction = None
                return {"direction": "short", "mode": "trend_following", "tp_target": None}

        return None

    # ================================================================
    # ポジション開閉
    # ================================================================
    def _open_position(self, signal: dict, current_price: float, df: pd.DataFrame):
        direction = signal["direction"]
        mode = signal["mode"]
        is_buy = direction == "long"
        side = "buy" if is_buy else "sell"

        current_atr = df["atr"].iloc[-1]
        if pd.isna(current_atr) or current_atr <= 0:
            return

        # SL計算（モード別ATR倍率）
        if mode == "mean_reversion":
            atr_mult = self.mr_atr_sl_mult
        else:
            atr_mult = self.tf_atr_sl_mult

        atr_sl_pct = (current_atr * atr_mult / current_price) * 100
        atr_sl_pct = min(atr_sl_pct, self.sl_pct_max)

        # TP計算
        if mode == "mean_reversion":
            bb_mid = signal["tp_target"]
            if pd.isna(bb_mid):
                return
            if is_buy:
                tp_pct = ((bb_mid - current_price) / current_price) * 100
            else:
                tp_pct = ((current_price - bb_mid) / current_price) * 100
            # R:Rチェック
            if tp_pct < atr_sl_pct * self.mr_min_rr:
                logger.info(
                    f"[{self.STRATEGY_NAME}] [逆張り] R:R不足: "
                    f"TP={tp_pct:.3f}%, SL={atr_sl_pct:.3f}%"
                )
                return
            tp_price = bb_mid
        else:
            tp_pct = self.tf_tp_pct
            if is_buy:
                tp_price = current_price * (1 + tp_pct / 100)
            else:
                tp_price = current_price * (1 - tp_pct / 100)

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
            else:
                sl_price = current_price * (1 + atr_sl_pct / 100)

            mode_jp = "逆張り" if mode == "mean_reversion" else "順張り"
            logger.info(
                f"[{self.STRATEGY_NAME}] [{mode_jp}]エントリー: {side} @ {current_price:.2f}, "
                f"SL={sl_price:.2f}({atr_sl_pct:.2f}%), TP={tp_price:.2f}, "
                f"レジーム={self._current_regime.value}"
            )

            self.position = {
                "side": side,
                "size": size,
                "entry_price": current_price,
                "sl": sl_price,
                "tp": tp_price,
                "mode": mode,
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

        # TP: 逆張りモードではBBミドルを動的更新
        if self.position["mode"] == "mean_reversion" and self.mr_tp_bb_middle:
            bb_mid = df["bb_mid"].iloc[-1] if "bb_mid" in df.columns else None
            if bb_mid is not None and not pd.isna(bb_mid):
                self.position["tp"] = bb_mid

        if is_long and current_price >= self.position["tp"]:
            self._close_position("TP到達")
            return
        elif not is_long and current_price <= self.position["tp"]:
            self._close_position("TP到達")
            return

        # トレーリング
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
            mode_jp = "逆張り" if self.position.get("mode") == "mean_reversion" else "順張り"
            logger.info(f"[{self.STRATEGY_NAME}] [{mode_jp}]決済: {reason}, 結果: {result}")

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
