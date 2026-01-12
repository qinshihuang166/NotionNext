# 贡献指南 / Contributing Guide

感谢你考虑为币安价格预测项目做出贡献！
Thank you for considering contributing to the Binance Price Prediction Project!

---

## 🤝 如何贡献 / How to Contribute

### 报告 Bug / Report Bugs
如果你发现了 bug，请：
If you find a bug, please:

1. 检查现有 Issues / Check existing Issues
2. 创建新的 Issue，包含：
   - 详细描述问题
   - 复现步骤
   - 你的环境配置（Python 版本、操作系统等）
   - 错误截图或日志

### 提出新功能 / Suggest New Features
如果你想添加新功能：
If you want to add new features:

1. 先创建 Issue 讨论想法
2. 描述新功能的用途和实现方式
3. 等待维护者反馈

### 提交代码 / Submit Code

如果你想修复 bug 或实现新功能：
If you want to fix bugs or implement new features:

1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📋 代码规范 / Code Standards

### Python 代码风格 / Python Code Style
- 遵循 PEP 8 规范 / Follow PEP 8 standards
- 使用有意义的变量名 / Use meaningful variable names
- 添加中英文双语注释 / Add bilingual comments (Chinese & English)
- 保持代码简洁可读 / Keep code clean and readable

### 示例 / Example

```python
# Good / 好的代码
def calculate_moving_average(prices, window_size):
    """
    Calculate Simple Moving Average
    计算简单移动平均线

    Args:
        prices (list): List of prices / 价格列表
        window_size (int): Window size / 窗口大小

    Returns:
        list: Moving averages / 移动平均线
    """
    return [sum(prices[i:i+window_size]) / window_size
            for i in range(len(prices) - window_size + 1)]

# Bad / 不好的代码
def calc(p, w):
    return [sum(p[i:i+w])/w for i in range(len(p)-w+1)]
```

### 文档规范 / Documentation Standards
- 所有新功能需要更新文档 / All new features need documentation updates
- 使用中英文双语 / Use bilingual Chinese & English
- 包含使用示例 / Include usage examples
- 说明参数和返回值 / Describe parameters and return values

---

## 📝 提交信息格式 / Commit Message Format

使用清晰的提交信息格式：
Use clear commit message format:

```
<type>: <subject>

<body>

<footer>
```

### 类型 / Types:
- `feat`: 新功能 / New feature
- `fix`: Bug 修复 / Bug fix
- `docs`: 文档更新 / Documentation update
- `style`: 代码格式（不影响功能）/ Code formatting (no functional change)
- `refactor`: 代码重构 / Code refactoring
- `test`: 添加测试 / Add tests
- `chore`: 构建或辅助工具变动 / Build or auxiliary tool changes

### 示例 / Examples:

```
feat: Add MACD indicator support

Implement MACD (Moving Average Convergence Divergence) indicator
as a new feature in the data processor.

Closes #123
```

```
fix: Fix RSI calculation edge cases

Handle cases where all gains or losses are zero to avoid
division by zero errors in RSI calculation.

Fixes #45
```

---

## 🧪 测试要求 / Testing Requirements

### 运行测试 / Run Tests
提交代码前请确保：
Before submitting code, please ensure:

```bash
# 运行导入测试 / Run import tests
python -c "from utils.binance_client import BinanceUtility; from utils.data_processor import DataProcessor; print('OK')"

# 运行脚本测试 / Run script tests
python scripts/train_model.py --symbol BTCUSDT --local_data data/BTCUSDT_hist.csv
```

### 手动测试 / Manual Testing
- 测试所有主要功能 / Test all main features
- 在不同环境下验证 / Verify in different environments
- 检查文档是否准确 / Check if documentation is accurate

---

## 📚 文档要求 / Documentation Requirements

当添加新功能时，请更新：
When adding new features, please update:

1. **README.md** - 如果是新功能，添加到功能列表
2. **API.md** - 添加新的函数或参数说明
3. **TUTORIAL.md** - 如果是重要功能，添加教程
4. **代码注释** - 确保所有新代码都有注释

---

## 🎯 项目优先级 / Project Priorities

### 高优先级 / High Priority
- Bug 修复 / Bug fixes
- 安全问题 / Security issues
- 文档改进 / Documentation improvements

### 中优先级 / Medium Priority
- 新技术指标 / New technical indicators
- 性能优化 / Performance optimization
- 代码重构 / Code refactoring

### 低优先级 / Low Priority
- UI 改进 / UI improvements
- 非核心功能 / Non-core features
- 实验性功能 / Experimental features

---

## 📊 开发路线图 / Development Roadmap

### 短期目标 / Short-term Goals
- [ ] 添加更多技术指标（MACD、布林带）
- [ ] 改进错误处理
- [ ] 添加单元测试
- [ ] 优化 Web 界面

### 中期目标 / Mid-term Goals
- [ ] 支持更多机器学习算法
- [ ] 添加实时 WebSocket 数据
- [ ] 实现用户系统
- [ ] 添加多币种组合策略

### 长期目标 / Long-term Goals
- [ ] 集成深度学习模型
- [ ] 开发移动应用
- [ ] 部署到云平台
- [ ] 建立社区功能

---

## 🤝 社区准则 / Community Guidelines

### 行为规范 / Code of Conduct
- 尊重所有贡献者 / Respect all contributors
- 建设性反馈 / Constructive feedback
- 帮助新手 / Help beginners
- 欢迎多样化 / Welcome diversity

### 沟通方式 / Communication
- 使用英语或中文 / Use English or Chinese
- 保持专业和友好 / Stay professional and friendly
- 及时回复 Issues 和 PRs / Respond to issues and PRs in a timely manner

---

## 📞 获取帮助 / Getting Help

如果你在贡献过程中遇到问题：
If you encounter issues during contribution:

1. **查看文档 / Check Documentation**
   - README.md
   - API.md
   - SETUP.md

2. **搜索 Issues** / Search Issues
   - 查找类似问题 / Find similar issues

3. **提问求助** / Ask for Help
   - 在相关 Issue 下评论
   - 或创建新的 Issue

---

## 📄 许可证 / License

通过贡献代码，你同意你的贡献将使用 MIT 许可证。
By contributing code, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 致谢 / Acknowledgments

感谢所有贡献者的努力！
Thanks to all contributors for their efforts!

---

**再次感谢你的贡献！/ Thanks again for your contribution!** 🎉

让我们一起让这个项目变得更好！
Let's make this project better together!
