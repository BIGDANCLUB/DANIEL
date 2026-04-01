#!/usr/bin/env python3
"""user_stateのレスポンス構造を確認するデバッグスクリプト"""
import json
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
user_state = info.user_state(addr)

print("=== user_state full response ===")
print(json.dumps(user_state, indent=2, default=str))
