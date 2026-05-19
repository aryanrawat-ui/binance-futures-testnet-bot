from __future__ import annotations
import hashlib
import hmac
import time
from typing import Any
from urllib.parse import urlencode
import requests

from .logging_config import setup_logger

BASE_URL = "https://testnet.binancefuture.com"

logger = setup_logger("trading_bot.client")

class BinanceAPIError(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"Binance API Error {code}: {message}")

class BinanceClient:
    def __init__(self, api_key: str, api_secret: str, timeout: int = 10) -> None:
        if not api_key or not api_secret:
            raise ValueError("api_key and api_secret must not be empty.")
        self._api_key = api_key
        self._api_secret = api_secret
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"X-MBX-APIKEY": self._api_key})
        logger.debug("BinanceClient initialised (testnet)")

    def _sign(self, params: dict) -> dict:
        """Append a HMAC-SHA256 signature to the params dict."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        signed: bool = False,
    ) -> Any:
        url = f"{BASE_URL}{endpoint}"
        params = params or {}

        if signed:
            params = self._sign(params)
        logger.debug("→ %s %s | params=%s", method.upper(), endpoint, params)

        try:
            response = self._session.request(
                method,
                url,
                params=params if method.upper() == "GET" else None,
                data=params if method.upper() == "POST" else None,
                timeout=self._timeout,
            )
        except requests.exceptions.ConnectionError as exc:
            logger.error("Network error: %s", exc)
            raise ConnectionError(
                f"Could not reach Binance testnet ({BASE_URL}). "
                "Check your internet connection."
            ) from exc
        except requests.exceptions.Timeout as exc:
            logger.error("Request timed out after %ds", self._timeout)
            raise TimeoutError(
                f"Request timed out after {self._timeout}s."
            ) from exc

        logger.debug("← HTTP %s | body=%s", response.status_code, response.text[:500])

        data = response.json()

        if not response.ok:
            code = data.get("code", response.status_code)
            msg = data.get("msg", response.text)
            logger.error("API error %s: %s", code, msg)
            raise BinanceAPIError(code, msg)

        return data

    def ping(self) -> bool:
        """Returns True if the testnet is reachable."""
        try:
            self._request("GET", "/fapi/v1/ping")
            logger.info("Testnet ping: OK")
            return True
        except Exception as exc:
            logger.warning("Testnet ping failed: %s", exc)
            return False

    def get_exchange_info(self) -> dict:
        return self._request("GET", "/fapi/v1/exchangeInfo")

    def get_account_balance(self) -> list[dict]:
        return self._request("GET", "/fapi/v2/balance", signed=True)

    def place_order(self, **order_params) -> dict:
        logger.info(
            "Placing order: %s",
            {k: v for k, v in order_params.items() if k != "signature"},
        )
        result = self._request("POST", "/fapi/v1/order", params=order_params, signed=True)
        logger.info("Order placed successfully: orderId=%s status=%s", result.get("orderId"), result.get("status"))
        return result