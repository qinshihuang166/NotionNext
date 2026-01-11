import os
import sys
from flask import Flask, render_template, jsonify
import pandas as pd
import joblib

# Add project root to path
# Adding both parent and current for flexibility
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.binance_client import BinanceUtility
from utils.data_processor import DataProcessor

app = Flask(__name__)

# 全局变量存储模型
MODELS = {}
SYMBOLS = ['BTCUSDT', 'ETHUSDT']

def load_models():
    """
    从 models 目录加载预训练模型
    """
    # 尝试多种可能的模型路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for symbol in SYMBOLS:
        model_path = os.path.join(base_dir, 'models', f'{symbol}_price_model.pkl')
        if os.path.exists(model_path):
            MODELS[symbol] = joblib.load(model_path)
            print(f"成功加载模型 / Loaded model: {model_path}")
        else:
            print(f"警告: 未找到模型 / Warning: Model not found at {model_path}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict/<symbol>')
def predict_page(symbol):
    # 页面逻辑由 index.html 中的 JS 处理，或者这里渲染
    return render_template('index.html')

@app.route('/api/predict/<symbol>')
def api_predict(symbol):
    """
    预测 API 接口
    """
    if symbol not in MODELS:
        return jsonify({"error": f"Model for {symbol} not found. Please train it first."}), 404
    
    try:
        client = BinanceUtility()
        # 获取最近的数据进行预测
        df = client.fetch_historical_data(symbol, '1h', '2 days ago UTC')
        
        if df is None or len(df) < 30:
            return jsonify({"error": "Insufficient data from Binance"}), 500
            
        processor = DataProcessor()
        df_processed = processor.add_technical_indicators(df)
        
        feature_cols = ['open', 'high', 'low', 'close', 'volume', 'sma_7', 'sma_25', 'rsi_14', 'roc', 'volatility']
        latest_features = df_processed[feature_cols].tail(1)
        
        prediction = int(MODELS[symbol].predict(latest_features)[0])
        prob = MODELS[symbol].predict_proba(latest_features)[0].tolist()
        
        return jsonify({
            "symbol": symbol,
            "current_price": float(df['close'].iloc[-1]),
            "prediction": "UP" if prediction == 1 else "DOWN",
            "confidence": max(prob),
            "timestamp": str(df['timestamp'].iloc[-1])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    load_models()
    # 生产环境建议使用 Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
