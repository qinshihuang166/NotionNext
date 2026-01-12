"""
LSTM价格预测脚本
LSTM Price Prediction Script

使用训练好的模型进行价格预测
Use trained model to make price predictions

作者: qinshihuang166
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config_lstm import DataConfig, PathConfig
from utils.lstm_data_processor import LSTMDataProcessor
from utils.binance_client import BinanceUtility
import warnings
warnings.filterwarnings('ignore')


def load_model_and_scaler():
    """加载训练好的模型和scaler"""
    import tensorflow as tf
    
    model_path = PathConfig.MODEL_PATH
    scaler_path = PathConfig.SCALER_PATH
    
    # 检查文件是否存在
    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在: {model_path}")
        print("\n💡 请先训练模型:")
        print("   python scripts/lstm/train_lstm.py")
        sys.exit(1)
    
    if not os.path.exists(scaler_path):
        print(f"❌ Scaler文件不存在: {scaler_path}")
        print("\n💡 请先训练模型:")
        print("   python scripts/lstm/train_lstm.py")
        sys.exit(1)
    
    # 加载模型
    print(f"📂 加载模型: {model_path}")
    model = tf.keras.models.load_model(model_path)
    
    # 加载scaler
    print(f"📂 加载Scaler: {scaler_path}")
    processor = LSTMDataProcessor()
    processor.load_scaler(scaler_path)
    
    return model, processor


def prepare_recent_data(processor, symbol, interval, time_steps):
    """准备最近的数据用于预测"""
    print(f"\n📥 获取最新数据...")
    
    # 获取最新数据
    client = BinanceUtility()
    
    # 需要获取足够的数据来构建时间窗口 + 计算技术指标
    # 技术指标最多需要200个点，时间窗口需要time_steps个点
    lookback_hours = max(300, time_steps + 200)
    start_time = datetime.now() - timedelta(hours=lookback_hours)
    start_str = start_time.strftime("%d %b, %Y")
    
    df = client.fetch_historical_data(symbol, interval, start_str)
    
    if df is None or df.empty:
        print("❌ 无法获取数据")
        sys.exit(1)
    
    print(f"✓ 获取了 {len(df)} 个数据点")
    print(f"  时间范围: {df['timestamp'].min()} 到 {df['timestamp'].max()}")
    
    # 数据处理
    df = processor.clean_data(df)
    df = processor.add_features(df)
    df = processor.select_features(df)
    
    # 归一化（使用训练时的scaler）
    df_normalized = processor.normalize_data(df, fit=False)
    
    # 取最后time_steps个点
    recent_data = df_normalized.values[-time_steps:]
    
    # 重塑为模型输入格式: (1, time_steps, features)
    X = recent_data.reshape(1, time_steps, recent_data.shape[1])
    
    return X, df


def predict_next_price(model, X, processor):
    """预测下一个价格"""
    # 模型预测（归一化值）
    prediction_scaled = model.predict(X, verbose=0)
    
    # 反归一化（假设close是第4个特征，索引3）
    # 创建一个全零数组，只填入预测值到close的位置
    full_prediction = np.zeros((1, len(processor.feature_columns)))
    full_prediction[0, 3] = prediction_scaled[0, 0]  # close在索引3
    
    # 反归一化
    prediction_real = processor.scaler.inverse_transform(full_prediction)
    predicted_price = prediction_real[0, 3]
    
    return predicted_price


def predict_multiple_steps(model, X, processor, steps):
    """预测未来多个时间步"""
    predictions = []
    current_X = X.copy()
    
    for i in range(steps):
        # 预测下一个值
        prediction_scaled = model.predict(current_X, verbose=0)
        predictions.append(prediction_scaled[0, 0])
        
        # 更新输入（滑动窗口）
        # 将新预测添加到序列末尾，移除最旧的数据点
        new_point = current_X[0, -1, :].copy()  # 复制最后一个点的所有特征
        new_point[3] = prediction_scaled[0, 0]  # 更新close值
        
        # 滚动窗口
        current_X = np.roll(current_X, -1, axis=1)
        current_X[0, -1, :] = new_point
    
    # 反归一化所有预测
    predictions_array = np.array(predictions).reshape(-1, 1)
    full_predictions = np.zeros((len(predictions), len(processor.feature_columns)))
    full_predictions[:, 3] = predictions_array.flatten()
    
    predictions_real = processor.scaler.inverse_transform(full_predictions)
    predicted_prices = predictions_real[:, 3]
    
    return predicted_prices


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='LSTM价格预测脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 预测下一个价格
  python predict_lstm.py
  
  # 预测未来24小时
  python predict_lstm.py --steps 24
  
  # 预测ETH价格
  python predict_lstm.py --symbol ETHUSDT
  
  # 显示详细信息
  python predict_lstm.py --verbose
        """
    )
    
    parser.add_argument(
        '--symbol',
        type=str,
        default=DataConfig.SYMBOL,
        help=f'交易对符号 (默认: {DataConfig.SYMBOL})'
    )
    
    parser.add_argument(
        '--steps',
        type=int,
        default=1,
        help='预测未来多少个时间步 (默认: 1)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print(" "*20 + "🔮 LSTM 价格预测")
    print("="*70)
    print(f"\n交易对: {args.symbol}")
    print(f"预测步数: {args.steps}")
    print("="*70)
    
    # 1. 加载模型和scaler
    print("\n⚙️ 步骤 1: 加载模型")
    model, processor = load_model_and_scaler()
    
    if args.verbose:
        print("\n模型架构:")
        model.summary()
    
    # 2. 准备最新数据
    print("\n⚙️ 步骤 2: 准备数据")
    X, df_original = prepare_recent_data(
        processor, 
        args.symbol, 
        DataConfig.INTERVAL,
        DataConfig.TIME_STEPS
    )
    
    # 3. 进行预测
    print("\n⚙️ 步骤 3: 进行预测")
    
    if args.steps == 1:
        # 单步预测
        predicted_price = predict_next_price(model, X, processor)
        
        # 获取当前价格
        current_price = df_original['close'].iloc[-1]
        
        # 计算变化
        price_change = predicted_price - current_price
        price_change_pct = (price_change / current_price) * 100
        
        # 显示结果
        print("\n" + "="*70)
        print("📊 预测结果")
        print("="*70)
        print(f"\n当前价格: ${current_price:.2f}")
        print(f"预测价格: ${predicted_price:.2f}")
        print(f"\n价格变化: ${price_change:+.2f} ({price_change_pct:+.2f}%)")
        
        if price_change > 0:
            print(f"\n📈 预测: 价格上涨")
            trend_emoji = "🚀"
        else:
            print(f"\n📉 预测: 价格下跌")
            trend_emoji = "⬇️"
        
        print(f"\n{trend_emoji} 趋势信号: {'看涨' if price_change > 0 else '看跌'}")
        print("="*70)
        
    else:
        # 多步预测
        predicted_prices = predict_multiple_steps(model, X, processor, args.steps)
        
        # 当前价格
        current_price = df_original['close'].iloc[-1]
        
        # 创建预测结果DataFrame
        future_times = []
        current_time = df_original['timestamp'].iloc[-1]
        
        # 计算时间间隔
        interval_minutes = {
            '1m': 1, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '2h': 120, '4h': 240, '1d': 1440
        }.get(DataConfig.INTERVAL, 60)
        
        for i in range(1, args.steps + 1):
            future_time = current_time + timedelta(minutes=interval_minutes * i)
            future_times.append(future_time)
        
        predictions_df = pd.DataFrame({
            'timestamp': future_times,
            'predicted_price': predicted_prices,
            'change_from_current': predicted_prices - current_price,
            'change_pct': ((predicted_prices - current_price) / current_price) * 100
        })
        
        # 显示结果
        print("\n" + "="*70)
        print(f"📊 未来 {args.steps} 个时间点的预测")
        print("="*70)
        print(f"\n当前价格: ${current_price:.2f}")
        print(f"当前时间: {current_time}")
        print("\n预测结果:")
        print(predictions_df.to_string(index=False))
        
        # 总体趋势
        final_price = predicted_prices[-1]
        total_change = final_price - current_price
        total_change_pct = (total_change / current_price) * 100
        
        print(f"\n" + "-"*70)
        print(f"最终预测价格: ${final_price:.2f}")
        print(f"总体变化: ${total_change:+.2f} ({total_change_pct:+.2f}%)")
        
        if total_change > 0:
            print(f"📈 总体趋势: 上涨 🚀")
        else:
            print(f"📉 总体趋势: 下跌 ⬇️")
        
        print("="*70)
        
        # 保存预测结果
        save_path = os.path.join(PathConfig.RESULTS_DIR, f'predictions_{args.symbol}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        predictions_df.to_csv(save_path, index=False)
        print(f"\n💾 预测结果已保存: {save_path}")
    
    # 免责声明
    print("\n" + "="*70)
    print("⚠️  免责声明")
    print("="*70)
    print("本预测仅供参考，不构成投资建议。")
    print("加密货币交易存在高风险，请谨慎决策。")
    print("历史数据不能保证未来表现。")
    print("="*70)


if __name__ == "__main__":
    main()
