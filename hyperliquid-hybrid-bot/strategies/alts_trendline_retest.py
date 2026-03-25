"""
Alts_TrendlineRetest 戦略
===========================
15分足 トレンドラインブレイク → 裏タッチ（リテスト）でエントリー。

ロジック:
1. スイングハイ/ローを検出し、トレンドライン（上値抵抗線/下値支持線）を自動描画
2. 価格がトレンドラインをブレイク（出来高確認付き）
3. ブレイク後、価格がトレンドラインまで戻る「裏タッチ」を検出
4. 裏タッチ + リジェクション足（ヒゲ確認）でエントリー
5. TP1で半分利確、残りはATRトレーリング
"""

import time
import logging
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List
from utils import validate_order_result

logger = logging.getLogger(__name__)


class AltsTrendlineRetestStrategy:
    """アルト トレンドラインブレイク → 裏タッチリテスト戦略"""

    STRATEGY_NAME_PREFIX = "Alts_TL_Retest"

    def __init__(self, info, exchange, config: dict, risk_manager, telegram, coin: str):
        self.info = info
        self.exchange = exchange
        self.cfg = config["alts_trendline_retest"]
        self.risk_manager = risk_manager
        self.telegram = telegram
        self.coin = coin
        self.strategy_name = f"{self.STRATEGY_NAME_PREFIX}_{coin}"

        # 設定パラメータ
        self.leverage = self.cfg["leverage"]
        self.swing_lookback = self.cfg["swing_lookback"]        # スイングポイント検出の前後本数
        self.min_touches = self.cfg["min_touches"]              # トレンドライン有効に必要な最小タッチ数
        self.trendline_lookback = self.cfg["trendline_lookback"]  # トレンドライン計算に使うローソク足数
        self.breakout_vol_mult = self.cfg["breakout_vol_multiplier"]  # ブレイク時の出来高倍率
        self.retest_tolerance_pct = self.cfg["retest_tolerance_pct"]  # 裏タッチ許容範囲(%)
        self.retest_timeout_bars = self.cfg["retest_timeout_bars"]    # ブレイク後リテスト待ち最大本数
        self.rejection_wick_ratio = self.cfg["rejection_wick_ratio"]  # リジェクション足のヒゲ/実体比
        self.tp1_pct = self.cfg["tp1_pct"]
        self.tp1_close_ratio = self.cfg["tp1_close_ratio"]
        self.atr_period = self.cfg["atr_period"]
        self.atr_trailing_mult = self.cfg["atr_trailing_multiplier"]
        self.sl_pct = self.cfg["sl_pct"]
        self.candle_count = self.cfg["candle_count"]
        self.interval = self.cfg["interval"]
        self.loop_interval = self.cfg["loop_interval_sec"]

        # 状態管理
        self.position: Optional[dict] = None
        self.running = True

        # ブレイクアウト追跡状態
        self._breakout_state: Optional[dict] = None
        # {
        #   "direction": "long" or "short",
        #   "trendline_slope": float,
        #   "trendline_intercept": float,
        #   "breakout_bar_idx": int,   # ブレイク時のDF内インデックス
        #   "breakout_time": float,    # ブレイク時のunix time
        #   "bars_since_breakout": int
        # }

    def run(self):
        logger.info(f"[{self.strategy_name}] 戦略開始 - {self.coin} {self.interval} TrendlineRetest")
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

    # ================================================================
    # メインティック
    # ================================================================
    def _tick(self):
        if self.risk_manager.check_daily_drawdown():
            if self.position:
                self._close_position("日次DD制限", close_all=True)
            return

        df = self._get_candles()
        if df is None or len(df) < self.trendline_lookback + 10:
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

    # ================================================================
    # データ取得
    # ================================================================
    def _get_candles(self) -> Optional[pd.DataFrame]:
        try:
            end_time = int(time.time() * 1000)
            interval_sec = self._interval_to_seconds(self.interval)
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

            df = df.reset_index(drop=True)

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
            logger.error(f"[{self.strategy_name}] キャンドル取得エラー: {e}")
            return None

    def _interval_to_seconds(self, interval: str) -> int:
        mapping = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400}
        return mapping.get(interval, 900)

    # ================================================================
    # スイングポイント検出
    # ================================================================
    def _find_swing_highs(self, df: pd.DataFrame) -> List[Tuple[int, float]]:
        """スイングハイを検出。(index, price)のリストを返す"""
        swings = []
        lb = self.swing_lookback
        for i in range(lb, len(df) - lb):
            high = df["high"].iloc[i]
            is_swing = True
            for j in range(1, lb + 1):
                if df["high"].iloc[i - j] >= high or df["high"].iloc[i + j] >= high:
                    is_swing = False
                    break
            if is_swing:
                swings.append((i, high))
        return swings

    def _find_swing_lows(self, df: pd.DataFrame) -> List[Tuple[int, float]]:
        """スイングローを検出。(index, price)のリストを返す"""
        swings = []
        lb = self.swing_lookback
        for i in range(lb, len(df) - lb):
            low = df["low"].iloc[i]
            is_swing = True
            for j in range(1, lb + 1):
                if df["low"].iloc[i - j] <= low or df["low"].iloc[i + j] <= low:
                    is_swing = False
                    break
            if is_swing:
                swings.append((i, low))
        return swings

    # ================================================================
    # トレンドライン計算
    # ================================================================
    def _fit_trendline(self, points: List[Tuple[int, float]]) -> Optional[Tuple[float, float, int]]:
        """
        直近のスイングポイントからトレンドラインを最小二乗法でフィット。
        Returns: (slope, intercept, touch_count) or None
        """
        if len(points) < 2:
            return None

        # 直近のポイントを優先（最大8個）
        recent = points[-8:]
        xs = np.array([p[0] for p in recent], dtype=float)
        ys = np.array([p[1] for p in recent], dtype=float)

        # 最小二乗法フィット
        if len(xs) < 2:
            return None

        slope, intercept = np.polyfit(xs, ys, 1)

        # トレンドラインへのタッチ数をカウント（許容誤差内）
        touch_count = 0
        for x, y in recent:
            tl_value = slope * x + intercept
            tolerance = abs(tl_value) * (self.retest_tolerance_pct / 100)
            if abs(y - tl_value) <= tolerance:
                touch_count += 1

        return (slope, intercept, touch_count)

    def _get_trendline_value(self, slope: float, intercept: float, bar_idx: int) -> float:
        """指定バーインデックスでのトレンドラインの値を計算"""
        return slope * bar_idx + intercept

    # ================================================================
    # シグナル判定（2段階: ブレイク検出 → 裏タッチ検出）
    # ================================================================
    def _check_entry_signal(self, df: pd.DataFrame) -> Optional[str]:
        curr = df.iloc[-1]
        prev = df.iloc[-2]
        current_price = curr["close"]
        current_idx = len(df) - 1

        # === ブレイクアウト状態が無い場合: 新規ブレイク検出 ===
        if self._breakout_state is None:
            return self._detect_breakout(df, current_price, current_idx)

        # === ブレイクアウト状態がある場合: 裏タッチ（リテスト）検出 ===
        bs = self._breakout_state

        # タイムアウトチェック
        bs["bars_since_breakout"] += 1
        if bs["bars_since_breakout"] > self.retest_timeout_bars:
            logger.info(
                f"[{self.strategy_name}] リテスト待ちタイムアウト "
                f"({bs['bars_since_breakout']}本経過)"
            )
            self._breakout_state = None
            return None

        # トレンドラインの現在の値を計算
        tl_value = self._get_trendline_value(
            bs["trendline_slope"], bs["trendline_intercept"], current_idx
        )
        tolerance = abs(tl_value) * (self.retest_tolerance_pct / 100)

        direction = bs["direction"]

        if direction == "long":
            # 上方ブレイク後: 価格がトレンドライン付近まで下落して反発
            # 裏タッチ = 安値がトレンドラインに近づき、終値はトレンドライン上
            near_trendline = curr["low"] <= tl_value + tolerance
            above_trendline = current_price > tl_value
            rejection = self._is_bullish_rejection(curr)

            if near_trendline and above_trendline and rejection:
                logger.info(
                    f"[{self.strategy_name}] 裏タッチLONG検出: "
                    f"TL値={tl_value:.4f}, 安値={curr['low']:.4f}, "
                    f"終値={current_price:.4f}, 待ち{bs['bars_since_breakout']}本"
                )
                self._breakout_state = None
                return "long"

        elif direction == "short":
            # 下方ブレイク後: 価格がトレンドライン付近まで上昇して反落
            near_trendline = curr["high"] >= tl_value - tolerance
            below_trendline = current_price < tl_value
            rejection = self._is_bearish_rejection(curr)

            if near_trendline and below_trendline and rejection:
                logger.info(
                    f"[{self.strategy_name}] 裏タッチSHORT検出: "
                    f"TL値={tl_value:.4f}, 高値={curr['high']:.4f}, "
                    f"終値={current_price:.4f}, 待ち{bs['bars_since_breakout']}本"
                )
                self._breakout_state = None
                return "short"

        return None

    def _detect_breakout(self, df: pd.DataFrame, current_price: float, current_idx: int) -> Optional[str]:
        """トレンドラインブレイクを検出"""
        curr = df.iloc[-1]
        vol_ma = curr.get("vol_ma", 0)
        if pd.isna(vol_ma) or vol_ma == 0:
            return None

        vol_ratio = curr["volume"] / vol_ma

        # 分析対象のウィンドウ
        window = df.iloc[-self.trendline_lookback:]

        # --- 上値抵抗線ブレイク（＝上方ブレイク → LONG準備）---
        swing_highs = self._find_swing_highs(window)
        if swing_highs:
            # ウィンドウ内のインデックスをDF全体のインデックスに変換
            offset = len(df) - self.trendline_lookback
            swing_highs_global = [(idx + offset, price) for idx, price in swing_highs]

            result = self._fit_trendline(swing_highs_global)
            if result:
                slope, intercept, touches = result
                tl_value = self._get_trendline_value(slope, intercept, current_idx)

                # ブレイク条件: 終値がトレンドライン上 + 出来高確認 + 十分なタッチ
                if (current_price > tl_value and
                        vol_ratio >= self.breakout_vol_mult and
                        touches >= self.min_touches):
                    logger.info(
                        f"[{self.strategy_name}] 上値抵抗線ブレイク検出: "
                        f"価格={current_price:.4f} > TL={tl_value:.4f}, "
                        f"タッチ={touches}, 出来高比={vol_ratio:.1f}x"
                    )
                    self._breakout_state = {
                        "direction": "long",
                        "trendline_slope": slope,
                        "trendline_intercept": intercept,
                        "breakout_bar_idx": current_idx,
                        "breakout_time": time.time(),
                        "bars_since_breakout": 0,
                    }
                    return None  # ブレイク検出のみ、エントリーはリテスト後

        # --- 下値支持線ブレイク（＝下方ブレイク → SHORT準備）---
        swing_lows = self._find_swing_lows(window)
        if swing_lows:
            offset = len(df) - self.trendline_lookback
            swing_lows_global = [(idx + offset, price) for idx, price in swing_lows]

            result = self._fit_trendline(swing_lows_global)
            if result:
                slope, intercept, touches = result
                tl_value = self._get_trendline_value(slope, intercept, current_idx)

                if (current_price < tl_value and
                        vol_ratio >= self.breakout_vol_mult and
                        touches >= self.min_touches):
                    logger.info(
                        f"[{self.strategy_name}] 下値支持線ブレイク検出: "
                        f"価格={current_price:.4f} < TL={tl_value:.4f}, "
                        f"タッチ={touches}, 出来高比={vol_ratio:.1f}x"
                    )
                    self._breakout_state = {
                        "direction": "short",
                        "trendline_slope": slope,
                        "trendline_intercept": intercept,
                        "breakout_bar_idx": current_idx,
                        "breakout_time": time.time(),
                        "bars_since_breakout": 0,
                    }
                    return None

        return None

    # ================================================================
    # リジェクション足の判定
    # ================================================================
    def _is_bullish_rejection(self, candle) -> bool:
        """
        下ヒゲが長い陽線（ブルリジェクション）
        裏タッチ後の反発確認
        """
        body = abs(candle["close"] - candle["open"])
        lower_wick = min(candle["open"], candle["close"]) - candle["low"]
        upper_wick = candle["high"] - max(candle["open"], candle["close"])
        total_range = candle["high"] - candle["low"]

        if total_range == 0:
            return False

        # 下ヒゲが実体のrejection_wick_ratio倍以上 + 陽線
        is_bullish = candle["close"] > candle["open"]
        long_lower_wick = lower_wick > body * self.rejection_wick_ratio if body > 0 else lower_wick > total_range * 0.5

        return is_bullish or long_lower_wick

    def _is_bearish_rejection(self, candle) -> bool:
        """
        上ヒゲが長い陰線（ベアリジェクション）
        裏タッチ後の反落確認
        """
        body = abs(candle["close"] - candle["open"])
        upper_wick = candle["high"] - max(candle["open"], candle["close"])
        total_range = candle["high"] - candle["low"]

        if total_range == 0:
            return False

        is_bearish = candle["close"] < candle["open"]
        long_upper_wick = upper_wick > body * self.rejection_wick_ratio if body > 0 else upper_wick > total_range * 0.5

        return is_bearish or long_upper_wick

    # ================================================================
    # ポジション開閉
    # ================================================================
    def _open_position(self, signal: str, current_price: float, df: pd.DataFrame):
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
        if not self.position:
            return

        is_long = self.position["side"] == "buy"
        entry = self.position["entry_price"]

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

        # TP1: 半分利確
        if not self.position["tp1_hit"]:
            if is_long and current_price >= self.position["tp1"]:
                self._partial_close("TP1到達")
            elif not is_long and current_price <= self.position["tp1"]:
                self._partial_close("TP1到達")
            return

        # TP1後: ATRトレーリング
        atr = self.position["atr"]
        if atr > 0:
            trailing_distance = atr * self.atr_trailing_mult
            if is_long:
                new_sl = self.position["highest"] - trailing_distance
                if new_sl > self.position["sl"]:
                    self.position["sl"] = new_sl
            else:
                new_sl = self.position["lowest"] + trailing_distance
                if new_sl < self.position["sl"]:
                    self.position["sl"] = new_sl

    def _partial_close(self, reason: str):
        if not self.position:
            return

        close_size = self.position["original_size"] * self.tp1_close_ratio
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

            self.telegram.notify_exit(
                self.strategy_name, self.coin, self.position["side"],
                self.position["entry_price"],
                self._get_mid_price() or self.position["entry_price"],
                0, 0
            )
        except Exception as e:
            logger.error(f"[{self.strategy_name}] 半分利確エラー: {e}", exc_info=True)

    def _close_position(self, reason: str, close_all: bool = True):
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
