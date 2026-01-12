# 快速入门指南 / Quick Start Guide

欢迎来到 Binance 币价预测项目！本指南将帮助你在 10 分钟内完成从安装到首次预测的全过程。

Welcome to the Binance Price Prediction Project! This guide will help you complete the entire process from installation to your first prediction in 10 minutes.

## 📋 前置条件 / Prerequisites

确保你的系统已安装以下软件：
Make sure you have the following software installed:

- Python 3.8 或更高版本 / Python 3.8 or higher
- pip (Python 包管理器 / Python package manager)
- Git (可选，用于克隆项目 / Optional, for cloning the project)

## 🚀 5步快速开始 / 5 Steps to Get Started

### 步骤 1: 安装依赖 / Step 1: Install Dependencies

打开终端 / Open your terminal and run:

```bash
cd binance-prediction
pip install -r requirements.txt
```

如果安装速度慢，可以使用清华源 / If installation is slow, use Tsinghua mirror:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤 2: 下载历史数据 / Step 2: Download Historical Data

下载比特币和以太坊的历史价格数据：
Download historical price data for Bitcoin and Ethereum:

```bash
python scripts/download_data.py --symbols BTCUSDT,ETHUSDT
```

**预期输出 / Expected Output:**
```
正在下载 BTCUSDT... / Downloading BTCUSDT...
成功保存到 data/BTCUSDT_hist.csv / Successfully saved to data/BTCUSDT_hist.csv
正在下载 ETHUSDT... / Downloading ETHUSDT...
成功保存到 data/ETHUSDT_hist.csv / Successfully saved to data/ETHUSDT_hist.csv
```

### 步骤 3: 训练机器学习模型 / Step 3: Train Machine Learning Model

使用下载的数据训练预测模型：
Train a prediction model using the downloaded data:

```bash
python scripts/train_model.py --symbol BTCUSDT
```

**预期输出 / Expected Output:**
```
加载本地数据: data/BTCUSDT_hist.csv / Loading local data...
正在进行特征工程... / Feature engineering...
正在训练随机森林模型... / Training Random Forest model...

模型准确率 / Model Accuracy: 0.5234

分类报告 / Classification Report:
              precision    recall  f1-score   support
           0       0.52      0.55      0.53      1752
           1       0.53      0.50      0.51      1752
    accuracy                           0.52      3504
   macro avg       0.52      0.52      0.52      3504
weighted avg       0.52      0.52      0.52      3504

5折交叉验证平均分 / 5-Fold CV Mean Score: 0.5100

模型已保存至: models/BTCUSDT_price_model.pkl / Model saved to: models/BTCUSDT_price_model.pkl
```

### 步骤 4: 运行回测 / Step 4: Run Backtest

测试模型在历史数据上的表现：
Test model performance on historical data:

```bash
python scripts/backtest.py --symbol BTCUSDT --model models/BTCUSDT_price_model.pkl --data data/BTCUSDT_hist.csv
```

**预期输出 / Expected Output:**
```
开始对 BTCUSDT 进行回测... / Starting backtest for BTCUSDT...
回测图表已保存至: data/BTCUSDT_backtest.png / Backtest chart saved to: data/BTCUSDT_backtest.png
策略最终累计收益 / Final Strategy Return: 0.9876
市场基准最终收益 / Final Market Return: 1.0123
```

### 步骤 5: 进行实时预测 / Step 5: Make Real-time Prediction

使用训练好的模型预测当前市场趋势：
Use the trained model to predict current market trend:

```bash
python scripts/predict.py --symbol BTCUSDT
```

**预期输出 / Expected Output:**
```
============================================================
📈 BTCUSDT 价格预测报告 / Price Prediction Report
============================================================

⏰ 预测时间 / Prediction Time: 2024-01-15 14:30:45
💰 当前价格 / Current Price: 43250.75 USDT

📊 技术指标 / Technical Indicators:
   • SMA (7): 43210.50
   • SMA (25): 42890.25
   • RSI (14): 55.32
   • 波动率 / Volatility: 234.56

🎯 预测结果 / Prediction Result:
   ↗️  价格趋势 / Trend: 📈 上涨 / UP
   ✅ 上涨概率 / Probability: 52.35%

⚠️  风险提示 / Risk Warning:
   本预测仅供参考，不构成投资建议。
   This prediction is for reference only and does not constitute investment advice.
============================================================
```

## 🌐 启动 Web 仪表盘 / Start Web Dashboard

想要一个漂亮的图形界面？启动 Flask Web 应用：
Want a beautiful graphical interface? Start the Flask web app:

```bash
python scripts/app.py
```

然后打开浏览器访问 / Then open your browser and visit:
- **URL:** http://localhost:5000
- **功能：** 选择交易对，查看实时预测结果
- **Features:** Select trading pairs, view real-time predictions

## 📚 学习更多 / Learn More

### 使用 Jupyter Notebook 交互式学习
Interactive learning with Jupyter Notebook:

```bash
jupyter notebook notebooks/Analysis.ipynb
```

### 查看完整文档 / Read Complete Documentation

- **README.md** - 项目概述 / Project Overview
- **SETUP.md** - 详细环境配置 / Detailed Environment Setup
- **API.md** - API 接口文档 / API Documentation
- **TUTORIAL.md** - 分步学习指南 / Step-by-Step Tutorial

## 🔧 常见问题 / Frequently Asked Questions

### Q1: 预测准确率为什么只有 50% 左右？
**Q1: Why is the prediction accuracy only around 50%?**

A: 加密货币市场非常随机，50% 左右的准确率在短期内是正常的。这个项目主要用于学习机器学习和数据分析，而不是用于实际交易。
A: Cryptocurrency markets are highly random, and around 50% accuracy is normal for short-term predictions. This project is for learning ML and data analysis, not for actual trading.

### Q2: 需要币安 API Key 吗？
**Q2: Do I need a Binance API Key?**

A: 本项目使用的是币安的公开数据接口，不需要 API Key 也能运行。但如果需要更高的请求速率限制，可以申请免费 API Key。
A: This project uses Binance's public data endpoints, so you can run it without an API Key. However, if you need higher rate limits, you can apply for a free API Key.

### Q3: 可以预测其他交易对吗？
**Q3: Can I predict other trading pairs?**

A: 可以！只需要在命令中指定不同的交易对符号，例如：
A: Yes! Just specify a different trading pair symbol, for example:

```bash
# 下载数据 / Download data
python scripts/download_data.py --symbols ADAUSDT,SOLUSDT

# 训练模型 / Train model
python scripts/train_model.py --symbol ADAUSDT

# 预测 / Predict
python scripts/predict.py --symbol ADAUSDT
```

### Q4: 模型训练需要多长时间？
**Q4: How long does model training take?**

A: 在普通电脑上，使用 1 年的 1 小时数据训练 Random Forest 模型大约需要 1-5 分钟。
A: On a regular computer, training a Random Forest model with 1 year of hourly data takes about 1-5 minutes.

### Q5: 数据存储在哪里？
**Q5: Where is the data stored?**

A: - 历史数据 CSV: `data/` 目录
   A: - Historical data CSV: `data/` directory
   - 训练好的模型: `models/` 目录
   - Trained models: `models/` directory
   - 回测图表: `data/` 目录
   - Backtest charts: `data/` directory

## 🎓 下一步 / Next Steps

1. **探索特征工程 / Explore Feature Engineering:**
   - 修改 `utils/data_processor.py` 添加新的技术指标
   - Modify `utils/data_processor.py` to add new technical indicators

2. **尝试不同的模型 / Try Different Models:**
   - 在 `scripts/train_model.py` 中使用其他机器学习算法
   - Use other ML algorithms in `scripts/train_model.py`

3. **优化超参数 / Optimize Hyperparameters:**
   - 调整 Random Forest 的参数（n_estimators, max_depth 等）
   - Adjust Random Forest parameters (n_estimators, max_depth, etc.)

4. **深入可视化 / Deep Dive into Visualization:**
   - 使用 `utils/visualizer.py` 创建更多图表
   - Use `utils/visualizer.py` to create more charts

## ⚠️ 重要免责声明 / Important Disclaimer

**本项目的预测结果仅供参考，不构成任何投资建议。加密货币市场具有高风险，价格波动剧烈。请根据自身情况谨慎决策，投资有风险，入市需谨慎。**

**The prediction results of this project are for reference only and do not constitute any investment advice. Cryptocurrency markets carry high risks and prices are highly volatile. Please make decisions carefully based on your own situation. Investing involves risks, please be cautious when entering the market.**

## 🆘 获取帮助 / Get Help

如果遇到问题，请：
If you encounter issues, please:

1. 检查 Python 版本是否 >= 3.8
2. 确保所有依赖已正确安装
3. 查看错误日志并搜索解决方案
4. 阅读相关文档（SETUP.md, API.md）

Happy Learning! 🎉
祝学习愉快！🎉
