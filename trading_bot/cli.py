from __future__ import annotations
import argparse
import os
import sys
from dotenv import load_dotenv
from bot.client import BinanceAPIError, BinanceClient
from bot.logging_config import setup_logger
from bot.orders import (
    format_order_response,
    place_limit_order,
    place_market_order,
    place_stop_market_order,
)
from bot.validators import (
    cross_validate,
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

load_dotenv()

logger = setup_logger("trading_bot.cli")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot",
    )
    parser.add_argument(
        "--symbol",
        required=True,
        type=validate_symbol,
    )
    parser.add_argument(
        "--side",
        required=True,
        type=validate_side,
    )
    parser.add_argument(
        "--type",
        dest="order_type",
        required=True,
        type=validate_order_type,
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=validate_quantity,
    )
    parser.add_argument(
        "--price",
        type=validate_price,
        default=None,
    )
    parser.add_argument(
        "--stop-price",
        dest="stop_price",
        type=validate_stop_price,
        default=None,
    )
    parser.add_argument(
        "--tif",
        dest="time_in_force",
        default="GTC",
        choices=["GTC", "IOC", "FOK"],
    )
    return parser

def print_summary(args: argparse.Namespace) -> None:
    print("\n" + "=" * 50)
    print("ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"Symbol      : {args.symbol}")
    print(f"Side        : {args.side}")
    print(f"Type        : {args.order_type}")
    print(f"Quantity    : {args.quantity}")
    if args.price:
        print(f"Price       : {args.price}")
    if args.stop_price:
        print(f"Stop Price  : {args.stop_price}")
    print("=" * 50)

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        cross_validate(args)
    except argparse.ArgumentError as exc:
        parser.error(str(exc))

    print_summary(args)

    logger.info(
        "Request: symbol=%s side=%s type=%s qty=%s",
        args.symbol,
        args.side,
        args.order_type,
        args.quantity,
    )

    api_key = os.getenv("BINANCE_API_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET", "")

    if not api_key or not api_secret:
        print("\nMissing API credentials.\n")
        logger.error("Missing API credentials")
        sys.exit(1)

    client = BinanceClient(api_key, api_secret)
    try:
        if args.order_type == "MARKET":
            response = place_market_order(
                client,
                args.symbol,
                args.side,
                args.quantity,
            )

        elif args.order_type == "LIMIT":
            response = place_limit_order(
                client,
                args.symbol,
                args.side,
                args.quantity,
                args.price,
                args.time_in_force,
            )

        elif args.order_type == "STOP_MARKET":
            response = place_stop_market_order(
                client,
                args.symbol,
                args.side,
                args.quantity,
                args.stop_price,
            )

        else:
            raise ValueError(
                f"Unsupported order type: {args.order_type}"
            )

        print(format_order_response(response))
        print("\nOrder placed successfully!\n")
        logger.info(
            "Order completed. orderId=%s",
            response.get("orderId")
        )
    except BinanceAPIError as exc:
        print(f"\nBinance API Error: {exc.message}\n")
        logger.error(
            "Binance API error: %s",
            exc.message
        )
    except Exception as exc:
        print(f"\nUnexpected Error: {exc}\n")
        logger.exception("Unexpected error")
if __name__ == "__main__":
    main()
