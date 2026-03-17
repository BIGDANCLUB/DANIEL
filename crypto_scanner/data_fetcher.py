"""Data fetching layer — 100% Free APIs.

- CCXT (async): Binance/Bybit OHLCV, ticker, order book, funding rate
- Binance Public FAPI: Long/Short ratio (no key required)
- DexScreener: DEX pair discovery (no key required)
- CryptoPanic: Social/news sentiment (free tier, key optional)
"""

import asyncio
import time
import logging
from typing import Optional

import ccxt.async_support as ccxt_async
import pandas as pd
import requests

from config import Config

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# CEX data via CCXT (async)
# ──────────────────────────────────────────────
class CEXFetcher:
    """Fetch OHLCV, funding rate, and market data from CEX via CCXT async."""

    def __init__(self, exchange_id: str = None):
        self._exchange: Optional[ccxt_async.Exchange] = None
        self._exchange_id = exchange_id or Config.CEX_EXCHANGE

    async def _get_exchange(self) -> ccxt_async.Exchange:
        if self._exchange is None:
            exchange_cls = getattr(ccxt_async, self._exchange_id)
            params = {
                "enableRateLimit": True,
                "rateLimit": Config.CCXT_RATE_LIMIT_MS,
                "options": {"defaultType": Config.CEX_MARKET_TYPE},
            }
            if self._exchange_id == "binance" and Config.BINANCE_API_KEY:
                params["apiKey"] = Config.BINANCE_API_KEY
                params["secret"] = Config.BINANCE_API_SECRET
            elif self._exchange_id == "bybit" and Config.BYBIT_API_KEY:
                params["apiKey"] = Config.BYBIT_API_KEY
                params["secret"] = Config.BYBIT_API_SECRET
            self._exchange = exchange_cls(params)
        return self._exchange

    async def close(self):
        if self._exchange:
            await self._exchange.close()
            self._exchange = None

    async def fetch_top_symbols(self, top_n: int = None) -> list[str]:
        """Return top N USDT perpetual symbols by 24h quote volume."""
        top_n = top_n or Config.CEX_TOP_N
        ex = await self._get_exchange()
        await ex.load_markets()
        perps = [
            s for s, m in ex.markets.items()
            if m.get("swap") and m.get("quote") == "USDT" and m.get("active")
        ]
        tickers = await ex.fetch_tickers(perps)
        ranked = sorted(
            tickers.values(),
            key=lambda t: t.get("quoteVolume") or 0,
            reverse=True,
        )
        return [t["symbol"] for t in ranked[:top_n]]

    async def fetch_ohlcv(
        self, symbol: str, timeframe: str = "1h", limit: int = 250
    ) -> pd.DataFrame:
        """Fetch OHLCV as DataFrame."""
        ex = await self._get_exchange()
        raw = await ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        return df

    async def fetch_order_book(self, symbol: str, limit: int = 20) -> dict:
        """Fetch order book depth."""
        ex = await self._get_exchange()
        return await ex.fetch_order_book(symbol, limit=limit)

    async def fetch_ticker(self, symbol: str) -> dict:
        ex = await self._get_exchange()
        return await ex.fetch_ticker(symbol)

    async def fetch_funding_rate(self, symbol: str) -> dict:
        """Fetch current funding rate via CCXT (free, no key needed)."""
        ex = await self._get_exchange()
        try:
            fr = await ex.fetch_funding_rate(symbol)
            return fr
        except Exception as e:
            logger.debug("CCXT funding rate error for %s: %s", symbol, e)
            return {}


# ──────────────────────────────────────────────
# Multi-exchange funding rate (all free via CCXT)
# ──────────────────────────────────────────────
class MultiExchangeFundingFetcher:
    """Fetch funding rates from multiple exchanges using CCXT (all free)."""

    EXCHANGES = ["binance", "bybit"]

    @classmethod
    async def fetch_all(cls, symbol: str) -> list[dict]:
        """Fetch funding rate for a symbol across multiple exchanges."""
        results = []
        # Map symbol to each exchange's format
        base = symbol.replace("/USDT:USDT", "").replace("/USDT", "")
        ccxt_symbol = f"{base}/USDT:USDT"

        for ex_id in cls.EXCHANGES:
            exchange = None
            try:
                exchange_cls = getattr(ccxt_async, ex_id)
                exchange = exchange_cls({
                    "enableRateLimit": True,
                    "options": {"defaultType": "swap"},
                })
                await exchange.load_markets()
                if ccxt_symbol in exchange.markets:
                    fr = await exchange.fetch_funding_rate(ccxt_symbol)
                    rate = fr.get("fundingRate", 0) or 0
                    results.append({
                        "exchange": ex_id.capitalize(),
                        "rate": rate,
                        "timestamp": fr.get("fundingTimestamp"),
                        "next_timestamp": fr.get("nextFundingTimestamp"),
                    })
            except Exception as e:
                logger.debug("Funding rate %s/%s error: %s", ex_id, symbol, e)
            finally:
                if exchange:
                    await exchange.close()

        return results


# ──────────────────────────────────────────────
# Binance Public FAPI — Long/Short ratio (free)
# ──────────────────────────────────────────────
class BinanceLongShortFetcher:
    """Fetch long/short ratio from Binance public futures API (no key required)."""

    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        return symbol.replace("/USDT:USDT", "").replace("/USDT", "").upper() + "USDT"

    @classmethod
    def get_global_long_short_ratio(
        cls, symbol: str, period: str = "1h", limit: int = 1
    ) -> list[dict]:
        """
        Global long/short account ratio.
        Binance FAPI: /futures/data/globalLongShortAccountRatio
        Free, no API key needed.
        """
        clean = cls._clean_symbol(symbol)
        try:
            resp = requests.get(
                f"{Config.BINANCE_FAPI_BASE}/futures/data/globalLongShortAccountRatio",
                params={"symbol": clean, "period": period, "limit": limit},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "exchange": "Binance (Global)",
                    "longRatio": float(d.get("longAccount", 0.5)),
                    "shortRatio": float(d.get("shortAccount", 0.5)),
                    "longShortRatio": float(d.get("longShortRatio", 1.0)),
                    "timestamp": d.get("timestamp"),
                }
                for d in data
            ]
        except Exception as e:
            logger.debug("Binance global LS ratio error: %s", e)
            return []

    @classmethod
    def get_top_trader_long_short_ratio(
        cls, symbol: str, period: str = "1h", limit: int = 1
    ) -> list[dict]:
        """
        Top trader long/short ratio (accounts).
        Binance FAPI: /futures/data/topLongShortAccountRatio
        Free, no API key needed.
        """
        clean = cls._clean_symbol(symbol)
        try:
            resp = requests.get(
                f"{Config.BINANCE_FAPI_BASE}/futures/data/topLongShortAccountRatio",
                params={"symbol": clean, "period": period, "limit": limit},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "exchange": "Binance (Top Traders)",
                    "longRatio": float(d.get("longAccount", 0.5)),
                    "shortRatio": float(d.get("shortAccount", 0.5)),
                    "longShortRatio": float(d.get("longShortRatio", 1.0)),
                    "timestamp": d.get("timestamp"),
                }
                for d in data
            ]
        except Exception as e:
            logger.debug("Binance top trader LS ratio error: %s", e)
            return []

    @classmethod
    def get_top_trader_long_short_position_ratio(
        cls, symbol: str, period: str = "1h", limit: int = 1
    ) -> list[dict]:
        """
        Top trader long/short ratio (positions).
        Binance FAPI: /futures/data/topLongShortPositionRatio
        Free, no API key needed.
        """
        clean = cls._clean_symbol(symbol)
        try:
            resp = requests.get(
                f"{Config.BINANCE_FAPI_BASE}/futures/data/topLongShortPositionRatio",
                params={"symbol": clean, "period": period, "limit": limit},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "exchange": "Binance (Top Positions)",
                    "longRatio": float(d.get("longAccount", 0.5)),
                    "shortRatio": float(d.get("shortAccount", 0.5)),
                    "longShortRatio": float(d.get("longShortRatio", 1.0)),
                    "timestamp": d.get("timestamp"),
                }
                for d in data
            ]
        except Exception as e:
            logger.debug("Binance top position LS ratio error: %s", e)
            return []

    @classmethod
    def get_all_ratios(cls, symbol: str) -> list[dict]:
        """Get all 3 types of long/short ratios combined."""
        results = []
        results.extend(cls.get_global_long_short_ratio(symbol))
        results.extend(cls.get_top_trader_long_short_ratio(symbol))
        results.extend(cls.get_top_trader_long_short_position_ratio(symbol))
        return results


# ──────────────────────────────────────────────
# DEX data via DexScreener API (free, no key)
# ──────────────────────────────────────────────
class DexScreenerFetcher:
    """Fetch new/trending pairs from DexScreener (free, no key)."""

    BASE = "https://api.dexscreener.com"
    _last_call: float = 0

    @classmethod
    def _rate_limit(cls):
        elapsed = time.time() - cls._last_call
        if elapsed < Config.DEXSCREENER_RATE_LIMIT_S:
            time.sleep(Config.DEXSCREENER_RATE_LIMIT_S - elapsed)
        cls._last_call = time.time()

    @classmethod
    def search_pairs(cls, query: str = "SOL") -> list[dict]:
        """Search DexScreener for pairs matching a query."""
        cls._rate_limit()
        try:
            resp = requests.get(
                f"{cls.BASE}/latest/dex/search",
                params={"q": query},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json().get("pairs", [])
        except Exception as e:
            logger.warning("DexScreener search error: %s", e)
            return []

    @classmethod
    def get_token_profiles(cls, chain: str = "solana") -> list[dict]:
        """Get boosted / new tokens."""
        cls._rate_limit()
        try:
            resp = requests.get(
                f"{cls.BASE}/token-boosts/top/v1",
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list):
                return [t for t in data if t.get("chainId") == chain]
            return []
        except Exception as e:
            logger.warning("DexScreener token profiles error: %s", e)
            return []

    @classmethod
    def get_pairs_by_chain(cls, chain: str, pair_addresses: list[str]) -> list[dict]:
        """Fetch pair data by address list."""
        if not pair_addresses:
            return []
        cls._rate_limit()
        addrs = ",".join(pair_addresses[:30])
        try:
            resp = requests.get(
                f"{cls.BASE}/latest/dex/pairs/{chain}/{addrs}",
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json().get("pairs", [])
        except Exception as e:
            logger.warning("DexScreener pairs error: %s", e)
            return []

    @classmethod
    def get_trending_tokens(cls, chain: str = "solana") -> list[dict]:
        """Get recently created/trending pairs for a chain with filters."""
        cls._rate_limit()
        try:
            resp = requests.get(
                f"{cls.BASE}/latest/dex/search",
                params={"q": f"chain:{chain}"},
                timeout=10,
            )
            resp.raise_for_status()
            pairs = resp.json().get("pairs", [])
            filtered = []
            for p in pairs:
                liq = p.get("liquidity", {}).get("usd", 0) or 0
                vol = p.get("volume", {}).get("h24", 0) or 0
                if liq >= Config.DEXSCREENER_MIN_LIQUIDITY and vol >= Config.DEXSCREENER_MIN_VOLUME_24H:
                    filtered.append(p)
            return filtered
        except Exception as e:
            logger.warning("DexScreener trending error: %s", e)
            return []


# ──────────────────────────────────────────────
# CryptoPanic API — Social/news (free tier)
# ──────────────────────────────────────────────
class CryptoPanicFetcher:
    """
    CryptoPanic free API for crypto news aggregation.
    Free tier: public posts, no auth required (auth_token optional for more).
    Detects 'breakout', 'trendline', 'pump' mentions.
    """

    BREAKOUT_KEYWORDS = [
        "breakout", "trendline", "broke out", "breaking out",
        "pump", "surge", "rally", "moon", "explosion",
    ]

    @classmethod
    def get_news(cls, symbol: str, limit: int = 10) -> list[dict]:
        """Get recent news/posts for a coin."""
        clean = symbol.replace("/USDT:USDT", "").replace("/USDT", "").upper()
        params = {
            "currencies": clean,
            "kind": "news",
            "public": "true",
        }
        if Config.CRYPTOPANIC_API_KEY:
            params["auth_token"] = Config.CRYPTOPANIC_API_KEY

        try:
            resp = requests.get(
                f"{Config.CRYPTOPANIC_BASE_URL}/posts/",
                params=params,
                timeout=10,
            )
            resp.raise_for_status()
            results = resp.json().get("results", [])
            return results[:limit]
        except Exception as e:
            logger.debug("CryptoPanic error for %s: %s", clean, e)
            return []

    @classmethod
    def detect_social_boost(cls, symbol: str) -> dict:
        """
        Check if there are recent breakout/trendline mentions.
        Returns {boost: bool, mention_count: int, matching_titles: list}.
        """
        posts = cls.get_news(symbol)
        matching = []
        for post in posts:
            title = (post.get("title") or "").lower()
            if any(kw in title for kw in cls.BREAKOUT_KEYWORDS):
                matching.append(post.get("title", ""))

        return {
            "boost": len(matching) >= 1,
            "total_posts": len(posts),
            "breakout_mentions": len(matching),
            "matching_titles": matching[:3],
        }
