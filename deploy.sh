#!/bin/bash

# 微博热搜分析 - GitHub 部署脚本
# 使用方法: chmod +x deploy.sh && ./deploy.sh

set -e

echo "🚀 开始部署微博热搜分析到 GitHub..."

# 检查 git 是否已初始化
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git branch -M main
fi

# 添加所有文件
echo "📄 添加文件到暂存区..."
git add .

# 提交
echo "💾 提交代码..."
git commit -m "feat: 微博热搜产品创意分析 - GitHub Actions 自动化

- 使用 Claude Agent SDK 实现 AI 分析
- 支持定时执行（每天 9:00 和 18:00）
- 自动生成 HTML 可视化报告
- 报告上传到 GitHub Artifacts"

# 提示用户创建远程仓库
echo ""
echo "============================================"
echo "📋 请完成以下步骤:"
echo ""
echo "1️⃣  在 GitHub 创建新仓库:"
echo "    https://github.com/new"
echo "    仓库名: weibo-hotspot-analyzer"
echo "    类型: Public"
echo "    ❌ 不要勾选 'Add a README file'"
echo ""
echo "2️⃣  创建后，复制仓库地址，然后运行:"
echo "    git remote add origin https://github.com/你的用户名/weibo-hotspot-analyzer.git"
echo "    git push -u origin main"
echo ""
echo "3️⃣  配置 Secrets (Settings → Secrets → Actions → New):"
echo "    - ANTHROPIC_API_KEY: 你的 API Key"
echo "    - ANTHROPIC_BASE_URL: https://yunwu.ai"
echo "    - TIANAPI_KEY: f676388439939fde76b02b20ce32bd54"
echo "    - TAVILY_API_KEY: 你的 Tavily Key"
echo ""
echo "4️⃣  手动运行测试:"
echo "    Actions → 微博热搜产品创意分析 → Run workflow"
echo "============================================"
