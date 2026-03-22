"""
BTC_5m_MomentumRetrace 戦略
============================
5分足 RSI + MACD + 出来高を使ったモメンタムリトレースメント。

ロジック:
1. 5分足キャンドルを取得
2. RSI(14)でモメンタム方向確認
3. MACD(12,26,9)でトレンド確認
4. 出来高がMA(20)の1.5倍以上で確認
5. モメンタム確認後、押し目（ロング）/ 戻り（ショート）でエントリー
6. TP 1.0〜1.5%, トレーリング
7. レバレッジ8x
"""

import time
import logging
import pandas as pd
import numpy as np
from typing import Optional

logger = logging.getLogger(__name__)


class BTC5mMomentumStrategy:
    """BTC 5分足 モメンタムリトレースメント戦略"""

    STRATEGY_NAME = "BTC_5m_MomentumRetrace"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram):
        self.info = info
        self.exchange = exchange
        self.cfg = config["btc_5m_momentum"]
        self.risk_manager = risk_manager
        self.telegram = telegram

        self.coin = self.cfg["coin"]
        self.leverage = self.cfg["leverage"]
        self.rsi_period = self.cfg["rsi_period"]
        self.rsi_oversold = self.cfg["rsi_oversold"]
        self.rsi_overbought = self.cfg["rsi_overbought"]
        self.macd_fast = self.cfg["macd_fast"]
        self.macd_slow = self.cfg["macd_slow"]
        self.macd_signal = self.cfg["macd_signal"]
        self.vol_ma_period = self.cfg["volume_ma_period"]
        self.vol_threshold = self.cfg["volume_threshold"]
        self.tp_min = self.cfg["tp_min_pct"]
        self.tp_max = self.cfg["tp_max_pct"]
        self.sl_pct = self.cfg["sl_pct"]
        self.trailing_activation = self.cfg["trailing_activation_pct"]
        self.trailing_step = self.cfg["trailing_step_pct"]
        self.candle_count = self.cfg["candle_count"]
        self.interval = self.cfg["interval"]
        self.loop_interval = self.cfg["loop_interval_sec"]

        self.position: Optional[dict] = None
        self.running = True
        # モメンタム方向記録（押し目/戻り待ち用）
        self._momentum_direction: Optional[str] = None  # "bullish" or "bearish"
        self._momentum_confirmed_at: float = 0

    def run(self):
        """メインループ"""
        logger.info(f"[{self.STRATEGY_NAME}] 戦略開始 - {self.coin} {self.interval}")
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
        """1ティック処理"""
        if self.risk_manager.check_daily_drawdown():
            if self.position:
                self._close_position("日次DD制限")
            return

        df = self._get_candles()
        if df is None or len(df) < self.candle_count:
            return

        current_price = df["close"].iloc[-1]
        self.risk_manager.update_btc_price(current_price)

        if self.position:
            self._manage_position(current_price)
            return

        if not self.risk_manager.can_open_position(self.STRATEGY_NAME):
            return

        signal = self._check_entry_signal(df)
        if signal:
            self._open_position(signal, current_price)

    def _get_candles(self) -> Optional[pd.DataFrame]:
        """5分足キャンドルを取得"""
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

            # RSI計算
            df["rsi"] = self._calc_rsi(df["close"], self.rsi_period)

            # MACD計算
            ema_fast = df["close"].ewm(span=self.macd_fast, adjust=False).mean()
            ema_slow = df["close"].ewm(span=self.macd_slow, adjust=False).mean()
            df["macd"] = ema_fast - ema_slow
            df["macd_signal"] = df["macd"].ewm(span=self.macd_signal, adjust=False).mean()
            df["macd_hist"] = df["macd"] - df["macd_signal"]

            # 出来高MA
            df["vol_ma"] = df["volume"].rolling(window=self.vol_ma_period).mean()

            return df
        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] キャンドル取得エラー: {e}")
            return None

    @staticmethod
    def _calc_rsi(series: pd.Series, period: int) -> pd.Series:
        """RSIを計算"""
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=period, min_periods=period).mean()
        avg_loss = loss.rolling(window=period, min_periods=period).mean()
        rs = avg_gain / avg_loss.replace(0, np.inf)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _check_entry_signal(self, df: pd.DataFrame) -> Optional[str]:
        """
        エントリーシグナル判定。
        フェーズ1: モメンタム確認（RSI + MACD + Volume）
        フェーズ2: リトレースメント（押し目/戻り）でエントリー
        """
        if len(df) < 3:
            return None

        curr = df.iloc[-1]
        prev = df.iloc[-2]

        rsi = curr["rsi"]
        macd_hist = curr["macd_hist"]
        prev_macd_hist = prev["macd_hist"]
        volume = curr["volume"]
        vol_ma = curr["vol_ma"]

        if pd.isna(rsi) or pd.isna(macd_hist) or pd.isna(vol_ma) or vol_ma == 0:
            return None

        vol_ratio = volume / vol_ma

        # === フェーズ1: モメンタム確認 ===
        # Bullishモメンタム: RSIが中立以上 + MACD histが正に転換 + 出来高増
        if (rsi > 50 and rsi < self.rsi_overbought
                and macd_hist > 0 and prev_macd_hist <= 0
                and vol_ratio >= self.vol_threshold):
            self._momentum_direction = "bullish"
            self._momentum_confirmed_at = time.time()
            logger.info(
                f"[{self.STRATEGY_NAME}] Bullishモメンタム確認: "
                f"RSI={rsi:.1f}, MACD_hist={macd_hist:.4f}, Vol比={vol_ratio:.1f}x"
            )

        # Bearishモメンタム: RSIが中立以下 + MACD histが負に転換 + 出来高増
        elif (rsi < 50 and rsi > self.rsi_oversold
              and macd_hist < 0 and prev_macd_hist >= 0
              and vol_ratio >= self.vol_threshold):
            self._momentum_direction = "bearish"
            self._momentum_confirmed_at = time.time()
            logger.info(
                f"[{self.STRATEGY_NAME}] Bearishモメンタム確認: "
                f"RSI={rsi:.1f}, MACD_hist={macd_hist:.4f}, Vol比={vol_ratio:.1f}x"
            )

        # モメンタム有効期限: 15分（3本分）
        if self._momentum_direction and time.time() - self._momentum_confirmed_at > 900:
            self._momentum_direction = None

        # === フェーズ2: リトレースメント検出 ===
        if self._momentum_direction == "bullish":
            # 押し目: RSIが一旦下がってから再上昇
            if self.rsi_oversold < rsi < 50 and curr["close"] > prev["close"]:
                self._momentum_direction = None
                return "long"

        elif self._momentum_direction == "bearish":
            # 戻り: RSIが一旦上がってから再下降
            if 50 < rsi < self.rsi_overbought and curr["close"] < prev["close"]:
                self._momentum_direction = None
                return "short"

        return None

    def _open_position(self, signal: str, current_price: float):
        """ポジションを開く"""
        is_buy = signal == "long"
        side = "buy" if is_buy else "sell"

        size = self.risk_manager.calculate_position_size(
            strategy_name=self.STRATEGY_NAME,
            leverage=self.leverage,
            entry_price=current_price,
            sl_pct=self.sl_pct,
            is_btc=True
        )

        if size <= 0:
            return

        try:
            result = self.exchange.market_open(self.coin, is_buy, size, None, 0.01)
            logger.info(f"[{self.STRATEGY_NAME}] 注文結果: {result}")

            if is_buy:
                sl_price = current_price * (1 - self.sl_pct / 100)
                tp_price = current_price * (1 + self.tp_min / 100)
            else:
                sl_price = current_price * (1 + self.sl_pct / 100)
                tp_price = current_price * (1 - self.tp_min / 100)

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

            self.risk_manager.register_position(
                self.STRATEGY_NAME, self.coin, side, size, current_price
            )
            self.telegram.notify_entry(
                self.STRATEGY_NAME, self.coin, side, size, current_price, self.leverage
            )

        except Exception as e:
            logger.error(f"[{self.STRATEGY_NAME}] 注文エラー: {e}", exc_info=True)

    def _manage_position(self, current_price: float):
        """ポジション管理"""
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

        # TPチェック
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
            if is_long:
                new_sl = self.position["highest"] * (1 - self.trailing_step / 100)
                if new_sl > self.position["sl"]:
                    self.position["sl"] = new_sl
            else:
                new_sl = self.position["lowest"] * (1 + self.trailing_step / 100)
                if new_sl < self.position["sl"]:
                    self.position["sl"] = new_sl

    def _close_position(self, reason: str):
        """ポジションクローズ"""
        if not self.position:
            return

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
