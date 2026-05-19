Binance Futures Testnet Trading Bot

This project is a simple Python CLI trading bot made for the Binance Futures Testnet (USDT-M).
It allows placing Market, Limit, and Stop-Market orders from the terminal using Binance Futures API endpoints.

The goal of this project was to understand:

how REST APIs work
how Binance order APIs work
request signing using HMAC SHA256
CLI-based automation
validation and logging in Python
Features
Place MARKET orders
Place LIMIT orders
Place STOP_MARKET orders
BUY and SELL support
Input validation using argparse
Logging to console + log file
Error handling for API/network issues
Project Structure
trading_bot/
│
├── bot/
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   ├── logging_config.py
│
├── cli.py
├── .env
├── requirements.txt
└── README.md
Setup
1. Create Binance Futures Testnet Account

Go to:

https://testnet.binancefuture.com

Generate API keys from:

Profile → API Management
2. Create Virtual Environment
python -m venv venv

Activate environment:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
3. Install Requirements
pip install -r requirements.txt
4. Add API Keys

Create .env file:

API_KEY=your_api_key
API_SECRET=your_api_secret
How to Run
MARKET Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
LIMIT Order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 100000
STOP_MARKET Order
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 50000
Logging

Logs are stored in:

logs/trading_bot.log

The logger records:

API requests
API responses
errors
exceptions
How I Explored Binance API

I explored the Binance Futures API documentation to understand:

authentication
request signing
order endpoints
required parameters for each order type

Main references used:

Binance Futures API Docs
https://binance-docs.github.io/apidocs/futures/en/
Binance Futures Testnet
https://testnet.binancefuture.com

I mainly used:

/fapi/v1/order
/fapi/v2/balance
/fapi/v1/ping

to understand order placement and account connectivity.

Assumptions
Project only works on Binance Futures Testnet
Only USDT-M futures are supported
Small quantities like 0.001 are recommended for BTC test orders
LIMIT orders may stay OPEN if market price is not reached
Challenges Faced

Some challenges while building the project:

understanding Binance request signing
handling validation for different order types
formatting CLI arguments correctly
handling API/network exceptions properly
Dependencies
requests
python-dotenv