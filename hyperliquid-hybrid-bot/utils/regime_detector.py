"""
相場レジーム自動判定モジュール
================================
ADX（トレンド強度）+ ボリンジャーバンド幅 + 価格位置で
「レンジ相場」か「トレンド相場」かを自動判定する。

判定ロジック:
- ADX < 20 → レンジ（トレンド弱い）
- ADX > 25 → トレンド（トレンド強い）
- 20 ≤ ADX ≤ 25 → BB幅とEMA傾きで補助判定
- BB幅が縮小 → レンジ寄り
- BB幅が拡大 → トレンド寄り
"""

import logging
import numpy as np
import pandas as pd
from enum import Enum

logger = logging.getLogger(__name__)


class MarketRegime(Enum):
    RANGING = "ranging"       # レンジ相場 → 逆張り
    TRENDING = "trending"     # トレンド相場 → 順張り
    UNKNOWN = "unknown"


class RegimeDetector:
    """
    ADX + BB幅で相場レジームを判定するクラス。
    各戦略から呼び出して使う。
    """

    def __init__(self, adx_period: int = 14, adx_range_threshold: float = 20.0,
                 adx_trend_threshold: float = 25.0, bb_period: int = 20,
                 bb_std: float = 2.0, bb_width_lookback: int = 20):
        self.adx_period = adx_period
        self.adx_range_threshold = adx_range_threshold
        self.adx_trend_threshold = adx_trend_threshold
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.bb_width_lookback = bb_width_lookback

    def detect(self, df: pd.DataFrame) -> MarketRegime:
        """
        DataFrameからレジームを判定する。
        dfには open, high, low, close カラムが必要。

        Returns:
            MarketRegime.RANGING or MarketRegime.TRENDING
        """
        required = max(self.adx_period * 2, self.bb_period + self.bb_width_lookback) + 5
        if len(df) < required:
            return MarketRegime.UNKNOWN

        # ADX計算
        adx = self._calc_adx(df)
        if adx is None or pd.isna(adx):
            return MarketRegime.UNKNOWN

        # BB幅（正規化）
        bb_width_percentile = self._calc_bb_width_percentile(df)

        # 判定
        if adx < self.adx_range_threshold:
            regime = MarketRegime.RANGING
        elif adx > self.adx_trend_threshold:
            regime = MarketRegime.TRENDING
        else:
            # グレーゾーン: BB幅で補助判定
            if bb_width_percentile is not None and bb_width_percentile < 40:
                regime = MarketRegime.RANGING
            elif bb_width_percentile is not None and bb_width_percentile > 60:
                regime = MarketRegime.TRENDING
            else:
                # 本当に曖昧な場合はレンジ寄り（逆張りの方がリスク低い）
                regime = MarketRegime.RANGING

        logger.debug(
            f"[RegimeDetector] ADX={adx:.1f}, BB幅%ile={bb_width_percentile:.0f}% "
            f"→ {regime.value}"
        )
        return regime

    def _calc_adx(self, df: pd.DataFrame) -> float | None:
        """ADX（Average Directional Index）を計算"""
        try:
            high = df["high"].values
            low = df["low"].values
            close = df["close"].values
            n = self.adx_period

            # +DM / -DM
            up_move = np.diff(high)
            down_move = -np.diff(low)

            plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
            minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

            # True Range
            tr = np.maximum(
                high[1:] - low[1:],
                np.maximum(
                    np.abs(high[1:] - close[:-1]),
                    np.abs(low[1:] - close[:-1])
                )
            )

            # Wilder's smoothing (EMA-like)
            atr = self._wilder_smooth(tr, n)
            plus_di_smooth = self._wilder_smooth(plus_dm, n)
            minus_di_smooth = self._wilder_smooth(minus_dm, n)

            if atr is None or len(atr) == 0:
                return None

            # +DI / -DI
            plus_di = 100 * plus_di_smooth / np.where(atr == 0, 1, atr)
            minus_di = 100 * minus_di_smooth / np.where(atr == 0, 1, atr)

            # DX
            di_sum = plus_di + minus_di
            dx = 100 * np.abs(plus_di - minus_di) / np.where(di_sum == 0, 1, di_sum)

            # ADX = Wilder smooth of DX
            adx = self._wilder_smooth(dx, n)
            if adx is None or len(adx) == 0:
                return None

            return float(adx[-1])

        except Exception as e:
            logger.error(f"[RegimeDetector] ADX計算エラー: {e}")
            return None

    @staticmethod
    def _wilder_smooth(data: np.ndarray, period: int) -> np.ndarray | None:
        """Wilder's smoothing method"""
        if len(data) < period:
            return None
        result = np.full(len(data), np.nan)
        result[period - 1] = np.mean(data[:period])
        for i in range(period, len(data)):
            result[i] = (result[i - 1] * (period - 1) + data[i]) / period
        return result

    def _calc_bb_width_percentile(self, df: pd.DataFrame) -> float | None:
        """
        BB幅の現在値が直近N本中の何パーセンタイルにあるか。
        低い = レンジ（バンド縮小）、高い = トレンド（バンド拡大）
        """
        try:
            close = df["close"]
            bb_mid = close.rolling(window=self.bb_period).mean()
            bb_std = close.rolling(window=self.bb_period).std()
            bb_upper = bb_mid + (bb_std * self.bb_std)
            bb_lower = bb_mid - (bb_std * self.bb_std)

            # 正規化BB幅 = (upper - lower) / mid
            bb_width = (bb_upper - bb_lower) / bb_mid
            bb_width = bb_width.dropna()

            if len(bb_width) < self.bb_width_lookback:
                return None

            recent = bb_width.iloc[-self.bb_width_lookback:]
            current = bb_width.iloc[-1]

            # パーセンタイル計算
            percentile = (recent < current).sum() / len(recent) * 100
            return float(percentile)

        except Exception as e:
            logger.error(f"[RegimeDetector] BB幅計算エラー: {e}")
            return None
