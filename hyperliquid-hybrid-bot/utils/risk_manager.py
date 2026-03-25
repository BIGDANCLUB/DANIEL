"""
共通リスク管理モジュール
========================
全戦略で共有するRiskManagerクラス。
- 総露出2%以内の監視
- 1トレードあたり0.5%以内のポジションサイジング
- 日次ドローダウン10%で全戦略停止
- BTC急落時のアルト戦略一時停止（相関監視）
- スレッドセーフな設計（threading.Lock使用）
"""

import time
import threading
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class RiskManager:
    """
    全戦略共通のリスク管理クラス。
    スレッドセーフにポジション・露出・ドローダウンを管理する。
    """

    def __init__(self, info, config: dict):
        """
        Args:
            info: Hyperliquid Info インスタンス
            config: config.json の risk セクション
        """
        self.info = info
        self.config = config
        self._lock = threading.Lock()

        # リスクパラメータ
        self.max_total_exposure_pct = config["risk"]["max_total_exposure_pct"]
        self.max_risk_per_trade_pct = config["risk"]["max_risk_per_trade_pct"]
        self.daily_dd_limit_pct = config["risk"]["daily_drawdown_limit_pct"]
        self.btc_corr_window = config["risk"]["btc_correlation_window_minutes"]
        self.btc_corr_drop = config["risk"]["btc_correlation_drop_pct"]
        self.btc_alloc_pct = config["risk"]["btc_allocation_pct"]
        self.alts_alloc_pct = config["risk"]["alts_allocation_pct"]

        # 状態管理
        self.account_address = config["account_address"]
        self.daily_start_equity: Optional[float] = None
        self.daily_pnl: float = 0.0
        self.is_daily_stopped: bool = False
        self.is_alts_paused: bool = False  # BTC相関停止フラグ

        # 各戦略のアクティブポジション追跡（strategy_name -> position_info）
        self._positions: Dict[str, dict] = {}

        # BTC価格履歴（相関監視用）
        self._btc_price_history: List[dict] = []  # [{timestamp, price}]

        # 初期化時に開始資産を記録
        self._init_daily_equity()

    def _init_daily_equity(self):
        """日次開始時の資産額を記録"""
        try:
            equity = self._get_account_equity()
            if equity and equity > 0:
                self.daily_start_equity = equity
                logger.info(f"[RiskManager] 日次開始資産: ${equity:,.2f}")
        except Exception as e:
            logger.error(f"[RiskManager] 資産取得エラー: {e}")

    def _get_account_equity(self) -> Optional[float]:
        """Hyperliquid APIからアカウント資産を取得"""
        try:
            user_state = self.info.user_state(self.account_address)
            # marginSummary.accountValue が総資産
            equity = float(user_state.get("marginSummary", {}).get("accountValue", 0))
            return equity
        except Exception as e:
            logger.error(f"[RiskManager] アカウント資産取得失敗: {e}")
            return None

    def get_total_equity(self) -> float:
        """現在の総資産を取得"""
        equity = self._get_account_equity()
        return equity if equity else 0.0

    def get_btc_allocation(self) -> float:
        """BTC戦略に割り当てられた資金額を返す"""
        return self.get_total_equity() * (self.btc_alloc_pct / 100.0)

    def get_alts_allocation(self) -> float:
        """アルト戦略に割り当てられた資金額を返す"""
        return self.get_total_equity() * (self.alts_alloc_pct / 100.0)

    def calculate_position_size(self, strategy_name: str, leverage: int,
                                entry_price: float, sl_pct: float,
                                is_btc: bool = True) -> float:
        """
        ポジションサイズを計算。
        公式: size = (総資産 × risk_per_trade%) / (エントリー価格 × SL%)

        レバレッジはマージン計算に使用。実際のサイズはリスクベースで決定。

        Args:
            strategy_name: 戦略名
            leverage: レバレッジ倍率
            entry_price: エントリー価格
            sl_pct: ストップロス幅（%）
            is_btc: BTC戦略かどうか

        Returns:
            ポジションサイズ（コントラクト数）
        """
        with self._lock:
            equity = self.get_total_equity()
            if equity <= 0:
                logger.warning(f"[RiskManager] 資産が0以下のためサイズ計算不可")
                return 0.0

            # 配分資金の取得
            allocation = self.get_btc_allocation() if is_btc else self.get_alts_allocation()

            # リスク額 = 配分資金 × 1トレードリスク%
            risk_amount = allocation * (self.max_risk_per_trade_pct / 100.0)

            # ポジションサイズ = リスク額 / (エントリー価格 × SL%)
            if sl_pct <= 0 or entry_price <= 0:
                return 0.0

            position_size = risk_amount / (entry_price * (sl_pct / 100.0))

            # 総露出チェック
            current_exposure = self._get_total_exposure_pct()
            position_value = position_size * entry_price
            new_exposure_pct = ((self._get_total_exposure_value() + position_value) / equity) * 100

            if new_exposure_pct > self.max_total_exposure_pct:
                logger.warning(
                    f"[RiskManager] {strategy_name}: 総露出{new_exposure_pct:.2f}%が"
                    f"上限{self.max_total_exposure_pct}%を超過。サイズ縮小。"
                )
                # 許容範囲に収まるようサイズを調整
                remaining_pct = max(0, self.max_total_exposure_pct - current_exposure)
                max_value = equity * (remaining_pct / 100.0)
                position_size = max_value / entry_price if entry_price > 0 else 0.0

            logger.info(
                f"[RiskManager] {strategy_name}: サイズ={position_size:.6f}, "
                f"リスク額=${risk_amount:,.2f}, レバ={leverage}x"
            )
            return position_size

    def _get_total_exposure_value(self) -> float:
        """全戦略のポジション価値合計を取得"""
        total = 0.0
        for pos in self._positions.values():
            total += abs(pos.get("notional_value", 0.0))
        return total

    def _get_total_exposure_pct(self) -> float:
        """総露出を%で返す"""
        equity = self.get_total_equity()
        if equity <= 0:
            return 0.0
        return (self._get_total_exposure_value() / equity) * 100.0

    def register_position(self, strategy_name: str, coin: str, side: str,
                          size: float, entry_price: float):
        """ポジション登録"""
        with self._lock:
            self._positions[strategy_name] = {
                "coin": coin,
                "side": side,
                "size": size,
                "entry_price": entry_price,
                "notional_value": size * entry_price,
                "timestamp": time.time()
            }
            logger.info(
                f"[RiskManager] ポジション登録: {strategy_name} "
                f"{side} {size} {coin} @ {entry_price}"
            )

    def unregister_position(self, strategy_name: str):
        """ポジション解除"""
        with self._lock:
            if strategy_name in self._positions:
                del self._positions[strategy_name]
                logger.info(f"[RiskManager] ポジション解除: {strategy_name}")

    def can_open_position(self, strategy_name: str, coin: str = None, side: str = None) -> bool:
        """
        新規ポジションを開けるかチェック。
        - 日次DD停止中でないか
        - アルト戦略の場合、BTC相関停止中でないか
        - 同一コインの逆方向ポジションが既にないか
        """
        with self._lock:
            if self.is_daily_stopped:
                logger.warning(f"[RiskManager] {strategy_name}: 日次DD制限で停止中")
                return False

            # アルト戦略のBTC相関チェック
            if "alts" in strategy_name.lower() and self.is_alts_paused:
                logger.warning(f"[RiskManager] {strategy_name}: BTC急落によりアルト戦略停止中")
                return False

            # 同一コインの既存ポジションチェック
            if coin and side:
                for name, pos in self._positions.items():
                    if name == strategy_name:
                        continue
                    if pos.get("coin") == coin:
                        existing_side = pos.get("side")
                        if existing_side != side:
                            logger.warning(
                                f"[RiskManager] {strategy_name}: {coin}に逆方向ポジション"
                                f"({name}: {existing_side})が既にあるためスキップ"
                            )
                            return False
                        else:
                            logger.info(
                                f"[RiskManager] {strategy_name}: {coin}に同方向ポジション"
                                f"({name}: {existing_side})が既にあるためスキップ"
                            )
                            return False

            return True

    def check_daily_drawdown(self) -> bool:
        """
        日次ドローダウンをチェック。
        制限超過時はTrueを返し、全戦略停止フラグを立てる。

        Returns:
            True: DD制限超過（停止すべき）
            False: 正常
        """
        with self._lock:
            if self.daily_start_equity is None or self.daily_start_equity <= 0:
                return False

            current_equity = self.get_total_equity()
            if current_equity <= 0:
                return False

            dd_pct = ((self.daily_start_equity - current_equity) / self.daily_start_equity) * 100

            if dd_pct >= self.daily_dd_limit_pct:
                self.is_daily_stopped = True
                logger.critical(
                    f"[RiskManager] 日次ドローダウン{dd_pct:.2f}%が"
                    f"制限{self.daily_dd_limit_pct}%を超過！全戦略停止！"
                )
                return True

            return False

    def update_btc_price(self, price: float):
        """
        BTC価格を記録し、急落チェックを実行。
        15分間で-2%以上の下落でアルト全停止。

        Args:
            price: 現在のBTC価格
        """
        now = time.time()
        with self._lock:
            self._btc_price_history.append({"timestamp": now, "price": price})

            # 古いデータを削除（ウィンドウ外）
            cutoff = now - (self.btc_corr_window * 60)
            self._btc_price_history = [
                p for p in self._btc_price_history
                if p["timestamp"] >= cutoff
            ]

            # 最古の価格と比較
            if len(self._btc_price_history) >= 2:
                oldest_price = self._btc_price_history[0]["price"]
                if oldest_price > 0:
                    change_pct = ((price - oldest_price) / oldest_price) * 100

                    if change_pct <= self.btc_corr_drop:
                        if not self.is_alts_paused:
                            self.is_alts_paused = True
                            logger.critical(
                                f"[RiskManager] BTC急落検知: {change_pct:.2f}%"
                                f"（{self.btc_corr_window}分間）→ アルト全戦略停止"
                            )
                    else:
                        if self.is_alts_paused:
                            self.is_alts_paused = False
                            logger.info("[RiskManager] BTC回復 → アルト戦略再開")

    def reset_daily(self):
        """日次リセット（毎日0時に呼ぶ）"""
        with self._lock:
            self.daily_start_equity = self._get_account_equity()
            self.daily_pnl = 0.0
            self.is_daily_stopped = False
            logger.info(f"[RiskManager] 日次リセット完了。開始資産: ${self.daily_start_equity:,.2f}")

    def get_status(self) -> dict:
        """現在のリスク状態をサマリーで返す"""
        with self._lock:
            equity = self.get_total_equity()
            dd_pct = 0.0
            if self.daily_start_equity and self.daily_start_equity > 0:
                dd_pct = ((self.daily_start_equity - equity) / self.daily_start_equity) * 100

            return {
                "total_equity": equity,
                "daily_start_equity": self.daily_start_equity,
                "daily_dd_pct": dd_pct,
                "total_exposure_pct": self._get_total_exposure_pct(),
                "active_positions": len(self._positions),
                "is_daily_stopped": self.is_daily_stopped,
                "is_alts_paused": self.is_alts_paused,
                "positions": dict(self._positions)
            }
