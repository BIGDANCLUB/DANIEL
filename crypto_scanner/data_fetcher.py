"""Data fetching layer — 100% Free APIs (Direct REST).

- Binance FAPI: Futures OHLCV, ticker, order book, funding rate (no key required)
- Bybit V5 API: Futures OHLCV, ticker (no key required)
- Binance Public FAPI: Long/Short ratio (no key required)
- DexScreener: DEX pair discovery (no key required)
- CryptoPanic: Social/news sentiment (free tier, key optional)
"""

import asyncio
import time
import logging
from typing import Optional

import pandas as pd
import requests

from config import Config

logger = logging.getLogger(__name__)

# Try importing ccxt for backward compatibility (optional)
try:
    import ccxt.async_support as ccxt_async
    HAS_CCXT = True
except ImportError:
    HAS_CCXT = False


# ──────────────────────────────────────────────
# CEX data via Direct REST API (no CCXT dependency)
# ──────────────────────────────────────────────
class CEXFetcher:
    """Fetch OHLCV, funding rate, and market data via direct REST API calls."""

    _BINANCE_FAPI = "https://fapi.binance.com"
    _BYBIT_API = "https://api.bybit.com"

    def __init__(self, exchange_id: str = None):
        self._exchange_id = exchange_id or Config.CEX_EXCHANGE
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "CryptoScanner/1.0",
            "Accept": "application/json",
        })

    async def close(self):
        """Close the session."""
        self._session.close()

    def _get(self, url: str, params: dict = None, timeout: int = 15) -> dict:
        """Make a GET request with error handling."""
        resp = self._session.get(url, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        """Convert CCXT-style symbol to exchange format: BTC/USDT:USDT -> BTCUSDT"""
        return symbol.replace("/USDT:USDT", "").replace("/USDT", "").upper() + "USDT"

    @staticmethod
    def _to_ccxt_symbol(raw: str) -> str:
        """Convert BTCUSDT -> BTC/USDT:USDT for internal use."""
        base = raw.replace("USDT", "")
        return f"{base}/USDT:USDT"

    # ── Top symbols ──
    async def fetch_top_symbols(self, top_n: int = None) -> list[str]:
        """Return top N USDT perpetual symbols by 24h quote volume."""
        top_n = top_n or Config.CEX_TOP_N

        if self._exchange_id in ("binance", "binanceusdm"):
            return await self._binance_top_symbols(top_n)
        elif self._exchange_id == "bybit":
            return await self._bybit_top_symbols(top_n)
        else:
            return []

    async def _binance_top_symbols(self, top_n: int) -> list[str]:
        data = self._get(f"{self._BINANCE_FAPI}/fapi/v1/ticker/24hr")
        # Filter USDT perpetuals and sort by quoteVolume
        perps = [
            t for t in data
            if t["symbol"].endswith("USDT") and not t["symbol"].endswith("_PERP")
        ]
        ranked = sorted(perps, key=lambda t: float(t.get("quoteVolume", 0)), reverse=True)
        return [self._to_ccxt_symbol(t["symbol"]) for t in ranked[:top_n]]

    async def _bybit_top_symbols(self, top_n: int) -> list[str]:
        data = self._get(
            f"{self._BYBIT_API}/v5/market/tickers",
            params={"category": "linear"},
        )
        tickers = data.get("result", {}).get("list", [])
        # Filter USDT pairs and sort by turnover24h
        usdt = [t for t in tickers if t["symbol"].endswith("USDT")]
        ranked = sorted(usdt, key=lambda t: float(t.get("turnover24h", 0)), reverse=True)
        return [self._to_ccxt_symbol(t["symbol"]) for t in ranked[:top_n]]

    # ── OHLCV ──
    async def fetch_ohlcv(
        self, symbol: str, timeframe: str = "1h", limit: int = 250
    ) -> pd.DataFrame:
        """Fetch OHLCV as DataFrame."""
        if self._exchange_id in ("binance", "binanceusdm"):
            return await self._binance_ohlcv(symbol, timeframe, limit)
        elif self._exchange_id == "bybit":
            return await self._bybit_ohlcv(symbol, timeframe, limit)
        return pd.DataFrame()

    async def _binance_ohlcv(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        clean = self._clean_symbol(symbol)
        # Binance uses interval names like 1m, 5m, 1h, 4h, 1d
        data = self._get(
            f"{self._BINANCE_FAPI}/fapi/v1/klines",
            params={"symbol": clean, "interval": timeframe, "limit": limit},
        )
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_vol",
            "taker_buy_quote_vol", "ignore",
        ])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        return df

    async def _bybit_ohlcv(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        clean = self._clean_symbol(symbol)
        # Bybit interval mapping
        interval_map = {"1m": "1", "5m": "5", "15m": "15", "30m": "30",
                        "1h": "60", "4h": "240", "1d": "D"}
        interval = interval_map.get(timeframe, "60")
        data = self._get(
            f"{self._BYBIT_API}/v5/market/kline",
            params={"category": "linear", "symbol": clean,
                    "interval": interval, "limit": limit},
        )
        rows = data.get("result", {}).get("list", [])
        if not rows:
            return pd.DataFrame()
        # Bybit returns [startTime, open, high, low, close, volume, turnover] newest first
        df = pd.DataFrame(rows, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "turnover",
        ])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)  # Bybit returns newest first
        return df

    # ── Ticker ──
    async def fetch_ticker(self, symbol: str) -> dict:
        """Fetch 24h ticker data."""
        if self._exchange_id in ("binance", "binanceusdm"):
            return await self._binance_ticker(symbol)
        elif self._exchange_id == "bybit":
            return await self._bybit_ticker(symbol)
        return {}

    async def _binance_ticker(self, symbol: str) -> dict:
        clean = self._clean_symbol(symbol)
        data = self._get(
            f"{self._BINANCE_FAPI}/fapi/v1/ticker/24hr",
            params={"symbol": clean},
        )
        return {
            "symbol": symbol,
            "last": float(data.get("lastPrice", 0)),
            "percentage": float(data.get("priceChangePercent", 0)),
            "quoteVolume": float(data.get("quoteVolume", 0)),
        }

    async def _bybit_ticker(self, symbol: str) -> dict:
        clean = self._clean_symbol(symbol)
        data = self._get(
            f"{self._BYBIT_API}/v5/market/tickers",
            params={"category": "linear", "symbol": clean},
        )
        tickers = data.get("result", {}).get("list", [])
        if not tickers:
            return {"symbol": symbol, "last": 0, "percentage": 0, "quoteVolume": 0}
        t = tickers[0]
        last = float(t.get("lastPrice", 0))
        prev = float(t.get("prevPrice24h", 0))
        pct = ((last - prev) / prev * 100) if prev > 0 else 0
        return {
            "symbol": symbol,
            "last": last,
            "percentage": round(pct, 2),
            "quoteVolume": float(t.get("turnover24h", 0)),
        }

    # ── Order Book ──
    async def fetch_order_book(self, symbol: str, limit: int = 20) -> dict:
        """Fetch order book depth."""
        if self._exchange_id in ("binance", "binanceusdm"):
            clean = self._clean_symbol(symbol)
            data = self._get(
                f"{self._BINANCE_FAPI}/fapi/v1/depth",
                params={"symbol": clean, "limit": limit},
            )
            return {
                "bids": [[float(p), float(q)] for p, q in data.get("bids", [])],
                "asks": [[float(p), float(q)] for p, q in data.get("asks", [])],
            }
        elif self._exchange_id == "bybit":
            clean = self._clean_symbol(symbol)
            data = self._get(
                f"{self._BYBIT_API}/v5/market/orderbook",
                params={"category": "linear", "symbol": clean, "limit": limit},
            )
            result = data.get("result", {})
            return {
                "bids": [[float(p), float(q)] for p, q in result.get("b", [])],
                "asks": [[float(p), float(q)] for p, q in result.get("a", [])],
            }
        return {"bids": [], "asks": []}

    # ── Funding Rate ──
    async def fetch_funding_rate(self, symbol: str) -> dict:
        """Fetch current funding rate."""
        if self._exchange_id in ("binance", "binanceusdm"):
            clean = self._clean_symbol(symbol)
            try:
                data = self._get(
                    f"{self._BINANCE_FAPI}/fapi/v1/premiumIndex",
                    params={"symbol": clean},
                )
                return {
                    "fundingRate": float(data.get("lastFundingRate", 0)),
                    "fundingTimestamp": data.get("nextFundingTime"),
                    "markPrice": float(data.get("markPrice", 0)),
                }
            except Exception as e:
                logger.debug("Binance funding rate error for %s: %s", symbol, e)
                return {}
        elif self._exchange_id == "bybit":
            clean = self._clean_symbol(symbol)
            try:
                data = self._get(
                    f"{self._BYBIT_API}/v5/market/tickers",
                    params={"category": "linear", "symbol": clean},
                )
                tickers = data.get("result", {}).get("list", [])
                if tickers:
                    return {
                        "fundingRate": float(tickers[0].get("fundingRate", 0)),
                        "fundingTimestamp": None,
                        "markPrice": float(tickers[0].get("markPrice", 0)),
                    }
            except Exception as e:
                logger.debug("Bybit funding rate error for %s: %s", symbol, e)
            return {}
        return {}


# ──────────────────────────────────────────────
# Multi-exchange funding rate (direct REST)
# ──────────────────────────────────────────────
class MultiExchangeFundingFetcher:
    """Fetch funding rates from multiple exchanges using direct REST API."""

    EXCHANGES = ["binance", "bybit"]

    @classmethod
    async def fetch_all(cls, symbol: str) -> list[dict]:
        """Fetch funding rate for a symbol across multiple exchanges."""
        results = []
        base = symbol.replace("/USDT:USDT", "").replace("/USDT", "").upper()
        clean = base + "USDT"

        # Binance
        try:
            resp = requests.get(
                f"https://fapi.binance.com/fapi/v1/premiumIndex",
                params={"symbol": clean},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            results.append({
                "exchange": "Binance",
                "rate": float(data.get("lastFundingRate", 0)),
                "timestamp": data.get("time"),
                "next_timestamp": data.get("nextFundingTime"),
            })
        except Exception as e:
            logger.debug("Binance funding rate error: %s", e)

        # Bybit
        try:
            resp = requests.get(
                f"https://api.bybit.com/v5/market/tickers",
                params={"category": "linear", "symbol": clean},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            tickers = data.get("result", {}).get("list", [])
            if tickers:
                results.append({
                    "exchange": "Bybit",
                    "rate": float(tickers[0].get("fundingRate", 0)),
                    "timestamp": None,
                    "next_timestamp": None,
                })
        except Exception as e:
            logger.debug("Bybit funding rate error: %s", e)

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
