# 环境搭建指南 / Environment Setup Guide

本指南将帮助初学者从零开始搭建本项目所需的 Python 环境。

## 1. 安装 Python
确保你的电脑上安装了 Python 3.8 或更高版本。
- [下载 Python](https://www.python.org/downloads/)
- 安装时请务必勾选 **"Add Python to PATH"**。

## 2. 获取币安 API Key (可选)
虽然你可以使用本项目进行本地分析，但要获取最新数据，建议申请币安 API：
1. 登录 [币安官网](https://www.binance.com/)。
2. 进入 "API 管理"。
3. 创建新的 API Key。
4. 在项目根目录创建 `.env` 文件并填写：
   ```
   BINANCE_API_KEY=你的API_KEY
   BINANCE_API_SECRET=你的API_SECRET
   ```

## 3. 安装依赖库
打开终端 (Terminal) 或命令行 (CMD)，进入项目目录并运行：
```bash
pip install -r requirements.txt
```

### 常见问题
- **pip 安装速度慢**: 可以使用清华源加速：
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

## 4. 运行 Jupyter Notebook
如果你想学习教程：
```bash
jupyter notebook
```
然后在浏览器中打开 `notebooks/Analysis.ipynb`。

## 5. 一键设置脚本 (Linux/Mac)
我们提供了一个简单的设置脚本：
```bash
chmod +x setup.sh
./setup.sh
```
*(注：请在 Windows 上手动运行相关命令)*
