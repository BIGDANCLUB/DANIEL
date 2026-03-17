"""Data fetching layer: CCXT (CEX) + DexScreener (DEX)."""

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
    """Fetch OHLCV and market data from CEX via CCXT async."""

    def __init__(self):
        self._exchange: Optional[ccxt_async.Exchange] = None

    async def _get_exchange(self) -> ccxt_async.Exchange:
        if self._exchange is None:
            exchange_cls = getattr(ccxt_async, Config.CEX_EXCHANGE)
            params = {
                "enableRateLimit": True,
                "rateLimit": Config.CCXT_RATE_LIMIT_MS,
                "options": {"defaultType": Config.CEX_MARKET_TYPE},
            }
            if Config.BINANCE_API_KEY:
                params["apiKey"] = Config.BINANCE_API_KEY
                params["secret"] = Config.BINANCE_API_SECRET
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
        """Fetch OHLCV as DataFrame with columns [timestamp, open, high, low, close, volume]."""
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


# ──────────────────────────────────────────────
# DEX data via DexScreener API
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
            now = time.time() * 1000
            six_hours_ms = Config.LOOKBACK_HOURS * 3600 * 1000
            filtered = []
            for p in pairs:
                created = p.get("pairCreatedAt", 0)
                liq = p.get("liquidity", {}).get("usd", 0) or 0
                vol = p.get("volume", {}).get("h24", 0) or 0
                if (
                    (now - created) <= six_hours_ms or True  # include established pairs too
                ) and liq >= Config.DEXSCREENER_MIN_LIQUIDITY and vol >= Config.DEXSCREENER_MIN_VOLUME_24H:
                    filtered.append(p)
            return filtered
        except Exception as e:
            logger.warning("DexScreener trending error: %s", e)
            return []


# ──────────────────────────────────────────────
# CoinGlass API
# ──────────────────────────────────────────────
class CoinGlassFetcher:
    """CoinGlass API for funding rate, long/short ratio, order book."""

    @staticmethod
    def _headers() -> dict:
        return {
            "accept": "application/json",
            "CG-API-KEY": Config.COINGLASS_API_KEY,
            "coinglassSecret": Config.COINGLASS_API_KEY,
        }

    @classmethod
    def get_funding_rate(cls, symbol: str) -> list[dict]:
        """Get funding rate across exchanges."""
        if not Config.COINGLASS_API_KEY:
            return []
        try:
            resp = requests.get(
                f"{Config.COINGLASS_BASE_URL}/funding",
                headers=cls._headers(),
                params={"symbol": symbol.replace("/USDT:USDT", "").replace("/USDT", "")},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", [])
        except Exception as e:
            logger.warning("CoinGlass funding rate error: %s", e)
            return []

    @classmethod
    def get_long_short_ratio(cls, symbol: str, interval: str = "h1") -> list[dict]:
        """Get global long/short account ratio."""
        if not Config.COINGLASS_API_KEY:
            return []
        try:
            resp = requests.get(
                f"{Config.COINGLASS_BASE_URL}/long_short",
                headers=cls._headers(),
                params={
                    "symbol": symbol.replace("/USDT:USDT", "").replace("/USDT", ""),
                    "interval": interval,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", [])
        except Exception as e:
            logger.warning("CoinGlass long/short error: %s", e)
            return []

    @classmethod
    def get_order_book_depth(cls, symbol: str) -> dict:
        """Get aggregated order book from CoinGlass."""
        if not Config.COINGLASS_API_KEY:
            return {}
        try:
            resp = requests.get(
                f"{Config.COINGLASS_BASE_URL}/orderbook",
                headers=cls._headers(),
                params={"symbol": symbol.replace("/USDT:USDT", "").replace("/USDT", "")},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json().get("data", {})
        except Exception as e:
            logger.warning("CoinGlass order book error: %s", e)
            return {}


# ──────────────────────────────────────────────
# LunarCrush API (social boost)
# ──────────────────────────────────────────────
class LunarCrushFetcher:
    """LunarCrush API for social mentions and sentiment."""

    @classmethod
    def get_social_metrics(cls, symbol: str) -> dict:
        """Get social metrics for a given coin symbol."""
        if not Config.LUNARCRUSH_API_KEY:
            return {}
        try:
            clean = symbol.replace("/USDT:USDT", "").replace("/USDT", "").upper()
            resp = requests.get(
                f"{Config.LUNARCRUSH_BASE_URL}/coins/{clean}/v1",
                headers={"Authorization": f"Bearer {Config.LUNARCRUSH_API_KEY}"},
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json().get("data", {})
        except Exception as e:
            logger.warning("LunarCrush error for %s: %s", symbol, e)
            return {}
