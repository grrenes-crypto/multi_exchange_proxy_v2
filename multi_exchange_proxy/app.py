from flask import Flask, jsonify, request
import requests
import datetime

app = Flask(__name__)

# 🔗 Öffentliche API-Endpunkte der Exchanges
API_URLS = {
    "bybit": "https://api.bybit.com/v5/market/tickers?category=linear&symbol=",
    "binance": "https://api.binance.com/api/v3/ticker/24hr?symbol=",
    "okx": "https://www.okx.com/api/v5/market/ticker?instId=",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=",
    "bitget": "https://api.bitget.com/api/v2/market/ticker?symbol=",
    "mexc": "https://api.mexc.com/api/v3/ticker/24hr?symbol=",
    "coinbase": "https://api.exchange.coinbase.com/products/"
}

# ✅ Startseite – zeigt Status und verfügbare Exchanges
@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "✅ Multi Exchange Proxy v2 läuft.",
        "supported_exchanges": list(API_URLS.keys()),
        "usage": "/api/v1/liquidations?exchange=binance&symbol=BTCUSDT"
    })

# 🧩 Haupt-Endpunkt – holt Marktdaten von der gewählten Exchange
@app.route('/api/v1/liquidations', methods=['GET'])
def get_market_data():
    exchange = request.args.get('exchange', '').lower()
    symbol = request.args.get('symbol', '').upper()

    if exchange not in API_URLS:
        return jsonify({
            "error": "Exchange not supported.",
            "available": list(API_URLS.keys())
        }), 400

    url = API_URLS[exchange] + symbol

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return jsonify({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "exchange": exchange,
            "symbol": symbol,
            "data": data
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "exchange": exchange,
            "symbol": symbol
        }), 500

# 🧭 Healthcheck – Systemstatus für AlgoSync / SWINKINGKILLER
@app.route('/envcheck')
def envcheck():
    return jsonify({
        "status": "ok",
        "server": "multi-proxy-v2",
        "region": "Singapore",
        "time": datetime.datetime.utcnow().isoformat()
    })

# 🧩 Zusatzroute – einfache Serverprüfung / Debug
@app.route('/version')
def version():
    return jsonify({
        "version": "2.0.0",
        "build": "Stable",
        "compatible_with": ["AlgoSync API", "SWINKINGKILLER V74+50"],
        "author": "René"
    })

# 🚀 Serverstart
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
