"""
Alts_MidBreak_1H 戦略
======================
1時間足 レンジブレイク × 複数アルト銘柄。

ロジック:
1. 1時間足で直近50本の高値/安値レンジを算出
2. ブレイク + 出来高3倍以上 + RSI過熱回避でエントリー
3. TP 3〜5%狙い、トレーリング
4. レバレッジ12x
"""

import time
import logging
import pandas as pd
import numpy as np
from typing import Optional

logger = logging.getLogger(__name__)


class Alts1hBreakStrategy:
    """アルト 1時間足 ミッドブレイク戦略（複数銘柄対応）"""

    STRATEGY_NAME_PREFIX = "Alts_1H_Break"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram, coin: str):
        self.info = info
        self.exchange = exchange
        self.cfg = config["alts_1h_break"]
        self.risk_manager = risk_manager
        self.telegram = telegram
        self.coin = coin
        self.strategy_name = f"{self.STRATEGY_NAME_PREFIX}_{coin}"

        self.leverage = self.cfg["leverage"]
        self.range_period = self.cfg["range_period"]
        self.vol_multiplier = self.cfg["volume_multiplier"]
        self.rsi_period = self.cfg["rsi_period"]
        self.rsi_overbought = self.cfg["rsi_overbought"]
        self.rsi_oversold = self.cfg["rsi_oversold"]
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
        if self.risk_manager.check_daily_drawdown():
            if self.position:
                self._close_position("日次DD制限")
            return

        df = self._get_candles()
        if df is None or len(df) < self.range_period + 5:
            return

        current_price = df["close"].iloc[-1]

        if self.position:
            self._manage_position(current_price)
            return

        if not self.risk_manager.can_open_position(self.strategy_name):
            return

        signal = self._check_entry_signal(df)
        if signal:
            self._open_position(signal, current_price)

    def _get_candles(self) -> Optional[pd.DataFrame]:
        """1時間足キャンドルを取得"""
        try:
            import time
            end_time = int(time.time() * 1000)
            start_time = end_time - self.candle_count * 60 * 60 * 1000  # 1h = 3600s
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

            # RSI計算
            df["rsi"] = self._calc_rsi(df["close"], self.rsi_period)

            # 出来高MA
            df["vol_ma"] = df["volume"].rolling(window=self.range_period).mean()

            return df
        except Exception as e:
            logger.error(f"[{self.strategy_name}] キャンドル取得エラー: {e}")
            return None

    @staticmethod
    def _calc_rsi(series: pd.Series, period: int) -> pd.Series:
        """RSI計算"""
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=period, min_periods=period).mean()
        avg_loss = loss.rolling(window=period, min_periods=period).mean()
        rs = avg_gain / avg_loss.replace(0, np.inf)
        return 100 - (100 / (1 + rs))

    def _check_entry_signal(self, df: pd.DataFrame) -> Optional[str]:
        """
        レンジブレイクシグナル判定。
        直近range_period本のレンジ突破 + 出来高3倍 + RSI過熱回避。

        RSI過熱回避:
        - ロングの場合: RSIが既にoverboughtならスキップ（天井掴み防止）
        - ショートの場合: RSIが既にoversoldならスキップ（底売り防止）
        """
        curr = df.iloc[-1]
        current_price = curr["close"]
        current_volume = curr["volume"]
        vol_ma = curr["vol_ma"]
        rsi = curr["rsi"]

        if pd.isna(vol_ma) or vol_ma == 0 or pd.isna(rsi):
            return None

        # 直近range_period本のレンジ（現在足を除く）
        lookback = df.iloc[-(self.range_period + 1):-1]
        range_high = lookback["high"].max()
        range_low = lookback["low"].min()

        vol_ratio = current_volume / vol_ma

        # 上方ブレイク: 高値突破 + 出来高条件 + RSI過熱でない
        if (current_price > range_high
                and vol_ratio >= self.vol_multiplier
                and rsi < self.rsi_overbought):
            logger.info(
                f"[{self.strategy_name}] 上方ブレイク: "
                f"価格={current_price:.4f} > {range_high:.4f}, "
                f"Vol比={vol_ratio:.1f}x, RSI={rsi:.1f}"
            )
            return "long"

        # 下方ブレイク: 安値突破 + 出来高条件 + RSI過売でない
        if (current_price < range_low
                and vol_ratio >= self.vol_multiplier
                and rsi > self.rsi_oversold):
            logger.info(
                f"[{self.strategy_name}] 下方ブレイク: "
                f"価格={current_price:.4f} < {range_low:.4f}, "
                f"Vol比={vol_ratio:.1f}x, RSI={rsi:.1f}"
            )
            return "short"

        return None

    def _open_position(self, signal: str, current_price: float):
        """ポジションを開く"""
        is_buy = signal == "long"
        side = "buy" if is_buy else "sell"

        size = self.risk_manager.calculate_position_size(
            strategy_name=self.strategy_name,
            leverage=self.leverage,
            entry_price=current_price,
            sl_pct=self.sl_pct,
            is_btc=False
        )

        if size <= 0:
            return

        # サイズをHyperliquidの許容桁数に丸める
        sz_decimals = self.exchange.info.asset_to_sz_decimals.get(self.coin, 2)
        size = round(size, sz_decimals)
        if size <= 0:
            return

        try:
            result = self.exchange.market_open(self.coin, is_buy, size, None, 0.01)
            logger.info(f"[{self.strategy_name}] 注文結果: {result}")

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
                self.strategy_name, self.coin, side, size, current_price
            )
            self.telegram.notify_entry(
                self.strategy_name, self.coin, side, size, current_price, self.leverage
            )

        except Exception as e:
            logger.error(f"[{self.strategy_name}] 注文エラー: {e}", exc_info=True)

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

        # SL
        if is_long and current_price <= self.position["sl"]:
            self._close_position("SLヒット")
            return
        elif not is_long and current_price >= self.position["sl"]:
            self._close_position("SLヒット")
            return

        # TP
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
