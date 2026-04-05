#!/usr/bin/env python3
"""user_stateの全エンドポイントを試すデバッグスクリプト"""
import json
import requests
from hyperliquid.utils import constants

with open("config.json", encoding="utf-8") as f:
    config = json.load(f)

addr = config["account_address"]
base_url = constants.TESTNET_API_URL

print(f"=== アカウント: {addr} ===\n")

# 1. 通常の clearinghouseState
print("--- 1. clearinghouseState ---")
resp = requests.post(f"{base_url}/info", json={"type": "clearinghouseState", "user": addr})
data = resp.json()
ms = data.get("marginSummary", {})
print(f"  accountValue: {ms.get('accountValue')}")
print(f"  withdrawable: {data.get('withdrawable')}")

# 2. spotClearinghouseState (Spot残高)
print("\n--- 2. spotClearinghouseState ---")
resp = requests.post(f"{base_url}/info", json={"type": "spotClearinghouseState", "user": addr})
data2 = resp.json()
balances = data2.get("balances", [])
print(f"  balances: {json.dumps(balances, indent=4)}")

# 3. userTokenBalances (トークン残高)
print("\n--- 3. userTokenBalances ---")
try:
    resp = requests.post(f"{base_url}/info", json={"type": "userTokenBalances", "user": addr})
    data3 = resp.json()
    print(f"  response: {json.dumps(data3, indent=4)[:500]}")
except Exception as e:
    print(f"  error: {e}")

# 4. multiAccountState (マルチアカウント)
print("\n--- 4. multiAccountState ---")
try:
    resp = requests.post(f"{base_url}/info", json={"type": "multiAccountState", "user": addr})
    data4 = resp.json()
    print(f"  response: {json.dumps(data4, indent=4)[:800]}")
except Exception as e:
    print(f"  error: {e}")

# 5. portfolioState
print("\n--- 5. portfolioState ---")
try:
    resp = requests.post(f"{base_url}/info", json={"type": "portfolioState", "user": addr})
    data5 = resp.json()
    print(f"  response: {json.dumps(data5, indent=4)[:800]}")
except Exception as e:
    print(f"  error: {e}")

# 6. userFees (手数料情報にequityが含まれる場合)
print("\n--- 6. userFees ---")
try:
    resp = requests.post(f"{base_url}/info", json={"type": "userFees", "user": addr})
    data6 = resp.json()
    print(f"  response: {json.dumps(data6, indent=4)[:500]}")
except Exception as e:
    print(f"  error: {e}")
