"""
Telegram通知モジュール
======================
requestsベースの軽量Telegram通知。
- エントリー/決済通知
- リスク警告通知
- 日次P&Lレポート
- エラー通知
"""

import logging
import requests
import threading
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class TelegramAlert:
    """
    Telegram Bot APIを使った通知クラス。
    非同期送信（別スレッド）で戦略ループをブロックしない。
    """

    def __init__(self, config: dict):
        """
        Args:
            config: config.json の telegram セクション
        """
        tg_config = config.get("telegram", {})
        self.enabled = tg_config.get("enabled", False)
        self.bot_token = tg_config.get("bot_token", "")
        self.chat_id = tg_config.get("chat_id", "")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

        if self.enabled and (not self.bot_token or not self.chat_id):
            logger.warning("[Telegram] bot_token または chat_id が未設定。通知無効化。")
            self.enabled = False

    def _send_async(self, text: str):
        """別スレッドで送信（メインループをブロックしない）"""
        if not self.enabled:
            return
        t = threading.Thread(target=self._send, args=(text,), daemon=True)
        t.start()

    def _send(self, text: str):
        """実際のHTTPリクエスト送信"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code != 200:
                logger.warning(f"[Telegram] 送信失敗: {resp.status_code} {resp.text}")
        except Exception as e:
            logger.error(f"[Telegram] 送信エラー: {e}")

    def notify_entry(self, strategy: str, coin: str, side: str,
                     size: float, price: float, leverage: int):
        """エントリー通知"""
        emoji = "🟢" if side.upper() == "BUY" else "🔴"
        text = (
            f"{emoji} <b>エントリー</b>\n"
            f"戦略: {strategy}\n"
            f"銘柄: {coin}\n"
            f"方向: {side} {leverage}x\n"
            f"サイズ: {size:.6f}\n"
            f"価格: ${price:,.2f}\n"
            f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._send_async(text)

    def notify_exit(self, strategy: str, coin: str, side: str,
                    entry_price: float, exit_price: float,
                    pnl: float, pnl_pct: float):
        """決済通知"""
        emoji = "💰" if pnl >= 0 else "💸"
        text = (
            f"{emoji} <b>決済</b>\n"
            f"戦略: {strategy}\n"
            f"銘柄: {coin} ({side})\n"
            f"Entry: ${entry_price:,.2f}\n"
            f"Exit: ${exit_price:,.2f}\n"
            f"P&L: ${pnl:,.2f} ({pnl_pct:+.2f}%)\n"
            f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._send_async(text)

    def notify_risk_warning(self, message: str):
        """リスク警告通知"""
        text = (
            f"⚠️ <b>リスク警告</b>\n"
            f"{message}\n"
            f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._send_async(text)

    def notify_daily_pnl(self, start_equity: float, current_equity: float,
                         positions_count: int, trades_today: int = 0):
        """日次P&Lレポート"""
        pnl = current_equity - start_equity
        pnl_pct = (pnl / start_equity * 100) if start_equity > 0 else 0
        emoji = "📈" if pnl >= 0 else "📉"
        text = (
            f"{emoji} <b>日次P&Lレポート</b>\n"
            f"開始資産: ${start_equity:,.2f}\n"
            f"現在資産: ${current_equity:,.2f}\n"
            f"日次P&L: ${pnl:,.2f} ({pnl_pct:+.2f}%)\n"
            f"アクティブポジション: {positions_count}\n"
            f"本日トレード数: {trades_today}\n"
            f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._send_async(text)

    def notify_system(self, message: str):
        """システム通知（起動/停止/エラー等）"""
        text = (
            f"🤖 <b>システム通知</b>\n"
            f"{message}\n"
            f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._send_async(text)

    def notify_alts_pause(self, btc_change_pct: float):
        """BTC急落によるアルト停止通知"""
        text = (
            f"🛑 <b>アルト戦略停止</b>\n"
            f"BTC 15分変動: {btc_change_pct:+.2f}%\n"
            f"全アルト戦略を一時停止しました。\n"
            f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._send_async(text)

    def notify_alts_resume(self):
        """アルト戦略再開通知"""
        text = (
            f"✅ <b>アルト戦略再開</b>\n"
            f"BTC価格回復を確認。アルト戦略を再開します。\n"
            f"時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self._send_async(text)
