import os
import sys
from flask import Flask, render_template, jsonify
import pandas as pd
import joblib

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.binance_client import BinanceUtility
from utils.data_processor import DataProcessor

app = Flask(__name__)

# 全局变量存储模型和处理器
# Global variables for model and processor
MODELS = {}
SYMBOLS = ['BTCUSDT', 'ETHUSDT']

def load_models():
    """
    加载所有预训练好的模型
    Load all pre-trained models
    """
    for symbol in SYMBOLS:
        model_path = f'models/{symbol}_price_model.pkl'
        if os.path.exists(model_path):
            MODELS[symbol] = joblib.load(model_path)
            print(f"成功加载模型 for {symbol} / Loaded model for {symbol}")

@app.route('/')
def index():
    """
    仪表盘主页
    Dashboard Index
    """
    return """
    <html>
        <head><title>Binance Prediction</title></head>
        <body>
            <h1>币安价格预测仪表盘 / Binance Price Prediction Dashboard</h1>
            <p>可用的交易对 / Available Symbols: BTCUSDT, ETHUSDT</p>
            <ul>
                <li><a href="/predict/BTCUSDT">预测 BTCUSDT / Predict BTCUSDT</a></li>
                <li><a href="/predict/ETHUSDT">预测 ETHUSDT / Predict ETHUSDT</a></li>
            </ul>
        </body>
    </html>
    """

@app.route('/predict/<symbol>')
def predict(symbol):
    """
    预测接口：获取实时数据并进行预测
    Prediction API: fetch real-time data and make prediction
    """
    if symbol not in MODELS:
        return jsonify({"error": f"Model for {symbol} not found. Please train it first."}), 404
    
    # 1. 获取最新数据
    # 1. Fetch latest data
    client = BinanceUtility()
    df = client.fetch_historical_data(symbol, '1h', '2 days ago UTC')
    
    if df is None:
        return jsonify({"error": "Failed to fetch data from Binance"}), 500
        
    processor = DataProcessor()
    df_processed = processor.add_technical_indicators(df)
    
    # 获取最新的特征
    # Get latest features for prediction
    latest_features = df_processed.iloc[-1:].drop(columns=['timestamp'])
    # Ensure columns match training (we need to be careful with column order and names)
    # The prepare_features_labels method defined the feature list
    feature_cols = ['open', 'high', 'low', 'close', 'volume', 'sma_7', 'sma_25', 'rsi_14', 'roc', 'volatility']
    X = latest_features[feature_cols]
    
    prediction = int(MODELS[symbol].predict(X)[0])
    prob = MODELS[symbol].predict_proba(X)[0].tolist()
    
    return jsonify({
        "symbol": symbol,
        "current_price": float(df['close'].iloc[-1]),
        "prediction": "UP" if prediction == 1 else "DOWN",
        "confidence": max(prob),
        "timestamp": str(df['timestamp'].iloc[-1])
    })

if __name__ == '__main__':
    load_models()
    app.run(debug=True, host='0.0.0.0', port=5000)
