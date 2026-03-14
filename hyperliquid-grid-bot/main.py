#!/usr/bin/env python3
"""
Hyperliquid Martingale Averaging Grid Trading Bot
この戦略は小さい利益を高頻度で積み重ねる「勝手にりえき」型です

Strategy:
  1. Place symmetric Limit Buy / Limit Sell around mark price
  2. When one fills → cancel the other → hold directional position
  3. If price goes against us → Martingale: add bigger size at worse price
  4. On small reversal to profit → close all, restart grid from new mark price
  5. Max levels reached → force close & reset
"""

import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

from utils import (
    build_exchange_client,
    build_info_client,
    cancel_all_orders,
    display_startup_info,
    get_account_address,
    get_account_value,
    get_mark_price,
    get_open_orders,
    get_position,
    get_sz_decimals,
    place_limit_order,
    place_market_close,
    round_price,
    round_size,
    set_leverage,
)

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------


def setup_logging(config: dict):
    log_fmt = "%(asctime)s [%(levelname)s] %(message)s"
    handlers = [logging.StreamHandler(sys.stdout)]

    if config.get("log_to_file", True):
        log_dir = Path(config.get("log_dir", "logs"))
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"bot_{datetime.now():%Y%m%d_%H%M%S}.log"
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(level=logging.INFO, format=log_fmt, handlers=handlers)
    return logging.getLogger("grid_bot")


# ---------------------------------------------------------------------------
# Bot State
# ---------------------------------------------------------------------------


class BotState:
    """Tracks the current grid / martingale state."""

    def __init__(self):
        self.direction: str = ""  # "long" | "short" | ""
        self.level: int = 0  # Current martingale level (0 = no position)
        self.avg_entry: float = 0.0
        self.total_size: float = 0.0
        self.pending_buy_oid: int = 0
        self.pending_sell_oid: int = 0
        self.initial_account_value: float = 0.0

    def reset(self):
        self.direction = ""
        self.level = 0
        self.avg_entry = 0.0
        self.total_size = 0.0
        self.pending_buy_oid = 0
        self.pending_sell_oid = 0


# ---------------------------------------------------------------------------
# Core Logic
# ---------------------------------------------------------------------------


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def calc_grid_price(mark: float, bps: float, side: str) -> float:
    """Calculate grid price offset from mark price by bps."""
    offset = mark * (bps / 10000.0)
    if side == "buy":
        return round_price(mark - offset)
    return round_price(mark + offset)


def calc_martingale_price(last_price: float, bps: float, direction: str) -> float:
    """Next martingale entry: worse price in the adverse direction."""
    offset = last_price * (bps / 10000.0)
    if direction == "long":
        # Long position, price went down → next buy lower
        return round_price(last_price - offset)
    else:
        # Short position, price went up → next sell higher
        return round_price(last_price + offset)


def update_avg_entry(old_avg: float, old_size: float, new_price: float, new_size: float) -> float:
    """Weighted average entry price after adding to position."""
    if old_size + new_size == 0:
        return 0.0
    return (old_avg * old_size + new_price * new_size) / (old_size + new_size)


def check_tp(avg_entry: float, mark: float, direction: str, tp_pct: float) -> bool:
    """Check if we have reached take-profit threshold."""
    if avg_entry <= 0:
        return False
    if direction == "long":
        pnl_pct = (mark - avg_entry) / avg_entry * 100
    else:
        pnl_pct = (avg_entry - mark) / avg_entry * 100
    return pnl_pct >= tp_pct


def check_drawdown(initial_value: float, current_value: float, max_dd_pct: float) -> bool:
    """Returns True if drawdown limit is breached."""
    if initial_value <= 0:
        return False
    dd_pct = (initial_value - current_value) / initial_value * 100
    return dd_pct >= max_dd_pct


def find_filled_oid(open_oids: set, pending_oid: int) -> bool:
    """Returns True if the pending OID is no longer in open orders (= filled or cancelled)."""
    return pending_oid != 0 and pending_oid not in open_oids


def extract_oid_from_response(result: dict) -> int:
    """Try to extract OID from order placement response."""
    if not result:
        return 0
    try:
        resp = result.get("response", {})
        if resp.get("type") == "order":
            statuses = resp.get("data", {}).get("statuses", [])
            for s in statuses:
                if isinstance(s, dict) and "resting" in s:
                    return int(s["resting"].get("oid", 0))
    except Exception:
        pass
    return 0


# ---------------------------------------------------------------------------
# Main Bot Class
# ---------------------------------------------------------------------------


class MartingaleGridBot:
    def __init__(self, config: dict):
        self.cfg = config
        self.logger = logging.getLogger("grid_bot")
        self.state = BotState()

        # SDK clients
        self.info = build_info_client()
        self.exchange = build_exchange_client()
        self.address = get_account_address()

        # Symbol config
        self.symbol = config["symbol"]
        self.sz_decimals = get_sz_decimals(self.info, self.symbol)

    def run(self):
        """Main entry point."""
        self.logger.info("Bot starting...")

        # Set leverage
        set_leverage(
            self.exchange,
            self.symbol,
            self.cfg["leverage"],
            is_cross=self.cfg.get("is_cross", True),
        )

        # Display startup info
        display_startup_info(self.info, self.address, self.symbol, self.cfg)

        # Record initial account value for drawdown tracking
        self.state.initial_account_value = get_account_value(self.info, self.address) or 0
        self.logger.info(f"Initial account value: ${self.state.initial_account_value:,.2f}")

        # Check for existing position and sync state
        self._sync_existing_position()

        # Cancel stale orders from previous runs
        cancelled = cancel_all_orders(self.exchange, self.info, self.address, self.symbol)
        if cancelled:
            self.logger.info(f"Cancelled {cancelled} stale orders")

        # Main loop
        self.logger.info(f"Entering main loop (interval: {self.cfg['loop_interval_sec']}s)")
        while True:
            try:
                self._tick()
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt - shutting down...")
                cancel_all_orders(self.exchange, self.info, self.address, self.symbol)
                break
            except Exception as e:
                self.logger.error(f"Tick error: {e}", exc_info=True)

            time.sleep(self.cfg["loop_interval_sec"])

    def _sync_existing_position(self):
        """If bot restarts with an existing position, sync state."""
        pos = get_position(self.info, self.address, self.symbol)
        if pos:
            szi = float(pos.get("szi", "0"))
            entry = float(pos.get("entryPx", "0"))
            if szi > 0:
                self.state.direction = "long"
                self.state.total_size = abs(szi)
            elif szi < 0:
                self.state.direction = "short"
                self.state.total_size = abs(szi)
            self.state.avg_entry = entry
            self.state.level = 1  # Assume at least level 1
            self.logger.info(
                f"Synced existing position: {self.state.direction} "
                f"size={self.state.total_size} entry={self.state.avg_entry}"
            )

    def _tick(self):
        """Single iteration of the main loop."""

        # --- Risk check: account drawdown ---
        current_value = get_account_value(self.info, self.address)
        if current_value is None:
            self.logger.warning("Could not fetch account value, skipping tick")
            return

        if check_drawdown(
            self.state.initial_account_value,
            current_value,
            self.cfg["max_drawdown_pct"],
        ):
            self.logger.critical(
                f"MAX DRAWDOWN BREACHED! "
                f"Initial=${self.state.initial_account_value:,.2f} "
                f"Current=${current_value:,.2f} "
                f"Limit={self.cfg['max_drawdown_pct']}%"
            )
            self._emergency_close()
            self.logger.critical("Bot stopped due to drawdown limit.")
            sys.exit(1)

        mark = get_mark_price(self.info, self.symbol)
        if mark is None:
            self.logger.warning("Could not get mark price, skipping tick")
            return

        # --- State: No position → place initial grid ---
        if self.state.direction == "":
            self._handle_no_position(mark)
            return

        # --- State: Has position → check TP or Martingale ---
        self._handle_active_position(mark)

    def _handle_no_position(self, mark: float):
        """Place initial two-sided grid orders around mark price."""

        # Check if we already have pending orders
        open_orders = get_open_orders(self.info, self.address)
        open_oids = {o["oid"] for o in open_orders if o.get("coin") == self.symbol}

        buy_alive = self.state.pending_buy_oid in open_oids
        sell_alive = self.state.pending_sell_oid in open_oids

        # If both orders still pending, check if one filled
        if buy_alive and sell_alive:
            return  # Both still waiting, nothing to do

        # If one filled (missing from open orders) and other still alive
        if self.state.pending_buy_oid != 0 and self.state.pending_sell_oid != 0:
            buy_filled = find_filled_oid(open_oids, self.state.pending_buy_oid)
            sell_filled = find_filled_oid(open_oids, self.state.pending_sell_oid)

            if buy_filled and not sell_filled:
                # Buy filled → Long position
                self._on_initial_fill("long", mark)
                return
            elif sell_filled and not buy_filled:
                # Sell filled → Short position
                self._on_initial_fill("short", mark)
                return
            elif buy_filled and sell_filled:
                # Both disappeared (edge case) → re-check position
                pos = get_position(self.info, self.address, self.symbol)
                if pos:
                    self._sync_existing_position()
                    return
                # Both cancelled somehow → reset and re-place
                self.state.reset()

        # Place fresh two-sided grid
        self.logger.info(f"Placing initial grid around mark={mark}")
        bps = self.cfg["grid_spacing_bps"]
        size_usd = self.cfg["initial_size_usd"]
        size_coin = round_size(size_usd / mark, self.sz_decimals)

        if size_coin <= 0:
            self.logger.error(f"Calculated size is 0 (USD={size_usd}, mark={mark})")
            return

        buy_px = calc_grid_price(mark, bps, "buy")
        sell_px = calc_grid_price(mark, bps, "sell")

        # Place both limit orders
        buy_result = place_limit_order(self.exchange, self.symbol, True, size_coin, buy_px)
        sell_result = place_limit_order(self.exchange, self.symbol, False, size_coin, sell_px)

        self.state.pending_buy_oid = extract_oid_from_response(buy_result)
        self.state.pending_sell_oid = extract_oid_from_response(sell_result)

        self.logger.info(
            f"Grid placed: BUY {size_coin} @ {buy_px} (oid={self.state.pending_buy_oid}) | "
            f"SELL {size_coin} @ {sell_px} (oid={self.state.pending_sell_oid})"
        )

    def _on_initial_fill(self, direction: str, mark: float):
        """Handle initial grid fill → cancel opposite, enter position state."""
        self.logger.info(f"Initial {direction.upper()} fill detected!")

        # Cancel the opposite order
        if direction == "long" and self.state.pending_sell_oid:
            from utils import cancel_order
            cancel_order(self.exchange, self.symbol, self.state.pending_sell_oid)
        elif direction == "short" and self.state.pending_buy_oid:
            from utils import cancel_order
            cancel_order(self.exchange, self.symbol, self.state.pending_buy_oid)

        # Sync actual position from exchange
        pos = get_position(self.info, self.address, self.symbol)
        if pos:
            self.state.direction = direction
            self.state.total_size = abs(float(pos.get("szi", "0")))
            self.state.avg_entry = float(pos.get("entryPx", "0"))
            self.state.level = 1
        else:
            # Position might have been too small or already closed
            self.state.direction = direction
            bps = self.cfg["grid_spacing_bps"]
            entry_px = calc_grid_price(mark, bps, "buy" if direction == "long" else "sell")
            self.state.avg_entry = entry_px
            self.state.total_size = round_size(self.cfg["initial_size_usd"] / mark, self.sz_decimals)
            self.state.level = 1

        self.state.pending_buy_oid = 0
        self.state.pending_sell_oid = 0

        self.logger.info(
            f"Position entered: {self.state.direction} "
            f"size={self.state.total_size} avg_entry={self.state.avg_entry} level={self.state.level}"
        )

    def _handle_active_position(self, mark: float):
        """Manage an active position: check TP, or Martingale if adverse."""

        # Re-sync position from exchange
        pos = get_position(self.info, self.address, self.symbol)
        if not pos:
            self.logger.info("Position closed externally, resetting state")
            self.state.reset()
            return

        szi = float(pos.get("szi", "0"))
        entry = float(pos.get("entryPx", "0"))
        upnl = float(pos.get("unrealizedPnl", "0"))
        self.state.avg_entry = entry
        self.state.total_size = abs(szi)

        # Display status
        direction_str = "LONG" if self.state.direction == "long" else "SHORT"
        pnl_pct = 0
        if entry > 0:
            if self.state.direction == "long":
                pnl_pct = (mark - entry) / entry * 100
            else:
                pnl_pct = (entry - mark) / entry * 100

        self.logger.info(
            f"[{direction_str} L{self.state.level}] "
            f"size={self.state.total_size} avg={entry:.2f} mark={mark:.2f} "
            f"uPnL=${upnl:+.2f} ({pnl_pct:+.3f}%)"
        )

        # --- Check Take Profit ---
        if check_tp(entry, mark, self.state.direction, self.cfg["tp_percent"]):
            self.logger.info(
                f"TP HIT! PnL%={pnl_pct:+.3f}% >= {self.cfg['tp_percent']}% → closing all"
            )
            self._close_all_and_reset()
            return

        # --- Check if max levels reached ---
        if self.state.level >= self.cfg["max_levels"]:
            self.logger.warning(
                f"Max levels ({self.cfg['max_levels']}) reached → force close & reset"
            )
            self._close_all_and_reset()
            return

        # --- Check max position exposure ---
        pos_usd = self.state.total_size * mark
        if pos_usd >= self.cfg["max_position_usd"]:
            self.logger.warning(
                f"Max position exposure ${pos_usd:,.0f} >= ${self.cfg['max_position_usd']:,.0f} → no more martingale"
            )
            return

        # --- Check if price moved adversely → place martingale order ---
        self._maybe_place_martingale(mark)

    def _maybe_place_martingale(self, mark: float):
        """Check if we need to place next martingale level order."""

        # Check if we already have a pending martingale order
        open_orders = get_open_orders(self.info, self.address)
        symbol_orders = [o for o in open_orders if o.get("coin") == self.symbol]

        if symbol_orders:
            # We have pending orders, check if any filled
            open_oids = {o["oid"] for o in symbol_orders}

            if self.state.direction == "long":
                # Check if our martingale buy filled
                buy_orders = [o for o in symbol_orders if o.get("side") == "B"]
                if buy_orders:
                    return  # Still pending, wait

                # No buy orders left but we had one → it filled, level up
                if self.state.pending_buy_oid and self.state.pending_buy_oid not in open_oids:
                    self.state.level += 1
                    self.state.pending_buy_oid = 0
                    # Re-sync from exchange
                    pos = get_position(self.info, self.address, self.symbol)
                    if pos:
                        self.state.avg_entry = float(pos.get("entryPx", "0"))
                        self.state.total_size = abs(float(pos.get("szi", "0")))
                    self.logger.info(
                        f"Martingale BUY filled! Level={self.state.level} "
                        f"new_avg={self.state.avg_entry} size={self.state.total_size}"
                    )
                    return
            else:
                sell_orders = [o for o in symbol_orders if o.get("side") == "A"]
                if sell_orders:
                    return  # Still pending

                if self.state.pending_sell_oid and self.state.pending_sell_oid not in open_oids:
                    self.state.level += 1
                    self.state.pending_sell_oid = 0
                    pos = get_position(self.info, self.address, self.symbol)
                    if pos:
                        self.state.avg_entry = float(pos.get("entryPx", "0"))
                        self.state.total_size = abs(float(pos.get("szi", "0")))
                    self.logger.info(
                        f"Martingale SELL filled! Level={self.state.level} "
                        f"new_avg={self.state.avg_entry} size={self.state.total_size}"
                    )
                    return

            return  # Has other orders, wait

        # No pending orders → place next martingale level
        if self.state.level >= self.cfg["max_levels"]:
            return

        bps = self.cfg["grid_spacing_bps"]
        multiplier = self.cfg["martingale_multiplier"]
        base_size_usd = self.cfg["initial_size_usd"]

        # Next size = initial * multiplier^level
        next_size_usd = base_size_usd * (multiplier ** self.state.level)
        next_size_coin = round_size(next_size_usd / mark, self.sz_decimals)

        if next_size_coin <= 0:
            return

        # Calculate next entry price (worse than current average)
        next_price = calc_martingale_price(self.state.avg_entry, bps * (self.state.level + 1), self.state.direction)

        if self.state.direction == "long":
            result = place_limit_order(self.exchange, self.symbol, True, next_size_coin, next_price)
            self.state.pending_buy_oid = extract_oid_from_response(result)
            self.logger.info(
                f"Martingale BUY L{self.state.level + 1}: {next_size_coin} @ {next_price} "
                f"(oid={self.state.pending_buy_oid})"
            )
        else:
            result = place_limit_order(self.exchange, self.symbol, False, next_size_coin, next_price)
            self.state.pending_sell_oid = extract_oid_from_response(result)
            self.logger.info(
                f"Martingale SELL L{self.state.level + 1}: {next_size_coin} @ {next_price} "
                f"(oid={self.state.pending_sell_oid})"
            )

    def _close_all_and_reset(self):
        """Close entire position and reset grid."""
        self.logger.info("Closing all positions and resetting grid...")

        # Cancel all open orders first
        cancel_all_orders(self.exchange, self.info, self.address, self.symbol)

        # Market close position
        place_market_close(self.exchange, self.symbol)

        # Verify close
        time.sleep(2)
        pos = get_position(self.info, self.address, self.symbol)
        if pos:
            szi = abs(float(pos.get("szi", "0")))
            if szi > 0:
                self.logger.warning(f"Position not fully closed ({szi} remaining), retrying...")
                place_market_close(self.exchange, self.symbol, size=szi)

        self.state.reset()
        self.logger.info("Grid reset complete. New cycle will start next tick.")

    def _emergency_close(self):
        """Emergency: close everything and stop."""
        self.logger.critical("EMERGENCY CLOSE - cancelling all orders and closing positions")
        cancel_all_orders(self.exchange, self.info, self.address, self.symbol)
        place_market_close(self.exchange, self.symbol)
        self.state.reset()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------


def main():
    config = load_config()
    logger = setup_logging(config)

    logger.info("=" * 60)
    logger.info("  この戦略は小さい利益を高頻度で積み重ねる「勝手にりえき」型です")
    logger.info("  Martingale Averaging Grid Bot for Hyperliquid Perps")
    logger.info("=" * 60)

    bot = MartingaleGridBot(config)
    bot.run()


if __name__ == "__main__":
    main()
