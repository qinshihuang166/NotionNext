# 🛠️ TROUBLESHOOTING：常见错误与解决方案（全中文）

> 这个文件专门用来帮助初学者快速定位问题。
> 
> 建议：遇到报错先复制整段错误信息，再对照本文逐条排查。

---

## 0. 先做 3 个快速检查

### 0.1 你在正确目录吗？

运行脚本前请进入：

```bash
cd binance-prediction
```

### 0.2 你激活了虚拟环境吗？

如果你用了 venv：

- Windows：`venv\Scripts\activate`
- Linux/macOS：`source venv/bin/activate`

### 0.3 你装对依赖了吗？

```bash
pip install -r requirements_lstm.txt
```

---

## 1. 安装相关问题

### 1.1 `ModuleNotFoundError: No module named 'tensorflow'`

原因：没安装 TensorFlow 或装在别的环境。

解决：

```bash
pip install tensorflow
python -c "import tensorflow as tf; print(tf.__version__)"
```

如果还是不行，尝试：

```bash
pip install tensorflow==2.12.0
```

### 1.2 Windows 安装 TensorFlow 报错

建议：

- 使用 Python 3.9 或 3.10（更稳定）
- 使用 conda 安装：

```bash
conda create -n lstm_crypto python=3.9
conda activate lstm_crypto
conda install tensorflow
pip install -r requirements_lstm.txt
```

### 1.3 `TA-Lib` 安装失败

说明：

- 本项目 **默认不依赖 TA-Lib**。
- 技术指标已在 `utils/technical_indicators.py` 用 pandas/numpy 自己实现。

你可以直接忽略 TA-Lib。

---

## 2. 数据下载相关问题

### 2.1 下载失败 / 数据为空

可能原因：

- 网络不稳定
- Binance API 临时异常
- 请求被限流

解决方案：

1) 直接重试：

```bash
python scripts/lstm/download_lstm_data.py
```

2) 减少数据量（先跑通流程）：

```bash
python scripts/lstm/download_lstm_data.py --days 90
```

3) 如果你有 API Key，可以在 `.env` 中配置（提高稳定性）：

```env
BINANCE_API_KEY=你的key
BINANCE_API_SECRET=你的secret
```

---

## 3. 训练相关问题

### 3.1 `FileNotFoundError: data/BTCUSDT_raw_data.csv`

原因：你还没下载数据。

解决：

```bash
python scripts/lstm/download_lstm_data.py
```

### 3.2 训练很慢（CPU 跑不动）

解决方案（按推荐顺序）：

1) 用快速模式：

```bash
python scripts/lstm/train_lstm.py --quick-test
```

2) 用 CPU 友好模式：

```bash
python scripts/lstm/train_lstm.py --cpu-friendly
```

3) 减少数据量：

在 `config_lstm.py`：

```python
DataConfig.LOOKBACK_DAYS = 90
DataConfig.TIME_STEPS = 30
```

### 3.3 GPU 未被识别

检查：

```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

如果输出是 `[]`：

- 你可能没装 CUDA（NVIDIA）
- 或者 TensorFlow / CUDA 版本不匹配

建议初学者：

- 先用 CPU 跑通流程
- 有条件再配置 GPU

### 3.4 `ResourceExhaustedError` / OOM（显存/内存不够）

解决：

1) 降低批大小（最常用）：

```python
TrainingConfig.BATCH_SIZE = 16
```

2) 简化模型：

```python
ModelConfig.LSTM_UNITS = [64, 32]
ModelConfig.DROPOUT_RATE = 0.2
```

3) 减小时间窗口：

```python
DataConfig.TIME_STEPS = 30
```

4) 如果是 GPU，开启混合精度（仅在支持的 GPU 上推荐）：

```python
TrainingConfig.MIXED_PRECISION = True
```

### 3.5 Loss 变成 NaN

常见原因：

- 数据中有 NaN/Inf
- 学习率过大
- 特征归一化异常

解决（依次尝试）：

1) 降低学习率：

```python
ModelConfig.LEARNING_RATE = 0.0001
```

2) 检查数据：

```python
import numpy as np
print(np.isnan(X_train).any(), np.isinf(X_train).any())
```

3) 确保归一化在合理范围：

```python
print(X_train.min(), X_train.max())
```

---

## 4. 预测相关问题

### 4.1 预测脚本提示模型不存在

原因：你还没有训练模型。

解决：

```bash
python scripts/lstm/train_lstm.py
```

### 4.2 预测结果“很奇怪”（数值不对）

最常见原因：

- 忘记反归一化
- 训练和预测使用了不同 scaler

本项目会自动保存 scaler：

- `lstm_models/<SYMBOL>_scaler.pkl`

预测时会自动加载。

如果你手动改过文件名或目录，请确认路径。

---

## 5. 可视化相关问题

### 5.1 运行脚本没有弹出图

原因：训练脚本为了在服务器/无界面环境运行，使用了 `Agg` 后端，会把图保存到文件。

请查看：

```bash
ls lstm_results/
```

你会看到：

- `training_history.png`
- `prediction_vs_actual.png`
- `error_analysis.png`

---

## 6. 最推荐的“排错流程”（新手友好）

1) 先跑快速流程验证一切可用：

```bash
python scripts/lstm/download_lstm_data.py --days 90
python scripts/lstm/train_lstm.py --quick-test
```

2) 确认训练成功后，再逐步增加：

- 数据量：90 天 → 365 天 → 730 天
- 模型规模：小模型 → 默认模型 → 生产模型

3) 每次只改一个参数，并记录结果。

---

## 7. 还解决不了？

建议你在 GitHub Issue 里提供：

- 你运行的命令
- 你的系统（Windows/macOS/Linux）
- Python 版本
- 完整报错信息（从第一行到最后一行）

这样别人才能准确帮你定位。
