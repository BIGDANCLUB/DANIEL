# Hyperliquid Martingale Averaging Grid Bot

> この戦略は小さい利益を高頻度で積み重ねる「勝手にりえき」型です

Hyperliquid Perpetual DEXでBTC-USD（他ペア切替可能）のMartingale Averaging Grid戦略を自動実行するPythonボットです。

## 戦略概要

1. **初期グリッド**: Mark Priceから±N bpsにLimit Buy / Limit Sellを同時発注
2. **片方約定**: もう片方を即キャンセル → 方向性ポジション保有
3. **逆行時（Martingale）**: サイズを倍率増加して悪い価格で追加エントリー → 平均取得価格を更新
4. **利確**: 平均取得価格から+X%で全ポジション決済 → 新グリッド発注
5. **最大レベル超過**: 全決済してリセット

## フォルダ構造

```
hyperliquid-grid-bot/
├── main.py           # エントリポイント（ボットエンジン）
├── utils.py          # SDK ラッパー・ユーティリティ
├── config.yaml       # 全パラメータ設定
├── .env.example      # 環境変数テンプレート
├── .gitignore
├── requirements.txt
├── logs/             # ログ出力先
└── README.md
```

## インストール

### 1. Python環境（3.9+推奨）

```bash
cd hyperliquid-grid-bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 環境変数設定

```bash
cp .env.example .env
```

`.env`を編集:

```
ACCOUNT_ADDRESS=0xあなたのメインウォレットアドレス
SECRET_KEY=0xあなたのAPIウォレット秘密鍵
NETWORK=testnet
```

**テストネットの場合**: https://app.hyperliquid-testnet.xyz でAPIキーを生成

**メインネットの場合**: https://app.hyperliquid.xyz/API でAPIキーを生成し、`NETWORK=mainnet`に変更

### 3. config.yaml調整

デフォルト値は保守的に設定済み:
- `grid_spacing_bps: 8` (0.08%)
- `tp_percent: 0.25` (0.25%)
- `martingale_multiplier: 1.8`
- `max_levels: 4`
- `initial_size_usd: 50`
- `max_drawdown_pct: 10`

## テストネットでの起動

```bash
# .envでNETWORK=testnetを確認
python main.py
```

## メインネットでの起動

```bash
# .envでNETWORK=mainnetに変更
python main.py
```

## パラメータ説明

| パラメータ | デフォルト | 説明 |
|---|---|---|
| `symbol` | BTC | 取引ペア |
| `leverage` | 5 | レバレッジ倍率 |
| `grid_spacing_bps` | 8 | グリッド間隔 (bps) |
| `initial_size_usd` | 50 | 初期注文サイズ (USD) |
| `martingale_multiplier` | 1.8 | マーチンゲール倍率 |
| `max_levels` | 4 | 最大グリッドレベル |
| `tp_percent` | 0.25 | 利確率 (%) |
| `max_drawdown_pct` | 10 | 最大ドローダウン (%) |
| `max_position_usd` | 5000 | 最大ポジションサイズ (USD) |
| `loop_interval_sec` | 15 | ループ間隔 (秒) |

## 注意事項

- **テストネットで十分にテストしてからメインネットで使用してください**
- Martingale戦略は大きな逆行で急速に損失が拡大するリスクがあります
- `max_drawdown_pct`と`max_levels`を必ず設定してリスクを制限してください
- BOTは15秒間隔でポーリングするため、急激な価格変動には対応が遅れる場合があります
- 本ソフトウェアは教育・研究目的です。実際の取引での損失について一切責任を負いません
