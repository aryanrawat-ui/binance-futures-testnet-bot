from __future__ import annotations
import argparse
from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if len(s) < 3:
        raise argparse.ArgumentTypeError(
            f"Symbol '{symbol}' is too short. Use something like BTCUSDT."
        )
    return s

def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise argparse.ArgumentTypeError(
            f"Side must be one of {sorted(VALID_SIDES)}, got '{side}'."
        )
    return s

def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()

    if t not in VALID_ORDER_TYPES:
        raise argparse.ArgumentTypeError(
            f"Order type must be one of "
            f"{sorted(VALID_ORDER_TYPES)}, got '{order_type}'."
        )
    return t


def validate_quantity(qty: str) -> float:
    try:
        value = Decimal(qty)
        if value <= 0:
            raise argparse.ArgumentTypeError(
                "Quantity must be greater than 0."
            )
        return float(value)

    except InvalidOperation:
        raise argparse.ArgumentTypeError(
            f"Invalid quantity '{qty}'. "
            "Must be a positive number (e.g. 0.001)."
        )


def validate_price(price: str) -> float:
    try:
        value = Decimal(price)

        if value <= 0:
            raise argparse.ArgumentTypeError(
                "Price must be greater than 0."
            )
        return float(value)

    except InvalidOperation:
        raise argparse.ArgumentTypeError(
            f"Invalid price '{price}'. "
            "Must be a positive number (e.g. 30000)."
        )


def validate_stop_price(price: str) -> float:
    return validate_price(price)


def cross_validate(args: argparse.Namespace) -> None:

    if args.order_type == "LIMIT" and not args.price:
        raise argparse.ArgumentError(
            None,
            "A LIMIT order requires --price. "
            "Example: --price 30000"
        )

    if args.order_type == "STOP_MARKET" and not args.stop_price:
        raise argparse.ArgumentError(
            None,
            "A STOP_MARKET order requires --stop-price. "
            "Example: --stop-price 29500"
        )

    if args.order_type == "MARKET" and args.price:
        raise argparse.ArgumentError(
            None,
            "A MARKET order does not accept --price."
        )
