"""Core scanner engine: orchestrates fetching, analysis, and scoring."""

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
    compute_scan_score,
    compute_ema,
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
        return {
            "Symbol": self.symbol,
            "Source": self.source,
            "Price": self.price,
            "24h %": self.change_pct,
            "24h Vol": self.volume_24h,
            "Vol Ratio": self.volume_ratio,
            "Above 200EMA": self.above_ema,
            "Trendline Break": breakout,
            "Break Strength": self.trendline_break.get("break_strength", 0),
            "Social Boost": self.social_boost,
            "Score": self.score,
            "Scan Time": self.scan_time.strftime("%H:%M:%S"),
        }


class ScannerEngine:
    """Main scanner: fetches data, applies filters, returns scored results."""

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
        """Analyze a single CEX symbol."""
        # Fetch 1H OHLCV for volume spike + trendline
        df_1h = await self.cex.fetch_ohlcv(symbol, timeframe="1h", limit=250)
        if df_1h.empty or len(df_1h) < 30:
            return None

        # Fetch 4H OHLCV for 200 EMA check
        df_4h = await self.cex.fetch_ohlcv(symbol, timeframe="4h", limit=250)

        # Volume spike (1H)
        vol_spike, vol_ratio = detect_volume_spike(df_1h, recent_bars=1, lookback_bars=24)

        # 200 EMA on 4H
        ema_ok = False
        if df_4h is not None and len(df_4h) >= 200:
            ema_ok = is_above_ema(df_4h, period=200)

        # Trendline break detection on 1H
        tl_result = detect_trendline_break(df_1h)

        # Social boost (Phase 2 placeholder — always False for now unless API key is set)
        social = False

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
            vol_h6 = volume.get("h6", 0) or 0
            vol_h24 = volume.get("h24", 0) or 0

            # Simple volume spike: h1 vol > (h24 vol / 24) * 3
            hourly_avg = vol_h24 / 24 if vol_h24 > 0 else 0
            vol_ratio = vol_h1 / hourly_avg if hourly_avg > 0 else 0
            vol_spike = vol_ratio >= Config.VOLUME_SPIKE_MULTIPLIER

            # DEX pairs don't have deep OHLCV history, so trendline/EMA = simplified
            tl_result = {
                "resistance_break": h1_change > 5 and h6_change > 10,
                "support_break": False,
                "breakout_type": "bullish" if h1_change > 5 else None,
                "break_strength": min(abs(h1_change) / 20, 1.0),
            }

            above_ema = h24_change > 0  # simplified for DEX

            score = compute_scan_score(above_ema, vol_spike, vol_ratio, tl_result, False)

            if score < 20:
                return None

            symbol_name = pair.get("baseToken", {}).get("symbol", "?")
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
                social_boost=False,
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
        logger.info("Starting full scan...")
        start = time.time()

        # Run CEX async scan
        cex_results = await self.scan_cex()

        # Run DEX scan (sync, runs fast)
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
