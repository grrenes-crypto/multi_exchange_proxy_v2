from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# 🔗 API-Links der Exchanges (öffentliche Endpunkte)
API_URLS = {
    "bybit": "https://api.bybit.com/v5/market/tickers?category=linear&symbol=",
    "binance": "https://api.binance.com/api/v3/ticker/24hr?symbol=",
    "okx": "https://www.okx.com/api/v5/market/ticker?instId=",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=",
    "bitget": "https://api.bitget.com/api/v2/market/ticker?symbol=",
    "mexc": "https://api.mexc.com/api/v3/ticker/24hr?symbol=",
    "coinbase": "https://api.exchange.coinbase.com/products/"
}

# ✅ Startseite zeigt Status-Info
@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "✅ Multi Exchange Proxy läuft. Verwende /api/v1/liquidations?exchange=binance&symbol=BTCUSDT",
        "supported_exchanges": list(API_URLS.keys())
    })

# 🧩 API-Endpunkt für Kursabfragen
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
            "exchange": exchange,
            "symbol": symbol,
            "data": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
