"""
Phase 8D: Notification Bot (Telegram + Discord)
================================================
Send alert notifications via:
- Telegram Bot API
- Discord Webhook

Both are free and require minimal setup.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional

import aiohttp
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("notifier")


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
class NotifierConfig:
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Discord
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")

    # Notification settings
    NOTIFY_MIN_SCORE: float = float(os.getenv("NOTIFY_MIN_SCORE", "50"))
    NOTIFY_COOLDOWN_SEC: int = int(os.getenv("NOTIFY_COOLDOWN_SEC", "300"))
    NOTIFY_MAX_PER_SCAN: int = int(os.getenv("NOTIFY_MAX_PER_SCAN", "5"))


# ──────────────────────────────────────────────
# Message formatters
# ──────────────────────────────────────────────
def format_signal_telegram(signal) -> str:
    """Format a signal for Telegram (MarkdownV2)."""
    tl = signal.trendline_break or {}
    bt = tl.get("breakout_type", "—")
    pattern = tl.get("pattern_label", "—")

    emoji_dir = "🟢" if bt == "bullish" else ("🔴" if bt == "bearish" else "⚪")
    emoji_score = "🔥" if signal.score >= 70 else ("⚡" if signal.score >= 40 else "📊")

    # Escape special characters for MarkdownV2
    def esc(text):
        special = r"_*[]()~`>#+-=|{}.!"
        return "".join(f"\\{c}" if c in special else c for c in str(text))

    lines = [
        f"{emoji_score} *{esc(signal.symbol)}* \\| Score: *{signal.score:.0f}*",
        f"{emoji_dir} {esc(bt.upper())} break \\| Pattern: {esc(pattern)}",
        f"💰 Price: ${esc(f'{signal.price:,.4f}')}",
        f"📈 24h: {esc(f'{signal.change_pct:+.2f}%')} \\| Vol: {esc(f'{signal.volume_ratio:.1f}x')}",
    ]

    # Optional fields
    if tl.get("volume_confirmed"):
        lines.append("✅ Volume confirmed")
    if tl.get("multi_tf_confirmed"):
        lines.append("✅ Multi\\-TF confirmed")
    if signal.social_boost:
        lines.append("📱 Social boost detected")

    # AI prediction if available
    extra = signal.extra or {}
    ai_pred = extra.get("ai_prediction", {})
    if ai_pred.get("win_probability") is not None:
        wp = ai_pred["win_probability"]
        conf = ai_pred.get("confidence", "")
        lines.append(f"🤖 AI: {esc(f'{wp:.0%}')} win prob \\({esc(conf)}\\)")

    lines.append(f"\n_Source: {esc(signal.source)}_")
    lines.append(f"_Time: {esc(datetime.now(timezone.utc).strftime('%H:%M UTC'))}_")

    return "\n".join(lines)


def format_signal_discord(signal) -> dict:
    """Format a signal for Discord embed."""
    tl = signal.trendline_break or {}
    bt = tl.get("breakout_type", "—")
    pattern = tl.get("pattern_label", "—")

    color = 0x00E676 if bt == "bullish" else (0xFF5252 if bt == "bearish" else 0xFFC107)

    fields = [
        {"name": "Score", "value": f"{signal.score:.0f}/100", "inline": True},
        {"name": "Breakout", "value": bt.upper(), "inline": True},
        {"name": "Pattern", "value": pattern, "inline": True},
        {"name": "Price", "value": f"${signal.price:,.4f}", "inline": True},
        {"name": "24h Change", "value": f"{signal.change_pct:+.2f}%", "inline": True},
        {"name": "Volume", "value": f"{signal.volume_ratio:.1f}x", "inline": True},
    ]

    extras = []
    if tl.get("volume_confirmed"):
        extras.append("Volume Confirmed")
    if tl.get("multi_tf_confirmed"):
        extras.append("Multi-TF Confirmed")
    if signal.social_boost:
        extras.append("Social Boost")

    if extras:
        fields.append({"name": "Confirmations", "value": " | ".join(extras), "inline": False})

    # AI prediction
    extra = signal.extra or {}
    ai_pred = extra.get("ai_prediction", {})
    if ai_pred.get("win_probability") is not None:
        fields.append({
            "name": "AI Prediction",
            "value": f"{ai_pred['win_probability']:.0%} win ({ai_pred.get('confidence', '')})",
            "inline": True,
        })

    return {
        "embeds": [{
            "title": f"{'🟢' if bt == 'bullish' else '🔴'} {signal.symbol}",
            "description": f"{signal.source} — Trendline Break Alert",
            "color": color,
            "fields": fields,
            "footer": {"text": f"Crypto Scanner | {datetime.now(timezone.utc).strftime('%H:%M UTC')}"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }]
    }


def format_scan_summary_telegram(signals: list, scan_time: datetime) -> str:
    """Format scan summary message for Telegram."""
    def esc(text):
        special = r"_*[]()~`>#+-=|{}.!"
        return "".join(f"\\{c}" if c in special else c for c in str(text))

    lines = [
        f"📊 *Scan Summary* \\| {esc(scan_time.strftime('%H:%M UTC'))}",
        f"Total signals: *{len(signals)}*",
        "",
    ]

    for s in signals[:NotifierConfig.NOTIFY_MAX_PER_SCAN]:
        bt = s.trendline_break.get("breakout_type", "—") if s.trendline_break else "—"
        emoji = "🟢" if bt == "bullish" else "🔴"
        lines.append(f"{emoji} {esc(s.symbol)} — Score: {s.score:.0f} \\| {esc(f'{s.change_pct:+.1f}%')}")

    if len(signals) > NotifierConfig.NOTIFY_MAX_PER_SCAN:
        lines.append(f"\n_\\+{len(signals) - NotifierConfig.NOTIFY_MAX_PER_SCAN} more signals_")

    return "\n".join(lines)


def format_scan_summary_discord(signals: list, scan_time: datetime) -> dict:
    """Format scan summary for Discord."""
    desc_lines = []
    for s in signals[:NotifierConfig.NOTIFY_MAX_PER_SCAN]:
        bt = s.trendline_break.get("breakout_type", "—") if s.trendline_break else "—"
        emoji = "🟢" if bt == "bullish" else "🔴"
        desc_lines.append(f"{emoji} **{s.symbol}** — Score: {s.score:.0f} | {s.change_pct:+.1f}%")

    if len(signals) > NotifierConfig.NOTIFY_MAX_PER_SCAN:
        desc_lines.append(f"\n*+{len(signals) - NotifierConfig.NOTIFY_MAX_PER_SCAN} more signals*")

    return {
        "embeds": [{
            "title": f"📊 Scan Summary — {scan_time.strftime('%H:%M UTC')}",
            "description": "\n".join(desc_lines),
            "color": 0x1A237E,
            "footer": {"text": f"Total: {len(signals)} signals | Crypto Scanner"},
            "timestamp": scan_time.isoformat(),
        }]
    }


# ──────────────────────────────────────────────
# Senders
# ──────────────────────────────────────────────
class TelegramNotifier:
    """Send notifications via Telegram Bot API."""

    def __init__(
        self, bot_token: str = None, chat_id: str = None
    ):
        self.bot_token = bot_token or NotifierConfig.TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or NotifierConfig.TELEGRAM_CHAT_ID
        self._last_send: dict[str, float] = {}

    @property
    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    async def send_message(self, text: str, parse_mode: str = "MarkdownV2") -> bool:
        """Send a message to the configured chat."""
        if not self.is_configured:
            logger.debug("Telegram not configured, skipping")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        logger.info("Telegram message sent")
                        return True
                    else:
                        body = await resp.text()
                        logger.warning("Telegram send failed (%d): %s", resp.status, body[:200])
                        return False
        except Exception as e:
            logger.error("Telegram error: %s", e)
            return False

    async def send_signal(self, signal) -> bool:
        """Send a single signal notification with cooldown."""
        key = signal.symbol
        import time
        now = time.time()
        last = self._last_send.get(key, 0)
        if now - last < NotifierConfig.NOTIFY_COOLDOWN_SEC:
            logger.debug("Cooldown active for %s", key)
            return False

        text = format_signal_telegram(signal)
        ok = await self.send_message(text)
        if ok:
            self._last_send[key] = now
        return ok

    async def send_scan_summary(self, signals: list, scan_time: datetime) -> bool:
        """Send scan summary."""
        if not signals:
            return False
        text = format_scan_summary_telegram(signals, scan_time)
        return await self.send_message(text)


class DiscordNotifier:
    """Send notifications via Discord Webhook."""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or NotifierConfig.DISCORD_WEBHOOK_URL
        self._last_send: dict[str, float] = {}

    @property
    def is_configured(self) -> bool:
        return bool(self.webhook_url)

    async def send_embed(self, payload: dict) -> bool:
        """Send an embed to Discord."""
        if not self.is_configured:
            logger.debug("Discord not configured, skipping")
            return False

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status in (200, 204):
                        logger.info("Discord message sent")
                        return True
                    else:
                        body = await resp.text()
                        logger.warning("Discord send failed (%d): %s", resp.status, body[:200])
                        return False
        except Exception as e:
            logger.error("Discord error: %s", e)
            return False

    async def send_signal(self, signal) -> bool:
        """Send a single signal notification with cooldown."""
        key = signal.symbol
        import time
        now = time.time()
        last = self._last_send.get(key, 0)
        if now - last < NotifierConfig.NOTIFY_COOLDOWN_SEC:
            return False

        payload = format_signal_discord(signal)
        ok = await self.send_embed(payload)
        if ok:
            self._last_send[key] = now
        return ok

    async def send_scan_summary(self, signals: list, scan_time: datetime) -> bool:
        """Send scan summary."""
        if not signals:
            return False
        payload = format_scan_summary_discord(signals, scan_time)
        return await self.send_embed(payload)


# ──────────────────────────────────────────────
# Unified Notifier
# ──────────────────────────────────────────────
class UnifiedNotifier:
    """
    Unified notification manager that sends to all configured channels.

    Usage:
        notifier = UnifiedNotifier()
        await notifier.notify_signals(signals, scan_time)
    """

    def __init__(self):
        self.telegram = TelegramNotifier()
        self.discord = DiscordNotifier()

    @property
    def any_configured(self) -> bool:
        return self.telegram.is_configured or self.discord.is_configured

    @property
    def status(self) -> dict:
        return {
            "telegram": {
                "configured": self.telegram.is_configured,
                "chat_id": self.telegram.chat_id[:4] + "..." if self.telegram.chat_id else "",
            },
            "discord": {
                "configured": self.discord.is_configured,
            },
        }

    async def notify_signals(
        self, signals: list, scan_time: datetime,
        min_score: float = None, send_summary: bool = True
    ) -> dict:
        """
        Send notifications for qualifying signals.

        Returns dict with send results.
        """
        min_score = min_score or NotifierConfig.NOTIFY_MIN_SCORE
        qualifying = [s for s in signals if s.score >= min_score]
        qualifying.sort(key=lambda s: s.score, reverse=True)

        results = {"telegram": [], "discord": [], "total_sent": 0}

        if not qualifying:
            return results

        # Send individual signals (top N)
        for signal in qualifying[:NotifierConfig.NOTIFY_MAX_PER_SCAN]:
            if self.telegram.is_configured:
                ok = await self.telegram.send_signal(signal)
                results["telegram"].append({"symbol": signal.symbol, "sent": ok})
                if ok:
                    results["total_sent"] += 1

            if self.discord.is_configured:
                ok = await self.discord.send_signal(signal)
                results["discord"].append({"symbol": signal.symbol, "sent": ok})
                if ok:
                    results["total_sent"] += 1

            # Brief delay between messages to avoid rate limits
            await asyncio.sleep(0.5)

        # Send summary
        if send_summary and len(qualifying) > 1:
            if self.telegram.is_configured:
                await self.telegram.send_scan_summary(qualifying, scan_time)
            if self.discord.is_configured:
                await self.discord.send_scan_summary(qualifying, scan_time)

        return results

    async def send_test(self) -> dict:
        """Send test message to all configured channels."""
        results = {}
        test_text = "🧪 *Test Notification*\n\nCrypto Scanner is connected\\!"

        if self.telegram.is_configured:
            ok = await self.telegram.send_message(test_text)
            results["telegram"] = "success" if ok else "failed"

        if self.discord.is_configured:
            payload = {
                "embeds": [{
                    "title": "🧪 Test Notification",
                    "description": "Crypto Scanner is connected!",
                    "color": 0x00E676,
                }]
            }
            ok = await self.discord.send_embed(payload)
            results["discord"] = "success" if ok else "failed"

        return results
