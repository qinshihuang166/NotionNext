#!/bin/bash

echo "Starting Binance Price Prediction Project Setup..."

# 创建必要的目录
mkdir -p data models notebooks scripts utils

# 安装依赖
echo "Installing dependencies..."
pip install -r requirements.txt

# 创建示例 .env 文件
if [ ! -f .env ]; then
  echo "Creating .env.example..."
  echo "BINANCE_API_KEY=your_api_key_here" > .env
  echo "BINANCE_API_SECRET=your_api_secret_here" >> .env
fi

echo "Setup complete! You can now run 'python scripts/download_data.py' to get started."
