# 📊 DATA_GUIDE：数据处理全流程说明（中文版）

> 本文档解释本项目中「从 Binance 获取数据 → 清洗 → 特征工程 → 归一化 → 序列化 → 划分数据集」的完整流程。

---

## 1. 数据从哪里来？

本项目使用 Binance 公共接口获取 K 线数据（OHLCV）：

- open：开盘价
- high：最高价
- low：最低价
- close：收盘价
- volume：成交量

### 1.1 下载脚本

推荐使用脚本下载：

```bash
cd binance-prediction
python scripts/lstm/download_lstm_data.py
```

常用参数：

```bash
# 下载 ETH 2年数据
python scripts/lstm/download_lstm_data.py --symbol ETHUSDT --days 730

# 下载多个交易对
python scripts/lstm/download_lstm_data.py --symbols BTCUSDT,ETHUSDT,BNBUSDT --days 365
```

下载成功后，会生成：

- `data/<SYMBOL>_raw_data.csv`

---

## 2. 为什么要做数据清洗？

金融时间序列数据很“脏”，常见问题包括：

- 重复行
- 缺失值（例如接口短暂异常）
- 异常值（极端跳点、成交量异常）
- 时间顺序错误（必须保证按时间升序）

本项目在 `utils/lstm_data_processor.py` 的 `clean_data()` 中处理：

- 去重
- 按时间排序
- 缺失值前向/后向填充
- 删除明显非法数据（close ≤ 0 或 volume < 0）

> 提示：如果你想更激进地处理异常值，可以在此处扩展 winsorize / z-score clip。

---

## 3. 特征工程：为什么要加技术指标？

只用 OHLCV 也能训练 LSTM，但技术指标可以帮助模型更快“理解”市场状态。

### 3.1 本项目内置的指标

在 `utils/technical_indicators.py` 中，我们用 **pandas/numpy 自己实现** 了核心指标，避免新手安装 TA-Lib 的痛点。

常用指标包括：

- RSI（相对强弱指标）
- MACD（趋势/动量）
- Bollinger Bands（波动率）
- EMA/SMA（趋势）
- ATR（波动范围）
- OBV（成交量能量潮）
- Stochastic / Williams %R（超买超卖）

### 3.2 如何配置要使用哪些特征？

在 `config_lstm.py`：

```python
class DataConfig:
    USE_TECHNICAL_INDICATORS = True
    TECHNICAL_INDICATORS = [
        'RSI',
        'MACD',
        'MACD_signal',
        'MACD_hist',
        'BB_upper',
        'BB_middle',
        'BB_lower',
        'EMA_12',
        'EMA_26',
        'ATR',
        'OBV',
    ]
```

数据处理器会把最终用于训练的特征列保存到：

- `processor.feature_columns`

---

## 4. 归一化：为什么必须做？

神经网络对不同量纲非常敏感。

例如：
- close 可能是 40,000
- RSI 是 0-100
- volume 可能是 100,000,000

不归一化会导致：
- 训练不稳定
- loss 不下降
- 模型偏向某些数值大的特征

### 4.1 本项目的归一化方式

默认使用 `MinMaxScaler` 把所有特征缩放到 `[0, 1]`。

```python
class DataConfig:
    SCALER_TYPE = 'MinMaxScaler'
    FEATURE_RANGE = (0, 1)
```

训练完成后会保存 scaler：

- `lstm_models/<SYMBOL>_scaler.pkl`

预测时必须加载同一个 scaler，才能保持数据分布一致。

---

## 5. 时间序列窗口：如何把表格变成 LSTM 输入？

LSTM 的输入形状必须是：

```
(samples, time_steps, features)
```

### 5.1 Sliding Window（滑动窗口）

假设 `TIME_STEPS=3`，特征序列为：

```
[1, 2, 3, 4, 5]
```

则训练样本为：

- X1=[1,2,3] → y1=4
- X2=[2,3,4] → y2=5

在项目中由 `create_sequences()` 实现。

---

## 6. 数据集划分：为什么是 70/15/15？

本项目默认划分：

- 训练集：70%
- 验证集：15%
- 测试集：15%

注意：

- **时间序列不能 shuffle**
- 必须按时间顺序切分，否则会发生“信息泄露”（未来数据泄露到训练集）

---

## 7. 缺失值与异常值（Outliers）处理建议

### 7.1 缺失值

默认策略：

- `ffill`（用前一个值填充）
- `bfill`（前向填充仍缺失时再后向填充）

### 7.2 异常值

常见策略：

1. 删除（谨慎，可能删掉真实极端行情）
2. 裁剪（winsorize，例如 1%~99% 分位裁剪）
3. 使用鲁棒归一化（RobustScaler）

建议新手：先不要过度处理异常值，先跑通流程，再逐步增强。

---

## 8. 数据增强（Data Augmentation）思路

时间序列也可以做简单的数据增强，常见方法：

- 加小噪声（Gaussian noise）
- 随机缩放（scale）
- 随机平移（shift）

目的：

- 提高泛化能力
- 降低过拟合

> 注意：金融时间序列增强要谨慎，太强的增强可能破坏真实规律。

---

## 9. 你应该如何验证数据处理是否正确？

建议你检查：

1. 数据是否按时间排序
2. 是否存在 NaN/Inf
3. 归一化是否在 [0,1]
4. X 的形状是否为 3D

示例代码：

```python
import numpy as np

print('X_train shape:', X_train.shape)
print('min/max:', np.min(X_train), np.max(X_train))
print('has nan:', np.isnan(X_train).any())
```

---

## 10. 下一步

- 学习 LSTM 原理：`LSTM_TUTORIAL.md`
- 直接跑训练：`python scripts/lstm/train_lstm.py --quick-test`
- 看笔记本：`notebooks/01_数据准备_LSTM.ipynb`

---

如果你想让我帮你扩展：
- 更完整的异常值检测
- walk-forward 验证（时间序列交叉验证）
- 多币种特征融合
- Attention / Transformer

可以继续在仓库里提 Issue。
