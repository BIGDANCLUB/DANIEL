"""
Phase 8A: Multi-Timeframe Strategy Engine
==========================================
HTF (Higher Timeframe) direction + LTF (Lower Timeframe) entry precision.
Combines 1m, 5m, 15m, 1h, 4h analysis for optimal signal confluence.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from technical_analysis import (
    detect_trendline_break,
    detect_volume_spike,
    is_above_ema,
    compute_rsi,
    get_rsi_signal,
    get_macd_signal,
    get_bb_signal,
)

logger = logging.getLogger("mtf_strategy")


# ──────────────────────────────────────────────
# Timeframe weight configuration
# ──────────────────────────────────────────────
TIMEFRAME_WEIGHTS = {
    "1m": 0.05,
    "5m": 0.10,
    "15m": 0.15,
    "1h": 0.30,
    "4h": 0.40,
}

TIMEFRAME_MIN_BARS = {
    "1m": 60,
    "5m": 60,
    "15m": 50,
    "1h": 30,
    "4h": 30,
}


@dataclass
class TimeframeAnalysis:
    """Analysis result for a single timeframe."""
    timeframe: str
    trend: str  # "bullish", "bearish", "neutral"
    trendline_break: dict = field(default_factory=dict)
    rsi: dict = field(default_factory=dict)
    macd: dict = field(default_factory=dict)
    bb: dict = field(default_factory=dict)
    volume_spike: bool = False
    volume_ratio: float = 0.0
    above_ema: bool = False
    score: float = 0.0


@dataclass
class MTFSignal:
    """Combined multi-timeframe signal."""
    symbol: str
    htf_trend: str  # 4h dominant direction
    ltf_entry: str  # 1h/15m entry trigger
    timeframes: dict = field(default_factory=dict)  # tf -> TimeframeAnalysis
    alignment_score: float = 0.0  # 0-100 how well TFs align
    entry_quality: str = "low"  # "low", "medium", "high", "premium"
    recommended_action: str = "wait"  # "long", "short", "wait"
    confluence_factors: list = field(default_factory=list)
    mtf_score_bonus: float = 0.0  # bonus to add to base score


def analyze_single_timeframe(df: pd.DataFrame, timeframe: str) -> TimeframeAnalysis:
    """Run full analysis on a single timeframe DataFrame."""
    if df is None or df.empty or len(df) < TIMEFRAME_MIN_BARS.get(timeframe, 30):
        return TimeframeAnalysis(timeframe=timeframe, trend="neutral")

    # Trendline break
    tl = detect_trendline_break(df)

    # Volume
    vol_spike, vol_ratio = detect_volume_spike(df, recent_bars=1, lookback_bars=24)

    # EMA (only meaningful for 1h+ timeframes)
    ema_ok = False
    if timeframe in ("1h", "4h") and len(df) >= 200:
        ema_ok = is_above_ema(df, period=200)
    elif timeframe in ("15m",) and len(df) >= 50:
        ema_ok = is_above_ema(df, period=50)

    # Indicators
    rsi_data = get_rsi_signal(df)
    macd_data = get_macd_signal(df)
    bb_data = get_bb_signal(df)

    # Determine trend
    trend = _determine_trend(tl, rsi_data, macd_data, ema_ok)

    # Compute per-TF score
    score = _compute_tf_score(tl, vol_spike, vol_ratio, ema_ok, rsi_data, macd_data, bb_data)

    return TimeframeAnalysis(
        timeframe=timeframe,
        trend=trend,
        trendline_break=tl,
        rsi=rsi_data,
        macd=macd_data,
        bb=bb_data,
        volume_spike=vol_spike,
        volume_ratio=vol_ratio,
        above_ema=ema_ok,
        score=score,
    )


def _determine_trend(tl: dict, rsi: dict, macd: dict, ema_ok: bool) -> str:
    """Determine trend direction from indicators."""
    bullish_signals = 0
    bearish_signals = 0

    if tl.get("resistance_break"):
        bullish_signals += 2
    if tl.get("support_break"):
        bearish_signals += 2

    if ema_ok:
        bullish_signals += 1
    else:
        bearish_signals += 1

    if macd.get("trend") == "bullish":
        bullish_signals += 1
    elif macd.get("trend") == "bearish":
        bearish_signals += 1

    if rsi.get("bullish_zone"):
        bullish_signals += 1
    if rsi.get("overbought"):
        bearish_signals += 1
    if rsi.get("oversold"):
        bullish_signals += 1  # potential reversal

    if bullish_signals > bearish_signals + 1:
        return "bullish"
    elif bearish_signals > bullish_signals + 1:
        return "bearish"
    return "neutral"


def _compute_tf_score(
    tl: dict, vol_spike: bool, vol_ratio: float,
    ema_ok: bool, rsi: dict, macd: dict, bb: dict
) -> float:
    """Compute score for a single timeframe (0-100)."""
    score = 0.0

    # Trendline break
    if tl.get("resistance_break") or tl.get("support_break"):
        score += 30
        score += min(tl.get("break_strength", 0) * 15, 15)
        if tl.get("volume_confirmed"):
            score += 5

    # Volume
    if vol_spike:
        score += min(vol_ratio * 3, 12)

    # EMA
    if ema_ok:
        score += 10

    # RSI
    if rsi.get("bullish_zone") or rsi.get("signal") == "bullish_cross":
        score += 8
    elif rsi.get("oversold"):
        score += 5

    # MACD
    if macd.get("bullish_cross"):
        score += 10
    elif macd.get("trend") == "bullish":
        score += 5

    # BB
    if bb.get("squeeze"):
        score += 8
    elif bb.get("signal") == "above_upper":
        score += 4

    return min(score, 100)


def compute_mtf_signal(
    symbol: str,
    tf_data: dict[str, pd.DataFrame],
) -> MTFSignal:
    """
    Compute multi-timeframe signal from dict of {timeframe: DataFrame}.

    Parameters
    ----------
    symbol : str
    tf_data : dict mapping timeframe string to OHLCV DataFrame
              e.g. {"1h": df_1h, "4h": df_4h, "15m": df_15m}
    """
    analyses = {}
    for tf, df in tf_data.items():
        analyses[tf] = analyze_single_timeframe(df, tf)

    # HTF trend (4h > 1h priority)
    htf_trend = "neutral"
    if "4h" in analyses:
        htf_trend = analyses["4h"].trend
    elif "1h" in analyses:
        htf_trend = analyses["1h"].trend

    # LTF entry signal (15m > 5m > 1m)
    ltf_entry = "neutral"
    for ltf in ("15m", "5m", "1m"):
        if ltf in analyses:
            ltf_entry = analyses[ltf].trend
            break

    # Alignment score — how well do TFs agree?
    alignment_score, confluence = _compute_alignment(analyses, htf_trend)

    # Entry quality
    entry_quality = _classify_entry_quality(alignment_score, analyses)

    # Recommended action
    recommended = _determine_action(htf_trend, ltf_entry, alignment_score, analyses)

    # MTF bonus for base score
    mtf_bonus = _compute_mtf_bonus(alignment_score, entry_quality, analyses)

    return MTFSignal(
        symbol=symbol,
        htf_trend=htf_trend,
        ltf_entry=ltf_entry,
        timeframes={tf: a for tf, a in analyses.items()},
        alignment_score=alignment_score,
        entry_quality=entry_quality,
        recommended_action=recommended,
        confluence_factors=confluence,
        mtf_score_bonus=mtf_bonus,
    )


def _compute_alignment(
    analyses: dict[str, TimeframeAnalysis], htf_trend: str
) -> tuple[float, list[str]]:
    """Compute alignment score (0-100) and list of confluence factors."""
    if not analyses:
        return 0.0, []

    score = 0.0
    confluence = []
    total_weight = 0.0

    for tf, analysis in analyses.items():
        weight = TIMEFRAME_WEIGHTS.get(tf, 0.1)
        total_weight += weight

        if analysis.trend == htf_trend and htf_trend != "neutral":
            score += weight * 100
            confluence.append(f"{tf} trend aligned ({analysis.trend})")

        # Bonus for volume confirmation across TFs
        if analysis.volume_spike:
            score += weight * 20
            confluence.append(f"{tf} volume spike ({analysis.volume_ratio:.1f}x)")

        # Bonus for trendline break across TFs
        if analysis.trendline_break.get("resistance_break") and htf_trend == "bullish":
            score += weight * 30
            confluence.append(f"{tf} resistance break")
        elif analysis.trendline_break.get("support_break") and htf_trend == "bearish":
            score += weight * 30
            confluence.append(f"{tf} support break")

    if total_weight > 0:
        score = min(score / total_weight, 100)

    return round(score, 1), confluence


def _classify_entry_quality(
    alignment_score: float, analyses: dict[str, TimeframeAnalysis]
) -> str:
    """Classify entry quality based on alignment and indicator confluence."""
    # Count strong signals across timeframes
    strong_count = sum(1 for a in analyses.values() if a.score >= 60)
    total = len(analyses)

    if alignment_score >= 80 and strong_count >= 3:
        return "premium"
    elif alignment_score >= 60 and strong_count >= 2:
        return "high"
    elif alignment_score >= 40:
        return "medium"
    return "low"


def _determine_action(
    htf_trend: str, ltf_entry: str, alignment: float,
    analyses: dict[str, TimeframeAnalysis]
) -> str:
    """Determine recommended action."""
    if alignment < 30:
        return "wait"

    # HTF bullish + LTF confirms = long
    if htf_trend == "bullish" and ltf_entry == "bullish" and alignment >= 50:
        return "long"
    # HTF bearish + LTF confirms = short
    elif htf_trend == "bearish" and ltf_entry == "bearish" and alignment >= 50:
        return "short"
    # HTF has direction but LTF not yet confirmed
    elif htf_trend != "neutral" and alignment >= 40:
        return f"wait_for_{htf_trend}_entry"

    return "wait"


def _compute_mtf_bonus(
    alignment: float, quality: str,
    analyses: dict[str, TimeframeAnalysis]
) -> float:
    """Compute bonus points to add to the base scan score."""
    bonus = 0.0

    # Alignment bonus (max 15)
    bonus += min(alignment / 100 * 15, 15)

    # Quality bonus
    quality_bonus = {"premium": 10, "high": 6, "medium": 3, "low": 0}
    bonus += quality_bonus.get(quality, 0)

    # Cross-TF volume confirmation bonus
    vol_confirmed_tfs = sum(1 for a in analyses.values() if a.volume_spike)
    if vol_confirmed_tfs >= 3:
        bonus += 5
    elif vol_confirmed_tfs >= 2:
        bonus += 3

    return min(bonus, 25)  # Cap at 25 bonus points


async def fetch_mtf_data(
    fetcher, symbol: str, timeframes: list[str] = None
) -> dict[str, pd.DataFrame]:
    """
    Fetch OHLCV data for multiple timeframes concurrently.

    Parameters
    ----------
    fetcher : CEXFetcher instance
    symbol : str
    timeframes : list of timeframe strings, default ["15m", "1h", "4h"]
    """
    if timeframes is None:
        timeframes = ["15m", "1h", "4h"]

    bar_limits = {
        "1m": 200,
        "5m": 200,
        "15m": 200,
        "1h": 250,
        "4h": 250,
    }

    tasks = [
        fetcher.fetch_ohlcv(symbol, timeframe=tf, limit=bar_limits.get(tf, 200))
        for tf in timeframes
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    tf_data = {}
    for tf, result in zip(timeframes, results):
        if isinstance(result, pd.DataFrame) and not result.empty:
            tf_data[tf] = result
        elif isinstance(result, Exception):
            logger.debug("Failed to fetch %s for %s: %s", tf, symbol, result)

    return tf_data
