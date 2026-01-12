# Binance 币价预测项目 / Binance Price Prediction Project

这是一个专为初学者设计的币安 (Binance) 加密货币价格预测分析项目。通过使用机器学习，我们可以根据历史价格数据预测未来的价格走势。

This is a Binance cryptocurrency price prediction analysis project designed specifically for beginners. By using machine learning, we can predict future price trends based on historical price data.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🌟 项目特点 / Project Features

- **📊 Binance API 集成**: 自动获取实时和历史 K 线数据 / Automatically fetch real-time and historical K-line data
- **🔧 特征工程**: 自动计算 SMA, RSI, ROC 等技术指标 / Automatically calculate technical indicators like SMA, RSI, ROC
- **🤖 机器学习模型**: 使用随机森林算法进行价格涨跌预测 / Use Random Forest algorithm for price movement prediction
- **📈 回测系统**: 在历史数据上测试预测策略的有效性 / Test prediction strategy effectiveness on historical data
- **🌐 Web 仪表盘**: 简单的 Flask Web 界面显示预测结果 / Simple Flask web interface to display prediction results
- **📚 对新手友好**: 提供详细的中文文档和 Jupyter Notebook 教程 / Provide detailed Chinese documentation and Jupyter Notebook tutorials
- **🎨 数据可视化**: 丰富的图表展示分析结果 / Rich charts to display analysis results
- **⚡ 实时预测**: 支持对当前市场进行实时价格预测 / Support real-time price prediction on current market

## 📁 项目结构 / Project Structure

```
binance-prediction/
├── data/                          # 存储历史价格 CSV 数据 / Store historical price CSV data
├── models/                        # 存储训练好的模型文件 / Store trained model files
├── scripts/                       # 核心脚本 / Core scripts
│   ├── app.py                     # Flask Web 应用 / Flask web application
│   ├── backtest.py                # 回测脚本 / Backtesting script
│   ├── download_data.py           # 数据下载脚本 / Data download script
│   ├── predict.py                 # 实时预测脚本 / Real-time prediction script
│   └── train_model.py             # 模型训练脚本 / Model training script
├── utils/                         # 工具类 / Utility classes
│   ├── binance_client.py          # Binance API 客户端 / Binance API client
│   ├── data_processor.py          # 数据处理和特征工程 / Data processing and feature engineering
│   └── visualizer.py              # 数据可视化工具 / Data visualization utility
├── notebooks/                     # Jupyter Notebook 交互式教程 / Interactive tutorials
│   ├── 01_Data_Exploration.ipynb  # 数据探索 / Data exploration
│   ├── 02_Feature_Engineering.ipynb  # 特征工程 / Feature engineering
│   ├── Analysis.ipynb             # 完整分析流程 / Complete analysis workflow
│   └── README.md                  # 笔记本使用指南 / Notebook usage guide
├── .github/workflows/             # GitHub Actions 工作流 / GitHub Actions workflows
│   └── test.yml                   # 自动化测试 / Automated testing
├── .env.example                   # 环境变量示例 / Environment variables example
├── .gitignore                     # Git 忽略文件 / Git ignore file
├── requirements.txt               # 项目依赖 / Project dependencies
├── setup.sh                       # 一键安装脚本 / One-click installation script
├── README.md                      # 项目概览（本文件）/ Project overview (this file)
├── QUICKSTART.md                  # 快速入门指南 / Quick start guide
├── SETUP.md                       # 详细环境搭建指南 / Detailed environment setup guide
├── API.md                         # 接口文档 / API documentation
└── TUTORIAL.md                    # 分步学习指南 / Step-by-step tutorial
```

## 🚀 快速开始 / Quick Start

### 方式 1: 使用快速入门指南 / Use Quick Start Guide

强烈推荐新手先阅读 [QUICKSTART.md](./QUICKSTART.md)，里面有详细的 10 分钟快速上手教程。
Highly recommend beginners to read [QUICKSTART.md](./QUICKSTART.md) first, which contains a detailed 10-minute quick start tutorial.

### 方式 2: 5 命令快速运行 / 5 Commands to Quick Run

```bash
# 1. 安装依赖 / Install dependencies
pip install -r requirements.txt

# 2. 下载数据 / Download data
python scripts/download_data.py --symbols BTCUSDT

# 3. 训练模型 / Train model
python scripts/train_model.py --symbol BTCUSDT

# 4. 运行回测 / Run backtest
python scripts/backtest.py --symbol BTCUSDT --model models/BTCUSDT_price_model.pkl --data data/BTCUSDT_hist.csv

# 5. 进行实时预测 / Make real-time prediction
python scripts/predict.py --symbol BTCUSDT
```

### 方式 3: 一键安装（Linux/Mac）/ One-Click Installation (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
```

### 启动 Web 仪表盘 / Start Web Dashboard

```bash
python scripts/app.py
```
访问 `http://localhost:5000` 查看预测结果 / Visit `http://localhost:5000` to view prediction results.

## 📖 学习路径 / Learning Path

### 🎯 完全初学者 / Absolute Beginners

建议按以下顺序学习：
Follow this order:

1. **📚 阅读 [QUICKSTART.md](./QUICKSTART.md)** - 10 分钟快速上手
2. **💻 运行 [notebooks/01_Data_Exploration.ipynb](./notebooks/01_Data_Exploration.ipynb)** - 学习数据获取和探索
3. **🔧 运行 [notebooks/02_Feature_Engineering.ipynb](./notebooks/02_Feature_Engineering.ipynb)** - 学习特征工程
4. **🤖 运行 [notebooks/Analysis.ipynb](./notebooks/Analysis.ipynb)** - 完整的模型训练流程

### 🚀 有一定基础 / With Some Background

直接运行脚本 / Run scripts directly:
```bash
python scripts/train_model.py --symbol BTCUSDT
python scripts/predict.py --symbol BTCUSDT
```

## 📚 文档导航 / Documentation Navigation

| 文档 / Document | 描述 / Description |
|-----------------|-------------------|
| [QUICKSTART.md](./QUICKSTART.md) | 10 分钟快速入门指南 / Quick start guide |
| [SETUP.md](./SETUP.md) | 详细环境搭建指南 / Environment setup |
| [API.md](./API.md) | API 接口文档 / API documentation |
| [TUTORIAL.md](./TUTORIAL.md) | 分步学习指南 / Learning guide |
| [notebooks/README.md](./notebooks/README.md) | Notebook 使用指南 / Notebook guide |

## 🛠️ 核心功能 / Core Features

- **数据获取**: 支持多种时间间隔（1m, 5m, 1h, 1d 等）
- **特征工程**: SMA, RSI, ROC, Volatility
- **模型训练**: 随机森林，支持交叉验证
- **回测系统**: 模拟历史交易表现
- **实时预测**: 对当前市场进行预测
- **Web 仪表盘**: Flask Web 应用展示结果

## 🛡️ 免责声明 / Disclaimer

**⚠️ 重要提示：本项目的预测结果仅供参考，不构成任何投资建议。加密货币市场具有高风险，价格波动剧烈，请根据自身情况谨慎决策。**

## 👥 贡献者 / Contributors

- **qinshihuang166** - 项目发起者

## 📄 许可证 / License

MIT License - 详见 [LICENSE](./LICENSE) 文件。

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！⭐**

Made with ❤️ by qinshihuang166

</div>
