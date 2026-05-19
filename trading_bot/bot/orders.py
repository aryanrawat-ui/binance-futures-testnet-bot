from __future__ import annotations

from .client import BinanceClient
from .logging_config import setup_logger

logger = setup_logger("trading_bot.orders")


def _base_params(symbol: str, side: str, quantity: float) -> dict:
    return {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "quantity": quantity,
    }


def place_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
) -> dict:

    params = _base_params(symbol, side, quantity)

    params["type"] = "MARKET"

    logger.debug("Market order params: %s", params)

    return client.place_order(**params)


def place_limit_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:

    params = _base_params(symbol, side, quantity)

    params["type"] = "LIMIT"
    params["price"] = price
    params["timeInForce"] = time_in_force

    logger.debug("Limit order params: %s", params)

    return client.place_order(**params)


def place_stop_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: float,
    stop_price: float,
) -> dict:

    params = _base_params(symbol, side, quantity)

    params["type"] = "STOP_MARKET"
    params["stopPrice"] = stop_price

    logger.debug("Stop-market order params: %s", params)

    return client.place_order(**params)


def format_order_response(response: dict) -> str:

    lines = [
        "",
        "─" * 50,
        "  ORDER CONFIRMATION",
        "─" * 50,
        f"  Order ID   : {response.get('orderId', 'N/A')}",
        f"  Symbol     : {response.get('symbol', 'N/A')}",
        f"  Side       : {response.get('side', 'N/A')}",
        f"  Type       : {response.get('type', 'N/A')}",
        f"  Status     : {response.get('status', 'N/A')}",
        f"  Qty        : {response.get('origQty', 'N/A')}",
        f"  Exec Qty   : {response.get('executedQty', 'N/A')}",
        f"  Avg Price  : {response.get('avgPrice', 'N/A')}",
        f"  Price      : {response.get('price', 'N/A')}",
        f"  Time       : {response.get('updateTime', 'N/A')}",
        "─" * 50,
    ]

    return "\n".join(lines)