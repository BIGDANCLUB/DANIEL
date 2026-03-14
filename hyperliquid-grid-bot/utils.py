"""
Hyperliquid SDK Wrapper & Utility Functions
この戦略は小さい利益を高頻度で積み重ねる「勝手にりえき」型です
"""

import os
import logging
import time
from typing import Optional

import eth_account
from dotenv import load_dotenv
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants

load_dotenv()

logger = logging.getLogger("grid_bot")


def get_network_url() -> str:
    network = os.getenv("NETWORK", "testnet").lower()
    if network == "mainnet":
        return constants.MAINNET_API_URL
    return constants.TESTNET_API_URL


def get_account_address() -> str:
    addr = os.getenv("ACCOUNT_ADDRESS", "")
    if not addr:
        raise ValueError("ACCOUNT_ADDRESS not set in .env")
    return addr


def get_secret_key() -> str:
    key = os.getenv("SECRET_KEY", "")
    if not key:
        raise ValueError("SECRET_KEY not set in .env")
    return key


def build_info_client() -> Info:
    return Info(get_network_url(), skip_ws=True)


def build_exchange_client() -> Exchange:
    account = eth_account.Account.from_key(get_secret_key())
    return Exchange(account, get_network_url())


def get_mark_price(info: Info, symbol: str) -> Optional[float]:
    """Get current mark/mid price for a symbol."""
    try:
        mids = info.all_mids()
        if symbol in mids:
            return float(mids[symbol])
    except Exception as e:
        logger.error(f"Failed to get mark price: {e}")
    return None


def get_user_state(info: Info, address: str) -> Optional[dict]:
    """Get full user state (positions, margin, equity)."""
    try:
        return info.user_state(address)
    except Exception as e:
        logger.error(f"Failed to get user state: {e}")
    return None


def get_open_orders(info: Info, address: str) -> list:
    """Get all open orders for user."""
    try:
        return info.open_orders(address)
    except Exception as e:
        logger.error(f"Failed to get open orders: {e}")
    return []


def get_position(info: Info, address: str, symbol: str) -> Optional[dict]:
    """Get position for a specific symbol. Returns None if no position."""
    state = get_user_state(info, address)
    if not state:
        return None
    for pos in state.get("assetPositions", []):
        p = pos.get("position", {})
        if p.get("coin") == symbol:
            szi = float(p.get("szi", "0"))
            if szi != 0:
                return p
    return None


def get_account_value(info: Info, address: str) -> Optional[float]:
    """Get total account value (margin + unrealized PnL)."""
    state = get_user_state(info, address)
    if state:
        return float(state.get("marginSummary", {}).get("accountValue", "0"))
    return None


def get_sz_decimals(info: Info, symbol: str) -> int:
    """Get the size decimal precision for a symbol."""
    meta = info.meta()
    for asset in meta.get("universe", []):
        if asset.get("name") == symbol:
            return asset.get("szDecimals", 3)
    return 3


def place_limit_order(
    exchange: Exchange,
    symbol: str,
    is_buy: bool,
    size: float,
    price: float,
    reduce_only: bool = False,
) -> Optional[dict]:
    """Place a limit GTC order. Returns response or None on error."""
    try:
        order_type = {"limit": {"tif": "Gtc"}}
        result = exchange.order(
            symbol,
            is_buy,
            size,
            price,
            order_type,
            reduce_only=reduce_only,
        )
        logger.info(
            f"Limit {'BUY' if is_buy else 'SELL'} {size} {symbol} @ {price} -> {_extract_status(result)}"
        )
        return result
    except Exception as e:
        logger.error(f"Order failed: {e}")
    return None


def place_market_close(
    exchange: Exchange, symbol: str, size: Optional[float] = None
) -> Optional[dict]:
    """Market close a position (reduce only)."""
    try:
        result = exchange.market_close(symbol, sz=size)
        logger.info(f"Market close {symbol} sz={size} -> {_extract_status(result)}")
        return result
    except Exception as e:
        logger.error(f"Market close failed: {e}")
    return None


def cancel_order(exchange: Exchange, symbol: str, oid: int) -> Optional[dict]:
    """Cancel a single order by OID."""
    try:
        result = exchange.cancel(symbol, oid)
        logger.debug(f"Cancel {symbol} oid={oid} -> {result}")
        return result
    except Exception as e:
        logger.error(f"Cancel failed oid={oid}: {e}")
    return None


def cancel_all_orders(exchange: Exchange, info: Info, address: str, symbol: str) -> int:
    """Cancel all open orders for a symbol. Returns count cancelled."""
    orders = get_open_orders(info, address)
    count = 0
    for o in orders:
        if o.get("coin") == symbol:
            cancel_order(exchange, symbol, o["oid"])
            count += 1
    return count


def set_leverage(exchange: Exchange, symbol: str, leverage: int, is_cross: bool = True):
    """Set leverage for a symbol."""
    try:
        result = exchange.update_leverage(leverage, symbol, is_cross=is_cross)
        logger.info(f"Set leverage {symbol} -> {leverage}x ({'cross' if is_cross else 'isolated'})")
        return result
    except Exception as e:
        logger.error(f"Set leverage failed: {e}")
    return None


def round_price(price: float, tick: float = 0.1) -> float:
    """Round price to nearest tick."""
    return round(round(price / tick) * tick, 8)


def round_size(size: float, decimals: int) -> float:
    """Round size to allowed decimal places."""
    return round(size, decimals)


def _extract_status(result: dict) -> str:
    """Extract human-readable status from SDK response."""
    if not result:
        return "no response"
    status = result.get("status", "unknown")
    resp = result.get("response", {})
    if isinstance(resp, dict) and resp.get("type") == "order":
        data = resp.get("data", {})
        statuses = data.get("statuses", [])
        if statuses:
            return str(statuses[0])
    return str(status)


def display_startup_info(info: Info, address: str, symbol: str, config: dict):
    """Display account info at bot startup."""
    state = get_user_state(info, address)
    if not state:
        logger.warning("Could not fetch user state at startup")
        return

    margin = state.get("marginSummary", {})
    account_value = float(margin.get("accountValue", "0"))
    total_margin = float(margin.get("totalMarginUsed", "0"))

    logger.info("=" * 60)
    logger.info("  Hyperliquid Martingale Grid Bot - Startup")
    logger.info("=" * 60)
    logger.info(f"  Network    : {os.getenv('NETWORK', 'testnet')}")
    logger.info(f"  Address    : {address[:10]}...{address[-6:]}")
    logger.info(f"  Symbol     : {symbol}")
    logger.info(f"  Leverage   : {config['leverage']}x")
    logger.info(f"  Account Val: ${account_value:,.2f}")
    logger.info(f"  Margin Used: ${total_margin:,.2f}")

    # Show existing positions
    for pos in state.get("assetPositions", []):
        p = pos.get("position", {})
        szi = float(p.get("szi", "0"))
        if szi != 0:
            entry = p.get("entryPx", "?")
            upnl = float(p.get("unrealizedPnl", "0"))
            logger.info(
                f"  Position   : {p['coin']} size={szi} entry={entry} uPnL=${upnl:+.2f}"
            )

    # Show open orders
    orders = get_open_orders(info, address)
    symbol_orders = [o for o in orders if o.get("coin") == symbol]
    logger.info(f"  Open Orders: {len(symbol_orders)} for {symbol}")
    for o in symbol_orders[:5]:
        side = "BUY" if o.get("side") == "B" else "SELL"
        logger.info(f"    {side} {o.get('sz')} @ {o.get('limitPx')}")

    logger.info("=" * 60)
