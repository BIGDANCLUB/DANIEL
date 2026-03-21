"""
Core scanner engine — Phase 8
================================
- Multi-exchange CEX scanning (Binance + Bybit)
- CryptoPanic social filter
- Multi-TF trendline confirmation (Phase 8A: enhanced 15m/1h/4h)
- Watchlist support
- Signal history tracking & hit-rate analysis
- Alert condition engine
- Market overview dashboard data
- AI win prediction integration (Phase 8C)
- Notification dispatch (Phase 8D)
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional

import pandas as pd

from config import Config
from data_fetcher import CEXFetcher, DexScreenerFetcher, CryptoPanicFetcher
from technical_analysis import (
    is_above_ema,
    detect_volume_spike,
    detect_trendline_break,
    confirm_trendline_multi_tf,
    compute_scan_score,
    compute_scan_score_v2,
    compute_ema,
    get_rsi_signal,
    get_macd_signal,
    get_bb_signal,
    PATTERN_LABELS,
)
from mtf_strategy import compute_mtf_signal, fetch_mtf_data, MTFSignal
from ai_predictor import SignalPredictor
from notifier import UnifiedNotifier

logger = logging.getLogger(__name__)

WATCHLIST_FILE = os.path.join(os.path.dirname(__file__), ".watchlist.json")


class ScanResult:
    """Single coin scan result."""

    def __init__(
        self,
        symbol: str,
        source: str,
        price: float,
        change_pct: float,
        volume_24h: float,
        volume_ratio: float,
        above_ema: bool,
        trendline_break: dict,
        social_boost: bool,
        score: float,
        scan_time: datetime,
        extra: dict = None,
    ):
        self.symbol = symbol
        self.source = source
        self.price = price
        self.change_pct = change_pct
        self.volume_24h = volume_24h
        self.volume_ratio = volume_ratio
        self.above_ema = above_ema
        self.trendline_break = trendline_break
        self.social_boost = social_boost
        self.score = score
        self.scan_time = scan_time
        self.extra = extra or {}

    def to_dict(self) -> dict:
        breakout = self.trendline_break.get("breakout_type") or "—"
        pattern = self.trendline_break.get("pattern_label", "—")
        vol_conf = self.trendline_break.get("volume_confirmed", False)
        conf_bars = self.trendline_break.get("confirmation_bars", 0)
        return {
            "Symbol": self.symbol,
            "Source": self.source,
            "Price": self.price,
            "24h %": self.change_pct,
            "24h Vol": self.volume_24h,
            "Vol Ratio": self.volume_ratio,
            "Above 200EMA": self.above_ema,
            "Trendline Break": breakout,
            "Pattern": pattern,
            "Vol Confirm": vol_conf,
            "Conf Bars": conf_bars,
            "Break Strength": self.trendline_break.get("break_strength", 0),
            "Social": self.social_boost,
            "Score": self.score,
            "Scan Time": self.scan_time.strftime("%H:%M:%S"),
        }


# ──────────────────────────────────────────────
# Watchlist persistence
# ──────────────────────────────────────────────
def load_watchlist() -> list[str]:
    """Load watchlist from file."""
    try:
        if os.path.exists(WATCHLIST_FILE):
            with open(WATCHLIST_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def save_watchlist(symbols: list[str]):
    """Save watchlist to file."""
    try:
        with open(WATCHLIST_FILE, "w") as f:
            json.dump(sorted(set(symbols)), f, indent=2)
    except Exception as e:
        logger.warning("Failed to save watchlist: %s", e)


def add_to_watchlist(symbol: str):
    wl = load_watchlist()
    if symbol not in wl:
        wl.append(symbol)
        save_watchlist(wl)


def remove_from_watchlist(symbol: str):
    wl = load_watchlist()
    wl = [s for s in wl if s != symbol]
    save_watchlist(wl)


# ──────────────────────────────────────────────
# Signal history tracking & hit-rate analysis
# ──────────────────────────────────────────────
SIGNAL_HISTORY_FILE = os.path.join(os.path.dirname(__file__), ".signal_history.json")
MAX_HISTORY_RECORDS = 500


def load_signal_history() -> list[dict]:
    try:
        if os.path.exists(SIGNAL_HISTORY_FILE):
            with open(SIGNAL_HISTORY_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def save_signal_history(records: list[dict]):
    try:
        # Keep only the latest MAX_HISTORY_RECORDS
        trimmed = records[-MAX_HISTORY_RECORDS:]
        with open(SIGNAL_HISTORY_FILE, "w") as f:
            json.dump(trimmed, f, indent=2, default=str)
    except Exception as e:
        logger.warning("Failed to save signal history: %s", e)


def record_signals(results: list["ScanResult"]):
    """Append current scan results to signal history."""
    history = load_signal_history()
    for r in results:
        history.append({
            "symbol": r.symbol,
            "source": r.source,
            "price_at_signal": r.price,
            "score": r.score,
            "breakout_type": r.trendline_break.get("breakout_type"),
            "pattern": r.trendline_break.get("pattern_label", "—"),
            "volume_ratio": r.volume_ratio,
            "above_ema": r.above_ema,
            "social_boost": r.social_boost,
            "scan_time": r.scan_time.isoformat(),
            "price_after_1h": None,
            "price_after_4h": None,
            "price_after_24h": None,
            "hit": None,  # True if price rose >2% within 24h
        })
    save_signal_history(history)


async def update_signal_outcomes():
    """Check past signals and update their outcome prices."""
    history = load_signal_history()
    if not history:
        return

    now = datetime.now(timezone.utc)
    updated = False
    fetcher = None

    try:
        for record in history:
            if record.get("hit") is not None:
                continue  # Already resolved
            signal_time = datetime.fromisoformat(record["scan_time"])
            hours_elapsed = (now - signal_time).total_seconds() / 3600

            # Only check CEX signals (we can fetch ticker)
            if "DEX" in record.get("source", ""):
                if hours_elapsed >= 24:
                    record["hit"] = False  # Can't track DEX, mark as unknown
                    updated = True
                continue

            symbol = record["symbol"]

            # Check at 1h, 4h, 24h marks
            needs_check = False
            if hours_elapsed >= 1 and record.get("price_after_1h") is None:
                needs_check = True
            if hours_elapsed >= 4 and record.get("price_after_4h") is None:
                needs_check = True
            if hours_elapsed >= 24 and record.get("price_after_24h") is None:
                needs_check = True

            if not needs_check:
                continue

            if fetcher is None:
                fetcher = CEXFetcher()

            try:
                ticker = await fetcher.fetch_ticker(symbol)
                current_price = ticker.get("last", 0) or 0
                if current_price <= 0:
                    continue

                if hours_elapsed >= 1 and record.get("price_after_1h") is None:
                    record["price_after_1h"] = current_price
                    updated = True
                if hours_elapsed >= 4 and record.get("price_after_4h") is None:
                    record["price_after_4h"] = current_price
                    updated = True
                if hours_elapsed >= 24 and record.get("price_after_24h") is None:
                    record["price_after_24h"] = current_price
                    updated = True

                # Determine hit/miss after 24h
                if hours_elapsed >= 24 and record.get("hit") is None:
                    entry = record["price_at_signal"]
                    if entry > 0:
                        max_price = max(
                            record.get("price_after_1h") or entry,
                            record.get("price_after_4h") or entry,
                            record.get("price_after_24h") or entry,
                        )
                        gain_pct = (max_price - entry) / entry * 100
                        record["hit"] = gain_pct >= 2.0  # 2% threshold
                        record["max_gain_pct"] = round(gain_pct, 2)
                    updated = True
            except Exception:
                continue

    finally:
        if fetcher:
            await fetcher.close()

    if updated:
        save_signal_history(history)


def compute_hit_rate_stats() -> dict:
    """Compute hit-rate statistics from signal history."""
    history = load_signal_history()
    if not history:
        return {"total": 0, "resolved": 0, "hits": 0, "misses": 0, "hit_rate": 0, "avg_gain": 0}

    resolved = [r for r in history if r.get("hit") is not None]
    hits = [r for r in resolved if r["hit"]]
    misses = [r for r in resolved if not r["hit"]]
    gains = [r.get("max_gain_pct", 0) for r in resolved if "max_gain_pct" in r]

    return {
        "total": len(history),
        "resolved": len(resolved),
        "hits": len(hits),
        "misses": len(misses),
        "hit_rate": len(hits) / max(len(resolved), 1),
        "avg_gain": sum(gains) / max(len(gains), 1) if gains else 0,
        "pending": len(history) - len(resolved),
    }


# ──────────────────────────────────────────────
# Alert condition engine
# ──────────────────────────────────────────────
ALERTS_FILE = os.path.join(os.path.dirname(__file__), ".alerts.json")


def load_alerts() -> list[dict]:
    try:
        if os.path.exists(ALERTS_FILE):
            with open(ALERTS_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return []


def save_alerts(alerts: list[dict]):
    try:
        with open(ALERTS_FILE, "w") as f:
            json.dump(alerts, f, indent=2)
    except Exception as e:
        logger.warning("Failed to save alerts: %s", e)


def add_alert(alert: dict):
    """Add a new alert condition.
    alert = {
        "name": str,
        "min_score": int (0-100),
        "breakout_type": "bullish" | "bearish" | "any" | None,
        "patterns": [str] or None,
        "min_volume_ratio": float or None,
        "require_social": bool,
        "require_multi_tf": bool,
        "symbols": [str] or None (empty = all),
        "enabled": True,
    }
    """
    alerts = load_alerts()
    alert.setdefault("enabled", True)
    alert.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    alerts.append(alert)
    save_alerts(alerts)


def remove_alert(index: int):
    alerts = load_alerts()
    if 0 <= index < len(alerts):
        alerts.pop(index)
        save_alerts(alerts)


def check_alerts(results: list["ScanResult"]) -> list[dict]:
    """Check scan results against configured alerts. Returns triggered alerts."""
    alerts = load_alerts()
    triggered = []

    for alert in alerts:
        if not alert.get("enabled", True):
            continue

        for r in results:
            # Symbol filter
            if alert.get("symbols") and r.symbol not in alert["symbols"]:
                continue

            # Score filter
            if r.score < alert.get("min_score", 0):
                continue

            # Breakout type filter
            req_type = alert.get("breakout_type")
            actual_type = r.trendline_break.get("breakout_type")
            if req_type and req_type != "any" and actual_type != req_type:
                continue

            # Pattern filter
            req_patterns = alert.get("patterns")
            if req_patterns:
                actual_pattern = r.trendline_break.get("pattern_label", "")
                if actual_pattern not in req_patterns:
                    continue

            # Volume ratio filter
            min_vr = alert.get("min_volume_ratio")
            if min_vr and r.volume_ratio < min_vr:
                continue

            # Social filter
            if alert.get("require_social") and not r.social_boost:
                continue

            # Multi-TF filter
            if alert.get("require_multi_tf") and not r.trendline_break.get("multi_tf_confirmed"):
                continue

            triggered.append({
                "alert_name": alert.get("name", "Unnamed"),
                "symbol": r.symbol,
                "source": r.source,
                "score": r.score,
                "price": r.price,
                "breakout_type": actual_type,
                "pattern": r.trendline_break.get("pattern_label", "—"),
                "time": datetime.now(timezone.utc).isoformat(),
            })

    return triggered


# ──────────────────────────────────────────────
# Market overview data
# ──────────────────────────────────────────────
class MarketOverview:
    """Fetch market-wide metrics (all free)."""

    @staticmethod
    def get_btc_dominance_and_fear() -> dict:
        """Fetch BTC price + rough market data from CCXT/Binance."""
        import requests
        result = {
            "btc_price": 0,
            "btc_change_24h": 0,
            "eth_price": 0,
            "eth_change_24h": 0,
            "fear_greed_value": 0,
            "fear_greed_label": "N/A",
        }
        # BTC/ETH from Binance public
        try:
            resp = requests.get(
                "https://api.binance.com/api/v3/ticker/24hr",
                params={"symbols": '["BTCUSDT","ETHUSDT"]'},
                timeout=10,
            )
            resp.raise_for_status()
            for t in resp.json():
                if t["symbol"] == "BTCUSDT":
                    result["btc_price"] = float(t["lastPrice"])
                    result["btc_change_24h"] = float(t["priceChangePercent"])
                elif t["symbol"] == "ETHUSDT":
                    result["eth_price"] = float(t["lastPrice"])
                    result["eth_change_24h"] = float(t["priceChangePercent"])
        except Exception:
            pass

        # Fear & Greed Index (free API)
        try:
            resp = requests.get(
                "https://api.alternative.me/fng/?limit=1",
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json().get("data", [{}])[0]
            result["fear_greed_value"] = int(data.get("value", 0))
            result["fear_greed_label"] = data.get("value_classification", "N/A")
        except Exception:
            pass

        return result


# ──────────────────────────────────────────────
# Scanner Engine — Phase 4 (Multi-Exchange)
# ──────────────────────────────────────────────
class ScannerEngine:
    """Main scanner — Phase 8 with MTF + AI + Notifications."""

    # Exchanges to scan
    CEX_EXCHANGES = ["binance", "bybit"]

    def __init__(self):
        self._results_cache: list[ScanResult] = []
        self._last_scan: Optional[datetime] = None
        self._scan_stats: dict = {}
        self._last_triggered_alerts: list[dict] = []
        # Phase 8 additions
        self.ai_predictor = SignalPredictor()
        self.notifier = UnifiedNotifier()
        self._mtf_signals: dict[str, MTFSignal] = {}  # symbol -> MTFSignal

    async def scan_cex_exchange(
        self, exchange_id: str, top_n: int = None
    ) -> list[ScanResult]:
        """Scan a single CEX exchange."""
        results = []
        fetcher = CEXFetcher(exchange_id=exchange_id)
        source_name = f"{exchange_id.capitalize()} Futures"
        errors = []
        scanned = 0
        filtered_out = 0
        try:
            top_n = top_n or Config.CEX_TOP_N
            symbols = await fetcher.fetch_top_symbols(top_n=top_n)
            logger.info("Scanning %d symbols on %s...", len(symbols), exchange_id)

            for symbol in symbols:
                try:
                    scanned += 1
                    result = await self._analyze_cex_symbol(fetcher, symbol, source_name)
                    if result:
                        results.append(result)
                    else:
                        filtered_out += 1
                except Exception as e:
                    errors.append(f"{symbol}: {e}")
                    continue

        except Exception as e:
            logger.error("%s scan failed: %s", exchange_id, repr(e))
            errors.insert(0, f"EXCHANGE ERROR: {type(e).__name__}: {e}")
        finally:
            await fetcher.close()

        # Store diagnostic info
        self._scan_stats[f"{exchange_id}_detail"] = {
            "scanned": scanned,
            "signals": len(results),
            "filtered_out": filtered_out,
            "errors": len(errors),
            "sample_errors": errors[:5],
        }
        logger.info(
            "%s: scanned=%d, signals=%d, filtered_out=%d, errors=%d",
            exchange_id, scanned, len(results), filtered_out, len(errors),
        )
        if errors:
            logger.info("%s sample errors: %s", exchange_id, errors[:3])

        return results

    async def _analyze_cex_symbol(
        self, fetcher: CEXFetcher, symbol: str, source: str
    ) -> Optional[ScanResult]:
        """Analyze a single CEX symbol with Phase 8 MTF + AI."""
        df_1h = await fetcher.fetch_ohlcv(symbol, timeframe="1h", limit=250)
        if df_1h.empty or len(df_1h) < 30:
            return None

        df_4h = await fetcher.fetch_ohlcv(symbol, timeframe="4h", limit=250)

        # Phase 8A: Fetch 15m for MTF strategy
        df_15m = await fetcher.fetch_ohlcv(symbol, timeframe="15m", limit=200)

        # Volume spike (1H)
        vol_spike, vol_ratio = detect_volume_spike(df_1h, recent_bars=1, lookback_bars=24)

        # 200 EMA on 4H
        ema_ok = False
        if df_4h is not None and len(df_4h) >= 200:
            ema_ok = is_above_ema(df_4h, period=200)

        # Multi-timeframe trendline break
        if df_4h is not None and len(df_4h) >= 30:
            multi_tf = confirm_trendline_multi_tf(df_1h, df_4h)
            tl_result = multi_tf["1h"]
            if multi_tf["both_confirm"]:
                tl_result["break_strength"] = min(
                    tl_result.get("break_strength", 0) + 0.3, 1.0
                )
                tl_result["multi_tf_confirmed"] = True
            else:
                tl_result["multi_tf_confirmed"] = False
        else:
            tl_result = detect_trendline_break(df_1h)
            tl_result["multi_tf_confirmed"] = False

        # Phase 6: RSI, MACD, BB signals
        rsi_data = get_rsi_signal(df_1h)
        macd_data = get_macd_signal(df_1h)
        bb_data = get_bb_signal(df_1h)

        # Social boost
        social = False
        try:
            social_data = CryptoPanicFetcher.detect_social_boost(symbol)
            social = social_data.get("boost", False)
        except Exception:
            pass

        # Phase 6: Enhanced scoring with all indicators
        score = compute_scan_score_v2(
            ema_ok, vol_spike, vol_ratio, tl_result, social,
            rsi_data=rsi_data, macd_data=macd_data, bb_data=bb_data,
        )

        # Phase 8A: MTF strategy signal
        mtf_signal = None
        tf_data = {"1h": df_1h}
        if df_4h is not None and not df_4h.empty:
            tf_data["4h"] = df_4h
        if df_15m is not None and not df_15m.empty:
            tf_data["15m"] = df_15m

        if len(tf_data) >= 2:
            try:
                mtf_signal = compute_mtf_signal(symbol, tf_data)
                score = min(score + mtf_signal.mtf_score_bonus, 100)
                self._mtf_signals[symbol] = mtf_signal
            except Exception as e:
                logger.debug("MTF analysis error for %s: %s", symbol, e)

        # Allow results through if they have any notable signal
        if not (vol_spike or tl_result.get("resistance_break") or
                tl_result.get("support_break") or score >= 15):
            return None

        current_price = float(df_1h["close"].iloc[-1])
        ticker = await fetcher.fetch_ticker(symbol)
        change_pct = ticker.get("percentage", 0) or 0
        volume_24h = ticker.get("quoteVolume", 0) or 0

        result = ScanResult(
            symbol=symbol,
            source=source,
            price=current_price,
            change_pct=round(change_pct, 2),
            volume_24h=round(volume_24h, 0),
            volume_ratio=vol_ratio,
            above_ema=ema_ok,
            trendline_break=tl_result,
            social_boost=social,
            score=score,
            scan_time=datetime.now(timezone.utc),
            extra={
                "timeframe_analysis": "15M+1H+4H",
                "rsi": rsi_data,
                "macd": macd_data,
                "bb": bb_data,
                "mtf": {
                    "htf_trend": mtf_signal.htf_trend if mtf_signal else "N/A",
                    "ltf_entry": mtf_signal.ltf_entry if mtf_signal else "N/A",
                    "alignment_score": mtf_signal.alignment_score if mtf_signal else 0,
                    "entry_quality": mtf_signal.entry_quality if mtf_signal else "N/A",
                    "recommended_action": mtf_signal.recommended_action if mtf_signal else "wait",
                    "confluence_factors": mtf_signal.confluence_factors[:5] if mtf_signal else [],
                },
            },
        )

        # Phase 8C: AI prediction
        try:
            ai_pred = self.ai_predictor.predict(result)
            result.extra["ai_prediction"] = ai_pred
        except Exception as e:
            logger.debug("AI prediction error for %s: %s", symbol, e)

        return result

    def scan_dex(self) -> list[ScanResult]:
        """Scan DexScreener for trending DEX pairs."""
        results = []
        dex_errors = []
        total_pairs = 0
        for chain in Config.DEXSCREENER_CHAINS:
            try:
                pairs = DexScreenerFetcher.get_trending_tokens(chain)
                logger.info("DexScreener: %d pairs for %s", len(pairs), chain)
                total_pairs += len(pairs)
                for pair in pairs[:20]:
                    result = self._analyze_dex_pair(pair, chain)
                    if result:
                        results.append(result)
            except Exception as e:
                dex_errors.append(f"{chain}: {e}")
                logger.warning("DexScreener scan error (%s): %s", chain, e)
        self._scan_stats["dex_detail"] = {
            "total_pairs": total_pairs,
            "signals": len(results),
            "errors": dex_errors[:3],
        }
        return results

    def _analyze_dex_pair(self, pair: dict, chain: str) -> Optional[ScanResult]:
        """Analyze a single DexScreener pair."""
        try:
            price_change = pair.get("priceChange", {})
            h1_change = price_change.get("h1", 0) or 0
            h6_change = price_change.get("h6", 0) or 0
            h24_change = price_change.get("h24", 0) or 0

            volume = pair.get("volume", {})
            vol_h1 = volume.get("h1", 0) or 0
            vol_h24 = volume.get("h24", 0) or 0

            hourly_avg = vol_h24 / 24 if vol_h24 > 0 else 0
            vol_ratio = vol_h1 / hourly_avg if hourly_avg > 0 else 0
            vol_spike = vol_ratio >= Config.VOLUME_SPIKE_MULTIPLIER

            tl_result = {
                "resistance_break": h1_change > 5 and h6_change > 10,
                "support_break": False,
                "breakout_type": "bullish" if h1_change > 5 else None,
                "break_strength": min(abs(h1_change) / 20, 1.0),
                "volume_confirmed": vol_spike,
                "pattern": "unknown",
                "pattern_label": "—",
                "confirmation_bars": 0,
                "multi_tf_confirmed": False,
            }

            above_ema = h24_change > 0

            social = False
            symbol_name = pair.get("baseToken", {}).get("symbol", "?")
            try:
                social_data = CryptoPanicFetcher.detect_social_boost(symbol_name)
                social = social_data.get("boost", False)
            except Exception:
                pass

            score = compute_scan_score(above_ema, vol_spike, vol_ratio, tl_result, social)

            if score < 10:
                return None

            quote_name = pair.get("quoteToken", {}).get("symbol", "?")
            display_symbol = f"{symbol_name}/{quote_name}"

            return ScanResult(
                symbol=display_symbol,
                source=f"DEX ({chain})",
                price=float(pair.get("priceUsd", 0) or 0),
                change_pct=round(h24_change, 2),
                volume_24h=round(vol_h24, 0),
                volume_ratio=round(vol_ratio, 2),
                above_ema=above_ema,
                trendline_break=tl_result,
                social_boost=social,
                score=score,
                scan_time=datetime.now(timezone.utc),
                extra={
                    "chain": chain,
                    "pair_address": pair.get("pairAddress", ""),
                    "liquidity_usd": pair.get("liquidity", {}).get("usd", 0),
                    "dexId": pair.get("dexId", ""),
                    "h1_change": h1_change,
                    "h6_change": h6_change,
                },
            )
        except Exception as e:
            logger.debug("DEX pair analysis error: %s", e)
            return None

    async def run_full_scan(
        self, exchanges: list[str] = None, include_dex: bool = True
    ) -> list[ScanResult]:
        """Run full scan: multi-CEX + DEX, sort by score."""
        exchanges = exchanges or self.CEX_EXCHANGES
        logger.info("Starting full scan (Phase 4) — exchanges: %s", exchanges)
        start = time.time()

        all_results = []
        stats = {}

        # Scan each CEX exchange
        for ex_id in exchanges:
            ex_results = await self.scan_cex_exchange(ex_id)
            all_results.extend(ex_results)
            stats[ex_id] = len(ex_results)
            logger.info("%s: %d signals", ex_id, len(ex_results))

        # DEX scan
        if include_dex:
            dex_results = self.scan_dex()
            all_results.extend(dex_results)
            stats["dex"] = len(dex_results)

        # Deduplicate: if same base symbol appears on multiple exchanges, keep highest score
        seen = {}
        deduped = []
        for r in sorted(all_results, key=lambda x: x.score, reverse=True):
            base = r.symbol.split("/")[0]
            if base not in seen:
                seen[base] = r
                deduped.append(r)
            else:
                # Keep both but mark the lower one
                deduped.append(r)

        deduped.sort(key=lambda r: r.score, reverse=True)

        self._results_cache = deduped
        self._last_scan = datetime.now(timezone.utc)
        # Merge basic stats into detail stats (don't overwrite)
        self._scan_stats.update(stats)

        # Phase 5: Record signals to history
        record_signals(deduped)

        # Phase 5: Check alerts
        self._last_triggered_alerts = check_alerts(deduped)

        # Phase 8D: Send notifications for triggered alerts
        if deduped and self.notifier.any_configured:
            try:
                await self.notifier.notify_signals(
                    deduped, datetime.now(timezone.utc)
                )
            except Exception as e:
                logger.debug("Notification error: %s", e)

        elapsed = time.time() - start
        logger.info(
            "Scan complete: %d results in %.1fs (stats: %s)",
            len(deduped), elapsed, stats,
        )
        return deduped

    @property
    def cached_results(self) -> list[ScanResult]:
        return self._results_cache

    @property
    def last_scan_time(self) -> Optional[datetime]:
        return self._last_scan

    @property
    def scan_stats(self) -> dict:
        return self._scan_stats

    @property
    def triggered_alerts(self) -> list[dict]:
        return self._last_triggered_alerts

    @property
    def mtf_signals(self) -> dict:
        return self._mtf_signals

    def get_mtf_signal(self, symbol: str) -> Optional[MTFSignal]:
        return self._mtf_signals.get(symbol)


# ──────────────────────────────────────────────
# Phase 6: Mini Backtester
# ──────────────────────────────────────────────
class MiniBacktester:
    """
    Backtest trendline break strategy on historical OHLCV data.
    Simulates entries on trendline break signals, exits on:
    - Take profit: +X%
    - Stop loss: -Y%
    - Max hold: N bars
    """

    def __init__(
        self,
        take_profit_pct: float = 3.0,
        stop_loss_pct: float = 2.0,
        max_hold_bars: int = 24,
        min_score: float = 40.0,
    ):
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.max_hold_bars = max_hold_bars
        self.min_score = min_score

    async def run_backtest(
        self, symbol: str, exchange_id: str = "binance", timeframe: str = "1h", bars: int = 500
    ) -> dict:
        """
        Run backtest on a single symbol.
        Returns: {trades: [...], stats: {...}}
        """
        fetcher = CEXFetcher(exchange_id=exchange_id)
        try:
            df = await fetcher.fetch_ohlcv(symbol, timeframe=timeframe, limit=bars)
        finally:
            await fetcher.close()

        if df.empty or len(df) < 100:
            return {"trades": [], "stats": {"error": "Insufficient data"}}

        trades = []
        position = None  # {entry_price, entry_idx, entry_time}

        # Slide a window through the data
        window_size = 100
        for i in range(window_size, len(df)):
            window = df.iloc[i - window_size:i + 1].copy()

            if position is not None:
                # Check exit conditions
                current_price = float(df["close"].iloc[i])
                entry_price = position["entry_price"]
                bars_held = i - position["entry_idx"]
                pnl_pct = (current_price - entry_price) / entry_price * 100

                exit_reason = None
                if pnl_pct >= self.take_profit_pct:
                    exit_reason = "TP"
                elif pnl_pct <= -self.stop_loss_pct:
                    exit_reason = "SL"
                elif bars_held >= self.max_hold_bars:
                    exit_reason = "timeout"

                if exit_reason:
                    trades.append({
                        "entry_time": position["entry_time"],
                        "entry_price": entry_price,
                        "exit_time": str(df.index[i]),
                        "exit_price": current_price,
                        "pnl_pct": round(pnl_pct, 2),
                        "bars_held": bars_held,
                        "exit_reason": exit_reason,
                    })
                    position = None
                continue

            # Check for entry signal (every 6 bars to avoid over-trading)
            if i % 6 != 0:
                continue

            from technical_analysis import (
                detect_trendline_break as _dtb,
                detect_volume_spike as _dvs,
                is_above_ema as _iae,
                get_rsi_signal as _grs,
                get_macd_signal as _gms,
                get_bb_signal as _gbs,
                compute_scan_score_v2 as _css2,
            )

            tl = _dtb(window)
            vs, vr = _dvs(window)
            ema_ok = _iae(window) if len(window) >= 200 else False
            rsi_d = _grs(window)
            macd_d = _gms(window)
            bb_d = _gbs(window)

            score = _css2(ema_ok, vs, vr, tl, False,
                          rsi_data=rsi_d, macd_data=macd_d, bb_data=bb_d)

            if score >= self.min_score and tl.get("resistance_break"):
                position = {
                    "entry_price": float(df["close"].iloc[i]),
                    "entry_idx": i,
                    "entry_time": str(df.index[i]),
                }

        # Close any remaining position at end
        if position:
            final_price = float(df["close"].iloc[-1])
            pnl_pct = (final_price - position["entry_price"]) / position["entry_price"] * 100
            trades.append({
                "entry_time": position["entry_time"],
                "entry_price": position["entry_price"],
                "exit_time": str(df.index[-1]),
                "exit_price": final_price,
                "pnl_pct": round(pnl_pct, 2),
                "bars_held": len(df) - 1 - position["entry_idx"],
                "exit_reason": "end",
            })

        # Compute stats
        stats = self._compute_stats(trades)
        return {"trades": trades, "stats": stats}

    @staticmethod
    def _compute_stats(trades: list[dict]) -> dict:
        if not trades:
            return {"total": 0, "wins": 0, "losses": 0, "win_rate": 0,
                    "avg_pnl": 0, "total_pnl": 0, "max_win": 0, "max_loss": 0,
                    "profit_factor": 0, "avg_bars": 0}

        pnls = [t["pnl_pct"] for t in trades]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p <= 0]
        bars = [t["bars_held"] for t in trades]

        gross_profit = sum(wins) if wins else 0
        gross_loss = abs(sum(losses)) if losses else 0

        return {
            "total": len(trades),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": len(wins) / max(len(trades), 1),
            "avg_pnl": sum(pnls) / len(pnls),
            "total_pnl": sum(pnls),
            "max_win": max(pnls) if pnls else 0,
            "max_loss": min(pnls) if pnls else 0,
            "profit_factor": gross_profit / max(gross_loss, 0.01),
            "avg_bars": sum(bars) / max(len(bars), 1),
        }
