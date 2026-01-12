# API 文档 / API Documentation

本文档详细说明了项目中各个模块和函数的使用方法。
This document details the usage of various modules and functions in the project.

## 📋 目录 / Table of Contents

1. [Binance Utility Module](#1-binance-utility-module)
2. [Data Processor Module](#2-data-processor-module)
3. [Command Line Scripts](#3-command-line-scripts)
4. [Flask Web API](#4-flask-web-api)

---

## 1. Binance Utility Module / 币安工具模块

### 类 / Class: `BinanceUtility`

用于与币安 API 交互，获取市场数据。
Used to interact with Binance API and fetch market data.

**位置 / Location**: `utils/binance_client.py`

#### 初始化 / Initialization

```python
from utils.binance_client import BinanceUtility

# 使用环境变量中的 API Key / Use API Key from environment variables
client = BinanceUtility()

# 或手动指定 API Key / Or manually specify API Key
client = BinanceUtility(api_key='your_key', api_secret='your_secret')
```

**参数 / Parameters**:
- `api_key` (str, optional): 币安 API Key / Binance API Key
- `api_secret` (str, optional): 币安 API Secret / Binance API Secret

---

#### 方法 1: `fetch_historical_data(symbol, interval, start_str, end_str=None)`

获取历史 K 线数据。
Fetch historical K-line data.

**参数 / Parameters**:

| 参数 / Parameter | 类型 / Type | 说明 / Description | 示例 / Example |
|----------------|-------------|------------------|----------------|
| `symbol` | str | 交易对 / Trading pair | `'BTCUSDT'`, `'ETHUSDT'` |
| `interval` | str | K 线间隔 / K-line interval | `'1m'`, `'5m'`, `'1h'`, `'1d'` |
| `start_str` | str | 开始时间 / Start time | `'1 year ago UTC'`, `'2023-01-01'` |
| `end_str` | str, optional | 结束时间 / End time | `'2023-12-31'`, `'now'` |

**返回值 / Returns**:
- `pandas.DataFrame`: 包含以下列的 DataFrame
  - `timestamp`: 时间戳 / Timestamp
  - `open`: 开盘价 / Open price
  - `high`: 最高价 / High price
  - `low`: 最低价 / Low price
  - `close`: 收盘价 / Close price
  - `volume`: 成交量 / Volume

**使用示例 / Usage Example**:

```python
# 获取比特币过去 6 个月的小时数据
# Fetch hourly data for Bitcoin over past 6 months
df = client.fetch_historical_data(
    symbol='BTCUSDT',
    interval='1h',
    start_str='6 months ago UTC'
)

print(df.head())
```

**支持的时间间隔 / Supported Intervals**:
- `'1m'`: 1 分钟 / 1 minute
- `'5m'`: 5 分钟 / 5 minutes
- `'15m'`: 15 分钟 / 15 minutes
- `'1h'`: 1 小时 / 1 hour
- `'4h'`: 4 小时 / 4 hours
- `'1d'`: 1 天 / 1 day
- `'1w'`: 1 周 / 1 week

---

#### 方法 2: `get_realtime_price(symbol)`

获取实时价格。
Get real-time price.

**参数 / Parameters**:
- `symbol` (str): 交易对 / Trading pair

**返回值 / Returns**:
- `float`: 当前价格 / Current price (or `None` if failed)

**使用示例 / Usage Example**:

```python
price = client.get_realtime_price('BTCUSDT')
print(f"Current BTC price: {price} USDT")
```

---

## 2. Data Processor Module / 数据处理模块

### 类 / Class: `DataProcessor`

用于数据预处理和特征工程。
Used for data preprocessing and feature engineering.

**位置 / Location**: `utils/data_processor.py`

---

#### 方法 1: `add_technical_indicators(df)`

向 DataFrame 添加技术指标特征。
Add technical indicator features to DataFrame.

**参数 / Parameters**:
- `df` (pandas.DataFrame): 包含 OHLCV 数据的 DataFrame
  - 必须包含列 / Must contain columns: `'open'`, `'high'`, `'low'`, `'close'`, `'volume'`

**返回值 / Returns**:
- `pandas.DataFrame`: 添加了以下特征列的 DataFrame
  - `sma_7`: 7 周期简单移动平均线 / 7-period simple moving average
  - `sma_25`: 25 周期简单移动平均线 / 25-period simple moving average
  - `rsi_14`: 14 周期相对强弱指数 / 14-period relative strength index
  - `roc`: 5 周期价格变动率 / 5-period rate of change
  - `volatility`: 7 周期价格标准差 / 7-period price standard deviation

**使用示例 / Usage Example**:

```python
from utils.data_processor import DataProcessor

processor = DataProcessor()
df_with_features = processor.add_technical_indicators(df)

print(df_with_features[['timestamp', 'close', 'sma_7', 'sma_25', 'rsi_14']].head())
```

**技术指标说明 / Technical Indicators Explanation**:

| 指标 / Indicator | 计算方法 / Calculation | 用途 / Usage |
|------------------|----------------------|-------------|
| SMA (Simple Moving Average) | 过去 N 个周期的平均价格 / Average price over past N periods | 识别趋势方向 / Identify trend direction |
| RSI (Relative Strength Index) | 涨跌幅的平均比值 / Ratio of average gains to losses | 判断超买超卖 / Identify overbought/oversold |
| ROC (Rate of Change) | 价格变动的百分比 / Percentage change in price | 反映变化速度 / Reflect change speed |
| Volatility | 价格标准差 / Price standard deviation | 衡量风险 / Measure risk |

---

#### 方法 2: `prepare_features_labels(df, target_col='close', horizon=1)`

准备特征和标签用于机器学习。
Prepare features and labels for machine learning.

**参数 / Parameters**:
- `df` (pandas.DataFrame): 包含特征列的 DataFrame
- `target_col` (str): 目标列名 / Target column name (default: `'close'`)
- `horizon` (int): 预测的周期数 / Number of periods ahead to predict (default: `1`)

**返回值 / Returns**:
- `X` (pandas.DataFrame): 特征矩阵 / Feature matrix
- `y` (pandas.Series): 标签向量 / Label vector (0=下跌/DOWN, 1=上涨/UP)

**使用示例 / Usage Example**:

```python
X, y = processor.prepare_features_labels(df_with_features)

print(f"Feature matrix shape: {X.shape}")
print(f"Label vector shape: {y.shape}")
print(f"\nFirst 10 labels: {y.head(10).values}")
```

**标签定义 / Label Definition**:
- `0`: 价格下跌或持平 / Price down or unchanged (DOWN)
- `1`: 价格上涨 / Price up (UP)

---

## 3. Command Line Scripts / 命令行脚本

### 3.1 数据下载脚本 / Data Download Script

**文件 / File**: `scripts/download_data.py`

从币安下载历史数据并保存为 CSV 文件。
Download historical data from Binance and save as CSV files.

**用法 / Usage**:

```bash
python scripts/download_data.py --symbols BTCUSDT,ETHUSDT --interval 1h --start "6 months ago UTC"
```

**参数 / Parameters**:

| 参数 / Argument | 必需 / Required | 默认值 / Default | 说明 / Description |
|---------------|----------------|------------------|------------------|
| `--symbols` | 否 / No | `BTCUSDT,ETHUSDT` | 交易对列表，逗号分隔 / Comma-separated trading pairs |
| `--interval` | 否 / No | `1h` | K 线间隔 / K-line interval |
| `--start` | 否 / No | `2 years ago UTC` | 开始时间 / Start time |

**输出 / Output**:
- CSV 文件保存在 `data/` 目录 / CSV files saved in `data/` directory
- 文件命名格式 / File naming format: `{SYMBOL}_hist.csv`

**示例 / Examples**:

```bash
# 下载 BTC 和 ETH 的 1 小时数据
# Download 1-hour data for BTC and ETH
python scripts/download_data.py --symbols BTCUSDT,ETHUSDT

# 下载 BTC 的日线数据，从 1 年前开始
# Download daily data for BTC starting from 1 year ago
python scripts/download_data.py --symbols BTCUSDT --interval 1d --start "1 year ago UTC"
```

---

### 3.2 模型训练脚本 / Model Training Script

**文件 / File**: `scripts/train_model.py`

训练随机森林分类模型并保存。
Train Random Forest classifier model and save it.

**用法 / Usage**:

```bash
python scripts/train_model.py --symbol BTCUSDT --local_data data/BTCUSDT_hist.csv
```

**参数 / Parameters**:

| 参数 / Argument | 必需 / Required | 默认值 / Default | 说明 / Description |
|---------------|----------------|------------------|------------------|
| `--symbol` | 否 / No | `BTCUSDT` | 交易对符号 / Trading pair symbol |
| `--local_data` | 否 / No | `None` | 本地 CSV 文件路径 / Local CSV file path |

**输出 / Output**:
- 模型文件保存在 `models/` 目录 / Model file saved in `models/` directory
- 文件命名格式 / File naming format: `{SYMBOL}_price_model.pkl`

**训练过程 / Training Process**:
1. 加载数据（从币安或本地文件）/ Load data (from Binance or local file)
2. 添加技术指标特征 / Add technical indicator features
3. 划分训练集和测试集 (80%/20%) / Split train and test sets (80%/20%)
4. 训练随机森林模型 (100 棵树) / Train Random Forest (100 trees)
5. 评估模型性能 / Evaluate model performance
   - 准确率 / Accuracy
   - 分类报告 / Classification report
   - 5 折交叉验证 / 5-fold cross-validation
6. 保存模型 / Save model

**示例 / Examples**:

```bash
# 从币安获取数据并训练 BTC 模型
# Fetch data from Binance and train BTC model
python scripts/train_model.py --symbol BTCUSDT

# 使用本地数据训练模型
# Train model using local data
python scripts/train_model.py --symbol BTCUSDT --local_data data/BTCUSDT_hist.csv
```

---

### 3.3 回测脚本 / Backtesting Script

**文件 / File**: `scripts/backtest.py`

在历史数据上回测预测策略。
Backtest prediction strategy on historical data.

**用法 / Usage**:

```bash
python scripts/backtest.py --symbol BTCUSDT --model models/BTCUSDT_price_model.pkl --data data/BTCUSDT_hist.csv
```

**参数 / Parameters**:

| 参数 / Argument | 必需 / Required | 默认值 / Default | 说明 / Description |
|---------------|----------------|------------------|------------------|
| `--symbol` | 否 / No | `BTCUSDT` | 交易对符号 / Trading pair symbol |
| `--model` | 是 / Yes | - | 模型文件路径 / Model file path |
| `--data` | 是 / Yes | - | 数据文件路径 / Data file path |

**回测策略 / Backtesting Strategy**:
- 如果预测为上涨 (1): 买入/持有 / Buy/Hold
- 如果预测为下跌 (0): 卖出/持币 / Sell/Hold cash

**输出 / Output**:
- 收益对比图保存在 `data/` 目录 / Return comparison chart saved in `data/` directory
- 文件命名格式 / File naming format: `{SYMBOL}_backtest.png`

**性能指标 / Performance Metrics**:
- 策略最终累计收益 / Strategy final cumulative return
- 市场基准收益 / Market benchmark return (买入并持有 / Buy and Hold)

---

## 4. Flask Web API / Flask Web 应用接口

### 启动 Web 应用 / Start Web Application

**文件 / File**: `scripts/app.py`

启动 Flask Web 服务器。
Start Flask web server.

**用法 / Usage**:

```bash
python scripts/app.py
```

**访问地址 / Access URL**: `http://localhost:5000`

---

### API 端点 / API Endpoints

#### GET `/`

主页 / Home page

**响应 / Response**: HTML 页面 / HTML page

---

#### GET `/predict/<symbol>`

预测页面 / Prediction page

**参数 / Parameter**:
- `symbol`: 交易对 / Trading pair (e.g., `BTCUSDT`, `ETHUSDT`)

**响应 / Response**: HTML 页面显示预测结果 / HTML page showing prediction result

---

#### GET `/api/predict/<symbol>`

预测 API 端点 / Prediction API endpoint

**参数 / Parameter**:
- `symbol`: 交易对 / Trading pair (e.g., `BTCUSDT`, `ETHUSDT`)

**响应 / Response** (JSON):

```json
{
  "symbol": "BTCUSDT",
  "current_price": 43250.5,
  "prediction": "UP",
  "confidence": 0.65,
  "timestamp": "2024-01-15 10:30:00"
}
```

**响应字段 / Response Fields**:

| 字段 / Field | 类型 / Type | 说明 / Description |
|-------------|-------------|------------------|
| `symbol` | str | 交易对 / Trading pair |
| `current_price` | float | 当前价格 (USDT) / Current price |
| `prediction` | str | 预测结果 / Prediction result (`"UP"` or `"DOWN"`) |
| `confidence` | float | 预测置信度 / Prediction confidence (0-1) |
| `timestamp` | str | 数据时间戳 / Data timestamp |

**错误响应 / Error Response**:

```json
{
  "error": "Model for BTCUSDT not found. Please train it first."
}
```

**状态码 / Status Codes**:
- `200`: 成功 / Success
- `404`: 模型未找到 / Model not found
- `500`: 服务器错误 / Server error

**使用示例 / Usage Example**:

```python
import requests

# 获取 BTC 预测
# Get BTC prediction
response = requests.get('http://localhost:5000/api/predict/BTCUSDT')
data = response.json()

if 'error' not in data:
    print(f"Symbol: {data['symbol']}")
    print(f"Current Price: ${data['current_price']}")
    print(f"Prediction: {data['prediction']}")
    print(f"Confidence: {data['confidence']*100:.2f}%")
else:
    print(f"Error: {data['error']}")
```

---

## 📚 完整示例 / Complete Example

### 从头到尾的完整工作流 / Complete End-to-End Workflow

```python
# 1. 导入库 / Import libraries
from utils.binance_client import BinanceUtility
from utils.data_processor import DataProcessor
from sklearn.ensemble import RandomForestClassifier
import joblib

# 2. 获取数据 / Fetch data
client = BinanceUtility()
df = client.fetch_historical_data('BTCUSDT', '1h', '6 months ago UTC')

# 3. 特征工程 / Feature engineering
processor = DataProcessor()
df_features = processor.add_technical_indicators(df)
X, y = processor.prepare_features_labels(df_features)

# 4. 训练模型 / Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. 保存模型 / Save model
joblib.dump(model, 'models/BTCUSDT_price_model.pkl')

# 6. 使用模型预测 / Use model to predict
latest_data = X.tail(1)
prediction = model.predict(latest_data)
probability = model.predict_proba(latest_data)

print(f"Prediction: {'UP' if prediction[0] == 1 else 'DOWN'}")
print(f"Confidence: {probability[0].max()*100:.2f}%")
```

---

## 🆘 常见问题 / Common Questions

### Q: 如何使用其他交易对？
**A**: 将 `symbol` 参数改为其他币种，例如 `ETHUSDT`, `ADAUSDT` 等。

### Q: 如何改变预测时间范围？
**A**: 修改 `prepare_features_labels` 函数中的 `horizon` 参数。

### Q: 模型准确率太低怎么办？
**A**:
- 尝试增加训练数据量
- 调整模型参数（如 n_estimators, max_depth）
- 尝试其他机器学习算法
- 添加更多特征

### Q: 如何获取实时数据？
**A**: 使用 `BinanceUtility().get_realtime_price(symbol)` 方法。

---

**更多帮助 / More Help**: 查看 [README.md](README.md) 或 [TUTORIAL.md](TUTORIAL.md)

