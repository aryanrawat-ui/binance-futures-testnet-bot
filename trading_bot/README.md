# Binance Futures Testnet Trading Bot

This project is a simple Python CLI trading bot built for the Binance Futures Testnet (USDT-M).

It supports placing:
- MARKET orders
- LIMIT orders
- STOP_MARKET orders

using Binance Futures REST API endpoints from the terminal.

The main goal of this project was to understand:
- REST APIs
- Binance Futures API structure
- request signing using HMAC SHA256
- CLI-based automation
- logging and validation in Python

---

# Features

- Place MARKET orders
- Place LIMIT orders
- Place STOP_MARKET orders
- BUY and SELL support
- Input validation using argparse
- Logging to console and log file
- Error handling for API/network issues

---

# Project Structure

```txt
trading_bot/
│
├── bot/
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── logs/
│   └── trading_bot.log
│
├── cli.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Setup

## 1. Create Binance Futures Testnet Account

Go to:

https://testnet.binancefuture.com

Generate API keys from:

Profile → API Management

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 4. Add API Keys

Create a `.env` file:

```env
API_KEY=your_api_key
API_SECRET=your_api_secret
```

---

# How to Run

## MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

## LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000
```

---

## STOP_MARKET Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 50000
```

---

# Logging

Logs are stored in:

```txt
logs/trading_bot.log
```

The logger records:
- API requests
- API responses
- errors
- exceptions

---

# How I Explored Binance API

I explored the Binance Futures API documentation to understand:
- authentication
- request signing
- order endpoints
- required parameters for different order types

Main references used:

- Binance Futures API Docs  
  https://binance-docs.github.io/apidocs/futures/en/

- Binance Futures Testnet  
  https://testnet.binancefuture.com

Main endpoints explored:
- `/fapi/v1/order`
- `/fapi/v2/balance`
- `/fapi/v1/ping`

These endpoints helped me understand:
- order placement
- connectivity testing
- account balance handling

---

# Assumptions

- Project only works on Binance Futures Testnet
- Only USDT-M futures are supported
- Small quantities like `0.001` are recommended for BTC test orders
- LIMIT orders may stay OPEN if market price is not reached

---

# Challenges Faced

Some challenges while building this project:
- understanding Binance request signing
- handling validation for multiple order types
- formatting CLI arguments correctly
- handling API/network exceptions properly

---

# Dependencies

- requests
- python-dotenv
