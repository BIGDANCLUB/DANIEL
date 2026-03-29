#!/usr/bin/env python3
"""
トレード分析スクリプト
=====================
逆張り/順張りどちらで損失が出ているかを分析する。
ローカルで実行: python analyze_trades.py
"""
import json
from hyperliquid.info import Info
from hyperliquid.utils import constants

with open("config.json") as f:
    config = json.load(f)

info = Info(constants.TESTNET_API_URL, skip_ws=True)
addr = config["account_address"]

fills = info.user_fills(addr)
print(f"=== 全約定数: {len(fills)} ===\n")

# 直近50件の決済(closedPnl != 0)を分析
closed = [f for f in fills if float(f.get("closedPnl", 0)) != 0]
print(f"決済済み: {len(closed)}件\n")

total_pnl = 0
wins = 0
losses = 0

print(f"{'時刻':<22} {'コイン':<6} {'方向':<6} {'PnL':>12} {'価格':>12}")
print("-" * 65)

for f in closed[-30:]:  # 直近30件
    pnl = float(f.get("closedPnl", 0))
    total_pnl += pnl
    if pnl > 0:
        wins += 1
    else:
        losses += 1

    t = f.get("time", "")
    if isinstance(t, int):
        from datetime import datetime
        t = datetime.fromtimestamp(t / 1000).strftime("%Y-%m-%d %H:%M:%S")

    coin = f.get("coin", "")
    side = f.get("side", "")
    px = f.get("px", "")
    marker = "✅" if pnl > 0 else "❌"
    print(f"{t:<22} {coin:<6} {side:<6} {pnl:>+12.4f} {px:>12} {marker}")

print("-" * 65)
print(f"合計PnL: ${total_pnl:+.4f}")
print(f"勝ち: {wins}回, 負け: {losses}回, 勝率: {wins/(wins+losses)*100:.1f}%" if wins+losses > 0 else "")

# 現在のポジション
positions = info.user_state(addr).get("assetPositions", [])
print(f"\n=== 現在のポジション ===")
for p in positions:
    pos = p.get("position", {})
    if float(pos.get("szi", 0)) != 0:
        coin = pos.get("coin", "")
        szi = float(pos.get("szi", 0))
        entry = pos.get("entryPx", "")
        upnl = float(pos.get("unrealizedPnl", 0))
        lev = pos.get("leverage", {}).get("value", "")
        direction = "LONG" if szi > 0 else "SHORT"
        print(f"  {coin}: {direction} size={abs(szi)} entry={entry} uPnL=${upnl:+.4f} lev={lev}x")

if not any(float(p.get("position", {}).get("szi", 0)) != 0 for p in positions):
    print("  ポジションなし")

# アカウント残高
user_state = info.user_state(addr)
equity = float(user_state.get("marginSummary", {}).get("accountValue", 0))
print(f"\n=== アカウント残高: ${equity:,.2f} ===")
