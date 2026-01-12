# 环境搭建指南 / Environment Setup Guide

本指南将帮助初学者从零开始搭建本项目所需的 Python 环境。
This guide will help beginners set up the Python environment required for this project from scratch.

## 📋 目录 / Table of Contents

1. [安装 Python / Install Python](#1-安装-python--install-python)
2. [获取币安 API Key / Get Binance API Key](#2-获取币安-api-key--get-binance-api-key)
3. [安装依赖库 / Install Dependencies](#3-安装依赖库--install-dependencies)
4. [配置环境变量 / Configure Environment Variables](#4-配置环境变量--configure-environment-variables)
5. [验证安装 / Verify Installation](#5-验证安装--verify-installation)
6. [运行 Jupyter Notebook / Run Jupyter Notebook](#6-运行-jupyter-notebook--run-jupyter-notebook)
7. [常见问题 / Common Issues](#7-常见问题--common-issues)

---

## 1. 安装 Python / Install Python

### 检查 Python 版本 / Check Python Version

打开终端 (Terminal) 或命令提示符 (CMD)，运行：
Open terminal or command prompt and run:

```bash
python --version
# 或 / or
python3 --version
```

如果显示 Python 3.8 或更高版本，则已安装。
If Python 3.8 or higher is displayed, it's already installed.

### 安装 Python / Install Python

如果没有安装或版本过低，请下载并安装：
If not installed or version is too low, please download and install:

**Windows 用户 / Windows Users:**
1. 访问 [Python 官网](https://www.python.org/downloads/)
   Visit [Python Official Website](https://www.python.org/downloads/)
2. 下载 Python 3.8 或更高版本
   Download Python 3.8 or higher
3. ⚠️ **重要**: 安装时务必勾选 **"Add Python to PATH"**
   ⚠️ **Important**: Check **"Add Python to PATH"** during installation
4. 点击 "Install Now"
   Click "Install Now"

**Mac 用户 / Mac Users:**
```bash
# 使用 Homebrew 安装 / Install using Homebrew
brew install python
```

**Linux 用户 / Linux Users:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

---

## 2. 获取币安 API Key / Get Binance API Key

虽然本项目可以在没有 API Key 的情况下获取公开市场数据，但申请 API Key 可以获得更高的请求频率限制。
Although this project can fetch public market data without an API Key, applying for an API Key provides higher request rate limits.

### 是否需要 API Key？/ Do You Need an API Key?

- ✅ **不需要 / Not Required**: 如果只是学习、测试，或者获取历史数据
- If just learning, testing, or fetching historical data

- ✅ **推荐 / Recommended**: 如果要频繁获取实时数据或运行 Web 应用
- If you need to frequently fetch real-time data or run web applications

### 获取步骤 / Steps to Get

1. 登录 [币安官网](https://www.binance.com/) 并注册账户
   Login to [Binance Website](https://www.binance.com/) and register an account

2. 进入 "API 管理" (API Management)
   Go to "API Management"

3. 点击 "创建 API" (Create API)
   Click "Create API"

4. **重要提示 / Important Tips**:
   - ✅ 选择 "只读权限" (Read-Only) 即可满足本项目需求
     - "Read-Only" permission is sufficient for this project
   - ❌ 不要启用提现权限
     - Do not enable withdrawal permissions
   - 🔒 妥善保管 API Secret，不要泄露
     - Keep API Secret safe and do not leak it
   - 📍 绑定 IP 地址（可选，提高安全性）
     - Bind IP address (optional, improves security)

5. 复制 API Key 和 API Secret
   Copy API Key and API Secret

---

## 3. 安装依赖库 / Install Dependencies

### 方法 1: 使用 requirements.txt（推荐）/ Using requirements.txt (Recommended)

在项目根目录下运行：
Run in the project root directory:

```bash
# 进入项目目录 / Enter project directory
cd binance-prediction

# 安装所有依赖 / Install all dependencies
pip install -r requirements.txt
```

### 方法 2: 使用国内镜像加速（中国用户）/ Using China Mirror (Chinese Users)

如果下载速度慢，可以使用清华镜像源：
If download speed is slow, you can use Tsinghua mirror:

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

其他可用镜像源 / Other available mirrors:
- 阿里云 Aliyun: `https://mirrors.aliyun.com/pypi/simple/`
- 豆瓣 Douban: `https://pypi.douban.com/simple/`

### 方法 3: 逐个安装 / Install Individually

如果遇到问题，可以尝试逐个安装：
If you encounter issues, try installing individually:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn requests python-binance flask jupyter notebook joblib python-dotenv
```

### 依赖库说明 / Dependencies Explanation

| 库 / Library | 用途 / Purpose |
|-------------|---------------|
| pandas | 数据处理和表格操作 / Data processing and table operations |
| numpy | 数值计算 / Numerical computing |
| scikit-learn | 机器学习模型 / Machine learning models |
| matplotlib | 数据可视化 / Data visualization |
| seaborn | 统计图表 / Statistical charts |
| requests | HTTP 请求 / HTTP requests |
| python-binance | Binance API 客户端 / Binance API client |
| flask | Web 框架 / Web framework |
| jupyter/notebook | 交互式开发环境 / Interactive development environment |
| joblib | 模型保存和加载 / Model saving and loading |
| python-dotenv | 环境变量管理 / Environment variable management |

---

## 4. 配置环境变量 / Configure Environment Variables

### 创建 .env 文件 / Create .env File

在项目根目录创建 `.env` 文件：
Create `.env` file in project root:

```bash
# Linux/Mac
touch .env

# Windows (使用文本编辑器创建)
# Windows (create using text editor)
```

### 填写配置 / Fill Configuration

编辑 `.env` 文件，填入你的 API Key：
Edit `.env` file and fill in your API Key:

```bash
# Binance API Configuration / 币安 API 配置
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**注意 / Notes:**
- 如果没有 API Key，可以留空或删除这两行
- If you don't have an API Key, you can leave it blank or delete these lines
- `.env` 文件已在 `.gitignore` 中，不会被提交到 GitHub
- `.env` file is in `.gitignore` and won't be committed to GitHub

### 使用示例 .env 文件 / Use Example .env File

```bash
# 复制示例文件 / Copy example file
cp .env.example .env

# 然后编辑 .env 文件 / Then edit .env file
```

---

## 5. 验证安装 / Verify Installation

### 测试 Python 环境 / Test Python Environment

```bash
# 进入 Python 交互式环境 / Enter Python interactive environment
python

# 运行以下代码 / Run the following code
import pandas as pd
import numpy as np
import sklearn
import matplotlib
import flask

print("✅ All libraries imported successfully!")
print("✅ 所有库导入成功！")

# 退出 / Exit
exit()
```

### 测试项目导入 / Test Project Imports

```bash
# 在项目根目录下 / In the project root directory
python -c "from utils.binance_client import BinanceUtility; from utils.data_processor import DataProcessor; print('✅ Project imports successful!')"
```

### 测试 Binance API 连接 / Test Binance API Connection

```bash
python scripts/download_data.py --symbols BTCUSDT
```

如果成功下载数据，说明一切正常！
If data is downloaded successfully, everything is working!

---

## 6. 运行 Jupyter Notebook / Run Jupyter Notebook

### 启动 Jupyter / Start Jupyter

```bash
# 在项目根目录下 / In the project root directory
jupyter notebook
```

### 使用教程 / Use Tutorials

浏览器会自动打开，然后导航到 `notebooks/` 文件夹：
Browser will open automatically, then navigate to `notebooks/` folder:

1. `01_Data_Exploration.ipynb` - 数据获取与探索 / Data fetching and exploration
2. `02_Feature_Engineering.ipynb` - 特征工程 / Feature engineering
3. `03_Model_Training.ipynb` - 模型训练与评估 / Model training and evaluation

### 关闭 Jupyter / Close Jupyter

在终端中按 `Ctrl + C` 停止 Jupyter 服务。
Press `Ctrl + C` in the terminal to stop Jupyter service.

---

## 7. 常见问题 / Common Issues

### 问题 1: pip 不是内部或外部命令
**Problem**: pip is not recognized as an internal or external command

**解决方案 / Solution**:
- Windows: 重新安装 Python，确保勾选 "Add Python to PATH"
- Linux/Mac: `sudo apt install python3-pip` 或 `sudo yum install python3-pip`

### 问题 2: ModuleNotFoundError: No module named 'xxx'
**Problem**: ModuleNotFoundError: No module named 'xxx'

**解决方案 / Solution**:
```bash
pip install xxx
# 或使用完整 requirements.txt
# or use full requirements.txt
pip install -r requirements.txt
```

### 问题 3: Permission denied 错误
**Problem**: Permission denied error

**解决方案 / Solution**:
```bash
# Linux/Mac: 使用 sudo / Use sudo
sudo pip install -r requirements.txt

# 或使用虚拟环境 / Or use virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 问题 4: Binance API 连接超时
**Problem**: Binance API connection timeout

**解决方案 / Solution**:
- 检查网络连接 / Check network connection
- 使用 VPN（如在中国大陆）/ Use VPN (if in mainland China)
- 检查 API Key 是否正确 / Check if API Key is correct

### 问题 5: matplotlib 显示中文乱码
**Problem**: matplotlib Chinese character display issues

**解决方案 / Solution**:
- 在代码中设置字体 / Set font in code:
```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

### 问题 6: Jupyter 无法启动
**Problem**: Jupyter won't start

**解决方案 / Solution**:
```bash
# 重新安装 jupyter / Reinstall jupyter
pip install --upgrade --force-reinstall jupyter notebook
```

### 问题 7: 端口 5000 被占用
**Problem**: Port 5000 is already in use

**解决方案 / Solution**:
```bash
# 查找占用进程 / Find process using the port
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# 或使用其他端口 / Or use a different port
# 修改 scripts/app.py 中的端口号 / Change port in scripts/app.py
```

---

## 🎯 一键设置脚本 / One-Click Setup Script

我们提供了一个自动化设置脚本（仅 Linux/Mac）：
We provide an automated setup script (Linux/Mac only):

```bash
# 给脚本执行权限 / Give script execute permission
chmod +x setup.sh

# 运行设置脚本 / Run setup script
./setup.sh
```

这个脚本会自动：
This script will automatically:
1. 创建必要的目录 / Create necessary directories
2. 安装所有依赖 / Install all dependencies
3. 创建示例 .env 文件 / Create example .env file

**Windows 用户需要手动执行上述步骤。**
**Windows users need to manually perform the above steps.**

---

## ✅ 下一步 / Next Steps

完成环境搭建后，你可以：
After completing environment setup, you can:

1. 📖 阅读学习指南 / Read learning guide:
   [TUTORIAL.md](TUTORIAL.md)

2. 📓 运行 Jupyter Notebook / Run Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

3. 🚀 开始第一个项目 / Start your first project:
   ```bash
   python scripts/download_data.py --symbols BTCUSDT
   ```

---

## 📞 需要帮助？/ Need Help?

如果遇到问题：
If you encounter issues:

1. 查看 [常见问题](#7-常见问题--common-issues) 部分
   Check [Common Issues](#7-常见问题--common-issues) section

2. 搜索 GitHub Issues / Search GitHub Issues

3. 创建新的 Issue / Create new Issue

---

**祝你搭建顺利！/ Happy Setup!** 🎉
