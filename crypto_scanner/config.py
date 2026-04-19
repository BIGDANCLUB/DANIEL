"""Configuration management for Crypto Scanner — 100% Free APIs (Phase 8)."""

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
    CEX_TOP_N: int = 150  # Top N by volume to scan

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

    # Phase 8: Telegram / Discord notifications
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")

    # Phase 8: AI predictor
    AI_MIN_TRAIN_SAMPLES: int = 30

    # Phase 8: MTF timeframes
    MTF_TIMEFRAMES: list = ["15m", "1h", "4h"]

    # RISEx Auto-Trader
    RISEX_PRIVATE_KEY: str = os.getenv("RISEX_PRIVATE_KEY", "")
    RISEX_API_WALLET_ADDRESS: str = os.getenv("RISEX_API_WALLET_ADDRESS", "")
    RISEX_API_BASE: str = os.getenv("RISEX_API_BASE", "https://api.rise.trade")
    RISEX_MIN_SCORE: float = float(os.getenv("RISEX_MIN_SCORE", "80"))
    RISEX_USD_PER_TRADE: float = float(os.getenv("RISEX_USD_PER_TRADE", "10"))
    RISEX_LEVERAGE: int = int(os.getenv("RISEX_LEVERAGE", "5"))
    RISEX_MAX_OPEN_TRADES: int = int(os.getenv("RISEX_MAX_OPEN_TRADES", "3"))
    RISEX_AUTO_TRADE: bool = os.getenv("RISEX_AUTO_TRADE", "false").lower() == "true"
