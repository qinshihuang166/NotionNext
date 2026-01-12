# 贡献指南 / Contributing Guide

感谢你对 Binance 币价预测项目的兴趣！我们欢迎各种形式的贡献。

Thank you for your interest in the Binance Price Prediction Project! We welcome all forms of contributions.

## 🤝 如何贡献 / How to Contribute

### 报告 Bug / Report Bugs

如果你发现了 bug，请：
If you find a bug, please:

1. 检查 [Issues](../../issues) 确认该 bug 是否已被报告
2. 如果没有被报告，创建一个新的 Issue，包括：
   - 清晰的标题
   - 详细的描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 环境信息（Python 版本、操作系统等）
   - 相关的日志或截图

### 提出新功能 / Propose New Features

我们欢迎新功能的建议！在提出之前：
We welcome feature suggestions! Before proposing:

1. 检查是否已有类似的功能请求
2. 清晰描述你想要的功能
3. 解释为什么这个功能有价值
4. 如果可能，提供实现思路

### 提交代码 / Submit Code

如果你想贡献代码：
If you want to contribute code:

#### 步骤 1: Fork 并克隆仓库 / Fork and Clone

```bash
# Fork 本仓库 / Fork this repository
# 然后克隆你的 fork / Then clone your fork
git clone https://github.com/your-username/binance-price-prediction.git
cd binance-price-prediction
```

#### 步骤 2: 创建分支 / Create Branch

```bash
# 创建特性分支 / Create feature branch
git checkout -b feature/your-feature-name
```

分支命名约定 / Branch naming convention:
- `feature/feature-name` - 新功能
- `fix/bug-name` - Bug 修复
- `docs/update-name` - 文档更新
- `refactor/component-name` - 代码重构

#### 步骤 3: 进行更改 / Make Changes

遵循以下准则：
Follow these guidelines:

- **代码风格 / Code Style**:
  - 使用有意义的变量和函数名
  - 添加清晰的注释（中英文双语）
  - 遵循 PEP 8 Python 代码风格
  - 保持函数简短和单一职责

- **文档 / Documentation**:
  - 更新相关文档
  - 为新函数添加 docstring
  - 更新 README 或相关说明文档

- **测试 / Testing**:
  - 确保代码能正常运行
  - 测试边界情况
  - 不要破坏现有功能

#### 步骤 4: 提交更改 / Commit Changes

```bash
# 添加更改 / Add changes
git add .

# 提交更改 / Commit changes
git commit -m "feat: add new feature description"
```

提交信息格式 / Commit message format:
```
<type>: <subject>

<body>

<footer>
```

类型 / Types:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例 / Example:
```
feat: add MACD indicator to technical indicators

- Add MACD calculation to data_processor.py
- Update documentation with MACD explanation
- Add MACD to feature list

Closes #123
```

#### 步骤 5: 推送并创建 PR / Push and Create PR

```bash
# 推送到你的 fork / Push to your fork
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。
Then create a Pull Request on GitHub.

**PR 模板 / PR Template:**

```markdown
## 描述 / Description
简要描述这个 PR 的内容和目的。

## 变更类型 / Type of Change
- [ ] Bug 修复 / Bug fix
- [ ] 新功能 / New feature
- [ ] 破坏性变更 / Breaking change
- [ ] 文档更新 / Documentation update

## 测试 / Testing
描述你如何测试这些更改：
- [ ] 测试通过
- [ ] 添加了新测试
- [ ] 更新了文档

## 相关 Issues / Related Issues
Closes #(issue number)
```

## 📝 开发环境设置 / Development Environment Setup

### 1. 安装依赖 / Install Dependencies

```bash
# 创建虚拟环境（推荐）/ Create virtual environment (recommended)
python -m venv venv

# 激活虚拟环境 / Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 安装开发工具 / Install development tools
pip install flake8 black pytest
```

### 2. 代码质量检查 / Code Quality Check

```bash
# 使用 flake8 检查代码 / Check code with flake8
flake8 binance-prediction

# 使用 black 格式化代码 / Format code with black
black binance-prediction
```

### 3. 运行测试 / Run Tests

```bash
# 运行所有测试 / Run all tests
pytest

# 运行特定测试 / Run specific test
pytest tests/test_module.py
```

## 📚 代码规范 / Code Standards

### Python 代码规范 / Python Code Standards

遵循 PEP 8：
Follow PEP 8:

- 使用 4 个空格缩进
- 每行不超过 79 个字符
- 使用空行分隔函数和类
- 使用有意义的项目名称

### 注释规范 / Comment Standards

**文件头注释 / File Header Comment:**
```python
"""
模块功能描述 / Module description
This module provides functionality for...

作者 / Author: Your Name
日期 / Date: YYYY-MM-DD
"""
```

**函数注释 / Function Comment:**
```python
def calculate_sma(df, window=20):
    """
    计算简单移动平均线 / Calculate Simple Moving Average

    Parameters:
    -----------
    df : pd.DataFrame
        包含价格数据的 DataFrame / DataFrame with price data
    window : int
        移动窗口大小 / Size of moving window

    Returns:
    --------
    pd.Series
        SMA 值 / SMA values

    Example:
    --------
    >>> sma = calculate_sma(df, window=20)
    """
    # 实现 / Implementation
    pass
```

**行内注释 / Inline Comments:**
```python
# 计算价格变化 / Calculate price change
price_change = df['close'].diff()

# 去除缺失值 / Remove missing values
df.dropna(inplace=True)
```

### 命名规范 / Naming Conventions

- **变量 / Variables**: `snake_case`
  ```python
  current_price = 100
  ```
- **函数 / Functions**: `snake_case`
  ```python
  def calculate_indicator():
  ```
- **类 / Classes**: `PascalCase`
  ```python
  class DataProcessor:
  ```
- **常量 / Constants**: `UPPER_CASE`
  ```python
  DEFAULT_WINDOW = 20
  ```

## 🎨 文档规范 / Documentation Standards

### README 更新 / README Updates

如果你添加了新功能，记得更新 README：
If you add new features, remember to update README:

- 更新项目结构
- 添加新功能说明
- 更新使用示例

### 代码文档 / Code Documentation

- 所有公共函数必须有 docstring
- 使用清晰的语言解释功能
- 包含参数和返回值的说明
- 提供使用示例

## 🔍 审查流程 / Review Process

### 提交 PR 后 / After Submitting PR

1. **自动检查 / Automated Checks**:
   - GitHub Actions 将自动运行测试
   - 检查代码风格
   - 确保构建成功

2. **人工审查 / Manual Review**:
   - 维护者会审查你的代码
   - 可能提出修改建议
   - 响应审查意见并及时更新

3. **合并 / Merge**:
   - 审查通过后将被合并
   - 可能需要解决冲突

### 响应审查 / Responding to Reviews

- 及时回应审查意见
- 如果不理解，礼貌地询问
- 感谢审查者的时间

## 📖 贡献领域 / Contribution Areas

我们特别欢迎以下领域的贡献：
We especially welcome contributions in these areas:

### 1. 新技术指标 / New Technical Indicators

添加更多的技术分析指标：
Add more technical analysis indicators:

```python
# 示例：添加 MACD 指标
def add_macd(df, fast=12, slow=26, signal=9):
    """
    添加 MACD 指标
    """
    # 实现逻辑
    pass
```

### 2. 新的机器学习模型 / New ML Models

尝试不同的算法：
Try different algorithms:

- LSTM (深度学习)
- XGBoost / LightGBM
- 支持向量机
- 贝叶斯分类器

### 3. 数据可视化增强 / Visualization Enhancements

改进或添加新的图表：
Improve or add new charts:

- 交互式图表（Plotly）
- 更美观的样式
- 更多图表类型

### 4. 文档改进 / Documentation Improvements

- 修正错误
- 添加更多示例
- 翻译成其他语言
- 添加教程

### 5. 性能优化 / Performance Optimization

- 加快数据加载
- 优化模型训练速度
- 减少内存使用

## 🏆 认可贡献者 / Recognizing Contributors

所有贡献者将在项目中获得认可：
All contributors will be recognized:

- 在 README 中列出
- 在发布说明中提及
- 在贡献者列表中显示

## 💬 联系方式 / Contact

如果你在贡献过程中有任何问题：
If you have any questions during the contribution process:

- 创建 Issue 提问
- 在 PR 中询问
- 加入讨论

---

再次感谢你的贡献！🎉
Thank you again for your contribution! 🎉
