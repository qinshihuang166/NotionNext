"""
LSTM 回测脚本（Backtesting）

目标：
- 使用测试集的预测结果做一个最基础的方向策略回测
- 对比 Buy & Hold 基准

注意：
- 这里只是教学性质的回测示例（不含手续费/滑点/杠杆/做空等）
- 不构成任何投资建议

使用：
    cd binance-prediction
    python scripts/lstm/backtest.py

作者: qinshihuang166
"""

from __future__ import annotations

import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config_lstm import DataConfig, PathConfig
from utils.lstm_data_processor import LSTMDataProcessor
from utils.lstm_metrics import calc_regression_metrics, calc_direction_metrics


def _ensure_matplotlib_backend() -> None:
    import matplotlib

    matplotlib.use('Agg')


def load_model() -> "object":
    import tensorflow as tf

    if not os.path.exists(PathConfig.MODEL_PATH):
        raise FileNotFoundError(
            f"❌ 找不到模型文件: {PathConfig.MODEL_PATH}\n"
            f"请先训练模型：python scripts/lstm/train_lstm.py"
        )

    return tf.keras.models.load_model(PathConfig.MODEL_PATH)


def inverse_close(processor: LSTMDataProcessor, close_scaled: np.ndarray) -> np.ndarray:
    close_scaled = np.asarray(close_scaled).reshape(-1)
    full = np.zeros((len(close_scaled), len(processor.feature_columns)), dtype=float)
    full[:, 3] = close_scaled
    real = processor.scaler.inverse_transform(full)
    return real[:, 3]


def build_test_set(processor: LSTMDataProcessor) -> dict:
    """构建测试集并返回真实价格序列"""

    df_raw = processor.load_raw_data()
    df_raw = processor.clean_data(df_raw)
    df_raw = processor.add_features(df_raw)
    df_features_real = processor.select_features(df_raw)

    processor.load_scaler(PathConfig.SCALER_PATH)
    df_features_scaled = processor.normalize_data(df_features_real, fit=False)

    X_all, y_scaled_all = processor.create_sequences(df_features_scaled.values)

    y_real_all = df_features_real['close'].values[DataConfig.TIME_STEPS :]

    X_train, X_val, X_test, y_train_scaled, y_val_scaled, y_test_scaled = processor.split_data(X_all, y_scaled_all)

    total = len(y_real_all)
    train_size = int(total * DataConfig.TRAIN_RATIO)
    val_size = int(total * DataConfig.VAL_RATIO)

    y_test_real = y_real_all[train_size + val_size :]

    # 同步取出测试集对应的时间戳（便于画图/保存）
    ts_all = df_features_real.index.values[DataConfig.TIME_STEPS :]
    ts_test = ts_all[train_size + val_size :]

    return {
        'X_test': X_test,
        'y_test_scaled': y_test_scaled,
        'y_test_real': y_test_real,
        'ts_test': ts_test,
    }


def backtest_strategy(y_true: np.ndarray, y_pred: np.ndarray) -> pd.DataFrame:
    """最简单的方向策略回测：预测涨→持有；预测跌→空仓"""

    y_true = np.asarray(y_true).reshape(-1)
    y_pred = np.asarray(y_pred).reshape(-1)

    # 使用上一时刻真实价格作为“当前价”
    prev_true = np.roll(y_true, 1)
    prev_true[0] = y_true[0]

    # 持仓信号：预测价格高于当前价 => 做多
    position = (y_pred > prev_true).astype(int)

    # 市场收益（买入并持有）
    market_ret = (y_true / prev_true) - 1.0
    market_ret[0] = 0.0

    # 策略收益：只有持仓时才获得市场收益
    strategy_ret = position * market_ret

    df = pd.DataFrame(
        {
            'close': y_true,
            'pred': y_pred,
            'position': position,
            'market_return': market_ret,
            'strategy_return': strategy_ret,
        }
    )

    df['cum_market'] = (1 + df['market_return']).cumprod()
    df['cum_strategy'] = (1 + df['strategy_return']).cumprod()

    return df


def plot_equity_curve(df: pd.DataFrame, out_path: str) -> None:
    _ensure_matplotlib_backend()
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df['cum_market'], label='Buy & Hold', linewidth=2)
    ax.plot(df['cum_strategy'], label='LSTM Strategy', linewidth=2)
    ax.set_title('累计收益曲线（教学示例）')
    ax.set_xlabel('时间步')
    ax.set_ylabel('净值')
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()


def main() -> None:
    print('=' * 70)
    print('📈 LSTM 回测（Backtesting）')
    print('=' * 70)

    PathConfig.create_directories()

    model = load_model()
    processor = LSTMDataProcessor()
    test = build_test_set(processor)

    X_test = test['X_test']
    y_true = test['y_test_real']

    y_pred_scaled = model.predict(X_test, verbose=0).reshape(-1)
    y_pred = inverse_close(processor, y_pred_scaled)

    # 回归和方向指标（用于参考）
    reg = calc_regression_metrics(y_true, y_pred)
    direction = calc_direction_metrics(y_true, y_pred)

    print('\n✅ 模型在测试集上的参考指标（真实价格尺度）')
    print(f'  MAE : {reg.mae:.4f}')
    print(f'  RMSE: {reg.rmse:.4f}')
    print(f'  方向准确率: {direction.accuracy:.4f}')

    # 回测
    bt = backtest_strategy(y_true, y_pred)

    final_market = bt['cum_market'].iloc[-1]
    final_strategy = bt['cum_strategy'].iloc[-1]

    print('\n📊 回测结果（不含手续费/滑点）')
    print(f'  Buy & Hold 期末净值: {final_market:.4f}')
    print(f'  策略期末净值       : {final_strategy:.4f}')

    # 保存
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = PathConfig.RESULTS_DIR

    csv_path = os.path.join(out_dir, f'backtest_{ts}.csv')
    bt.to_csv(csv_path, index=False)
    print(f'\n💾 回测明细已保存: {csv_path}')

    plot_path = os.path.join(out_dir, f'backtest_equity_{ts}.png')
    plot_equity_curve(bt, plot_path)
    print(f'🖼️ 净值曲线已保存: {plot_path}')

    print('\n⚠️ 免责声明：此回测仅用于教学，不构成投资建议。')


if __name__ == '__main__':
    main()
