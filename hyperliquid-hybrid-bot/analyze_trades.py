#!/usr/bin/env python3
"""
トレード詳細分析スクリプト v2
==============================
- 全トレードのPnL分析
- 順張り/逆張りの推定分類（エントリー時のRSI + BB位置で判定）
- 戦略別・コイン別の損益サマリー
"""
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
from hyperliquid.info import Info
from hyperliquid.utils import constants

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

try:
    info = Info(constants.TESTNET_API_URL, skip_ws=True)
except (IndexError, KeyError):
    info = Info(constants.TESTNET_API_URL, skip_ws=True,
                spot_meta={"universe": [], "tokens": []})

addr = config["account_address"]

# ================================================================
# 1. 約定データ取得
# ================================================================
fills = info.user_fills(addr)
print(f"=== 全約定数: {len(fills)} ===\n")

# トレード（エントリー→決済）を再構成
# closedPnl != 0 の約定 = 決済約定
closed = [f for f in fills if float(f.get("closedPnl", 0)) != 0]
# closedPnl == 0 の約定 = エントリー約定
entries = [f for f in fills if float(f.get("closedPnl", 0)) == 0]

print(f"エントリー約定: {len(entries)}件")
print(f"決済約定: {len(closed)}件\n")

# ================================================================
# 2. インジケータ取得（RSI + BB）でレジーム推定
# ================================================================
def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.inf)
    return 100 - (100 / (1 + rs))

def calc_adx(df, period=14):
    """ADX計算"""
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values

    up_move = np.diff(high)
    down_move = -np.diff(low)
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr = np.maximum(
        high[1:] - low[1:],
        np.maximum(np.abs(high[1:] - close[:-1]), np.abs(low[1:] - close[:-1]))
    )

    def wilder_smooth(data, n):
        if len(data) < n:
            return np.full(len(data), np.nan)
        result = np.full(len(data), np.nan)
        result[n - 1] = np.mean(data[:n])
        for i in range(n, len(data)):
            result[i] = (result[i - 1] * (n - 1) + data[i]) / n
        return result

    atr = wilder_smooth(tr, period)
    plus_di_s = wilder_smooth(plus_dm, period)
    minus_di_s = wilder_smooth(minus_dm, period)

    plus_di = 100 * plus_di_s / np.where(atr == 0, 1, atr)
    minus_di = 100 * minus_di_s / np.where(atr == 0, 1, atr)

    di_sum = plus_di + minus_di
    dx = 100 * np.abs(plus_di - minus_di) / np.where(di_sum == 0, 1, di_sum)

    adx = wilder_smooth(dx, period)
    return adx

def get_regime_at_time(coin, ts_ms, interval="5m"):
    """特定時刻のRSI, BB位置, ADXを取得してレジーム推定"""
    try:
        interval_sec = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600}.get(interval, 300)
        end_time = int(ts_ms) + interval_sec * 1000
        start_time = end_time - 250 * interval_sec * 1000

        candles = info.candles_snapshot(coin, interval, start_time, end_time)
        if not candles or len(candles) < 50:
            return None

        df = pd.DataFrame(candles)
        df = df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})
        for col in ["open", "high", "low", "close", "volume"]:
            if col in df.columns:
                df[col] = df[col].astype(float)

        df["rsi"] = calc_rsi(df["close"], 14)
        df["bb_mid"] = df["close"].rolling(window=20).mean()
        bb_std = df["close"].rolling(window=20).std()
        df["bb_upper"] = df["bb_mid"] + (bb_std * 2.0)
        df["bb_lower"] = df["bb_mid"] - (bb_std * 2.0)

        # ADX
        adx_values = calc_adx(df, 14)
        # adxはdiffで1要素短いため、先頭にNaNを追加
        df["adx"] = np.nan
        df.iloc[1:, df.columns.get_loc("adx")] = adx_values

        last = df.iloc[-1]
        rsi = last["rsi"]
        close = last["close"]
        bb_lower = last["bb_lower"]
        bb_upper = last["bb_upper"]
        bb_mid = last["bb_mid"]
        adx = last["adx"]

        if pd.isna(rsi) or pd.isna(bb_lower) or pd.isna(adx):
            return None

        # BB位置: 0=下限, 0.5=中央, 1=上限
        bb_range = bb_upper - bb_lower
        if bb_range > 0:
            bb_position = (close - bb_lower) / bb_range
        else:
            bb_position = 0.5

        # レジーム判定
        if adx < 20:
            regime = "RANGE"
        elif adx > 25:
            regime = "TREND"
        else:
            regime = "GRAY"

        # 逆張り/順張り推定
        # RSI極端 + BB端 = 逆張りシグナルでエントリー
        if rsi <= 35 or rsi >= 65:
            if bb_position < 0.15 or bb_position > 0.85:
                strategy_type = "MeanRev"  # 逆張り
            else:
                strategy_type = "Momentum"  # 順張り
        else:
            strategy_type = "Momentum"  # 順張り

        return {
            "rsi": rsi,
            "adx": adx,
            "bb_position": bb_position,
            "regime": regime,
            "strategy_type": strategy_type,
        }
    except Exception as e:
        return None

# ================================================================
# 3. エントリーのタイムスタンプとマッチして分析
# ================================================================
print("=" * 80)
print("トレード分析中... (各トレードのインジケータを取得)")
print("=" * 80)

# エントリー約定をタイムスタンプ順に並べ、対応する決済とマッチ
# 簡易版: 全決済約定のPnLをタイムスタンプ基準でインジケータ推定

# 戦略別集計
stats = {
    "MeanRev": {"wins": 0, "losses": 0, "pnl": 0.0, "trades": []},
    "Momentum": {"wins": 0, "losses": 0, "pnl": 0.0, "trades": []},
    "Unknown": {"wins": 0, "losses": 0, "pnl": 0.0, "trades": []},
}

# コイン別集計
coin_stats = {}

# 全決済をグループ化（同じタイムスタンプ = 同じトレードの分割決済）
from collections import defaultdict
trade_groups = defaultdict(list)
for f in closed:
    t = f.get("time", 0)
    coin = f.get("coin", "")
    key = f"{t}_{coin}"
    trade_groups[key].append(f)

# 各トレードグループを分析
analyzed = 0
total_trades = len(trade_groups)

for key, group in sorted(trade_groups.items()):
    total_pnl = sum(float(f.get("closedPnl", 0)) for f in group)
    coin = group[0].get("coin", "")
    ts = group[0].get("time", 0)
    side = group[0].get("side", "")
    px = group[0].get("px", "")

    # 時刻表示
    if isinstance(ts, int):
        t_str = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
    else:
        t_str = str(ts)

    # インジケータ取得（API負荷軽減のため、サンプリング）
    interval = "15m" if coin != "BTC" else "5m"
    regime_info = get_regime_at_time(coin, ts, interval)

    if regime_info:
        stype = regime_info["strategy_type"]
        regime = regime_info["regime"]
        rsi = regime_info["rsi"]
        adx = regime_info["adx"]
    else:
        stype = "Unknown"
        regime = "?"
        rsi = 0
        adx = 0

    # 集計
    stats[stype]["pnl"] += total_pnl
    if total_pnl > 0:
        stats[stype]["wins"] += 1
    else:
        stats[stype]["losses"] += 1
    stats[stype]["trades"].append({
        "time": t_str, "coin": coin, "pnl": total_pnl,
        "regime": regime, "rsi": rsi, "adx": adx
    })

    # コイン別
    if coin not in coin_stats:
        coin_stats[coin] = {"wins": 0, "losses": 0, "pnl": 0.0}
    coin_stats[coin]["pnl"] += total_pnl
    if total_pnl > 0:
        coin_stats[coin]["wins"] += 1
    else:
        coin_stats[coin]["losses"] += 1

    analyzed += 1
    marker = "+" if total_pnl > 0 else "-"
    print(
        f"  [{analyzed}/{total_trades}] {t_str} {coin:<5} "
        f"PnL={total_pnl:>+8.4f} | "
        f"Type={stype:<8} Regime={regime:<5} RSI={rsi:5.1f} ADX={adx:5.1f}"
    )

    # API負荷軽減
    time.sleep(0.1)

# ================================================================
# 4. サマリー出力
# ================================================================
print("\n" + "=" * 80)
print("=== 戦略タイプ別サマリー ===")
print("=" * 80)

for stype, s in stats.items():
    total = s["wins"] + s["losses"]
    if total == 0:
        continue
    wr = s["wins"] / total * 100
    avg_pnl = s["pnl"] / total

    # 平均利益と平均損失を計算
    win_pnls = [t["pnl"] for t in s["trades"] if t["pnl"] > 0]
    loss_pnls = [t["pnl"] for t in s["trades"] if t["pnl"] <= 0]
    avg_win = sum(win_pnls) / len(win_pnls) if win_pnls else 0
    avg_loss = sum(loss_pnls) / len(loss_pnls) if loss_pnls else 0

    label = {"MeanRev": "逆張り", "Momentum": "順張り", "Unknown": "不明"}.get(stype, stype)
    print(f"\n  [{label}] ({stype})")
    print(f"    トレード数: {total}回 (勝ち{s['wins']} / 負け{s['losses']})")
    print(f"    勝率: {wr:.1f}%")
    print(f"    合計PnL: ${s['pnl']:+.4f}")
    print(f"    平均PnL: ${avg_pnl:+.4f}")
    print(f"    平均利益: ${avg_win:+.4f} / 平均損失: ${avg_loss:+.4f}")
    if avg_loss != 0:
        print(f"    リスクリワード比: 1:{abs(avg_win/avg_loss):.2f}")

print("\n" + "=" * 80)
print("=== コイン別サマリー ===")
print("=" * 80)

for coin, s in sorted(coin_stats.items()):
    total = s["wins"] + s["losses"]
    wr = s["wins"] / total * 100 if total > 0 else 0
    print(f"  {coin:<6}: PnL=${s['pnl']:>+10.4f} | {total}回 (勝{s['wins']}/負{s['losses']}) | 勝率{wr:.0f}%")

# 全体
all_pnl = sum(s["pnl"] for s in stats.values())
all_wins = sum(s["wins"] for s in stats.values())
all_losses = sum(s["losses"] for s in stats.values())
all_total = all_wins + all_losses
print(f"\n  {'全体':<6}: PnL=${all_pnl:>+10.4f} | {all_total}回 (勝{all_wins}/負{all_losses}) | 勝率{all_wins/all_total*100:.0f}%" if all_total > 0 else "")

# 残高
user_state = info.user_state(addr)
equity = float(user_state.get("marginSummary", {}).get("accountValue", 0))
print(f"\n=== アカウント残高: ${equity:,.2f} ===")
