"""
RISEx API Trading Module
========================
Automated trading on RISEx (rise.trade) — on-chain perpetuals DEX on RISE Chain.

Authentication: EVM wallet private key (API Wallet)
The API Wallet must be authorized on the RISEx UI before use.

SECURITY WARNING:
  - NEVER hardcode your private key in source code
  - Store it in .env as RISEX_PRIVATE_KEY
  - NEVER share or commit the .env file

Setup (一度だけ必要):
  1. rise.trade → API Wallets → Generate
  2. "Authorize API Wallet" ボタンを押す
  3. 表示された Private Key を .env に保存:
     RISEX_PRIVATE_KEY=0x...
     RISEX_API_WALLET_ADDRESS=0x...
"""

import hashlib
import hmac
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("risex_trader")

# ── RISEx API base URL (update if they publish an official one) ──
RISEX_API_BASE = os.getenv("RISEX_API_BASE", "https://api.rise.trade")

# ── EVM signing (requires eth_account / web3 package) ──
try:
    from eth_account import Account
    from eth_account.messages import encode_defunct
    HAS_ETH_ACCOUNT = True
except ImportError:
    HAS_ETH_ACCOUNT = False
    logger.warning("eth_account not installed — run: pip install eth-account")


# ─────────────────────────────────────────────
# Data models
# ─────────────────────────────────────────────
@dataclass
class RiseXOrder:
    symbol: str          # e.g. "BTC-PERP"
    side: str            # "buy" or "sell"
    order_type: str      # "market" or "limit"
    size: float          # quantity in base asset
    price: Optional[float] = None   # limit price (None for market)
    leverage: int = 5
    reduce_only: bool = False


@dataclass
class RiseXPosition:
    symbol: str
    side: str
    size: float
    entry_price: float
    unrealized_pnl: float
    leverage: int


@dataclass
class TradeResult:
    success: bool
    order_id: Optional[str] = None
    error: Optional[str] = None
    raw: Optional[dict] = None


# ─────────────────────────────────────────────
# RISEx API client
# ─────────────────────────────────────────────
class RiseXClient:
    """
    Client for RISEx perpetuals DEX.
    Uses API Wallet (delegated EVM wallet) for authentication.
    """

    def __init__(
        self,
        private_key: str = None,
        wallet_address: str = None,
        api_base: str = RISEX_API_BASE,
    ):
        self.private_key = private_key or os.getenv("RISEX_PRIVATE_KEY", "")
        self.wallet_address = wallet_address or os.getenv("RISEX_API_WALLET_ADDRESS", "")
        self.api_base = api_base.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._auth_token: Optional[str] = None
        self._token_expiry: float = 0

    @property
    def is_configured(self) -> bool:
        return bool(self.private_key and self.wallet_address)

    def _sign_message(self, message: str) -> str:
        """Sign a message with the API wallet private key."""
        if not HAS_ETH_ACCOUNT:
            raise ImportError("pip install eth-account  が必要です")
        account = Account.from_key(self.private_key)
        msg = encode_defunct(text=message)
        signed = account.sign_message(msg)
        return signed.signature.hex()

    def _build_auth_headers(self, body: dict = None) -> dict:
        """Build authentication headers for RISEx API."""
        timestamp = str(int(time.time() * 1000))
        nonce = timestamp

        # Sign: timestamp + nonce + (body JSON if present)
        payload = timestamp + nonce
        if body:
            payload += json.dumps(body, separators=(",", ":"), sort_keys=True)

        signature = self._sign_message(payload)

        return {
            "X-API-Wallet": self.wallet_address,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Signature": signature,
        }

    def _get(self, path: str, params: dict = None) -> dict:
        """Make an authenticated GET request."""
        headers = self._build_auth_headers()
        url = f"{self.api_base}{path}"
        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            logger.error("RiseX GET %s → %s: %s", path, resp.status_code, resp.text[:300])
            raise
        except Exception as e:
            logger.error("RiseX GET %s error: %s", path, e)
            raise

    def _post(self, path: str, body: dict) -> dict:
        """Make an authenticated POST request."""
        headers = self._build_auth_headers(body)
        url = f"{self.api_base}{path}"
        try:
            resp = self.session.post(url, json=body, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            logger.error("RiseX POST %s → %s: %s", path, resp.status_code, resp.text[:300])
            raise
        except Exception as e:
            logger.error("RiseX POST %s error: %s", path, e)
            raise

    # ── Public endpoints (no auth needed) ──

    def get_markets(self) -> list[dict]:
        """Get all available markets."""
        try:
            resp = self.session.get(f"{self.api_base}/v1/markets", timeout=10)
            resp.raise_for_status()
            return resp.json().get("markets", resp.json())
        except Exception as e:
            logger.error("get_markets: %s", e)
            return []

    def get_ticker(self, symbol: str) -> Optional[dict]:
        """Get ticker for a symbol."""
        try:
            resp = self.session.get(
                f"{self.api_base}/v1/ticker",
                params={"symbol": symbol},
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error("get_ticker %s: %s", symbol, e)
            return None

    # ── Private endpoints (auth required) ──

    def get_account(self) -> Optional[dict]:
        """Get account balance and equity."""
        if not self.is_configured:
            return None
        try:
            return self._get("/v1/account")
        except Exception:
            return None

    def get_positions(self) -> list[RiseXPosition]:
        """Get open positions."""
        if not self.is_configured:
            return []
        try:
            data = self._get("/v1/positions")
            positions = data.get("positions", data if isinstance(data, list) else [])
            result = []
            for p in positions:
                result.append(RiseXPosition(
                    symbol=p.get("symbol", ""),
                    side=p.get("side", ""),
                    size=float(p.get("size", 0)),
                    entry_price=float(p.get("entryPrice", p.get("entry_price", 0))),
                    unrealized_pnl=float(p.get("unrealizedPnl", p.get("unrealized_pnl", 0))),
                    leverage=int(p.get("leverage", 1)),
                ))
            return result
        except Exception:
            return []

    def get_open_orders(self, symbol: str = None) -> list[dict]:
        """Get open orders."""
        if not self.is_configured:
            return []
        try:
            params = {"symbol": symbol} if symbol else {}
            data = self._get("/v1/orders", params)
            return data.get("orders", data if isinstance(data, list) else [])
        except Exception:
            return []

    def place_order(self, order: RiseXOrder) -> TradeResult:
        """
        Place a market or limit order.

        Args:
            order: RiseXOrder dataclass with trade parameters

        Returns:
            TradeResult with success status and order ID
        """
        if not self.is_configured:
            return TradeResult(success=False, error="API Wallet not configured")

        if not HAS_ETH_ACCOUNT:
            return TradeResult(success=False, error="eth-account package not installed")

        body = {
            "symbol": order.symbol,
            "side": order.side.lower(),
            "type": order.order_type.lower(),
            "size": str(order.size),
            "leverage": order.leverage,
            "reduceOnly": order.reduce_only,
            "timestamp": int(time.time() * 1000),
        }
        if order.price is not None and order.order_type == "limit":
            body["price"] = str(order.price)

        try:
            resp = self._post("/v1/orders", body)
            order_id = resp.get("orderId", resp.get("order_id", resp.get("id")))
            logger.info(
                "RiseX order placed: %s %s %s @ %s (id=%s)",
                order.side.upper(), order.size, order.symbol,
                order.price or "MARKET", order_id
            )
            return TradeResult(success=True, order_id=str(order_id), raw=resp)
        except Exception as e:
            return TradeResult(success=False, error=str(e))

    def cancel_order(self, order_id: str, symbol: str = None) -> bool:
        """Cancel an open order."""
        if not self.is_configured:
            return False
        try:
            body = {"orderId": order_id}
            if symbol:
                body["symbol"] = symbol
            self._post("/v1/orders/cancel", body)
            logger.info("Cancelled order %s", order_id)
            return True
        except Exception as e:
            logger.error("cancel_order %s: %s", order_id, e)
            return False

    def close_position(self, symbol: str) -> TradeResult:
        """Close all position for a symbol (market order, reduce only)."""
        positions = self.get_positions()
        pos = next((p for p in positions if p.symbol == symbol), None)
        if not pos or pos.size == 0:
            return TradeResult(success=False, error=f"No open position for {symbol}")

        close_side = "sell" if pos.side.lower() in ("long", "buy") else "buy"
        order = RiseXOrder(
            symbol=symbol,
            side=close_side,
            order_type="market",
            size=pos.size,
            reduce_only=True,
        )
        return self.place_order(order)

    def test_connection(self) -> dict:
        """Test API connectivity and authentication."""
        result = {
            "configured": self.is_configured,
            "eth_account": HAS_ETH_ACCOUNT,
            "markets": False,
            "account": False,
            "error": None,
        }
        try:
            markets = self.get_markets()
            result["markets"] = len(markets) > 0
        except Exception as e:
            result["error"] = f"markets: {e}"

        if self.is_configured:
            try:
                acct = self.get_account()
                result["account"] = acct is not None
                if acct:
                    result["equity"] = acct.get("equity", acct.get("totalEquity", "?"))
            except Exception as e:
                result["error"] = f"account: {e}"

        return result


# ─────────────────────────────────────────────
# Symbol converter (scanner format → RISEx format)
# ─────────────────────────────────────────────
def scanner_symbol_to_risex(symbol: str) -> str:
    """
    Convert scanner symbol to RISEx format.
    e.g. "BTC/USDT" → "BTC-PERP"
         "ETH/USDT:USDT" → "ETH-PERP"
    """
    base = symbol.split("/")[0].upper()
    return f"{base}-PERP"


# ─────────────────────────────────────────────
# Auto-trader: executes trades based on scan signals
# ─────────────────────────────────────────────
class RiseXAutoTrader:
    """
    Automatically trades on RISEx when high-score signals appear.

    Default rule:
      - Score >= 80 AND bullish breakout → BUY (long)
      - Score >= 80 AND bearish breakout → SELL (short)
      - Max open trades: configurable
      - Fixed USD size per trade: configurable
    """

    def __init__(
        self,
        client: RiseXClient,
        min_score: float = 80.0,
        usd_per_trade: float = 10.0,
        leverage: int = 5,
        max_open_trades: int = 3,
        allowed_symbols: list[str] = None,
    ):
        self.client = client
        self.min_score = min_score
        self.usd_per_trade = usd_per_trade
        self.leverage = leverage
        self.max_open_trades = max_open_trades
        self.allowed_symbols = allowed_symbols  # None = allow all
        self._trade_log: list[dict] = []
        self._open_trade_ids: list[str] = []

    def evaluate_signal(self, signal) -> Optional[RiseXOrder]:
        """
        Decide whether to trade based on a scan signal.
        Returns an RiseXOrder if we should trade, else None.
        """
        if signal.score < self.min_score:
            return None

        tl = signal.trendline_break or {}
        bt = tl.get("breakout_type", "")
        if bt not in ("bullish", "bearish"):
            return None

        risex_sym = scanner_symbol_to_risex(signal.symbol)
        if self.allowed_symbols and risex_sym not in self.allowed_symbols:
            return None

        if len(self._open_trade_ids) >= self.max_open_trades:
            logger.info("Max open trades reached (%d), skipping %s", self.max_open_trades, risex_sym)
            return None

        # Calculate size: USD / current price = base quantity
        if signal.price <= 0:
            return None
        size = round(self.usd_per_trade * self.leverage / signal.price, 6)

        return RiseXOrder(
            symbol=risex_sym,
            side="buy" if bt == "bullish" else "sell",
            order_type="market",
            size=size,
            leverage=self.leverage,
        )

    def execute_signal(self, signal) -> Optional[TradeResult]:
        """Evaluate and execute a signal if it qualifies."""
        order = self.evaluate_signal(signal)
        if not order:
            return None

        result = self.client.place_order(order)

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbol": order.symbol,
            "side": order.side,
            "size": order.size,
            "score": signal.score,
            "success": result.success,
            "order_id": result.order_id,
            "error": result.error,
        }
        self._trade_log.append(log_entry)

        if result.success and result.order_id:
            self._open_trade_ids.append(result.order_id)
            logger.info(
                "AUTO-TRADE executed: %s %s %s (score=%.0f, id=%s)",
                order.side.upper(), order.size, order.symbol,
                signal.score, result.order_id
            )
        else:
            logger.warning("AUTO-TRADE failed: %s — %s", order.symbol, result.error)

        return result

    def execute_signals(self, signals: list) -> list[TradeResult]:
        """Process a list of scan signals."""
        results = []
        qualified = [s for s in signals if s.score >= self.min_score]
        qualified.sort(key=lambda s: s.score, reverse=True)

        for signal in qualified:
            r = self.execute_signal(signal)
            if r:
                results.append(r)

        return results

    @property
    def trade_log(self) -> list[dict]:
        return list(self._trade_log)
