"""
Core scanner engine — Phase 2
================================
- Multi-timeframe trendline confirmation (1H + 4H)
- CryptoPanic social filter integrated into scoring
- Pattern classification in results
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Optional

import pandas as pd

from config import Config
from data_fetcher import CEXFetcher, DexScreenerFetcher, CryptoPanicFetcher
from technical_analysis import (
    is_above_ema,
    detect_volume_spike,
    detect_trendline_break,
    confirm_trendline_multi_tf,
    compute_scan_score,
    compute_ema,
    PATTERN_LABELS,
)

logger = logging.getLogger(__name__)


class ScanResult:
    """Single coin scan result."""

    def __init__(
        self,
        symbol: str,
        source: str,
        price: float,
        change_pct: float,
        volume_24h: float,
        volume_ratio: float,
        above_ema: bool,
        trendline_break: dict,
        social_boost: bool,
        score: float,
        scan_time: datetime,
        extra: dict = None,
    ):
        self.symbol = symbol
        self.source = source
        self.price = price
        self.change_pct = change_pct
        self.volume_24h = volume_24h
        self.volume_ratio = volume_ratio
        self.above_ema = above_ema
        self.trendline_break = trendline_break
        self.social_boost = social_boost
        self.score = score
        self.scan_time = scan_time
        self.extra = extra or {}

    def to_dict(self) -> dict:
        breakout = self.trendline_break.get("breakout_type") or "—"
        pattern = self.trendline_break.get("pattern_label", "—")
        vol_conf = self.trendline_break.get("volume_confirmed", False)
        conf_bars = self.trendline_break.get("confirmation_bars", 0)
        return {
            "Symbol": self.symbol,
            "Source": self.source,
            "Price": self.price,
            "24h %": self.change_pct,
            "24h Vol": self.volume_24h,
            "Vol Ratio": self.volume_ratio,
            "Above 200EMA": self.above_ema,
            "Trendline Break": breakout,
            "Pattern": pattern,
            "Vol Confirm": vol_conf,
            "Conf Bars": conf_bars,
            "Break Strength": self.trendline_break.get("break_strength", 0),
            "Social": self.social_boost,
            "Score": self.score,
            "Scan Time": self.scan_time.strftime("%H:%M:%S"),
        }


class ScannerEngine:
    """Main scanner — Phase 2."""

    def __init__(self):
        self.cex = CEXFetcher()
        self._results_cache: list[ScanResult] = []
        self._last_scan: Optional[datetime] = None

    async def scan_cex(self) -> list[ScanResult]:
        """Scan top CEX futures pairs."""
        results = []
        try:
            symbols = await self.cex.fetch_top_symbols()
            logger.info("Scanning %d CEX symbols...", len(symbols))

            for symbol in symbols:
                try:
                    result = await self._analyze_cex_symbol(symbol)
                    if result:
                        results.append(result)
                except Exception as e:
                    logger.debug("Error analyzing %s: %s", symbol, e)
                    continue

        except Exception as e:
            logger.error("CEX scan failed: %s", e)
        finally:
            await self.cex.close()

        return results

    async def _analyze_cex_symbol(self, symbol: str) -> Optional[ScanResult]:
        """Analyze a single CEX symbol with Phase 2 enhancements."""
        # Fetch 1H OHLCV
        df_1h = await self.cex.fetch_ohlcv(symbol, timeframe="1h", limit=250)
        if df_1h.empty or len(df_1h) < 30:
            return None

        # Fetch 4H OHLCV
        df_4h = await self.cex.fetch_ohlcv(symbol, timeframe="4h", limit=250)

        # Volume spike (1H)
        vol_spike, vol_ratio = detect_volume_spike(df_1h, recent_bars=1, lookback_bars=24)

        # 200 EMA on 4H
        ema_ok = False
        if df_4h is not None and len(df_4h) >= 200:
            ema_ok = is_above_ema(df_4h, period=200)

        # Multi-timeframe trendline break (Phase 2)
        if df_4h is not None and len(df_4h) >= 30:
            multi_tf = confirm_trendline_multi_tf(df_1h, df_4h)
            tl_result = multi_tf["1h"]  # primary result from 1H
            # Boost break_strength if 4H also confirms
            if multi_tf["both_confirm"]:
                tl_result["break_strength"] = min(
                    tl_result.get("break_strength", 0) + 0.3, 1.0
                )
                tl_result["multi_tf_confirmed"] = True
            else:
                tl_result["multi_tf_confirmed"] = False
        else:
            tl_result = detect_trendline_break(df_1h)
            tl_result["multi_tf_confirmed"] = False

        # Social boost via CryptoPanic (Phase 2 integration)
        social = False
        try:
            social_data = CryptoPanicFetcher.detect_social_boost(symbol)
            social = social_data.get("boost", False)
        except Exception:
            pass

        # Score
        score = compute_scan_score(ema_ok, vol_spike, vol_ratio, tl_result, social)

        # Only include if at least one core condition is met
        if not (vol_spike or tl_result.get("resistance_break")):
            return None

        current_price = float(df_1h["close"].iloc[-1])
        ticker = await self.cex.fetch_ticker(symbol)
        change_pct = ticker.get("percentage", 0) or 0
        volume_24h = ticker.get("quoteVolume", 0) or 0

        return ScanResult(
            symbol=symbol,
            source="Binance Futures",
            price=current_price,
            change_pct=round(change_pct, 2),
            volume_24h=round(volume_24h, 0),
            volume_ratio=vol_ratio,
            above_ema=ema_ok,
            trendline_break=tl_result,
            social_boost=social,
            score=score,
            scan_time=datetime.now(timezone.utc),
            extra={"timeframe_analysis": "1H+4H"},
        )

    def scan_dex(self) -> list[ScanResult]:
        """Scan DexScreener for trending DEX pairs."""
        results = []
        for chain in Config.DEXSCREENER_CHAINS:
            try:
                pairs = DexScreenerFetcher.get_trending_tokens(chain)
                logger.info("DexScreener: %d pairs for %s", len(pairs), chain)
                for pair in pairs[:20]:
                    result = self._analyze_dex_pair(pair, chain)
                    if result:
                        results.append(result)
            except Exception as e:
                logger.warning("DexScreener scan error (%s): %s", chain, e)
        return results

    def _analyze_dex_pair(self, pair: dict, chain: str) -> Optional[ScanResult]:
        """Analyze a single DexScreener pair."""
        try:
            price_change = pair.get("priceChange", {})
            h1_change = price_change.get("h1", 0) or 0
            h6_change = price_change.get("h6", 0) or 0
            h24_change = price_change.get("h24", 0) or 0

            volume = pair.get("volume", {})
            vol_h1 = volume.get("h1", 0) or 0
            vol_h24 = volume.get("h24", 0) or 0

            hourly_avg = vol_h24 / 24 if vol_h24 > 0 else 0
            vol_ratio = vol_h1 / hourly_avg if hourly_avg > 0 else 0
            vol_spike = vol_ratio >= Config.VOLUME_SPIKE_MULTIPLIER

            # DEX simplified trendline (no deep OHLCV)
            tl_result = {
                "resistance_break": h1_change > 5 and h6_change > 10,
                "support_break": False,
                "breakout_type": "bullish" if h1_change > 5 else None,
                "break_strength": min(abs(h1_change) / 20, 1.0),
                "volume_confirmed": vol_spike,
                "pattern": "unknown",
                "pattern_label": "—",
                "confirmation_bars": 0,
                "multi_tf_confirmed": False,
            }

            above_ema = h24_change > 0

            # Social boost for DEX token
            social = False
            symbol_name = pair.get("baseToken", {}).get("symbol", "?")
            try:
                social_data = CryptoPanicFetcher.detect_social_boost(symbol_name)
                social = social_data.get("boost", False)
            except Exception:
                pass

            score = compute_scan_score(above_ema, vol_spike, vol_ratio, tl_result, social)

            if score < 20:
                return None

            quote_name = pair.get("quoteToken", {}).get("symbol", "?")
            display_symbol = f"{symbol_name}/{quote_name}"

            return ScanResult(
                symbol=display_symbol,
                source=f"DEX ({chain})",
                price=float(pair.get("priceUsd", 0) or 0),
                change_pct=round(h24_change, 2),
                volume_24h=round(vol_h24, 0),
                volume_ratio=round(vol_ratio, 2),
                above_ema=above_ema,
                trendline_break=tl_result,
                social_boost=social,
                score=score,
                scan_time=datetime.now(timezone.utc),
                extra={
                    "chain": chain,
                    "pair_address": pair.get("pairAddress", ""),
                    "liquidity_usd": pair.get("liquidity", {}).get("usd", 0),
                    "dexId": pair.get("dexId", ""),
                    "h1_change": h1_change,
                    "h6_change": h6_change,
                },
            )
        except Exception as e:
            logger.debug("DEX pair analysis error: %s", e)
            return None

    async def run_full_scan(self) -> list[ScanResult]:
        """Run full scan: CEX + DEX, sort by score."""
        logger.info("Starting full scan (Phase 2)...")
        start = time.time()

        cex_results = await self.scan_cex()
        dex_results = self.scan_dex()

        all_results = cex_results + dex_results
        all_results.sort(key=lambda r: r.score, reverse=True)

        self._results_cache = all_results
        self._last_scan = datetime.now(timezone.utc)

        elapsed = time.time() - start
        logger.info("Scan complete: %d results in %.1fs", len(all_results), elapsed)
        return all_results

    @property
    def cached_results(self) -> list[ScanResult]:
        return self._results_cache

    @property
    def last_scan_time(self) -> Optional[datetime]:
        return self._last_scan
