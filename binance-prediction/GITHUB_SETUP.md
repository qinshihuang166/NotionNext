# GitHub 上传指南 / GitHub Upload Guide

本指南将帮助用户 qinshihuang166 将项目上传到 GitHub。
This guide will help user qinshihuang166 upload the project to GitHub.

## 📋 前提条件 / Prerequisites

1. ✅ 拥有 GitHub 账户 / Have a GitHub account
2. ✅ 已安装 Git / Git is installed
3. ✅ 项目代码已完成 / Project code is complete

## 🚀 上传步骤 / Upload Steps

### 步骤 1: 在 GitHub 上创建仓库 / Step 1: Create Repository on GitHub

1. 登录 GitHub / Log in to GitHub
2. 点击右上角的 "+" 号，选择 "New repository" / Click "+" in top right, select "New repository"
3. 填写仓库信息 / Fill in repository information:
   - **Repository name**: `binance-price-prediction`
   - **Description**: `A beginner-friendly cryptocurrency price prediction project using machine learning`
   - **Visibility**: Public (推荐公开) / Public (recommended)
   - **不要勾选** "Initialize this repository with a README" / **Do NOT check** "Initialize this repository with a README"
4. 点击 "Create repository" / Click "Create repository"

### 步骤 2: 配置本地 Git / Step 2: Configure Local Git

打开终端 / Open terminal:

```bash
# 检查 Git 是否安装 / Check if Git is installed
git --version

# 配置 Git 用户信息（如果还没配置过）/ Configure Git user info (if not configured)
git config --global user.name "qinshihuang166"
git config --global user.email "your-email@example.com"
```

### 步骤 3: 初始化本地仓库 / Step 3: Initialize Local Repository

```bash
# 进入项目目录 / Enter project directory
cd binance-prediction

# 初始化 Git 仓库 / Initialize Git repository
git init

# 添加所有文件到暂存区 / Add all files to staging area
git add .

# 创建首次提交 / Create initial commit
git commit -m "Initial commit: Binance Price Prediction Project

- Complete ML-based cryptocurrency price prediction system
- Includes data fetching, feature engineering, model training
- Web dashboard with Flask
- Interactive Jupyter notebooks for learning
- Comprehensive bilingual documentation (Chinese/English)"
```

### 步骤 4: 连接远程仓库 / Step 4: Connect to Remote Repository

```bash
# 添加远程仓库 / Add remote repository
# 替换 qinshihuang166 为你的 GitHub 用户名
# Replace qinshihuang166 with your GitHub username
git remote add origin https://github.com/qinshihuang166/binance-price-prediction.git

# 重命名主分支为 main / Rename main branch to main
git branch -M main
```

### 步骤 5: 推送到 GitHub / Step 5: Push to GitHub

```bash
# 首次推送到 GitHub / First push to GitHub
git push -u origin main
```

如果遇到认证问题，你可能需要：
If you encounter authentication issues, you may need to:

**选项 A: 使用 Personal Access Token (推荐) / Option A: Use Personal Access Token (Recommended)**

1. 在 GitHub 上生成 Personal Access Token:
   - Settings → Developer settings → Personal access tokens → Generate new token
   - 选择权限：`repo`
   - 复制生成的 token

2. 推送时使用 token / Use token when pushing:
   ```bash
   git push -u origin main
   # Username: qinshihuang166
   # Password: [粘贴你的 token / paste your token]
   ```

**选项 B: 使用 SSH 密钥 / Option B: Use SSH Key**

```bash
# 生成 SSH 密钥 / Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# 添加到 SSH agent / Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 复制公钥到 GitHub / Copy public key to GitHub
cat ~/.ssh/id_ed25519.pub
# Settings → SSH and GPG keys → New SSH key

# 修改远程 URL 为 SSH / Change remote URL to SSH
git remote set-url origin git@github.com:qinshihuang166/binance-price-prediction.git

# 重新推送 / Push again
git push -u origin main
```

## 🎉 上传成功后的操作 / Post-Upload Actions

### 1. 验证仓库 / Verify Repository

访问你的 GitHub 仓库：
Visit your GitHub repository:
```
https://github.com/qinshihuang166/binance-price-prediction
```

你应该看到：
You should see:
- ✅ 所有项目文件 / All project files
- ✅ README.md 显示在首页 / README.md displayed on homepage
- ✅ 完整的项目结构 / Complete project structure

### 2. 设置仓库描述和标签 / Set Repository Description and Tags

在仓库首页点击设置：
On repository homepage, click Settings:

1. 添加 Topics / Add Topics:
   - `cryptocurrency`
   - `machine-learning`
   - `price-prediction`
   - `binance`
   - `trading`
   - `python`

2. 更新 Description（如果需要）:
   ```
   A beginner-friendly cryptocurrency price prediction project using Random Forest. Includes data fetching, feature engineering, model training, backtesting, and a Flask web dashboard. Complete with Chinese/English documentation and Jupyter tutorials.
   ```

### 3. 启用 GitHub Actions / Enable GitHub Actions

GitHub Actions 会自动运行测试：
GitHub Actions will automatically run tests:

1. 进入 Actions 标签页 / Go to Actions tab
2. 应该能看到 "Python Testing" 工作流正在运行
3. 等待测试完成 / Wait for tests to complete
4. 确保显示绿色的 ✓ / Ensure green ✓ is shown

### 4. 添加项目徽章 / Add Project Badges

在 README.md 顶部添加徽章：
Add badges to the top of README.md:

```markdown
![GitHub](https://img.shields.io/badge/GitHub-Project-informational?style=flat&logo=github)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
```

### 5. 创建 Releases / Create Releases

为项目创建版本标签：
Create version tags for the project:

```bash
# 创建版本标签 / Create version tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial release

Features:
- Complete ML-based price prediction system
- Binance API integration
- Random Forest model with cross-validation
- Backtesting system
- Flask web dashboard
- Data visualization tools
- 3 interactive Jupyter notebooks
- Comprehensive bilingual documentation"

# 推送标签到 GitHub / Push tags to GitHub
git push origin v1.0.0
```

然后在 GitHub 上：
Then on GitHub:
1. 点击 "Releases" / Click "Releases"
2. 点击 "Draft a new release" / Click "Draft a new release"
3. 选择 tag `v1.0.0` / Select tag `v1.0.0`
4. 添加描述 / Add description
5. 点击 "Publish release" / Click "Publish release"

## 📊 项目展示优化 / Project Presentation Optimization

### 添加项目截图 / Add Project Screenshots

建议添加以下截图到 README 或创建单独的截图文档：
Consider adding these screenshots to README or create a separate screenshots document:

1. **Web 仪表盘截图 / Web Dashboard Screenshot**
   - 运行 `python scripts/app.py`
   - 访问 `http://localhost:5000`
   - 截图并保存

2. **数据可视化截图 / Data Visualization Screenshot**
   - 运行 Jupyter Notebook
   - 生成一些图表
   - 截图保存

3. **预测结果截图 / Prediction Result Screenshot**
   - 运行 `python scripts/predict.py`
   - 截图输出

### 优化 README 排版 / Optimize README Layout

确保 README 包含：
Ensure README includes:

- ✅ 项目徽章 / Project badges
- ✅ 清晰的项目描述 / Clear project description
- ✅ 功能特性列表 / Feature list
- ✅ 快速开始指南 / Quick start guide
- ✅ 截图或 GIF / Screenshots or GIFs
- ✅ 安装说明 / Installation instructions
- ✅ 使用示例 / Usage examples
- ✅ 项目结构 / Project structure
- ✅ 贡献指南链接 / Contributing guide link
- ✅ 许可证信息 / License information

## 🔧 常见问题 / Common Issues

### Q1: 推送时提示 "fatal: remote origin already exists"

**解决方案 / Solution:**
```bash
# 删除现有的远程仓库 / Remove existing remote
git remote remove origin

# 重新添加 / Add again
git remote add origin https://github.com/qinshihuang166/binance-price-prediction.git
```

### Q2: 推送时提示 "Updates were rejected"

**解决方案 / Solution:**
```bash
# 拉取远程更改 / Pull remote changes
git pull origin main --allow-unrelated-histories

# 重新推送 / Push again
git push -u origin main
```

### Q3: 文件太大，推送失败

**解决方案 / Solution:**

检查 `.gitignore` 文件，确保大文件被忽略：
Check `.gitignore` file, ensure large files are ignored:

```gitignore
# Data files / 数据文件
data/*.csv
data/*.png

# Model files / 模型文件
models/*.pkl

# Jupyter checkpoints
.ipynb_checkpoints/
```

## 📦 后续更新 / Future Updates

### 添加新功能后的提交 / Commit After Adding New Features

```bash
# 查看更改 / Check changes
git status

# 添加更改的文件 / Add changed files
git add .

# 提交更改 / Commit changes
git commit -m "feat: add new feature description"

# 推送到 GitHub / Push to GitHub
git push
```

### 创建 Pull Request（如果是 Fork）/ Create Pull Request (if Forked)

如果你想为原始仓库贡献代码：
If you want to contribute to the original repository:

1. Fork 原始仓库 / Fork original repository
2. 创建特性分支 / Create feature branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. 提交更改 / Commit changes
4. 推送到你的 Fork / Push to your fork
5. 在 GitHub 上创建 Pull Request / Create Pull Request on GitHub

## ✅ 上传完成检查清单 / Upload Completion Checklist

- [ ] GitHub 仓库已创建
- [ ] 本地 Git 已初始化
- [ ] 代码已推送到 GitHub
- [ ] README 显示正确
- [ ] GitHub Actions 测试通过
- [ ] 仓库描述和标签已设置
- [ ] 首次 Release 已创建
- [ ] 项目截图已添加（可选）

## 🎉 完成！/ Done!

恭喜你！你的项目已经成功上传到 GitHub。
Congratulations! Your project has been successfully uploaded to GitHub.

现在你可以：
Now you can:

1. ✅ 分享仓库链接给朋友 / Share repository link with friends
2. ✅ 在简历中展示项目 / Showcase project on resume
3. ✅ 持续更新和改进 / Continuously update and improve
4. ✅ 接受社区贡献 / Accept community contributions

仓库链接 / Repository URL:
```
https://github.com/qinshihuang166/binance-price-prediction
```

---

**如果遇到任何问题，请参考 GitHub 官方文档或提交 Issue。**
**If you encounter any issues, please refer to official GitHub documentation or submit an Issue.**

Happy Coding! 🚀
