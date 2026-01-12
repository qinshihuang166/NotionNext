"""
LSTM 模型评估脚本（综合评估）

包含：
- 回归指标（真实价格尺度）
- 方向预测指标（Confusion Matrix / Accuracy）
- 与简单基线（上一时刻价格）对比
- 可视化输出

使用：
    cd binance-prediction
    python scripts/lstm/evaluate.py

作者: qinshihuang166
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

# 添加项目根目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config_lstm import DataConfig, PathConfig
from utils.lstm_data_processor import LSTMDataProcessor
from utils.lstm_metrics import calc_regression_metrics, calc_direction_metrics, calc_naive_baseline


def _ensure_matplotlib_backend() -> None:
    """保证在无 GUI 环境也能保存图片"""

    import matplotlib

    matplotlib.use('Agg')


def load_model() -> "object":
    """加载训练好的模型"""

    import tensorflow as tf

    if not os.path.exists(PathConfig.MODEL_PATH):
        raise FileNotFoundError(
            f"❌ 找不到模型文件: {PathConfig.MODEL_PATH}\n"
            f"请先训练模型：python scripts/lstm/train_lstm.py"
        )

    return tf.keras.models.load_model(PathConfig.MODEL_PATH)


def build_eval_dataset(processor: LSTMDataProcessor) -> dict:
    """构建评估所需的数据集（包含 scaled 和 real 两套 y）"""

    # 1. 原始数据
    df_raw = processor.load_raw_data()
    df_raw = processor.clean_data(df_raw)
    df_raw = processor.add_features(df_raw)

    # 2. 选择特征（原始尺度）
    df_features_real = processor.select_features(df_raw)

    # 3. 使用训练时的 scaler 做 transform
    processor.load_scaler(PathConfig.SCALER_PATH)
    df_features_scaled = processor.normalize_data(df_features_real, fit=False)

    # 4. 构建序列（X 使用 scaled）
    X_all, y_scaled_all = processor.create_sequences(df_features_scaled.values)

    # y_true_real：用真实 close 对齐
    y_real_all = df_features_real['close'].values[DataConfig.TIME_STEPS :]

    # 5. 划分（按时间顺序）
    X_train, X_val, X_test, y_train_scaled, y_val_scaled, y_test_scaled = processor.split_data(X_all, y_scaled_all)

    # 真实价格也按同样切分
    total = len(y_real_all)
    train_size = int(total * DataConfig.TRAIN_RATIO)
    val_size = int(total * DataConfig.VAL_RATIO)

    y_train_real = y_real_all[:train_size]
    y_val_real = y_real_all[train_size : train_size + val_size]
    y_test_real = y_real_all[train_size + val_size :]

    return {
        'X_train': X_train,
        'X_val': X_val,
        'X_test': X_test,
        'y_train_scaled': y_train_scaled,
        'y_val_scaled': y_val_scaled,
        'y_test_scaled': y_test_scaled,
        'y_train_real': y_train_real,
        'y_val_real': y_val_real,
        'y_test_real': y_test_real,
        'df_features_real': df_features_real,
        'df_features_scaled': df_features_scaled,
    }


def inverse_close(processor: LSTMDataProcessor, close_scaled: np.ndarray) -> np.ndarray:
    """把 scaled close 反归一化成真实价格"""

    close_scaled = np.asarray(close_scaled).reshape(-1)
    full = np.zeros((len(close_scaled), len(processor.feature_columns)), dtype=float)
    full[:, 3] = close_scaled
    real = processor.scaler.inverse_transform(full)
    return real[:, 3]


def save_confusion_matrix(cm: np.ndarray, out_path: str) -> None:
    """保存混淆矩阵图片"""

    _ensure_matplotlib_backend()

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(cm, cmap='Blues')
    ax.set_title('涨跌方向混淆矩阵')
    ax.set_xlabel('预测')
    ax.set_ylabel('实际')

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center', color='black')

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['跌/不变(0)', '涨(1)'])
    ax.set_yticklabels(['跌/不变(0)', '涨(1)'])

    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description='LSTM 模型评估脚本')
    parser.add_argument('--symbol', type=str, default=DataConfig.SYMBOL, help='交易对，例如 BTCUSDT')
    args = parser.parse_args()

    # 当前版本：symbol 主要用于展示。若你要训练多币种，建议每个币种单独训练/保存模型。
    print('=' * 70)
    print('📊 LSTM 模型评估')
    print('=' * 70)
    print(f'交易对: {args.symbol}')

    # 准备目录
    PathConfig.create_directories()

    # 加载模型
    model = load_model()

    # 构建数据
    processor = LSTMDataProcessor()
    data = build_eval_dataset(processor)

    X_test = data['X_test']
    y_test_real = data['y_test_real']

    # 模型预测（scaled）
    y_pred_scaled = model.predict(X_test, verbose=0).reshape(-1)

    # 转回真实价格
    y_pred_real = inverse_close(processor, y_pred_scaled)

    # 计算指标
    reg = calc_regression_metrics(y_test_real, y_pred_real)
    direction = calc_direction_metrics(y_test_real, y_pred_real)

    # 基线：上一时刻价格
    baseline_pred = calc_naive_baseline(y_test_real)
    reg_baseline = calc_regression_metrics(y_test_real, baseline_pred)
    direction_baseline = calc_direction_metrics(y_test_real, baseline_pred)

    # 输出
    print('\n✅ 回归指标（真实价格尺度）')
    print(f'  MAE : {reg.mae:.4f}')
    print(f'  RMSE: {reg.rmse:.4f}')
    print(f'  MAPE: {reg.mape:.4f}%')
    print(f'  R2  : {reg.r2:.4f}')

    print('\n✅ 方向指标（涨跌方向）')
    print(f'  Accuracy : {direction.accuracy:.4f}')
    print(f'  Precision: {direction.precision:.4f}')
    print(f'  Recall   : {direction.recall:.4f}')
    print(f'  F1       : {direction.f1:.4f}')

    print('\n📌 基线对比（上一时刻价格作为预测）')
    print(f'  Baseline MAE : {reg_baseline.mae:.4f}')
    print(f'  Baseline RMSE: {reg_baseline.rmse:.4f}')
    print(f'  Baseline Acc : {direction_baseline.accuracy:.4f}')

    # 保存结果
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = PathConfig.RESULTS_DIR

    metrics_path = os.path.join(out_dir, f'eval_metrics_{ts}.json')
    pd.DataFrame(
        [
            {
                'model': 'LSTM',
                'mae': reg.mae,
                'mse': reg.mse,
                'rmse': reg.rmse,
                'mape': reg.mape,
                'r2': reg.r2,
                'direction_accuracy': direction.accuracy,
                'direction_precision': direction.precision,
                'direction_recall': direction.recall,
                'direction_f1': direction.f1,
            },
            {
                'model': 'Baseline(prev_close)',
                'mae': reg_baseline.mae,
                'mse': reg_baseline.mse,
                'rmse': reg_baseline.rmse,
                'mape': reg_baseline.mape,
                'r2': reg_baseline.r2,
                'direction_accuracy': direction_baseline.accuracy,
                'direction_precision': direction_baseline.precision,
                'direction_recall': direction_baseline.recall,
                'direction_f1': direction_baseline.f1,
            },
        ]
    ).to_json(metrics_path, orient='records', force_ascii=False, indent=2)

    print(f'\n💾 评估指标已保存: {metrics_path}')

    cm_path = os.path.join(out_dir, f'confusion_matrix_{ts}.png')
    save_confusion_matrix(direction.cm, cm_path)
    print(f'🖼️ 混淆矩阵已保存: {cm_path}')

    pred_path = os.path.join(out_dir, f'predictions_real_{ts}.csv')
    pd.DataFrame({'y_true': y_test_real, 'y_pred': y_pred_real}).to_csv(pred_path, index=False)
    print(f'💾 预测结果已保存: {pred_path}')


if __name__ == '__main__':
    main()
