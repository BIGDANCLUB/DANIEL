"""Technical analysis: 200EMA, volume spike, trendline break detection."""

import logging
from typing import Optional

import numpy as np
import pandas as pd
import pandas_ta as ta
from scipy import stats
from scipy.signal import argrelextrema

from config import Config

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 200 EMA
# ──────────────────────────────────────────────
def compute_ema(df: pd.DataFrame, period: int = 200, col: str = "close") -> pd.Series:
    """Compute EMA using pandas_ta."""
    ema = ta.ema(df[col], length=period)
    return ema


def is_above_ema(df: pd.DataFrame, period: int = 200) -> bool:
    """Check if current price is above the EMA."""
    ema = compute_ema(df, period)
    if ema is None or ema.dropna().empty:
        return False
    return float(df["close"].iloc[-1]) > float(ema.dropna().iloc[-1])


# ──────────────────────────────────────────────
# Volume spike detection
# ──────────────────────────────────────────────
def detect_volume_spike(
    df: pd.DataFrame,
    recent_bars: int = 1,
    lookback_bars: int = 24,
    multiplier: float = None,
) -> tuple[bool, float]:
    """
    Detect if recent volume is a spike vs historical average.
    Returns (is_spike, ratio).
    """
    multiplier = multiplier or Config.VOLUME_SPIKE_MULTIPLIER
    if len(df) < lookback_bars + recent_bars:
        return False, 0.0

    recent_vol = df["volume"].iloc[-recent_bars:].mean()
    hist_vol = df["volume"].iloc[-(lookback_bars + recent_bars):-recent_bars].mean()

    if hist_vol <= 0:
        return False, 0.0

    ratio = recent_vol / hist_vol
    return ratio >= multiplier, round(ratio, 2)


def get_volume_spike_mask(df: pd.DataFrame, lookback: int = 24, multiplier: float = 3.0) -> pd.Series:
    """Return boolean mask where volume spikes occur (for chart coloring)."""
    rolling_avg = df["volume"].rolling(window=lookback, min_periods=1).mean().shift(1)
    return df["volume"] > (rolling_avg * multiplier)


# ──────────────────────────────────────────────
# Trendline detection (swing high/low + linear regression)
# ──────────────────────────────────────────────
def find_swing_points(
    series: pd.Series, order: int = 5
) -> tuple[np.ndarray, np.ndarray]:
    """
    Find swing highs and swing lows using scipy argrelextrema.
    `order` = number of bars on each side to compare.
    Returns (swing_high_indices, swing_low_indices).
    """
    values = series.values
    swing_highs = argrelextrema(values, np.greater_equal, order=order)[0]
    swing_lows = argrelextrema(values, np.less_equal, order=order)[0]
    return swing_highs, swing_lows


def fit_trendline(
    indices: np.ndarray,
    values: np.ndarray,
    min_points: int = 3,
) -> Optional[dict]:
    """
    Fit a linear regression trendline to the given points.
    Returns dict with slope, intercept, r_squared, points_used, or None.
    """
    if len(indices) < min_points:
        return None

    # Use most recent points (up to 8)
    recent = min(len(indices), 8)
    idx = indices[-recent:]
    vals = values[idx]

    slope, intercept, r_value, p_value, std_err = stats.linregress(idx.astype(float), vals)

    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "indices": idx,
        "values": vals,
    }


def detect_trendline_break(
    df: pd.DataFrame,
    lookback: int = None,
    swing_order: int = 5,
    min_touches: int = None,
) -> dict:
    """
    Full trendline break detection pipeline.

    1. Find swing highs → fit resistance trendline
    2. Find swing lows → fit support trendline
    3. Check if the latest close breaks above resistance or below support

    Returns:
        {
            "resistance_break": bool,
            "support_break": bool,
            "resistance_line": dict | None,
            "support_line": dict | None,
            "breakout_type": "bullish" | "bearish" | None,
            "break_strength": float (0-1),
        }
    """
    lookback = lookback or Config.TRENDLINE_LOOKBACK_BARS
    min_touches = min_touches or Config.TRENDLINE_MIN_TOUCHES

    result = {
        "resistance_break": False,
        "support_break": False,
        "resistance_line": None,
        "support_line": None,
        "breakout_type": None,
        "break_strength": 0.0,
    }

    if len(df) < lookback:
        subset = df.copy()
    else:
        subset = df.iloc[-lookback:].copy()

    subset = subset.reset_index(drop=True)
    highs = subset["high"]
    lows = subset["low"]
    close = subset["close"]
    current_close = float(close.iloc[-1])
    current_idx = len(subset) - 1

    # Find swing points
    sh_idx, sl_idx = find_swing_points(highs, order=swing_order)
    _, sl_low_idx = find_swing_points(lows, order=swing_order)

    # Fit resistance trendline (using swing highs)
    res_line = fit_trendline(sh_idx, highs.values, min_points=min_touches)
    if res_line and res_line["r_squared"] > 0.5:
        result["resistance_line"] = res_line
        resistance_at_current = res_line["slope"] * current_idx + res_line["intercept"]

        # Breakout: close above resistance with margin
        margin = abs(resistance_at_current) * 0.002  # 0.2% tolerance
        if current_close > resistance_at_current + margin:
            result["resistance_break"] = True
            result["breakout_type"] = "bullish"
            # Strength: how far above the line (normalized)
            pct_above = (current_close - resistance_at_current) / resistance_at_current
            result["break_strength"] = min(pct_above * 100, 1.0)

    # Fit support trendline (using swing lows)
    sup_line = fit_trendline(sl_low_idx, lows.values, min_points=min_touches)
    if sup_line and sup_line["r_squared"] > 0.5:
        result["support_line"] = sup_line
        support_at_current = sup_line["slope"] * current_idx + sup_line["intercept"]

        margin = abs(support_at_current) * 0.002
        if current_close < support_at_current - margin:
            result["support_break"] = True
            if result["breakout_type"] is None:
                result["breakout_type"] = "bearish"
                pct_below = (support_at_current - current_close) / support_at_current
                result["break_strength"] = min(pct_below * 100, 1.0)

    return result


# ──────────────────────────────────────────────
# Composite scoring
# ──────────────────────────────────────────────
def compute_scan_score(
    above_ema: bool,
    volume_spike: bool,
    volume_ratio: float,
    trendline_break: dict,
    social_boost: bool = False,
) -> float:
    """
    Composite score 0-100.
    Weights:
        - 200 EMA above: 25
        - Volume spike: 25 (scaled by ratio)
        - Trendline break: 35
        - Social boost: 15
    """
    score = 0.0

    # EMA
    if above_ema:
        score += 25.0

    # Volume
    if volume_spike:
        vol_score = min(volume_ratio / 5.0, 1.0) * 25.0
        score += vol_score

    # Trendline
    if trendline_break.get("resistance_break"):
        base = 25.0
        strength_bonus = trendline_break.get("break_strength", 0) * 10.0
        score += base + strength_bonus

    # Social
    if social_boost:
        score += 15.0

    return round(min(score, 100.0), 1)
