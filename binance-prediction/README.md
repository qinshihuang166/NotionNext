# Binance 币价预测项目 / Binance Price Prediction Project

这是一个专为初学者设计的币安 (Binance) 加密货币价格预测分析项目。通过使用机器学习，我们可以根据历史价格数据预测未来的价格走势。

A cryptocurrency price prediction analysis project designed specifically for beginners. Using machine learning, we can predict future price trends based on historical price data.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📊 项目特点 / Project Features

- **Binance API 集成**: 自动获取实时和历史 K 线数据 / Automatic fetching of real-time and historical K-line data
- **特征工程**: 自动计算 SMA, RSI, ROC, Volatility 等技术指标 / Automatic calculation of technical indicators
- **机器学习模型**: 使用随机森林算法进行价格涨跌预测 / Random Forest algorithm for price movement prediction
- **回测系统**: 在历史数据上测试预测策略的有效性 / Backtesting prediction strategies on historical data
- **Web 仪表盘**: 简单的 Flask Web 界面显示预测结果 / Simple Flask web interface to display prediction results
- **对新手友好**: 提供详细的中文文档和 Jupyter Notebook 教程 / Detailed Chinese documentation and Jupyter Notebook tutorials

## 📁 项目结构 / Project Structure

```
binance-prediction/
├── data/              # 存储历史价格 CSV 数据 / Store historical price CSV data
├── models/            # 存储训练好的模型文件 / Store trained model files
├── scripts/           # 核心脚本 (训练、回测、Web App) / Core scripts
│   ├── download_data.py     # 数据下载脚本 / Data download script
│   ├── train_model.py       # 模型训练脚本 / Model training script
│   ├── backtest.py          # 回测脚本 / Backtesting script
│   ├── app.py               # Flask Web 应用 / Flask web app
│   └── templates/           # HTML 模板 / HTML templates
├── utils/             # 工具类 (API 调用、数据处理) / Utility classes
│   ├── binance_client.py    # Binance API 客户端 / Binance API client
│   └── data_processor.py    # 数据处理器 / Data processor
├── notebooks/         # Jupyter Notebook 交互式教程 / Interactive tutorials
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   └── 03_Model_Training.ipynb
├── .github/           # GitHub Actions 工作流 / GitHub Actions workflows
│   └── workflows/
│       └── test.yml   # 自动化测试 / Automated testing
├── requirements.txt   # 项目依赖 / Project dependencies
├── .env.example       # 环境变量示例 / Environment variable example
├── .gitignore         # Git 忽略文件 / Git ignore file
├── setup.sh           # 一键设置脚本 / One-click setup script
├── README.md          # 项目概览 / Project overview
├── SETUP.md           # 环境搭建指南 / Environment setup guide
├── API.md             # 接口文档 / API documentation
└── TUTORIAL.md        # 分步学习指南 / Step-by-step tutorial
```

## 🚀 快速开始 / Quick Start

### 方式 1: 使用命令行脚本 / Method 1: Using Command Line Scripts

#### 1. 安装依赖 / Install Dependencies
```bash
cd binance-prediction
pip install -r requirements.txt
```

#### 2. 下载历史数据 / Download Historical Data
```bash
python scripts/download_data.py --symbols BTCUSDT,ETHUSDT
```

#### 3. 训练模型 / Train Model
```bash
python scripts/train_model.py --symbol BTCUSDT
```

#### 4. 运行回测 / Run Backtest
```bash
python scripts/backtest.py --symbol BTCUSDT --model models/BTCUSDT_price_model.pkl --data data/BTCUSDT_hist.csv
```

#### 5. 启动 Web 仪表盘 / Start Web Dashboard
```bash
python scripts/app.py
```
访问 `http://localhost:5000` 查看预测结果。
Visit `http://localhost:5000` to view prediction results.

### 方式 2: 使用 Jupyter Notebooks 学习 / Method 2: Learning with Jupyter Notebooks

推荐初学者使用 Jupyter Notebooks 逐步学习每个环节。
Beginners are recommended to use Jupyter Notebooks to learn each step gradually.

```bash
# 启动 Jupyter Notebook / Start Jupyter Notebook
jupyter notebook

# 然后在浏览器中打开以下教程 / Then open the following tutorials in your browser:
# 1. notebooks/01_Data_Exploration.ipynb - 数据获取与探索 / Data fetching and exploration
# 2. notebooks/02_Feature_Engineering.ipynb - 特征工程 / Feature engineering
# 3. notebooks/03_Model_Training.ipynb - 模型训练与评估 / Model training and evaluation
```

### 一键设置 / One-Click Setup (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
```

## 📚 学习路径 / Learning Path

1. **阅读文档** / Read Documentation
   - [README.md](README.md) - 项目概览 / Project overview
   - [SETUP.md](SETUP.md) - 环境搭建指南 / Environment setup guide
   - [TUTORIAL.md](TUTORIAL.md) - 分步学习指南 / Step-by-step tutorial
   - [API.md](API.md) - 接口文档 / API documentation

2. **运行教程** / Run Tutorials
   - 按顺序运行三个 Jupyter Notebook / Run the three Jupyter Notebooks in order
   - 每个笔记本都有详细的中文和英文注释 / Each notebook has detailed Chinese and English comments

3. **实践项目** / Practice the Project
   - 使用命令行脚本训练自己的模型 / Train your own model using command line scripts
   - 运行回测验证策略效果 / Run backtesting to verify strategy effectiveness
   - 启动 Web 应用查看实时预测 / Start web app to view real-time predictions

## 🎯 核心功能说明 / Core Features Explanation

### 1. 数据获取 / Data Fetching
- 从 Binance API 获取历史 K 线数据 / Fetch historical K-line data from Binance API
- 支持多种时间间隔（1m, 5m, 1h, 1d） / Support multiple time intervals
- 自动处理缺失数据和异常值 / Automatically handle missing data and outliers

### 2. 特征工程 / Feature Engineering
- **SMA (Simple Moving Average)**: 简单移动平均线 / Simple moving average
- **RSI (Relative Strength Index)**: 相对强弱指数 / Relative strength index
- **ROC (Rate of Change)**: 变动率 / Rate of change
- **Volatility**: 波动率 / Volatility

### 3. 机器学习模型 / Machine Learning Model
- 使用随机森林分类器 / Using Random Forest classifier
- 预测下一个周期的价格涨跌 / Predict price movement in the next period
- 输出预测概率和置信度 / Output prediction probability and confidence

### 4. 回测系统 / Backtesting System
- 模拟历史交易策略 / Simulate historical trading strategies
- 计算累计收益率 / Calculate cumulative returns
- 对比策略与基准收益 / Compare strategy with benchmark returns
- 生成可视化图表 / Generate visualization charts

### 5. Web 仪表盘 / Web Dashboard
- 简洁的用户界面 / Clean user interface
- 实时价格显示 / Real-time price display
- 预测结果可视化 / Prediction result visualization
- 支持多个交易对 / Support multiple trading pairs

## 📖 技术指标说明 / Technical Indicators Explanation

| 指标 / Indicator | 中文名 / Chinese Name | 说明 / Description | 用途 / Usage |
|-----------------|---------------------|------------------|--------------|
| SMA | 简单移动平均线 | 计算过去 N 个周期的平均价格 | 识别趋势方向 / Identify trend direction |
| RSI | 相对强弱指数 | 衡量价格变动的速度和变化 | 判断超买超卖 / Identify overbought/oversold |
| ROC | 变动率 | 价格变动的百分比 | 反映价格变化速度 / Reflect price change speed |
| Volatility | 波动率 | 价格变动的标准差 | 衡量市场风险 / Measure market risk |

## 🤝 贡献者 / Contributors

- **qinshihuang166** - 项目创建者 / Project Creator

## 📝 GitHub 部署说明 (针对 qinshihuang166)

### 1. 创建新的 GitHub 仓库 / Create New GitHub Repository
1. 登录 [GitHub](https://github.com/) 并点击 "New repository"
   Login to [GitHub](https://github.com/) and click "New repository"
2. 仓库名称命名为 `binance-price-prediction`
   Name the repository `binance-price-prediction`
3. 选择 "Public" 或 "Private"
   Choose "Public" or "Private"
4. 点击 "Create repository"
   Click "Create repository"

### 2. 上传代码到 GitHub / Upload Code to GitHub
在本地终端中运行以下命令：
Run the following commands in your local terminal:

```bash
# 进入项目目录 / Enter project directory
cd binance-prediction

# 初始化 Git 仓库 / Initialize Git repository
git init

# 添加所有文件到暂存区 / Add all files to staging area
git add .

# 创建初始提交 / Create initial commit
git commit -m "Initial commit: Binance Price Prediction Project"

# 重命名主分支为 main / Rename main branch to main
git branch -M main

# 添加远程仓库 / Add remote repository
git remote add origin https://github.com/qinshihuang166/binance-price-prediction.git

# 推送到 GitHub / Push to GitHub
git push -u origin main
```

### 3. 后续更新 / Future Updates
当你对项目进行修改后，使用以下命令提交更改：
After making changes to the project, use the following commands to commit:

```bash
# 查看修改的文件 / View modified files
git status

# 添加修改的文件 / Add modified files
git add .

# 提交更改 / Commit changes
git commit -m "描述你的更改 / Describe your changes"

# 推送到 GitHub / Push to GitHub
git push
```

## ⚠️ 免责声明 / Disclaimer

本项目的预测结果仅供参考，不构成任何投资建议。加密货币市场具有高风险，价格波动极大，投资需谨慎。

The prediction results of this project are for reference only and do not constitute any investment advice. The cryptocurrency market is highly risky with extreme price volatility. Invest with caution.

**重要提示 / Important Notes:**
- 历史表现不代表未来结果 / Past performance does not guarantee future results
- 机器学习模型可能失效 / Machine learning models may fail
- 加密货币投资存在本金损失风险 / Cryptocurrency investment carries risk of capital loss
- 请仅在你能承受损失的范围内投资 / Only invest within your acceptable loss range

## 📞 联系方式 / Contact

如有问题或建议，欢迎通过以下方式联系：
For questions or suggestions, feel free to contact via:

- 创建 GitHub Issue / Create a GitHub Issue
- 发送邮件 / Send email (如适用 / if applicable)

## 📄 许可证 / License

MIT License

Copyright (c) 2024 qinshihuang166

---

**祝你学习愉快！/ Happy Learning!** 🎉

如有任何问题，请查阅 [TUTORIAL.md](TUTORIAL.md) 或创建 Issue。
If you have any questions, please check [TUTORIAL.md](TUTORIAL.md) or create an Issue.
