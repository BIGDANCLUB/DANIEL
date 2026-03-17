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

    @classmethod
    def get_global_ls_history(
        cls, symbol: str, period: str = "1h", limit: int = 30
    ) -> pd.DataFrame:
        """Get historical global long/short ratio as DataFrame."""
        clean = cls._clean_symbol(symbol)
        try:
            resp = requests.get(
                f"{Config.BINANCE_FAPI_BASE}/futures/data/globalLongShortAccountRatio",
                params={"symbol": clean, "period": period, "limit": limit},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(data)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            df["longAccount"] = df["longAccount"].astype(float)
            df["shortAccount"] = df["shortAccount"].astype(float)
            df["longShortRatio"] = df["longShortRatio"].astype(float)
            return df.sort_values("timestamp")
        except Exception as e:
            logger.debug("Binance LS history error: %s", e)
            return pd.DataFrame()


# ──────────────────────────────────────────────
# Binance FAPI — Funding Rate History (free)
# ──────────────────────────────────────────────
class BinanceFundingHistoryFetcher:
    """Fetch historical funding rates from Binance FAPI (no key required)."""

    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        return symbol.replace("/USDT:USDT", "").replace("/USDT", "").upper() + "USDT"

    @classmethod
    def get_funding_history(cls, symbol: str, limit: int = 100) -> pd.DataFrame:
        """
        Binance FAPI: /fapi/v1/fundingRate
        Free, no API key needed. Returns up to 1000 records.
        """
        clean = cls._clean_symbol(symbol)
        try:
            resp = requests.get(
                f"{Config.BINANCE_FAPI_BASE}/fapi/v1/fundingRate",
                params={"symbol": clean, "limit": limit},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(data)
            df["fundingTime"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
            df["fundingRate"] = df["fundingRate"].astype(float)
            df["markPrice"] = df["markPrice"].astype(float)
            return df.sort_values("fundingTime")
        except Exception as e:
            logger.debug("Binance funding history error: %s", e)
            return pd.DataFrame()


# ──────────────────────────────────────────────
# Binance FAPI — Open Interest (free)
# ──────────────────────────────────────────────
class BinanceOpenInterestFetcher:
    """Fetch open interest data from Binance FAPI (no key required)."""

    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        return symbol.replace("/USDT:USDT", "").replace("/USDT", "").upper() + "USDT"

    @classmethod
    def get_current_oi(cls, symbol: str) -> dict:
        """Current open interest."""
        clean = cls._clean_symbol(symbol)
        try:
            resp = requests.get(
                f"{Config.BINANCE_FAPI_BASE}/fapi/v1/openInterest",
                params={"symbol": clean},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "openInterest": float(data.get("openInterest", 0)),
                "symbol": data.get("symbol", ""),
                "time": data.get("time", 0),
            }
        except Exception as e:
            logger.debug("Binance OI error: %s", e)
            return {}

    @classmethod
    def get_oi_history(cls, symbol: str, period: str = "1h", limit: int = 30) -> pd.DataFrame:
        """
        Historical open interest (sum).
        Binance FAPI: /futures/data/openInterestHist
        Free, no key required.
        """
        clean = cls._clean_symbol(symbol)
        try:
            resp = requests.get(
                f"{Config.BINANCE_FAPI_BASE}/futures/data/openInterestHist",
                params={"symbol": clean, "period": period, "limit": limit},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(data)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            df["sumOpenInterest"] = df["sumOpenInterest"].astype(float)
            df["sumOpenInterestValue"] = df["sumOpenInterestValue"].astype(float)
            return df.sort_values("timestamp")
        except Exception as e:
            logger.debug("Binance OI history error: %s", e)
            return pd.DataFrame()


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

    # Fundamental / news categories that drive price
    FUNDA_CATEGORIES = {
        "partnership": {
            "keywords": [
                "partner", "partnership", "collaborat", "integrat", "team up",
                "join forces", "alliance", "deal with",
            ],
            "label": "Partnership / Integration",
            "icon": "handshake",
            "color": "#42A5F5",
        },
        "listing": {
            "keywords": [
                "list", "listing", "listed on", "adds", "added to",
                "now available", "trading live", "launches on",
            ],
            "label": "Exchange Listing",
            "icon": "exchange",
            "color": "#AB47BC",
        },
        "upgrade": {
            "keywords": [
                "upgrade", "update", "hard fork", "mainnet", "testnet",
                "v2", "v3", "launch", "release", "deploy", "migration",
                "protocol upgrade",
            ],
            "label": "Protocol Upgrade / Launch",
            "icon": "rocket",
            "color": "#66BB6A",
        },
        "regulation": {
            "keywords": [
                "sec", "regulat", "approved", "approval", "etf",
                "legal", "compliance", "license", "lawsuit", "ban",
                "government", "congress", "legislation",
            ],
            "label": "Regulatory / Legal",
            "icon": "gavel",
            "color": "#FFA726",
        },
        "adoption": {
            "keywords": [
                "adopt", "accept", "payment", "merchant", "institutional",
                "whale", "buy", "bought", "accumul", "inflow",
                "corporate", "treasury",
            ],
            "label": "Adoption / Institutional Buy",
            "icon": "trending_up",
            "color": "#26A69A",
        },
        "tokenomics": {
            "keywords": [
                "burn", "buyback", "halving", "halvening", "supply",
                "deflation", "staking", "airdrop", "unlock", "vest",
            ],
            "label": "Tokenomics Event",
            "icon": "fire",
            "color": "#EF5350",
        },
        "hack_exploit": {
            "keywords": [
                "hack", "exploit", "vulnerability", "breach", "attack",
                "drain", "stolen", "compromis", "rug",
            ],
            "label": "Security Incident",
            "icon": "warning",
            "color": "#FF1744",
        },
    }

    @classmethod
    def get_news(cls, symbol: str, limit: int = 20) -> list[dict]:
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

    @classmethod
    def analyze_fundamental_driver(cls, symbol: str) -> dict:
        """
        Analyze whether a price move is driven by fundamental news.

        Returns:
        {
            "is_funda_driven": bool,
            "drivers": [
                {
                    "category": str,
                    "label": str,
                    "color": str,
                    "confidence": float (0-1),
                    "matched_keywords": [str],
                    "articles": [{"title": str, "source": str, "published_at": str, "url": str}],
                }
            ],
            "summary": str,
            "total_articles": int,
            "funda_articles": int,
        }
        """
        posts = cls.get_news(symbol, limit=20)
        result = {
            "is_funda_driven": False,
            "drivers": [],
            "summary": "",
            "total_articles": len(posts),
            "funda_articles": 0,
        }

        if not posts:
            result["summary"] = "No recent news found — price move likely technical or organic."
            return result

        # Classify each article into categories
        category_hits: dict[str, list] = {}
        for post in posts:
            title = (post.get("title") or "").lower()
            for cat_key, cat_def in cls.FUNDA_CATEGORIES.items():
                matched_kws = [kw for kw in cat_def["keywords"] if kw in title]
                if matched_kws:
                    if cat_key not in category_hits:
                        category_hits[cat_key] = []
                    category_hits[cat_key].append({
                        "title": post.get("title", ""),
                        "source": post.get("source", {}).get("title", "Unknown"),
                        "published_at": post.get("published_at", ""),
                        "url": post.get("url", ""),
                        "matched_keywords": matched_kws,
                    })

        if not category_hits:
            result["summary"] = (
                f"{len(posts)} articles found, but none match fundamental categories. "
                "Price move is likely technical (trendline break, volume spike) or "
                "driven by broader market sentiment."
            )
            return result

        # Build drivers sorted by article count (strongest signal first)
        drivers = []
        total_funda = 0
        for cat_key, articles in sorted(
            category_hits.items(), key=lambda x: len(x[1]), reverse=True
        ):
            cat_def = cls.FUNDA_CATEGORIES[cat_key]
            # Confidence: based on article count relative to total
            confidence = min(len(articles) / max(len(posts), 1) * 3, 1.0)
            all_kws = set()
            for a in articles:
                all_kws.update(a["matched_keywords"])
            drivers.append({
                "category": cat_key,
                "label": cat_def["label"],
                "color": cat_def["color"],
                "confidence": round(confidence, 2),
                "matched_keywords": sorted(all_kws),
                "articles": articles[:5],
                "article_count": len(articles),
            })
            total_funda += len(articles)

        result["drivers"] = drivers
        result["funda_articles"] = total_funda
        result["is_funda_driven"] = total_funda >= 2 or (
            total_funda >= 1 and drivers[0]["confidence"] >= 0.5
        )

        # Generate summary
        if result["is_funda_driven"]:
            top = drivers[0]
            others = [d["label"] for d in drivers[1:3]]
            summary = f"Price move likely driven by: {top['label']} ({top['article_count']} articles, {top['confidence']:.0%} confidence)"
            if others:
                summary += f". Also related: {', '.join(others)}"
            summary += "."
        else:
            summary = (
                f"Some fundamental news detected ({total_funda} articles), "
                "but not enough to confirm as the primary driver. "
                "Likely a mix of technical + fundamental factors."
            )
        result["summary"] = summary

        return result
