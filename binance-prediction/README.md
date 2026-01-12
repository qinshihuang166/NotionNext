# Binance 币价预测项目 / Binance Price Prediction Project

这是一个专为初学者设计的币安 (Binance) 加密货币价格预测分析项目。通过使用机器学习，我们可以根据历史价格数据预测未来的价格走势。

## 项目特点
- **Binance API 集成**: 自动获取实时和历史 K 线数据。
- **特征工程**: 自动计算 SMA, RSI, ROC 等技术指标。
- **机器学习模型**: 使用随机森林算法进行价格涨跌预测。
- **回测系统**: 在历史数据上测试预测策略的有效性。
- **Web 仪表盘**: 简单的 Flask Web 界面显示预测结果。
- **对新手友好**: 提供详细的中文文档和 Jupyter Notebook 教程。

## 项目结构
```
binance-prediction/
├── data/              # 存储历史价格 CSV 数据
├── models/            # 存储训练好的模型文件
├── scripts/           # 核心脚本 (训练、回测、Web App)
├── utils/             # 工具类 (API 调用、数据处理)
├── notebooks/         # Jupyter Notebook 交互式教程
├── requirements.txt   # 项目依赖
├── README.md          # 项目概览
├── SETUP.md           # 环境搭建指南
├── API.md             # 接口文档
└── TUTORIAL.md        # 分步学习指南
```

## 快速开始

### 1. 克隆项目并安装依赖
```bash
cd binance-prediction
pip install -r requirements.txt
```

### 2. 下载数据
```bash
python scripts/download_data.py --symbols BTCUSDT,ETHUSDT
```

### 3. 训练模型
```bash
python scripts/train_model.py --symbol BTCUSDT
```

### 4. 运行回测
```bash
python scripts/backtest.py --symbol BTCUSDT --model models/BTCUSDT_price_model.pkl --data data/BTCUSDT_hist.csv
```

### 5. 启动 Web 仪表盘
```bash
python scripts/app.py
```
访问 `http://localhost:5000` 查看预测结果。

## 贡献者
- qinshihuang166

## GitHub 部署说明 (针对 qinshihuang166)
1. 在 GitHub 上创建一个新的仓库，命名为 `binance-price-prediction`。
2. 在本地进入 `binance-prediction` 目录：
   ```bash
   cd binance-prediction
   git init
   git add .
   git commit -m "Initial commit: Binance Price Prediction Project"
   git branch -M main
   git remote add origin https://github.com/qinshihuang166/binance-price-prediction.git
   git push -u origin main
   ```

## 免责声明
本项目的预测结果仅供参考，不构成任何投资建议。加密货币市场具有高风险，请谨慎决策。
