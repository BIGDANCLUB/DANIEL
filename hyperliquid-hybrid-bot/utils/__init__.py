import logging

_sl_logger = logging.getLogger(__name__)


def place_exchange_sl(exchange, info, account_address: str, coin: str,
                      is_long: bool, size: float, sl_price: float,
                      strategy_name: str = "") -> int | None:
    """
    取引所にストップロス（トリガー）注文を配置する。
    ソフトウェアSLと併用して、ループ間隔中のスリッページを防ぐ。

    Returns:
        order ID (oid) or None if failed
    """
    try:
        # SL = 反対売買 + reduce_only
        is_buy = not is_long  # ロングならSellで決済、ショートならBuyで決済

        # Hyperliquid: triggerPxはfloatで、round to significant digits
        # limit_pxはmarket triggerの場合でも必要（APIの仕様上）
        sl_price_rounded = float(f"{sl_price:.6g}")

        result = exchange.order(
            name=coin,
            is_buy=is_buy,
            sz=size,
            limit_px=sl_price_rounded,
            order_type={
                "trigger": {
                    "triggerPx": sl_price_rounded,
                    "isMarket": True,
                    "tpsl": "sl"
                }
            },
            reduce_only=True
        )

        # oidを抽出
        oid = _extract_oid(result)
        if oid:
            _sl_logger.info(
                f"[{strategy_name}] 取引所SL注文配置: {coin} "
                f"{'BUY' if is_buy else 'SELL'} @ {sl_price_rounded}, oid={oid}"
            )
        else:
            _sl_logger.warning(f"[{strategy_name}] SL注文配置 - oid取得失敗: {result}")
        return oid

    except Exception as e:
        _sl_logger.error(f"[{strategy_name}] 取引所SL注文エラー: {e}")
        return None


def cancel_exchange_sl(exchange, coin: str, oid: int, strategy_name: str = ""):
    """取引所のSL注文をキャンセルする"""
    try:
        result = exchange.cancel(coin, oid)
        _sl_logger.info(f"[{strategy_name}] SL注文キャンセル: oid={oid}, 結果: {result}")
    except Exception as e:
        _sl_logger.error(f"[{strategy_name}] SLキャンセルエラー: {e}")


def update_exchange_sl(exchange, info, account_address: str, coin: str,
                       is_long: bool, size: float, new_sl_price: float,
                       old_oid: int | None, strategy_name: str = "") -> int | None:
    """既存SL注文をキャンセルして新しいSL価格で再配置する"""
    if old_oid:
        cancel_exchange_sl(exchange, coin, old_oid, strategy_name)
    return place_exchange_sl(exchange, info, account_address, coin,
                             is_long, size, new_sl_price, strategy_name)


def _extract_oid(result: dict) -> int | None:
    """注文結果からoidを抽出する"""
    try:
        if not isinstance(result, dict):
            return None
        response = result.get("response", {})
        if isinstance(response, dict):
            data = response.get("data", {})
            if isinstance(data, dict):
                statuses = data.get("statuses", [])
                for s in statuses:
                    if isinstance(s, dict):
                        if "resting" in s:
                            return s["resting"].get("oid")
                        if "filled" in s:
                            return s["filled"].get("oid")
    except Exception:
        pass
    return None


def validate_order_result(result: dict) -> tuple[bool, str]:
    """
    Hyperliquid注文結果を検証する。
    status='ok'でもstatuses内にエラーがある場合がある。

    Returns:
        (success: bool, error_msg: str)
    """
    if not isinstance(result, dict):
        return False, str(result)

    if result.get("status") != "ok":
        err = result.get("response", str(result))
        return False, str(err)

    # statuses内のエラーチェック
    response = result.get("response", {})
    if isinstance(response, dict):
        data = response.get("data", {})
        if isinstance(data, dict):
            statuses = data.get("statuses", [])
            for s in statuses:
                if isinstance(s, dict) and "error" in s:
                    return False, s["error"]

    return True, ""
