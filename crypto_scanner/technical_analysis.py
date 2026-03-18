"""
Technical analysis — Phase 7
=============================
- 200 EMA (pandas_ta)
- Volume spike detection
- Advanced trendline detection:
  - Multi-order swing point detection (adaptive)
  - RANSAC-like robust line fitting (outlier rejection)
  - Multiple trendline candidates (best 3 resistance + 3 support)
  - Volume-confirmed breakout validation
  - Pattern classification (wedge, channel, triangle)
  - Multi-timeframe confirmation
- Phase 6: RSI, MACD, Bollinger Bands
- Phase 6: Multi-indicator composite scoring
"""

import logging
from typing import Optional
from itertools import combinations

import numpy as np
import pandas as pd
import talib
from scipy import stats
from scipy.signal import argrelextrema

from config import Config

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 200 EMA
# ──────────────────────────────────────────────
def compute_ema(df: pd.DataFrame, period: int = 200, col: str = "close") -> pd.Series:
    """Compute EMA using ta-lib."""
    values = df[col].astype(float).values
    ema_arr = talib.EMA(values, timeperiod=period)
    return pd.Series(ema_arr, index=df.index)


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
    """Detect if recent volume is a spike vs historical average."""
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
# Adaptive Swing Point Detection
# ──────────────────────────────────────────────
def find_swing_points(
    series: pd.Series, order: int = 5
) -> tuple[np.ndarray, np.ndarray]:
    """Find swing highs and swing lows using scipy argrelextrema."""
    values = series.values
    swing_highs = argrelextrema(values, np.greater_equal, order=order)[0]
    swing_lows = argrelextrema(values, np.less_equal, order=order)[0]
    return swing_highs, swing_lows


def find_swing_points_adaptive(
    series: pd.Series, min_order: int = 3, max_order: int = 10, min_points: int = 4
) -> tuple[np.ndarray, np.ndarray]:
    """
    Adaptive swing point detection.
    Tries multiple orders and picks the one yielding the best balance
    of point count (>= min_points) and significance.
    """
    values = series.values
    best_highs = np.array([], dtype=int)
    best_lows = np.array([], dtype=int)
    best_order = min_order

    for order in range(min_order, max_order + 1):
        highs = argrelextrema(values, np.greater_equal, order=order)[0]
        lows = argrelextrema(values, np.less_equal, order=order)[0]

        # We want at least min_points; prefer highest order that satisfies
        if len(highs) >= min_points and len(lows) >= min_points:
            best_highs = highs
            best_lows = lows
            best_order = order
        elif len(highs) >= min_points or len(lows) >= min_points:
            # Partial: keep if we haven't found better
            if len(best_highs) < min_points:
                best_highs = highs
                best_lows = lows
                best_order = order

    return best_highs, best_lows


# ──────────────────────────────────────────────
# Robust Trendline Fitting (RANSAC-like)
# ──────────────────────────────────────────────
def fit_trendline(
    indices: np.ndarray,
    values: np.ndarray,
    min_points: int = 3,
) -> Optional[dict]:
    """Simple linear regression trendline fit (kept for backward compat)."""
    if len(indices) < min_points:
        return None

    recent = min(len(indices), 8)
    idx = indices[-recent:]
    vals = values[idx]

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        idx.astype(float), vals
    )

    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "std_err": std_err,
        "indices": idx,
        "values": vals,
    }


def fit_trendline_ransac(
    indices: np.ndarray,
    values: np.ndarray,
    line_type: str = "resistance",
    min_points: int = 3,
    max_candidates: int = 5,
) -> list[dict]:
    """
    RANSAC-like robust trendline fitting.

    For resistance: fit lines through pairs of swing highs, then score
    by how many other highs are close to (or just below) the line.
    For support: same but with swing lows, points close to or just above.

    Returns sorted list of candidate trendlines (best first).
    """
    if len(indices) < min_points:
        return []

    pts = np.array(list(zip(indices.astype(float), values[indices])))

    if len(pts) < 2:
        return []

    candidates = []

    # Try all pairs of points to define candidate lines
    pair_limit = min(len(pts), 10)  # limit combos for performance
    recent_pts = pts[-pair_limit:]

    for (i1, p1), (i2, p2) in combinations(enumerate(recent_pts), 2):
        x1, y1 = p1
        x2, y2 = p2
        if x2 == x1:
            continue

        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        # Score: count inliers (points close to the line)
        predicted = slope * recent_pts[:, 0] + intercept
        residuals = recent_pts[:, 1] - predicted

        # For resistance: points should be at or below the line
        # For support: points should be at or above the line
        tolerance = np.std(recent_pts[:, 1]) * 0.03  # 3% of price std

        if line_type == "resistance":
            inliers = np.sum(np.abs(residuals) <= tolerance)
            # Penalty for points significantly above the line
            violations = np.sum(residuals > tolerance * 2)
        else:
            inliers = np.sum(np.abs(residuals) <= tolerance)
            violations = np.sum(residuals < -tolerance * 2)

        if inliers < min_points:
            continue

        # Compute R² for inlier subset
        inlier_mask = np.abs(residuals) <= tolerance
        if np.sum(inlier_mask) >= 2:
            inlier_x = recent_pts[inlier_mask, 0]
            inlier_y = recent_pts[inlier_mask, 1]
            ss_res = np.sum((inlier_y - (slope * inlier_x + intercept)) ** 2)
            ss_tot = np.sum((inlier_y - np.mean(inlier_y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        else:
            r_squared = 0

        # Combined score: more inliers + fewer violations + higher R²
        score = inliers * 2 - violations * 3 + r_squared * 5

        candidates.append({
            "slope": slope,
            "intercept": intercept,
            "r_squared": max(r_squared, 0),
            "inliers": int(inliers),
            "violations": int(violations),
            "score": round(score, 2),
            "indices": indices,
            "values": values[indices],
            "line_type": line_type,
        })

    # Sort by score descending, return top N
    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[:max_candidates]


# ──────────────────────────────────────────────
# Pattern Classification
# ──────────────────────────────────────────────
def classify_pattern(
    res_line: Optional[dict], sup_line: Optional[dict]
) -> str:
    """
    Classify the chart pattern based on resistance and support slopes.
    Returns: 'ascending_triangle', 'descending_triangle',
             'symmetrical_triangle', 'rising_wedge', 'falling_wedge',
             'channel_up', 'channel_down', 'horizontal_channel', 'unknown'
    """
    if res_line is None or sup_line is None:
        return "unknown"

    r_slope = res_line["slope"]
    s_slope = sup_line["slope"]

    # Normalize slopes relative to price range
    price_range = np.mean(res_line["values"]) if len(res_line.get("values", [])) > 0 else 1
    r_norm = r_slope / price_range * 1000
    s_norm = s_slope / price_range * 1000

    flat_threshold = 0.3
    converging = (r_norm < -flat_threshold and s_norm > flat_threshold) or (
        r_norm - s_norm < -flat_threshold
    )

    # Ascending triangle: flat resistance + rising support
    if abs(r_norm) < flat_threshold and s_norm > flat_threshold:
        return "ascending_triangle"

    # Descending triangle: flat support + falling resistance
    if abs(s_norm) < flat_threshold and r_norm < -flat_threshold:
        return "descending_triangle"

    # Symmetrical triangle: converging slopes (one up, one down)
    if r_norm < -flat_threshold and s_norm > flat_threshold:
        return "symmetrical_triangle"

    # Rising wedge: both up but converging
    if r_norm > 0 and s_norm > 0 and r_norm < s_norm:
        return "rising_wedge"

    # Falling wedge: both down but converging
    if r_norm < 0 and s_norm < 0 and r_norm > s_norm:
        return "falling_wedge"

    # Channels
    slope_diff = abs(r_norm - s_norm)
    if slope_diff < flat_threshold * 2:
        avg_slope = (r_norm + s_norm) / 2
        if avg_slope > flat_threshold:
            return "channel_up"
        elif avg_slope < -flat_threshold:
            return "channel_down"
        else:
            return "horizontal_channel"

    return "unknown"


PATTERN_LABELS = {
    "ascending_triangle": "Ascending Triangle",
    "descending_triangle": "Descending Triangle",
    "symmetrical_triangle": "Symmetrical Triangle",
    "rising_wedge": "Rising Wedge",
    "falling_wedge": "Falling Wedge",
    "channel_up": "Rising Channel",
    "channel_down": "Falling Channel",
    "horizontal_channel": "Horizontal Channel",
    "unknown": "—",
}


# ──────────────────────────────────────────────
# Volume-Confirmed Breakout
# ──────────────────────────────────────────────
def is_volume_confirmed_break(
    df: pd.DataFrame, break_bar: int = -1, vol_multiplier: float = 1.5
) -> bool:
    """
    Check if the breakout bar has above-average volume
    (confirms the break is not a false signal).
    """
    if len(df) < 10:
        return False
    break_vol = float(df["volume"].iloc[break_bar])
    avg_vol = float(df["volume"].iloc[-20:].mean())
    return break_vol > avg_vol * vol_multiplier


# ──────────────────────────────────────────────
# Advanced Trendline Break Detection
# ──────────────────────────────────────────────
def detect_trendline_break(
    df: pd.DataFrame,
    lookback: int = None,
    swing_order: int = 5,
    min_touches: int = None,
) -> dict:
    """
    Phase 2 trendline break detection.

    Improvements over Phase 1:
    1. Adaptive swing point detection (multiple orders)
    2. RANSAC-like robust fitting with outlier rejection
    3. Multiple candidate trendlines (picks best)
    4. Volume-confirmed breakout validation
    5. Pattern classification
    6. Close-above-then-retest confirmation
    """
    lookback = lookback or Config.TRENDLINE_LOOKBACK_BARS
    min_touches = min_touches or Config.TRENDLINE_MIN_TOUCHES

    result = {
        "resistance_break": False,
        "support_break": False,
        "resistance_line": None,
        "support_line": None,
        "resistance_candidates": [],
        "support_candidates": [],
        "breakout_type": None,
        "break_strength": 0.0,
        "volume_confirmed": False,
        "pattern": "unknown",
        "pattern_label": "—",
        "confirmation_bars": 0,
    }

    if len(df) < max(lookback, 30):
        subset = df.copy()
    else:
        subset = df.iloc[-lookback:].copy()

    subset = subset.reset_index(drop=True)
    highs = subset["high"]
    lows = subset["low"]
    close = subset["close"]
    current_close = float(close.iloc[-1])
    current_idx = len(subset) - 1

    # Step 1: Adaptive swing points
    sh_idx, sl_idx = find_swing_points_adaptive(
        highs, min_order=3, max_order=8, min_points=min_touches
    )
    sl_low_idx_h, sl_low_idx = find_swing_points_adaptive(
        lows, min_order=3, max_order=8, min_points=min_touches
    )

    # Step 2: RANSAC-like robust trendline fitting
    res_candidates = fit_trendline_ransac(
        sh_idx, highs.values, line_type="resistance", min_points=min_touches
    )
    sup_candidates = fit_trendline_ransac(
        sl_low_idx, lows.values, line_type="support", min_points=min_touches
    )

    # Fall back to simple fit if RANSAC yields nothing
    if not res_candidates:
        simple_res = fit_trendline(sh_idx, highs.values, min_points=min_touches)
        if simple_res and simple_res["r_squared"] > 0.3:
            simple_res["line_type"] = "resistance"
            simple_res["inliers"] = len(simple_res.get("indices", []))
            simple_res["violations"] = 0
            simple_res["score"] = simple_res["r_squared"] * 5
            res_candidates = [simple_res]

    if not sup_candidates:
        simple_sup = fit_trendline(sl_low_idx, lows.values, min_points=min_touches)
        if simple_sup and simple_sup["r_squared"] > 0.3:
            simple_sup["line_type"] = "support"
            simple_sup["inliers"] = len(simple_sup.get("indices", []))
            simple_sup["violations"] = 0
            simple_sup["score"] = simple_sup["r_squared"] * 5
            sup_candidates = [simple_sup]

    result["resistance_candidates"] = res_candidates
    result["support_candidates"] = sup_candidates

    # Step 3: Check breakout against best resistance line
    if res_candidates:
        best_res = res_candidates[0]
        result["resistance_line"] = best_res
        res_at_current = best_res["slope"] * current_idx + best_res["intercept"]

        margin = abs(res_at_current) * 0.002  # 0.2% tolerance
        if current_close > res_at_current + margin:
            result["resistance_break"] = True
            result["breakout_type"] = "bullish"

            pct_above = (current_close - res_at_current) / abs(res_at_current) if res_at_current != 0 else 0
            result["break_strength"] = round(min(pct_above * 50, 1.0), 3)

            # Volume confirmation
            result["volume_confirmed"] = is_volume_confirmed_break(subset)

            # Count confirmation bars (how many bars stayed above)
            confirm = 0
            for i in range(2, min(6, len(subset))):
                bar_close = float(close.iloc[-i])
                line_at = best_res["slope"] * (current_idx - i + 1) + best_res["intercept"]
                if bar_close > line_at:
                    confirm += 1
                else:
                    break
            result["confirmation_bars"] = confirm

    # Step 4: Check breakout against best support line
    if sup_candidates:
        best_sup = sup_candidates[0]
        result["support_line"] = best_sup
        sup_at_current = best_sup["slope"] * current_idx + best_sup["intercept"]

        margin = abs(sup_at_current) * 0.002
        if current_close < sup_at_current - margin:
            result["support_break"] = True
            if result["breakout_type"] is None:
                result["breakout_type"] = "bearish"
                pct_below = (sup_at_current - current_close) / abs(sup_at_current) if sup_at_current != 0 else 0
                result["break_strength"] = round(min(pct_below * 50, 1.0), 3)
                result["volume_confirmed"] = is_volume_confirmed_break(subset)

    # Step 5: Pattern classification
    result["pattern"] = classify_pattern(
        result["resistance_line"], result["support_line"]
    )
    result["pattern_label"] = PATTERN_LABELS.get(result["pattern"], "—")

    return result


# ──────────────────────────────────────────────
# Multi-Timeframe Trendline Confirmation
# ──────────────────────────────────────────────
def confirm_trendline_multi_tf(
    df_1h: pd.DataFrame, df_4h: pd.DataFrame
) -> dict:
    """
    Run trendline break detection on both 1H and 4H,
    return combined confidence.
    """
    result_1h = detect_trendline_break(df_1h)
    result_4h = detect_trendline_break(df_4h)

    combined = {
        "1h": result_1h,
        "4h": result_4h,
        "both_confirm": False,
        "confidence": 0.0,
    }

    h1_break = result_1h.get("resistance_break", False)
    h4_break = result_4h.get("resistance_break", False)

    if h1_break and h4_break:
        combined["both_confirm"] = True
        # Both timeframes confirm = very high confidence
        s1 = result_1h.get("break_strength", 0)
        s4 = result_4h.get("break_strength", 0)
        combined["confidence"] = round(min((s1 + s4) / 2 * 1.5 + 0.3, 1.0), 2)
    elif h1_break:
        combined["confidence"] = round(result_1h.get("break_strength", 0) * 0.6, 2)
    elif h4_break:
        combined["confidence"] = round(result_4h.get("break_strength", 0) * 0.8, 2)

    return combined


# ──────────────────────────────────────────────
# Composite scoring — Phase 2
# ──────────────────────────────────────────────
def compute_scan_score(
    above_ema: bool,
    volume_spike: bool,
    volume_ratio: float,
    trendline_break: dict,
    social_boost: bool = False,
) -> float:
    """
    Composite score 0-100. Phase 2 weights:
        - 200 EMA above:       20
        - Volume spike:        20 (scaled by ratio)
        - Trendline break:     35 (with volume confirm + pattern bonuses)
        - Social boost:        10
        - Multi-TF / Pattern:  15
    """
    score = 0.0

    # EMA
    if above_ema:
        score += 20.0

    # Volume
    if volume_spike:
        vol_score = min(volume_ratio / 5.0, 1.0) * 20.0
        score += vol_score

    # Trendline break
    if trendline_break.get("resistance_break"):
        base = 20.0
        strength_bonus = trendline_break.get("break_strength", 0) * 10.0
        score += base + strength_bonus

        # Volume-confirmed bonus
        if trendline_break.get("volume_confirmed"):
            score += 5.0

        # Pattern bonus
        pattern = trendline_break.get("pattern", "unknown")
        if pattern in ("ascending_triangle", "falling_wedge"):
            score += 10.0  # High-probability bullish patterns
        elif pattern in ("symmetrical_triangle", "channel_up"):
            score += 5.0
        elif pattern != "unknown":
            score += 3.0

        # Confirmation bars bonus
        confirm = trendline_break.get("confirmation_bars", 0)
        score += min(confirm * 2.0, 5.0)

    # Social
    if social_boost:
        score += 10.0

    return round(min(score, 100.0), 1)


# ──────────────────────────────────────────────
# Phase 6: RSI
# ──────────────────────────────────────────────
def compute_rsi(df: pd.DataFrame, period: int = 14, col: str = "close") -> pd.Series:
    """Compute RSI using ta-lib."""
    values = df[col].astype(float).values
    rsi_arr = talib.RSI(values, timeperiod=period)
    return pd.Series(rsi_arr, index=df.index)


def get_rsi_signal(df: pd.DataFrame, period: int = 14) -> dict:
    """
    Evaluate RSI conditions.
    Returns: {value, oversold, overbought, bullish_zone, signal}
    """
    rsi = compute_rsi(df, period)
    if rsi is None or rsi.dropna().empty:
        return {"value": 50, "oversold": False, "overbought": False, "bullish_zone": False, "signal": "neutral"}

    current = float(rsi.dropna().iloc[-1])
    prev = float(rsi.dropna().iloc[-2]) if len(rsi.dropna()) >= 2 else current

    signal = "neutral"
    if current < 30:
        signal = "oversold"
    elif current > 70:
        signal = "overbought"
    elif 40 <= current <= 60:
        signal = "neutral"
    elif current > 50 and prev <= 50:
        signal = "bullish_cross"  # RSI crossed above 50
    elif current < 50 and prev >= 50:
        signal = "bearish_cross"

    return {
        "value": round(current, 2),
        "oversold": current < 30,
        "overbought": current > 70,
        "bullish_zone": 50 < current < 70,
        "signal": signal,
    }


# ──────────────────────────────────────────────
# Phase 6: MACD
# ──────────────────────────────────────────────
def compute_macd(
    df: pd.DataFrame, fast: int = 12, slow: int = 26, signal_period: int = 9, col: str = "close"
) -> pd.DataFrame:
    """Compute MACD using ta-lib. Returns DataFrame with macd, signal, histogram."""
    values = df[col].astype(float).values
    macd_line, signal_line, histogram = talib.MACD(
        values, fastperiod=fast, slowperiod=slow, signalperiod=signal_period
    )
    return pd.DataFrame({
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram,
    }, index=df.index)


def get_macd_signal(df: pd.DataFrame) -> dict:
    """
    Evaluate MACD conditions.
    Returns: {macd, signal_line, histogram, bullish_cross, bearish_cross, trend}
    """
    macd_df = compute_macd(df)
    if macd_df.empty:
        return {"macd": 0, "signal_line": 0, "histogram": 0,
                "bullish_cross": False, "bearish_cross": False, "trend": "neutral"}

    clean = macd_df.dropna()
    if len(clean) < 2:
        return {"macd": 0, "signal_line": 0, "histogram": 0,
                "bullish_cross": False, "bearish_cross": False, "trend": "neutral"}

    curr_macd = float(clean["macd"].iloc[-1])
    curr_signal = float(clean["signal"].iloc[-1])
    curr_hist = float(clean["histogram"].iloc[-1])
    prev_hist = float(clean["histogram"].iloc[-2])

    bullish_cross = prev_hist < 0 and curr_hist >= 0
    bearish_cross = prev_hist > 0 and curr_hist <= 0

    trend = "neutral"
    if curr_macd > curr_signal and curr_hist > 0:
        trend = "bullish"
    elif curr_macd < curr_signal and curr_hist < 0:
        trend = "bearish"

    return {
        "macd": round(curr_macd, 6),
        "signal_line": round(curr_signal, 6),
        "histogram": round(curr_hist, 6),
        "bullish_cross": bullish_cross,
        "bearish_cross": bearish_cross,
        "trend": trend,
    }


# ──────────────────────────────────────────────
# Phase 6: Bollinger Bands
# ──────────────────────────────────────────────
def compute_bollinger_bands(
    df: pd.DataFrame, period: int = 20, std_dev: float = 2.0, col: str = "close"
) -> pd.DataFrame:
    """Compute Bollinger Bands using ta-lib. Returns DataFrame with lower, mid, upper, bandwidth, %b."""
    values = df[col].astype(float).values
    upper, mid, lower = talib.BBANDS(values, timeperiod=period, nbdevup=std_dev, nbdevdn=std_dev)

    bandwidth = np.where(mid != 0, (upper - lower) / mid, 0)
    pct_b = np.where((upper - lower) != 0, (values - lower) / (upper - lower), 0.5)

    return pd.DataFrame({
        "lower": lower,
        "mid": mid,
        "upper": upper,
        "bandwidth": bandwidth,
        "pct_b": pct_b,
    }, index=df.index)


def get_bb_signal(df: pd.DataFrame) -> dict:
    """
    Evaluate Bollinger Band conditions.
    Returns: {upper, mid, lower, bandwidth, pct_b, squeeze, signal}
    """
    bb = compute_bollinger_bands(df)
    if bb.empty:
        return {"upper": 0, "mid": 0, "lower": 0, "bandwidth": 0,
                "pct_b": 0.5, "squeeze": False, "signal": "neutral"}

    clean = bb.dropna()
    if clean.empty:
        return {"upper": 0, "mid": 0, "lower": 0, "bandwidth": 0,
                "pct_b": 0.5, "squeeze": False, "signal": "neutral"}

    row = clean.iloc[-1]
    bw = float(row["bandwidth"])
    pct_b = float(row["pct_b"])

    # Squeeze: bandwidth is in lowest 20th percentile of recent history
    recent_bw = clean["bandwidth"].iloc[-50:] if len(clean) >= 50 else clean["bandwidth"]
    squeeze = bw <= float(recent_bw.quantile(0.2))

    signal = "neutral"
    if pct_b > 1.0:
        signal = "above_upper"  # Price above upper band
    elif pct_b < 0.0:
        signal = "below_lower"  # Price below lower band
    elif squeeze:
        signal = "squeeze"  # Volatility contraction — breakout imminent

    return {
        "upper": round(float(row["upper"]), 6),
        "mid": round(float(row["mid"]), 6),
        "lower": round(float(row["lower"]), 6),
        "bandwidth": round(bw, 4),
        "pct_b": round(pct_b, 4),
        "squeeze": squeeze,
        "signal": signal,
    }


# ──────────────────────────────────────────────
# Phase 6: Enhanced composite scoring
# ──────────────────────────────────────────────
def compute_scan_score_v2(
    above_ema: bool,
    volume_spike: bool,
    volume_ratio: float,
    trendline_break: dict,
    social_boost: bool = False,
    rsi_data: dict = None,
    macd_data: dict = None,
    bb_data: dict = None,
) -> float:
    """
    Enhanced composite score 0-100. Phase 6 weights:
        - 200 EMA above:       15
        - Volume spike:        15 (scaled by ratio)
        - Trendline break:     30 (with volume confirm + pattern bonuses)
        - Social boost:         8
        - RSI signal:          12
        - MACD signal:         10
        - BB signal:           10
    """
    score = 0.0

    # EMA
    if above_ema:
        score += 15.0

    # Volume
    if volume_spike:
        vol_score = min(volume_ratio / 5.0, 1.0) * 15.0
        score += vol_score

    # Trendline break
    if trendline_break.get("resistance_break"):
        base = 15.0
        strength_bonus = trendline_break.get("break_strength", 0) * 10.0
        score += base + strength_bonus

        if trendline_break.get("volume_confirmed"):
            score += 5.0

        pattern = trendline_break.get("pattern", "unknown")
        if pattern in ("ascending_triangle", "falling_wedge"):
            score += 7.0
        elif pattern in ("symmetrical_triangle", "channel_up"):
            score += 4.0
        elif pattern != "unknown":
            score += 2.0

        confirm = trendline_break.get("confirmation_bars", 0)
        score += min(confirm * 1.5, 4.0)

    # Social
    if social_boost:
        score += 8.0

    # RSI (Phase 6)
    if rsi_data:
        rsi_val = rsi_data.get("value", 50)
        rsi_sig = rsi_data.get("signal", "neutral")
        if rsi_sig == "bullish_cross":
            score += 12.0
        elif rsi_data.get("bullish_zone"):
            score += 8.0
        elif rsi_sig == "oversold":
            score += 6.0  # Potential reversal
        elif rsi_sig == "overbought":
            score -= 3.0  # Slight negative

    # MACD (Phase 6)
    if macd_data:
        if macd_data.get("bullish_cross"):
            score += 10.0
        elif macd_data.get("trend") == "bullish":
            score += 6.0
        elif macd_data.get("bearish_cross"):
            score -= 2.0

    # Bollinger Bands (Phase 6)
    if bb_data:
        if bb_data.get("squeeze"):
            score += 8.0  # Volatility squeeze → breakout likely
        if bb_data.get("signal") == "above_upper":
            score += 5.0  # Strong momentum
        elif bb_data.get("signal") == "below_lower":
            score -= 2.0

    return round(max(min(score, 100.0), 0.0), 1)


# ──────────────────────────────────────────────
# Phase 7: Fibonacci Retracement & Extension
# ──────────────────────────────────────────────
FIBONACCI_RATIOS = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
FIBONACCI_EXT_RATIOS = [1.0, 1.272, 1.414, 1.618, 2.0, 2.618]


def compute_fibonacci_levels(
    df: pd.DataFrame, lookback: int = 100
) -> dict:
    """
    Compute Fibonacci retracement and extension levels based on
    recent swing high/low within the lookback window.
    """
    if len(df) < 20:
        return {"retracement": [], "extension": [], "swing_high": 0, "swing_low": 0, "trend": "unknown"}

    subset = df.iloc[-lookback:] if len(df) >= lookback else df
    swing_high = float(subset["high"].max())
    swing_low = float(subset["low"].min())

    high_idx = int(subset["high"].idxmax() if hasattr(subset["high"].idxmax(), '__int__') else 0)
    low_idx = int(subset["low"].idxmin() if hasattr(subset["low"].idxmin(), '__int__') else 0)

    diff = swing_high - swing_low
    if diff <= 0:
        return {"retracement": [], "extension": [], "swing_high": swing_high, "swing_low": swing_low, "trend": "flat"}

    # Determine trend: if high came after low → uptrend, else downtrend
    # Use position index for comparison
    high_pos = subset.index.get_loc(subset["high"].idxmax())
    low_pos = subset.index.get_loc(subset["low"].idxmin())
    is_uptrend = high_pos > low_pos

    retracement = []
    extension = []

    if is_uptrend:
        # Retracement from high back toward low
        for ratio in FIBONACCI_RATIOS:
            level = swing_high - diff * ratio
            retracement.append({
                "ratio": ratio,
                "label": f"{ratio:.1%}",
                "price": round(level, 6),
            })
        # Extension above high
        for ratio in FIBONACCI_EXT_RATIOS:
            level = swing_low + diff * ratio
            extension.append({
                "ratio": ratio,
                "label": f"{ratio:.1%}",
                "price": round(level, 6),
            })
    else:
        # Retracement from low back toward high (downtrend bounce)
        for ratio in FIBONACCI_RATIOS:
            level = swing_low + diff * ratio
            retracement.append({
                "ratio": ratio,
                "label": f"{ratio:.1%}",
                "price": round(level, 6),
            })
        # Extension below low
        for ratio in FIBONACCI_EXT_RATIOS:
            level = swing_high - diff * ratio
            extension.append({
                "ratio": ratio,
                "label": f"{ratio:.1%}",
                "price": round(level, 6),
            })

    return {
        "retracement": retracement,
        "extension": extension,
        "swing_high": swing_high,
        "swing_low": swing_low,
        "trend": "uptrend" if is_uptrend else "downtrend",
        "range": diff,
    }


# ──────────────────────────────────────────────
# Phase 7: Support / Resistance Cluster Zones
# ──────────────────────────────────────────────
def find_sr_clusters(
    df: pd.DataFrame, n_zones: int = 6, lookback: int = 200
) -> list[dict]:
    """
    Find support/resistance cluster zones by analyzing
    price level density from swing points + volume concentration.
    Returns sorted list of {price, strength, type, touches}.
    """
    subset = df.iloc[-lookback:] if len(df) >= lookback else df

    # Collect candidate levels from swing points
    sh_idx, sl_idx = find_swing_points_adaptive(subset["high"])
    _, sl_low_idx = find_swing_points_adaptive(subset["low"])

    levels = []
    for idx in sh_idx:
        levels.append(float(subset["high"].iloc[idx]))
    for idx in sl_low_idx:
        levels.append(float(subset["low"].iloc[idx]))

    if not levels:
        return []

    levels = np.array(levels)
    current_price = float(subset["close"].iloc[-1])

    # Cluster nearby levels using a tolerance of 0.5% of current price
    tolerance = current_price * 0.005
    clusters = []
    used = set()

    for i, level in enumerate(levels):
        if i in used:
            continue
        cluster_prices = [level]
        used.add(i)
        for j, other in enumerate(levels):
            if j not in used and abs(other - level) <= tolerance:
                cluster_prices.append(other)
                used.add(j)

        avg_price = np.mean(cluster_prices)
        touches = len(cluster_prices)
        strength = min(touches / 5.0, 1.0)  # Normalize by 5 touches

        sr_type = "resistance" if avg_price > current_price else "support"

        clusters.append({
            "price": round(avg_price, 6),
            "strength": round(strength, 2),
            "type": sr_type,
            "touches": touches,
            "distance_pct": round((avg_price - current_price) / current_price * 100, 2),
        })

    # Sort by distance from current price
    clusters.sort(key=lambda x: abs(x["distance_pct"]))
    return clusters[:n_zones]


# ──────────────────────────────────────────────
# Phase 7: BTC Correlation
# ──────────────────────────────────────────────
def compute_correlation(
    series_a: pd.Series, series_b: pd.Series, window: int = 30
) -> dict:
    """
    Compute rolling correlation between two price series.
    Returns: {current_corr, avg_corr, min_corr, max_corr, rolling_series}
    """
    if len(series_a) < window or len(series_b) < window:
        return {"current_corr": 0, "avg_corr": 0, "rolling": pd.Series(dtype=float)}

    # Align lengths
    min_len = min(len(series_a), len(series_b))
    a = series_a.iloc[-min_len:].pct_change().dropna()
    b = series_b.iloc[-min_len:].pct_change().dropna()

    min_len2 = min(len(a), len(b))
    a = a.iloc[-min_len2:]
    b = b.iloc[-min_len2:]

    if len(a) < window:
        return {"current_corr": 0, "avg_corr": 0, "rolling": pd.Series(dtype=float)}

    rolling_corr = a.rolling(window=window).corr(b)
    clean = rolling_corr.dropna()

    if clean.empty:
        return {"current_corr": 0, "avg_corr": 0, "rolling": pd.Series(dtype=float)}

    return {
        "current_corr": round(float(clean.iloc[-1]), 3),
        "avg_corr": round(float(clean.mean()), 3),
        "min_corr": round(float(clean.min()), 3),
        "max_corr": round(float(clean.max()), 3),
        "rolling": rolling_corr,
    }
