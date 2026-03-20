"""
Phase 8B: Real-Time WebSocket Engine
=====================================
Binance Futures WebSocket streams for:
- Real-time price updates (mini ticker)
- Open Interest changes
- Liquidation events (forceOrder)
- Aggregated trade stream

All streams use Binance's free public WebSocket API.
"""

import asyncio
import json
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Optional

import aiohttp

logger = logging.getLogger("realtime_ws")

BINANCE_WS_BASE = "wss://fstream.binance.com"


# ──────────────────────────────────────────────
# Data models
# ──────────────────────────────────────────────
@dataclass
class RealtimePrice:
    symbol: str
    price: float
    change_pct: float
    volume_24h: float
    timestamp: float


@dataclass
class LiquidationEvent:
    symbol: str
    side: str  # "BUY" (short liq) or "SELL" (long liq)
    price: float
    quantity: float
    usd_value: float
    timestamp: float


@dataclass
class OIChange:
    symbol: str
    open_interest: float
    oi_value_usd: float
    timestamp: float


@dataclass
class WSState:
    """State container for WebSocket streams."""
    prices: dict = field(default_factory=dict)  # symbol -> RealtimePrice
    liquidations: deque = field(default_factory=lambda: deque(maxlen=500))
    oi_snapshots: dict = field(default_factory=dict)  # symbol -> OIChange
    last_update: float = 0
    connected: bool = False
    reconnect_count: int = 0


# ──────────────────────────────────────────────
# Symbol conversion helpers
# ──────────────────────────────────────────────
def ccxt_to_binance_ws(symbol: str) -> str:
    """Convert CCXT symbol (BTC/USDT:USDT) to Binance WS format (btcusdt)."""
    base = symbol.split("/")[0].lower()
    quote = symbol.split("/")[1].split(":")[0].lower() if "/" in symbol else "usdt"
    return f"{base}{quote}"


def binance_ws_to_display(ws_symbol: str) -> str:
    """Convert Binance WS symbol (BTCUSDT) to display format (BTC/USDT)."""
    s = ws_symbol.upper()
    if s.endswith("USDT"):
        return f"{s[:-4]}/USDT"
    elif s.endswith("BUSD"):
        return f"{s[:-4]}/BUSD"
    return s


# ──────────────────────────────────────────────
# WebSocket Manager
# ──────────────────────────────────────────────
class BinanceWSManager:
    """
    Manages multiple Binance Futures WebSocket streams.

    Usage:
        manager = BinanceWSManager()
        manager.subscribe_symbols(["BTC/USDT:USDT", "ETH/USDT:USDT"])
        await manager.start()  # runs forever, call stop() to close
    """

    def __init__(self):
        self.state = WSState()
        self._symbols: list[str] = []
        self._ws_symbol_map: dict[str, str] = {}  # ws_sym -> ccxt_sym
        self._session: Optional[aiohttp.ClientSession] = None
        self._tasks: list[asyncio.Task] = []
        self._running = False
        self._callbacks: dict[str, list[Callable]] = {
            "price": [],
            "liquidation": [],
            "oi": [],
        }
        self._max_reconnects = 10

    def subscribe_symbols(self, symbols: list[str]):
        """Set symbols to subscribe to."""
        self._symbols = symbols
        self._ws_symbol_map = {}
        for sym in symbols:
            ws_sym = ccxt_to_binance_ws(sym)
            self._ws_symbol_map[ws_sym] = sym

    def on_price(self, callback: Callable):
        self._callbacks["price"].append(callback)

    def on_liquidation(self, callback: Callable):
        self._callbacks["liquidation"].append(callback)

    def on_oi(self, callback: Callable):
        self._callbacks["oi"].append(callback)

    async def start(self):
        """Start all WebSocket streams."""
        if self._running:
            return

        self._running = True
        self._session = aiohttp.ClientSession()

        self._tasks = [
            asyncio.create_task(self._run_ticker_stream()),
            asyncio.create_task(self._run_liquidation_stream()),
        ]

        self.state.connected = True
        logger.info("WebSocket manager started with %d symbols", len(self._symbols))

    async def stop(self):
        """Stop all streams."""
        self._running = False
        for task in self._tasks:
            task.cancel()
        if self._session:
            await self._session.close()
        self.state.connected = False
        logger.info("WebSocket manager stopped")

    # ── Ticker stream (all symbols combined) ──
    async def _run_ticker_stream(self):
        """Subscribe to mini ticker stream for price updates."""
        # Use combined stream for all symbols
        streams = [f"{ccxt_to_binance_ws(s)}@miniTicker" for s in self._symbols]
        url = f"{BINANCE_WS_BASE}/stream?streams={'/'.join(streams)}"

        await self._run_ws_loop(url, self._handle_ticker)

    def _handle_ticker(self, data: dict):
        """Process mini ticker data."""
        if "data" in data:
            d = data["data"]
        else:
            d = data

        ws_sym = d.get("s", "").lower()
        ccxt_sym = self._ws_symbol_map.get(ws_sym)
        if not ccxt_sym:
            # Try uppercase lookup
            ccxt_sym = self._ws_symbol_map.get(d.get("s", "").lower())
        display_sym = ccxt_sym or binance_ws_to_display(ws_sym)

        price_data = RealtimePrice(
            symbol=display_sym,
            price=float(d.get("c", 0)),
            change_pct=_calc_change_pct(float(d.get("o", 0)), float(d.get("c", 0))),
            volume_24h=float(d.get("q", 0)),
            timestamp=d.get("E", time.time() * 1000) / 1000,
        )

        self.state.prices[display_sym] = price_data
        self.state.last_update = time.time()

        for cb in self._callbacks["price"]:
            try:
                cb(price_data)
            except Exception as e:
                logger.debug("Price callback error: %s", e)

    # ── Liquidation stream ──
    async def _run_liquidation_stream(self):
        """Subscribe to all liquidation events."""
        url = f"{BINANCE_WS_BASE}/ws/!forceOrder@arr"
        await self._run_ws_loop(url, self._handle_liquidation)

    def _handle_liquidation(self, data: dict):
        """Process liquidation event."""
        order = data.get("o", data)
        ws_sym = order.get("s", "").lower()

        price = float(order.get("p", 0))
        qty = float(order.get("q", 0))

        liq = LiquidationEvent(
            symbol=binance_ws_to_display(ws_sym),
            side=order.get("S", ""),
            price=price,
            quantity=qty,
            usd_value=price * qty,
            timestamp=order.get("T", time.time() * 1000) / 1000,
        )

        self.state.liquidations.append(liq)

        for cb in self._callbacks["liquidation"]:
            try:
                cb(liq)
            except Exception as e:
                logger.debug("Liquidation callback error: %s", e)

    # ── Core WS loop with reconnection ──
    async def _run_ws_loop(self, url: str, handler: Callable):
        """Run a WebSocket connection with auto-reconnect."""
        reconnect_delay = 1
        while self._running:
            try:
                async with self._session.ws_connect(url, heartbeat=20) as ws:
                    self.state.reconnect_count = 0
                    reconnect_delay = 1
                    logger.info("WS connected: %s", url[:80])

                    async for msg in ws:
                        if not self._running:
                            break
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            try:
                                data = json.loads(msg.data)
                                handler(data)
                            except json.JSONDecodeError:
                                pass
                        elif msg.type in (aiohttp.WSMsgType.ERROR, aiohttp.WSMsgType.CLOSED):
                            break

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.state.reconnect_count += 1
                if self.state.reconnect_count > self._max_reconnects:
                    logger.error("Max reconnects reached for %s", url[:80])
                    break
                logger.warning("WS reconnecting (%d): %s", self.state.reconnect_count, e)
                await asyncio.sleep(min(reconnect_delay, 30))
                reconnect_delay *= 2


def _calc_change_pct(open_price: float, close_price: float) -> float:
    """Calculate percentage change."""
    if open_price == 0:
        return 0.0
    return round((close_price - open_price) / open_price * 100, 2)


# ──────────────────────────────────────────────
# Liquidation aggregator (for UI display)
# ──────────────────────────────────────────────
class LiquidationAggregator:
    """Aggregate liquidation events for display."""

    @staticmethod
    def summarize(events: list[LiquidationEvent], minutes: int = 15) -> dict:
        """Summarize liquidations in the last N minutes."""
        cutoff = time.time() - (minutes * 60)
        recent = [e for e in events if e.timestamp >= cutoff]

        if not recent:
            return {
                "total_count": 0,
                "total_usd": 0,
                "long_liqs": 0,
                "short_liqs": 0,
                "long_usd": 0,
                "short_usd": 0,
                "largest": None,
                "by_symbol": {},
            }

        long_liqs = [e for e in recent if e.side == "SELL"]  # long positions liquidated
        short_liqs = [e for e in recent if e.side == "BUY"]  # short positions liquidated

        by_symbol = {}
        for e in recent:
            if e.symbol not in by_symbol:
                by_symbol[e.symbol] = {"count": 0, "usd": 0}
            by_symbol[e.symbol]["count"] += 1
            by_symbol[e.symbol]["usd"] += e.usd_value

        largest = max(recent, key=lambda e: e.usd_value)

        return {
            "total_count": len(recent),
            "total_usd": sum(e.usd_value for e in recent),
            "long_liqs": len(long_liqs),
            "short_liqs": len(short_liqs),
            "long_usd": sum(e.usd_value for e in long_liqs),
            "short_usd": sum(e.usd_value for e in short_liqs),
            "largest": {
                "symbol": largest.symbol,
                "side": "Long" if largest.side == "SELL" else "Short",
                "usd": largest.usd_value,
                "price": largest.price,
            },
            "by_symbol": dict(sorted(
                by_symbol.items(), key=lambda x: x[1]["usd"], reverse=True
            )[:10]),
        }


# ──────────────────────────────────────────────
# Streamlit-compatible polling wrapper
# ──────────────────────────────────────────────
class RealtimePoller:
    """
    Alternative to WebSocket for Streamlit (which can't run persistent WS).
    Uses REST API polling at configurable intervals.
    """

    def __init__(self, symbols: list[str], interval_sec: float = 5.0):
        self.symbols = symbols
        self.interval = interval_sec
        self.prices: dict[str, RealtimePrice] = {}
        self._last_poll = 0

    async def poll_prices(self) -> dict[str, RealtimePrice]:
        """Poll current prices via REST API."""
        now = time.time()
        if now - self._last_poll < self.interval:
            return self.prices

        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        target_symbols = {ccxt_to_binance_ws(s).upper() for s in self.symbols}

                        for item in data:
                            if item["symbol"] in target_symbols:
                                display = binance_ws_to_display(item["symbol"])
                                self.prices[display] = RealtimePrice(
                                    symbol=display,
                                    price=float(item["lastPrice"]),
                                    change_pct=float(item["priceChangePercent"]),
                                    volume_24h=float(item["quoteVolume"]),
                                    timestamp=now,
                                )
                        self._last_poll = now
        except Exception as e:
            logger.debug("Poll prices error: %s", e)

        return self.prices

    async def poll_liquidations(self) -> list[dict]:
        """
        Binance doesn't have a REST endpoint for liquidations.
        For Streamlit, we return recent force orders from the trades endpoint.
        """
        # Note: Real liquidation data requires WebSocket.
        # This is a placeholder that returns empty for REST mode.
        return []

    async def poll_open_interest(self) -> dict[str, OIChange]:
        """Poll open interest for subscribed symbols."""
        results = {}
        base_url = "https://fapi.binance.com/fapi/v1/openInterest"

        try:
            async with aiohttp.ClientSession() as session:
                for sym in self.symbols[:20]:  # Limit to avoid rate limits
                    ws_sym = ccxt_to_binance_ws(sym).upper()
                    params = {"symbol": ws_sym}
                    try:
                        async with session.get(
                            base_url, params=params,
                            timeout=aiohttp.ClientTimeout(total=5)
                        ) as resp:
                            if resp.status == 200:
                                data = await resp.json()
                                display = binance_ws_to_display(ws_sym)
                                price = self.prices.get(display)
                                oi_val = float(data.get("openInterest", 0))
                                oi_usd = oi_val * (price.price if price else 0)

                                results[display] = OIChange(
                                    symbol=display,
                                    open_interest=oi_val,
                                    oi_value_usd=oi_usd,
                                    timestamp=time.time(),
                                )
                    except Exception:
                        pass
                    await asyncio.sleep(0.1)  # Rate limit
        except Exception as e:
            logger.debug("Poll OI error: %s", e)

        return results
