"""Configuration management for Crypto Scanner — 100% Free APIs."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API Keys (optional, for higher rate limits only)
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
    BYBIT_API_KEY: str = os.getenv("BYBIT_API_KEY", "")
    BYBIT_API_SECRET: str = os.getenv("BYBIT_API_SECRET", "")

    # Scanner parameters
    SCAN_INTERVAL_SEC: int = 60
    LOOKBACK_HOURS: int = 6
    VOLUME_SPIKE_MULTIPLIER: float = 3.0
    EMA_PERIOD: int = 200
    TRENDLINE_MIN_TOUCHES: int = 3
    TRENDLINE_LOOKBACK_BARS: int = 100

    # Supported CEX pairs (Binance Futures USDT-M)
    CEX_EXCHANGE: str = "binance"
    CEX_MARKET_TYPE: str = "future"
    CEX_TOP_N: int = 80  # Top N by volume to scan

    # DexScreener
    DEXSCREENER_CHAINS: list = ["solana", "ethereum"]
    DEXSCREENER_MIN_LIQUIDITY: float = 50_000
    DEXSCREENER_MIN_VOLUME_24H: float = 100_000

    # Rate limiting
    CCXT_RATE_LIMIT_MS: int = 100
    DEXSCREENER_RATE_LIMIT_S: float = 0.35

    # Binance public API (free, no key required)
    BINANCE_FAPI_BASE: str = "https://fapi.binance.com"

    # CryptoPanic (free tier, no key = public posts only)
    CRYPTOPANIC_API_KEY: str = os.getenv("CRYPTOPANIC_API_KEY", "")
    CRYPTOPANIC_BASE_URL: str = "https://cryptopanic.com/api/free/v1"
