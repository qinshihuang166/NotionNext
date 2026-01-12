import os
import sys
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import argparse

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processor import DataProcessor

def run_backtest(symbol, model_path, data_path):
    print(f"开始对 {symbol} 进行回测... / Starting backtest for {symbol}...")
    
    # 1. 加载数据和模型
    # 1. Load data and model
    df = pd.read_csv(data_path)
    model = joblib.load(model_path)
    
    # 2. 准备特征
    # 2. Prepare features
    processor = DataProcessor()
    df_processed = processor.add_technical_indicators(df)
    X, y = processor.prepare_features_labels(df_processed)
    
    # 我们只对最后20%的数据进行回测（模拟测试集）
    # Backtest on last 20% of data (simulation test set)
    split_idx = int(len(X) * 0.8)
    X_test = X[split_idx:]
    df_test = df_processed.iloc[split_idx:-1].copy() # 对应 X_test 的时间点
    
    # 3. 生成预测
    # 3. Generate predictions
    predictions = model.predict(X_test)
    df_test['prediction'] = predictions
    
    # 4. 模拟策略：如果是1（涨）则买入/持有，如果是0（跌）则卖出/持币
    # 4. Simple Strategy: Buy if 1 (Up), Sell/Hold if 0 (Down)
    df_test['returns'] = df_test['close'].pct_change()
    # 我们的策略收益：如果预测是1，我们获得下个周期的收益
    df_test['strategy_returns'] = df_test['prediction'].shift(1) * df_test['returns']
    
    # 计算累计收益
    # Calculate cumulative returns
    df_test['cum_market_returns'] = (1 + df_test['returns'].fillna(0)).cumprod()
    df_test['cum_strategy_returns'] = (1 + df_test['strategy_returns'].fillna(0)).cumprod()
    
    # 5. 可视化
    # 5. Visualization
    plt.figure(figsize=(12, 6))
    plt.plot(df_test['cum_market_returns'], label='Market Returns (Buy & Hold)')
    plt.plot(df_test['cum_strategy_returns'], label='Strategy Returns (ML Based)')
    plt.title(f'Backtesting Result for {symbol}')
    plt.xlabel('Time Steps')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    
    # 保存结果图
    if not os.path.exists('data'): os.makedirs('data')
    plt.savefig(f'data/{symbol}_backtest.png')
    print(f"回测图表已保存至: data/{symbol}_backtest.png / Backtest chart saved to: data/{symbol}_backtest.png")
    
    final_return = df_test['cum_strategy_returns'].iloc[-1]
    market_return = df_test['cum_market_returns'].iloc[-1]
    print(f"策略最终累计收益: {final_return:.4f}")
    print(f"市场基准最终收益: {market_return:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backtest ML Strategy')
    parser.add_argument('--symbol', type=str, default='BTCUSDT')
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--data', type=str, required=True)
    
    args = parser.parse_args()
    run_backtest(args.symbol, args.model, args.data)
