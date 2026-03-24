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
