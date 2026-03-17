"""
Technical analysis — Phase 2
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
"""

import logging
from typing import Optional
from itertools import combinations

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
    return ta.ema(df[col], length=period)


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
