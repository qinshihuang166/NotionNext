"""
实时预测脚本 / Real-time Prediction Script
This script uses a trained model to make predictions on current market data
此脚本使用训练好的模型对当前市场数据进行预测
"""

import os
import sys
import argparse
import pandas as pd
import joblib
from datetime import datetime

# Add project root to path / 将项目根目录添加到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.binance_client import BinanceUtility
from utils.data_processor import DataProcessor


def make_prediction(symbol, model_path=None):
    """
    使用训练好的模型进行价格预测
    Make price prediction using trained model
    
    Parameters:
    -----------
    symbol : str
        Trading pair symbol (e.g., 'BTCUSDT')
        交易对符号（例如 'BTCUSDT'）
    model_path : str
        Path to saved model file
        保存的模型文件路径
    """
    
    # 1. 确定模型路径 / Determine model path
    if model_path is None:
        model_path = f'models/{symbol}_price_model.pkl'
    
    # 检查模型是否存在 / Check if model exists
    if not os.path.exists(model_path):
        print(f"❌ 错误：未找到模型文件 / Error: Model file not found: {model_path}")
        print(f"请先运行训练脚本：python scripts/train_model.py --symbol {symbol}")
        print(f"Please run training script first: python scripts/train_model.py --symbol {symbol}")
        return None
    
    print(f"📊 正在加载模型... / Loading model from {model_path}...")
    try:
        model = joblib.load(model_path)
        print("✅ 模型加载成功 / Model loaded successfully\n")
    except Exception as e:
        print(f"❌ 模型加载失败 / Failed to load model: {e}")
        return None
    
    # 2. 获取实时数据 / Fetch real-time data
    print(f"📡 正在从 Binance 获取 {symbol} 的最新数据...")
    print(f"Fetching latest data for {symbol} from Binance...")
    
    client = BinanceUtility()
    df = client.fetch_historical_data(symbol, '1h', '7 days ago UTC')
    
    if df is None or len(df) < 30:
        print("❌ 数据不足，无法进行预测 / Insufficient data for prediction")
        return None
    
    print(f"✅ 数据获取成功，共 {len(df)} 条记录 / Data fetched successfully: {len(df)} records\n")
    
    # 3. 特征工程 / Feature engineering
    print("🔧 正在进行特征工程... / Performing feature engineering...")
    processor = DataProcessor()
    df_processed = processor.add_technical_indicators(df)
    
    # 4. 准备预测特征 / Prepare prediction features
    feature_cols = ['open', 'high', 'low', 'close', 'volume', 'sma_7', 'sma_25', 'rsi_14', 'roc', 'volatility']
    latest_features = df_processed[feature_cols].tail(1)
    
    # 5. 进行预测 / Make prediction
    print("🔮 正在预测... / Making prediction...\n")
    prediction = int(model.predict(latest_features)[0])
    prob = model.predict_proba(latest_features)[0]
    
    # 6. 显示结果 / Display results
    print("=" * 60)
    print(f"📈 {symbol} 价格预测报告 / Price Prediction Report")
    print("=" * 60)
    print(f"\n⏰ 预测时间 / Prediction Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💰 当前价格 / Current Price: {df['close'].iloc[-1]:.2f} USDT")
    print(f"\n📊 技术指标 / Technical Indicators:")
    print(f"   • SMA (7): {df_processed['sma_7'].iloc[-1]:.2f}")
    print(f"   • SMA (25): {df_processed['sma_25'].iloc[-1]:.2f}")
    print(f"   • RSI (14): {df_processed['rsi_14'].iloc[-1]:.2f}")
    print(f"   • 波动率 / Volatility: {df_processed['volatility'].iloc[-1]:.2f}")
    
    print(f"\n🎯 预测结果 / Prediction Result:")
    if prediction == 1:
        print(f"   ↗️  价格趋势 / Trend: 📈 上涨 / UP")
        print(f"   ✅ 上涨概率 / Probability: {prob[1]*100:.2f}%")
    else:
        print(f"   ↘️  价格趋势 / Trend: 📉 下跌 / DOWN")
        print(f"   ✅ 下跌概率 / Probability: {prob[0]*100:.2f}%")
    
    print(f"\n⚠️  风险提示 / Risk Warning:")
    print(f"   本预测仅供参考，不构成投资建议。")
    print(f"   This prediction is for reference only and does not constitute investment advice.")
    print("=" * 60)
    
    return {
        'symbol': symbol,
        'current_price': float(df['close'].iloc[-1]),
        'prediction': 'UP' if prediction == 1 else 'DOWN',
        'confidence': max(prob),
        'timestamp': str(datetime.now())
    }


def main():
    """
    主函数 / Main function
    """
    parser = argparse.ArgumentParser(
        description='实时预测加密货币价格 / Real-time cryptocurrency price prediction',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  python predict.py --symbol BTCUSDT
  python predict.py --symbol ETHUSDT --model models/ETHUSDT_price_model.pkl
        """
    )
    
    parser.add_argument(
        '--symbol', 
        type=str, 
        default='BTCUSDT',
        help='交易对符号，默认 BTCUSDT / Trading pair symbol, default BTCUSDT'
    )
    
    parser.add_argument(
        '--model', 
        type=str, 
        default=None,
        help='模型文件路径，默认 models/{symbol}_price_model.pkl / Model file path'
    )
    
    args = parser.parse_args()
    
    make_prediction(args.symbol, args.model)


if __name__ == "__main__":
    main()
