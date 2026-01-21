# -------------------------------------------------------------
# ✅ Multi Exchange Proxy v2.1.0 – SWINKINGKILLER Integration
# -------------------------------------------------------------
# Author: René
# Build: Stable | Last Update: 2026-01-22
# Compatible: AlgoSync API / SWINKINGKILLER V74+51
# -------------------------------------------------------------

from flask import Flask, jsonify, request
import requests
import datetime
import pytz

app = Flask(__name__)

# 🔗 Öffentliche API-Basis-URLs aller Exchanges
API_URLS = {
    "bybit": "https://api.bybit.com/v5/market/tickers?category=linear&symbol=",
    "binance": "https://api.binance.com/api/v3/ticker/24hr?symbol=",
    "okx": "https://www.okx.com/api/v5/market/ticker?instId=",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=",
    "bitget": "https://api.bitget.com/api/v2/market/ticker?symbol=",
    "mexc": "https://api.mexc.com/api/v3/ticker/24hr?symbol=",
    "coinbase": "https://api.exchange.coinbase.com/products/"
}

# 🏠 Startseite – Status & Hinweise
@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "✅ Multi Exchange Proxy v2.1 läuft.",
        "supported_exchanges": list(API_URLS.keys()),
        "usage": "/api/v1/liquidations?exchange=binance&symbol=BTCUSDT"
    })


# -------------------------------------------------------------
# 🧩 BASIS-ENDPUNKTE
# -------------------------------------------------------------

# 📈 Liquidations / Preisdaten
@app.route('/api/v1/liquidations', methods=['GET'])
def get_market_data():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()
    if exchange not in API_URLS:
        return jsonify({"error": "Exchange not supported", "available": list(API_URLS.keys())}), 400
    try:
        response = requests.get(API_URLS[exchange] + symbol, timeout=10)
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "data": response.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 💰 Funding Rate
@app.route('/api/v1/funding', methods=['GET'])
def get_funding():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()
    urls = {
        "bybit": f"https://api.bybit.com/v5/market/funding/history?symbol={symbol}",
        "binance": f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}",
        "okx": f"https://www.okx.com/api/v5/public/funding-rate?instId={symbol}-SWAP"
    }
    if exchange not in urls:
        return jsonify({"error": "Exchange not supported"}), 400
    try:
        r = requests.get(urls[exchange], timeout=10)
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "data": r.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------------
# 🧠 ERWEITERTE ENDPOINTS (Phase 1 – 2 – 3)
# -------------------------------------------------------------

# 📊 Volume / 24h Stats
@app.route('/api/v1/volume', methods=['GET'])
def get_volume():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()
    urls = {
        "bybit": f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={symbol}",
        "binance": f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}",
        "okx": f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-SWAP",
        "kraken": f"https://api.kraken.com/0/public/Ticker?pair={symbol}",
        "bitget": f"https://api.bitget.com/api/v2/market/ticker?symbol={symbol}",
        "mexc": f"https://api.mexc.com/api/v3/ticker/24hr?symbol={symbol}",
        "coinbase": f"https://api.exchange.coinbase.com/products/{symbol}/ticker"
    }
    if exchange not in urls:
        return jsonify({"error": "Exchange not supported"}), 400
    try:
        r = requests.get(urls[exchange], timeout=10)
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "data": r.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🧭 Orderbook / Depth Data
@app.route('/api/v1/orderbook', methods=['GET'])
def get_orderbook():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()
    limit = request.args.get('limit', '50')
    urls = {
        "bybit": f"https://api.bybit.com/v5/market/orderbook?category=linear&symbol={symbol}",
        "binance": f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}",
        "okx": f"https://www.okx.com/api/v5/market/books?instId={symbol}-SWAP&sz={limit}",
        "kraken": f"https://api.kraken.com/0/public/Depth?pair={symbol}&count={limit}",
        "bitget": f"https://api.bitget.com/api/v2/market/depth?symbol={symbol}&limit={limit}",
        "mexc": f"https://api.mexc.com/api/v3/depth?symbol={symbol}&limit={limit}",
        "coinbase": f"https://api.exchange.coinbase.com/products/{symbol}/book?level=2"
    }
    if exchange not in urls:
        return jsonify({"error": "Exchange not supported"}), 400
    try:
        r = requests.get(urls[exchange], timeout=10)
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "limit": limit,
            "data": r.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 💹 Open Interest
@app.route('/api/v1/openinterest', methods=['GET'])
def get_open_interest():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()
    urls = {
        "bybit": f"https://api.bybit.com/v5/market/open-interest?symbol={symbol}&interval=1h",
        "okx": f"https://www.okx.com/api/v5/public/open-interest?instId={symbol}-SWAP",
        "binance": f"https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}"
    }
    if exchange not in urls:
        return jsonify({"error": "Exchange not supported"}), 400
    try:
        r = requests.get(urls[exchange], timeout=10)
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "data": r.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔁 Recent Trades
@app.route('/api/v1/trades', methods=['GET'])
def get_trades():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()
    limit = request.args.get('limit', '50')
    urls = {
        "bybit": f"https://api.bybit.com/v5/market/recent-trade?category=linear&symbol={symbol}",
        "binance": f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit={limit}",
        "okx": f"https://www.okx.com/api/v5/market/trades?instId={symbol}-SWAP&limit={limit}",
        "kraken": f"https://api.kraken.com/0/public/Trades?pair={symbol}",
        "bitget": f"https://api.bitget.com/api/v2/market/fills?symbol={symbol}&limit={limit}",
        "mexc": f"https://api.mexc.com/api/v3/trades?symbol={symbol}&limit={limit}",
        "coinbase": f"https://api.exchange.coinbase.com/products/{symbol}/trades"
    }
    if exchange not in urls:
        return jsonify({"error": "Exchange not supported"}), 400
    try:
        r = requests.get(urls[exchange], timeout=10)
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "data": r.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 💎 Index / Mark Price
@app.route('/api/v1/indexprice', methods=['GET'])
def get_index_price():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()
    urls = {
        "bybit": f"https://api.bybit.com/v5/market/mark-price-kline?symbol={symbol}",
        "okx": f"https://www.okx.com/api/v5/market/mark-price-candles?instId={symbol}-SWAP",
        "binance": f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
    }
    if exchange not in urls:
        return jsonify({"error": "Exchange not supported"}), 400
    try:
        r = requests.get(urls[exchange], timeout=10)
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "data": r.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🕒 Exchange-Time + EU-Zeit (Österreich)
@app.route('/api/v1/exchangetime', methods=['GET'])
def get_exchange_time():
    exchange = request.args.get('exchange', '').lower()
    urls = {
        "bybit": "https://api.bybit.com/v5/market/time",
        "binance": "https://api.binance.com/api/v3/time",
        "okx": "https://www.okx.com/api/v5/public/time",
        "kraken": "https://api.kraken.com/0/public/Time",
        "bitget": "https://api.bitget.com/api/v2/public/time",
        "mexc": "https://api.mexc.com/api/v3/time",
        "coinbase": "https://api.exchange.coinbase.com/time"
    }
    if exchange not in urls:
        return jsonify({"error": "Exchange not supported"}), 400
    try:
        r = requests.get(urls[exchange], timeout=10)
        data = r.json()
        unix_time = None
        if "serverTime" in data:
            unix_time = int(data["serverTime"]) / 1000
        elif "time" in data:
            unix_time = int(data["time"]) / 1000
        elif "data" in data and isinstance(data["data"], list) and "ts" in data["data"][0]:
            unix_time = int(data["data"][0]["ts"]) / 1000
        elif "result" in data and "unixtime" in data["result"]:
            unix_time = int(data["result"]["unixtime"])
        elif "data" in data and "serverTime" in data["data"]:
            unix_time = int(data["data"]["serverTime"]) / 1000
        elif "epoch" in data:
            unix_time = float(data["epoch"])
        if not unix_time:
            return jsonify({"error": "Unable to parse server time"}), 500
        utc_time = datetime.datetime.utcfromtimestamp(unix_time).replace(tzinfo=pytz.utc)
        vienna_tz = pytz.timezone("Europe/Vienna")
        eu_time = utc_time.astimezone(vienna_tz)
        return jsonify({
            "exchange": exchange,
            "server_utc": utc_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "server_eu": eu_time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
            "server_timestamp": unix_time,
            "proxy_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------------
# 🩺 ENV-CHECK & VERSION
# -------------------------------------------------------------
@app.route('/envcheck')
def envcheck():
    return jsonify({
        "status": "ok",
        "server": "multi-proxy-v2",
        "region": "Singapore",
        "time": datetime.datetime.utcnow().isoformat()
    })


@app.route('/version')
def version():
    return jsonify({
        "version": "2.1.0",
        "build": "Stable",
        "compatible_with": ["AlgoSync API", "SWINKINGKILLER V74+51"],
        "author": "René"
    })


# 🚀 SERVERSTART
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
