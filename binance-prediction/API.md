# API 文档 / API Documentation

本项目分为几个核心模块，每个模块都有其特定的功能。

## 1. `utils.binance_client.BinanceUtility`
用于与币安 API 交互。

### `fetch_historical_data(symbol, interval, start_str)`
- **功能**: 获取历史 K 线数据。
- **参数**:
  - `symbol`: 交易对，如 `'BTCUSDT'`。
  - `interval`: 时间频率，如 `'1h'`, `'1d'`。
  - `start_str`: 开始时间，如 `'1 year ago UTC'`。

## 2. `utils.data_processor.DataProcessor`
用于数据预处理和特征生成。

### `add_technical_indicators(df)`
- **功能**: 向 DataFrame 添加 SMA, RSI 等指标。

### `prepare_features_labels(df, horizon=1)`
- **功能**: 将数据转换为模型可用的 X (特征) 和 y (标签)。

## 3. `scripts/train_model.py`
模型训练脚本。

- **用法**: `python scripts/train_model.py --symbol BTCUSDT`
- **输出**: 保存模型到 `models/` 目录。

## 4. `scripts/backtest.py`
策略回测脚本。

- **用法**: `python scripts/backtest.py --symbol BTCUSDT --model path/to/model --data path/to/data`
- **输出**: 生成 `data/symbol_backtest.png` 收益对比图。
