"""
LSTM 评估指标工具

提供：
- 回归指标：MAE / MSE / RMSE / MAPE / R2
- 方向指标：涨跌方向 Accuracy + Confusion Matrix

所有输出尽量使用中文描述，方便初学者理解。

作者: qinshihuang166
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


@dataclass
class RegressionMetrics:
    """回归任务评估指标"""

    mae: float
    mse: float
    rmse: float
    mape: float
    r2: float


@dataclass
class DirectionMetrics:
    """方向（涨跌）分类评估指标"""

    accuracy: float
    precision: float
    recall: float
    f1: float
    cm: np.ndarray


def calc_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> RegressionMetrics:
    """计算回归指标"""

    y_true = np.asarray(y_true).reshape(-1)
    y_pred = np.asarray(y_pred).reshape(-1)

    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))

    eps = 1e-8
    mape = float(np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + eps))) * 100)

    r2 = float(r2_score(y_true, y_pred))

    return RegressionMetrics(mae=mae, mse=mse, rmse=rmse, mape=mape, r2=r2)


def to_direction_labels(prices: np.ndarray) -> np.ndarray:
    """把价格序列转成涨跌方向标签（1=涨，0=跌/不变）"""

    prices = np.asarray(prices).reshape(-1)
    diff = np.diff(prices, prepend=prices[0])
    return (diff > 0).astype(int)


def calc_direction_metrics(y_true_prices: np.ndarray, y_pred_prices: np.ndarray) -> DirectionMetrics:
    """根据价格序列计算涨跌方向的分类指标"""

    y_true_dir = to_direction_labels(y_true_prices)
    y_pred_dir = to_direction_labels(y_pred_prices)

    acc = float(accuracy_score(y_true_dir, y_pred_dir))
    prec = float(precision_score(y_true_dir, y_pred_dir, zero_division=0))
    rec = float(recall_score(y_true_dir, y_pred_dir, zero_division=0))
    f1 = float(f1_score(y_true_dir, y_pred_dir, zero_division=0))
    cm = confusion_matrix(y_true_dir, y_pred_dir)

    return DirectionMetrics(accuracy=acc, precision=prec, recall=rec, f1=f1, cm=cm)


def calc_naive_baseline(prev_prices: np.ndarray) -> np.ndarray:
    """简单基线：用“上一时刻价格”作为预测值（Persistence baseline）"""

    prev_prices = np.asarray(prev_prices).reshape(-1)
    # baseline_pred[t] = actual[t-1]
    baseline_pred = np.roll(prev_prices, 1)
    baseline_pred[0] = prev_prices[0]
    return baseline_pred
