#!/usr/bin/env python3
"""
=============================================================================
Hyperliquid 時間軸＋戦略完全分散型ハイブリッドBOT
=============================================================================
パターン3: 上級者時間軸＋戦略分散型

BTCで2つの時間軸スキャル、アルトで2つの時間軸ブレイクを同時稼働。
「BTCで細かく確実に取り、アルトで一撃を狙う」ハイブリッド構成。

稼働戦略:
  1. BTC_1m_UltraScalp    - 1分足 FVG + Order Block スキャルピング (10x)
  2. BTC_5m_MomentumRetrace - 5分足 RSI + MACD モメンタムリトレース (8x)
  3. Alts_15m_Break × N銘柄 - 15分足 レンジブレイク (15x)
  4. Alts_1H_Break × N銘柄  - 1時間足 レンジブレイク (12x)

=============================================================================
■ Testnetモード切り替え方法
=============================================================================
config.json の "network" を変更するだけ:
  - メインネット: "network": "MAINNET"
  - テストネット: "network": "TESTNET"

Testnet用ウォレット:
  1. https://app.hyperliquid-testnet.xyz でテスト用ウォレットを作成
  2. Faucetでテスト用USDCを取得
  3. config.json に Testnet用の秘密鍵とアドレスを設定

=============================================================================
■ VPSでのDocker運用推奨コマンド
=============================================================================
# 1. Dockerfileを作成（プロジェクトルートに配置）
#    FROM python:3.11-slim
#    WORKDIR /app
#    COPY requirements.txt .
#    RUN pip install --no-cache-dir -r requirements.txt
#    COPY . .
#    CMD ["python", "main.py"]

# 2. docker-compose.yml を作成
#    version: '3.8'
#    services:
#      hybrid-bot:
#        build: .
#        container_name: hl-hybrid-bot
#        restart: unless-stopped
#        volumes:
#          - ./config.json:/app/config.json:ro
#          - ./logs:/app/logs
#        environment:
#          - TZ=Asia/Tokyo
#        logging:
#          driver: json-file
#          options:
#            max-size: "10m"
#            max-file: "3"

# 3. ビルド & 起動
#    docker-compose up -d --build

# 4. ログ確認
#    docker-compose logs -f hybrid-bot

# 5. 停止
#    docker-compose down

# 6. VPS推奨スペック: 2vCPU / 4GB RAM / SSD 20GB以上
#    推奨OS: Ubuntu 22.04 LTS
=============================================================================
"""

import json
import sys
import os
import signal
import time
import logging
import threading
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta

# Hyperliquid SDK
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from hyperliquid.utils.types import Meta

# 自作モジュール
from utils.risk_manager import RiskManager
from utils.telegram_alert import TelegramAlert
from strategies.btc_1m_fvg import BTC1mFVGStrategy
from strategies.btc_5m_momentum import BTC5mMomentumStrategy
from strategies.alts_15m_break import Alts15mBreakStrategy
from strategies.alts_1h_break import Alts1hBreakStrategy


def setup_logging(config: dict):
    """
    ログ設定: コンソール + ファイル（日次ローテーション）
    """
    log_cfg = config.get("logging", {})
    log_level = getattr(logging, log_cfg.get("level", "INFO").upper(), logging.INFO)
    log_dir = log_cfg.get("log_dir", "logs")

    # ログディレクトリ作成
    os.makedirs(log_dir, exist_ok=True)

    # ルートロガー設定
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # フォーマッター
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # コンソールハンドラー
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # ファイルハンドラー（日次ローテーション）
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "hybrid_bot.log"),
        when="midnight",
        interval=1,
        backupCount=log_cfg.get("backup_count", 30),
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"
    root_logger.addHandler(file_handler)

    logger = logging.getLogger(__name__)
    logger.info("ログ設定完了")
    return logger


def load_config(config_path: str = "config.json") -> dict:
    """config.jsonを読み込む"""
    if not os.path.exists(config_path):
        print(f"エラー: {config_path} が見つかりません。")
        print("config.json.example をコピーして config.json を作成してください。")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def init_hyperliquid(config: dict):
    """
    Hyperliquid SDK を初期化。
    MAINNET / TESTNET の切り替えに対応。

    Returns:
        (info, exchange) タプル
    """
    network = config.get("network", "MAINNET").upper()
    api_secret = config["api_secret"]
    account_address = config["account_address"]

    if network == "TESTNET":
        base_url = constants.TESTNET_API_URL
        logger.info("=== TESTNET モードで起動 ===")
    else:
        base_url = constants.MAINNET_API_URL
        logger.info("=== MAINNET モードで起動 ===")

    # Info: マーケットデータ取得用（認証不要）
    # SDK v0.22+ ではテストネットの spot_meta が空で IndexError になるため
    # 先に spot_meta を取得し、空なら空データを渡してスキップ
    try:
        info = Info(base_url, skip_ws=True)
    except (IndexError, KeyError):
        logger.warning("spot_meta取得失敗 - perps専用モードで初期化")
        empty_spot = {"universe": [], "tokens": []}
        info = Info(base_url, skip_ws=True, spot_meta=empty_spot)

    # Exchange: 注文実行用（秘密鍵で認証）
    exchange = Exchange(
        wallet=None,  # 直接秘密鍵を使う場合
        base_url=base_url,
        account_address=account_address
    )
    # SDK の setup パターンに合わせて秘密鍵をセット
    # 注意: SDK バージョンにより初期化方法が異なる場合あり
    # example_utils.setup() 相当の処理
    from eth_account import Account
    wallet = Account.from_key(api_secret)
    exchange = Exchange(wallet, base_url, account_address=account_address)

    logger.info(f"Hyperliquid SDK初期化完了 (network={network})")
    logger.info(f"アカウント: {account_address}")

    return info, exchange


# グローバル変数（シグナルハンドラー用）
logger = logging.getLogger(__name__)
all_strategies = []
shutdown_event = threading.Event()


def signal_handler(signum, frame):
    """Ctrl+C / SIGTERM でグレースフル停止"""
    logger.info("停止シグナル受信。全戦略を停止中...")
    shutdown_event.set()
    for strategy in all_strategies:
        strategy.stop()


def daily_reset_worker(risk_manager: RiskManager, telegram: TelegramAlert):
    """
    日次リセットワーカー。
    毎日0時（UTC）にリスクマネージャーをリセットし、日次P&Lレポートを送信。
    """
    while not shutdown_event.is_set():
        now = datetime.utcnow()
        # 次の0時までの秒数を計算
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (tomorrow - now).total_seconds()

        # 待機（シャットダウンイベントで中断可能）
        if shutdown_event.wait(timeout=wait_seconds):
            break

        # 日次P&Lレポート送信
        status = risk_manager.get_status()
        telegram.notify_daily_pnl(
            start_equity=status["daily_start_equity"] or 0,
            current_equity=status["total_equity"],
            positions_count=status["active_positions"]
        )

        # リセット
        risk_manager.reset_daily()
        logger.info("[DailyReset] 日次リセット完了")


def main():
    """メインエントリーポイント"""
    global logger, all_strategies

    # 設定読み込み
    config = load_config()

    # ログ設定
    logger = setup_logging(config)
    logger.info("=" * 60)
    logger.info("Hyperliquid ハイブリッドBOT 起動")
    logger.info("パターン3: 時間軸＋戦略完全分散型")
    logger.info("=" * 60)

    # Hyperliquid SDK初期化
    info, exchange = init_hyperliquid(config)

    # 共通モジュール初期化
    risk_manager = RiskManager(info, config)
    telegram = TelegramAlert(config)

    # 起動通知
    telegram.notify_system("ハイブリッドBOT起動")

    # シグナルハンドラー登録
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # ===========================================
    # 戦略インスタンス作成
    # ===========================================
    threads = []

    # 1. BTC_1m_UltraScalp
    if config["btc_1m_fvg"].get("enabled", True):
        btc_1m = BTC1mFVGStrategy(info, exchange, config, risk_manager, telegram)
        all_strategies.append(btc_1m)
        t = threading.Thread(
            target=btc_1m.run,
            name="BTC_1m_FVG",
            daemon=True
        )
        threads.append(t)
        logger.info("[Main] BTC_1m_UltraScalp 戦略を登録")

    # 2. BTC_5m_MomentumRetrace
    if config["btc_5m_momentum"].get("enabled", True):
        btc_5m = BTC5mMomentumStrategy(info, exchange, config, risk_manager, telegram)
        all_strategies.append(btc_5m)
        t = threading.Thread(
            target=btc_5m.run,
            name="BTC_5m_Momentum",
            daemon=True
        )
        threads.append(t)
        logger.info("[Main] BTC_5m_MomentumRetrace 戦略を登録")

    # 3. Alts_15m_Break × N銘柄
    if config["alts_15m_break"].get("enabled", True):
        for coin in config["alts_15m_break"]["coins"]:
            strat = Alts15mBreakStrategy(
                info, exchange, config, risk_manager, telegram, coin
            )
            all_strategies.append(strat)
            t = threading.Thread(
                target=strat.run,
                name=f"Alts_15m_{coin}",
                daemon=True
            )
            threads.append(t)
            logger.info(f"[Main] Alts_15m_Break_{coin} 戦略を登録")

    # 4. Alts_1H_Break × N銘柄
    if config["alts_1h_break"].get("enabled", True):
        for coin in config["alts_1h_break"]["coins"]:
            strat = Alts1hBreakStrategy(
                info, exchange, config, risk_manager, telegram, coin
            )
            all_strategies.append(strat)
            t = threading.Thread(
                target=strat.run,
                name=f"Alts_1H_{coin}",
                daemon=True
            )
            threads.append(t)
            logger.info(f"[Main] Alts_1H_Break_{coin} 戦略を登録")

    # 日次リセットワーカー
    daily_thread = threading.Thread(
        target=daily_reset_worker,
        args=(risk_manager, telegram),
        name="DailyReset",
        daemon=True
    )
    threads.append(daily_thread)

    # ===========================================
    # 全スレッド開始
    # ===========================================
    logger.info(f"[Main] 合計 {len(threads)} スレッドを起動")
    for t in threads:
        t.start()
        logger.info(f"[Main] スレッド起動: {t.name}")
        time.sleep(0.5)  # API負荷分散のため少し間隔を空ける

    # ステータス表示ループ
    logger.info("[Main] 全戦略稼働中。Ctrl+C で停止。")
    telegram.notify_system(
        f"全{len(all_strategies)}戦略が稼働開始しました。\n"
        f"BTC戦略: 1m FVG + 5m Momentum\n"
        f"アルト戦略: 15m Break({', '.join(config['alts_15m_break']['coins'])}) "
        f"+ 1H Break({', '.join(config['alts_1h_break']['coins'])})"
    )

    try:
        while not shutdown_event.is_set():
            # 60秒ごとにステータスログ出力
            shutdown_event.wait(timeout=60)
            if not shutdown_event.is_set():
                status = risk_manager.get_status()
                logger.info(
                    f"[Status] 資産=${status['total_equity']:,.2f} | "
                    f"DD={status['daily_dd_pct']:.2f}% | "
                    f"露出={status['total_exposure_pct']:.2f}% | "
                    f"ポジ={status['active_positions']} | "
                    f"DD停止={'YES' if status['is_daily_stopped'] else 'NO'} | "
                    f"アルト停止={'YES' if status['is_alts_paused'] else 'NO'}"
                )
    except KeyboardInterrupt:
        pass

    # グレースフル停止
    logger.info("[Main] 停止処理開始...")
    shutdown_event.set()
    for strategy in all_strategies:
        strategy.stop()

    # スレッド終了待ち（最大30秒）
    for t in threads:
        t.join(timeout=30)

    telegram.notify_system("ハイブリッドBOT停止")
    logger.info("[Main] ハイブリッドBOT正常終了")


if __name__ == "__main__":
    main()
