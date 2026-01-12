# Jupyter Notebooks 教程 / Jupyter Notebooks Tutorials

本目录包含交互式学习笔记本，帮助你逐步掌握币价预测的每个步骤。
This directory contains interactive learning notebooks to help you master each step of price prediction.

## 📚 笔记本列表 / Notebook List

### 1. [01_Data_Exploration.ipynb](./01_Data_Exploration.ipynb) - 数据探索
**学习时间 / Learning Time:** 30 分钟

**内容 / Contents:**
- 如何使用 Binance API 获取历史数据
- 理解 K 线数据结构（开盘价、最高价、最低价、收盘价、成交量）
- 基本数据统计和信息查看
- 可视化价格和成交量趋势
- 保存数据到本地文件

**适合人群 / For:**
- 完全的初学者
- 想了解加密货币数据结构的人

**前置知识 / Prerequisites:**
- 基本的 Python 语法
- 会运行 Jupyter Notebook

---

### 2. [02_Feature_Engineering.ipynb](./02_Feature_Engineering.ipynb) - 特征工程
**学习时间 / Learning Time:** 45 分钟

**内容 / Contents:**
- 理解特征工程的概念和重要性
- 计算技术指标：
  - SMA（简单移动平均线）
  - RSI（相对强弱指数）
  - ROC（变化率）
  - Volatility（波动率）
- 创建预测标签（上涨/下跌）
- 特征统计分析
- 特征相关性分析

**适合人群 / For:**
- 了解基础数据的人
- 想学习机器学习特征工程的人

**前置知识 / Prerequisites:**
- 完成 Notebook 1
- 基本的 Pandas 和 NumPy 知识

---

### 3. [Analysis.ipynb](./Analysis.ipynb) - 完整分析流程
**学习时间 / Learning Time:** 60 分钟

**内容 / Contents:**
- 端到端的完整分析流程
- 数据获取 → 特征工程 → 模型训练 → 预测 → 可视化
- 快速原型开发
- 模型性能评估

**适合人群 / For:**
- 想看完整流程的人
- 有一定机器学习基础的人

**前置知识 / Prerequisites:**
- 了解基本的机器学习概念
- 熟悉 Scikit-learn

---

## 🚀 如何使用 / How to Use

### 方法 1: 使用 Jupyter Notebook
```bash
# 安装 Jupyter（如果未安装）
pip install jupyter

# 启动 Jupyter
jupyter notebook

# 在浏览器中打开相应的 notebook 文件
```

### 方法 2: 使用 JupyterLab（推荐）
```bash
# 安装 JupyterLab
pip install jupyterlab

# 启动 JupyterLab
jupyter lab
```

### 方法 3: 使用 VS Code
1. 安装 VS Code
2. 安装 Python 和 Jupyter 扩展
3. 直接打开 .ipynb 文件

---

## 📖 学习建议 / Learning Tips

### 推荐学习顺序 / Recommended Order:
1. **初学者路径 / Beginner Path:**
   - Notebook 1 (Data Exploration)
   - Notebook 2 (Feature Engineering)
   - Notebook 3 (Complete Analysis)

2. **进阶者路径 / Advanced Path:**
   - 直接从 Notebook 3 开始
   - 根据需要回头查看其他 notebook

### 学习技巧 / Learning Tips:
- ✅ **逐个运行代码单元格 / Run cells one by one**
  - 理解每行代码的作用
  - 观察输出结果

- ✅ **动手修改代码 / Modify the code**
  - 尝试不同的参数
  - 添加自己的可视化

- ✅ **做笔记 / Take notes**
  - 记录关键概念
  - 记录遇到的问题和解决方案

- ✅ **实验 / Experiment**
  - 尝试不同的交易对
  - 尝试不同的时间范围
  - 添加自己的特征

---

## 💡 常见问题 / FAQ

### Q1: 运行 notebook 时出现 "ModuleNotFoundError"
**解决方案:**
```bash
# 确保在项目根目录下运行
cd binance-prediction

# 或者在 notebook 第一个单元格中添加：
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))
```

### Q2: 图表不显示
**解决方案:**
```python
# 在 notebook 开头添加：
%matplotlib inline
```

### Q3: 数据下载失败
**可能原因:**
- 网络问题
- Binance API 限制

**解决方案:**
- 检查网络连接
- 使用已有的数据文件（如果存在）
- 减少数据量

### Q4: 如何保存我的修改？
**解决方案:**
- 按 `Ctrl + S` (Windows/Linux) 或 `Cmd + S` (Mac) 保存 notebook
- 或在菜单中选择 `File` → `Save and Checkpoint`

---

## 🔗 相关资源 / Related Resources

### 项目文档 / Project Documentation:
- [../README.md](../README.md) - 项目概览
- [../QUICKSTART.md](../QUICKSTART.md) - 快速入门
- [../API.md](../API.md) - API 文档
- [../SETUP.md](../SETUP.md) - 环境搭建

### 外部学习资源 / External Learning Resources:
- [Jupyter Notebook 官方文档](https://jupyter-notebook.readthedocs.io/)
- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [Pandas 官方文档](https://pandas.pydata.org/docs/)
- [Scikit-learn 用户指南](https://scikit-learn.org/stable/user_guide.html)

---

## 📝 笔记本约定 / Notebook Conventions

在所有 notebook 中，我们遵循以下约定：
In all notebooks, we follow these conventions:

- 📖 **解释 / Explanation**: 概念和原理说明
- 💡 **提示 / Tip**: 实用建议
- ⚠️ **警告 / Warning**: 注意事项
- ✅ **完成 / Done**: 成功完成的步骤
- ❌ **错误 / Error**: 常见错误

所有代码都包含中英文双语注释。
All code includes bilingual comments (Chinese and English).

---

## 🎯 下一步 / Next Steps

完成所有 notebook 后，你可以：
After completing all notebooks, you can:

1. **运行脚本 / Run Scripts:**
   ```bash
   python scripts/download_data.py
   python scripts/train_model.py
   python scripts/backtest.py
   ```

2. **启动 Web 应用 / Start Web App:**
   ```bash
   python scripts/app.py
   ```

3. **进行实时预测 / Make Real-time Predictions:**
   ```bash
   python scripts/predict.py --symbol BTCUSDT
   ```

4. **尝试自己的改进 / Try Your Own Improvements:**
   - 添加新的技术指标
   - 尝试不同的机器学习模型
   - 优化超参数

---

## 🆘 获取帮助 / Get Help

如果在学习过程中遇到问题：
If you encounter issues during learning:

1. 查看相关文档（README, API.md, SETUP.md）
2. 检查错误信息并搜索解决方案
3. 尝试简化问题（减少数据量，使用简单参数）
4. 参考代码注释和说明

Happy Learning! 🎉
祝学习愉快！🎉
