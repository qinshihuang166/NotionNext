# 📦 LSTM项目完整安装指南

> 详细的安装步骤和环境配置
> 
> 适用于: Windows, macOS, Linux

---

## 📋 系统要求

### 最低配置
- Python 3.8+
- RAM: 8GB
- 存储: 2GB
- 网络: 稳定连接（下载数据）

### 推荐配置
- Python 3.9+
- RAM: 16GB
- 存储: 5GB
- GPU: NVIDIA with CUDA (可选，但强烈推荐)

---

## 🔧 安装步骤

### 方法 1: 使用 pip (推荐)

```bash
# 1. 克隆或下载项目
cd binance-prediction

# 2. 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 升级 pip
pip install --upgrade pip

# 4. 安装依赖
pip install -r requirements_lstm.txt

# 5. 验证安装
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
python -c "import tensorflow as tf; print('GPU可用:', len(tf.config.list_physical_devices('GPU')) > 0)"
```

### 方法 2: 使用 conda

```bash
# 1. 创建 conda 环境
conda create -n lstm_crypto python=3.9
conda activate lstm_crypto

# 2. 安装 TensorFlow
conda install tensorflow

# 3. 安装其他依赖
pip install -r requirements_lstm.txt

# 4. 验证
python -c "import tensorflow as tf; print(tf.__version__)"
```

---

## 🔍 常见安装问题

### 问题 1: TensorFlow 安装失败

**症状**: `pip install tensorflow` 报错

**解决方案**:

```bash
# 方案 A: 指定版本
pip install tensorflow==2.12.0

# 方案 B: 使用 conda
conda install -c conda-forge tensorflow

# 方案 C: 只需要 CPU 版本
pip install tensorflow-cpu
```

### 问题 2: 缺少系统依赖

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip
```

**macOS**:
```bash
brew install python@3.9
```

### 问题 3: GPU 支持问题

**检查 GPU 是否可用**:
```python
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
```

**如果输出为空列表**:

1. **检查 CUDA 版本**:
   ```bash
   nvidia-smi
   ```

2. **安装匹配的 CUDA**:
   - TensorFlow 2.12 需要 CUDA 11.8
   - 下载: https://developer.nvidia.com/cuda-toolkit

3. **重新安装 TensorFlow**:
   ```bash
   pip uninstall tensorflow
   pip install tensorflow==2.12.0
   ```

### 问题 4: Jupyter 无法导入模块

**解决方案**:
```bash
# 确保 Jupyter 在正确的环境中
pip install ipykernel
python -m ipykernel install --user --name=lstm_crypto
```

---

## 🧪 验证安装

运行以下测试脚本:

```bash
cd binance-prediction
python -c "
import sys
print('Python版本:', sys.version)

import tensorflow as tf
print('TensorFlow版本:', tf.__version__)
print('GPU可用:', len(tf.config.list_physical_devices('GPU')) > 0)

import pandas as pd
print('Pandas版本:', pd.__version__)

import numpy as np
print('NumPy版本:', np.__version__)

import sklearn
print('Scikit-learn版本:', sklearn.__version__)

print('\\n✅ 所有依赖安装成功!')
"
```

**期望输出**:
```
Python版本: 3.9.x
TensorFlow版本: 2.12.x
GPU可用: True (或 False)
Pandas版本: 1.x.x
NumPy版本: 1.2x.x
Scikit-learn版本: 0.24.x

✅ 所有依赖安装成功!
```

---

## 🐳 Docker 安装 (可选)

如果你熟悉 Docker:

```bash
# 使用 TensorFlow 官方镜像
docker pull tensorflow/tensorflow:latest-gpu-jupyter

# 运行容器
docker run -it --gpus all -p 8888:8888 -v $(pwd):/tf tensorflow/tensorflow:latest-gpu-jupyter

# 在容器中安装项目依赖
pip install -r requirements_lstm.txt
```

---

## 📝 下一步

安装完成后:

1. **快速测试**: `python scripts/lstm/train_lstm.py --quick-test`
2. **阅读文档**: `README_LSTM.md`
3. **运行笔记本**: `jupyter notebook notebooks/00_快速开始_LSTM预测.ipynb`

---

## 🔗 相关资源

- [TensorFlow 安装指南](https://www.tensorflow.org/install)
- [CUDA 安装指南](https://developer.nvidia.com/cuda-downloads)
- [Conda 文档](https://docs.conda.io/)

---

## 💬 需要帮助？

遇到问题？查看:
- [故障排除](README_LSTM.md#常见问题)
- [GitHub Issues](https://github.com/qinshihuang166)

---

Made with ❤️ by qinshihuang166
