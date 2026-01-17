# 微博热搜产品创意分析 - GitHub Actions 自动化

基于 Claude Agent SDK 的微博热搜产品创意分析工具，支持 GitHub Actions 云端定时执行。

## 项目结构

```
github-actions-migration/
├── .github/
│   └── workflows/
│       └── weibo-analysis.yml    # GitHub Actions 工作流
├── weibo_agent.py                # 主程序（Claude Agent SDK）
├── requirements.txt              # Python 依赖
└── README.md                     # 本文件
```

## 功能特性

- ✅ 自动获取微博热搜榜单（前20条）
- ✅ 深度搜索每个热点的新闻背景
- ✅ AI 评分（趣味性 80% + 实用性 20%）
- ✅ 自动生成产品创意方案
- ✅ 输出专业 HTML 可视化报告
- ✅ 支持定时执行和手动触发
- ✅ 报告自动上传到 Artifacts

## 快速部署指南

### 步骤 1: 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库，例如: weibo-hotspot-analyzer

# 克隆到本地
git clone https://github.com/你的用户名/weibo-hotspot-analyzer.git
cd weibo-hotspot-analyzer
```

### 步骤 2: 复制项目文件

将 `github-actions-migration` 目录下的所有文件复制到仓库根目录：

```bash
cp -r /path/to/github-actions-migration/* .
```

### 步骤 3: 配置 GitHub Secrets

1. 进入 GitHub 仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret** 添加以下密钥：

| Secret 名称 | 说明 | 获取方式 |
|-------------|------|----------|
| `ANTHROPIC_API_KEY` | Claude API 密钥 | [Anthropic Console](https://console.anthropic.com/) |
| `TIANAPI_KEY` | 天行数据 API 密钥 | 当前值: `f676388439939fde76b02b20ce32bd54` |
| `TAVILY_API_KEY` | Tavily 搜索 API 密钥 | [Tavily](https://tavily.com/) 免费注册 |

### 步骤 4: 推送代码

```bash
git add .
git commit -m "feat: 添加微博热搜分析 GitHub Actions"
git push origin main
```

### 步骤 5: 手动测试运行

1. 进入仓库的 **Actions** 标签页
2. 选择 **微博热搜产品创意分析** 工作流
3. 点击 **Run workflow** → **Run workflow**
4. 等待执行完成，查看日志和生成的报告

### 步骤 6: 查看报告

执行完成后，报告可通过以下方式获取：

- **Artifacts**: Actions 运行详情页 → 底部 Artifacts 区域下载
- **GitHub Pages** (如已启用): `https://你的用户名.github.io/仓库名/reports/运行编号/`

## 定时执行配置

默认配置每天执行两次（北京时间）：
- 09:00
- 18:00

修改 `.github/workflows/weibo-analysis.yml` 中的 cron 表达式可自定义：

```yaml
schedule:
  - cron: '0 1 * * *'   # UTC 01:00 = 北京时间 09:00
  - cron: '0 10 * * *'  # UTC 10:00 = 北京时间 18:00
```

## 获取 API Keys

### Anthropic API Key
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账户
3. 进入 API Keys 页面
4. 创建新的 API Key

### Tavily API Key
1. 访问 [Tavily](https://tavily.com/)
2. 免费注册账户
3. 获取 API Key（免费套餐每月 1000 次搜索）

### 天行数据 API Key
- 当前 Skill 已内置 Key: `f676388439939fde76b02b20ce32bd54`
- 如需更换，访问 [天行数据](https://www.tianapi.com/)

## 本地测试

```bash
# 设置环境变量
export ANTHROPIC_API_KEY="your-anthropic-key"
export TIANAPI_KEY="your-tianapi-key"
export TAVILY_API_KEY="your-tavily-key"

# 安装依赖
pip install -r requirements.txt

# 运行
python weibo_agent.py
```

## 常见问题

### Q: Actions 执行失败，提示 API Key 未配置？
A: 检查 Secrets 是否正确配置，名称必须完全匹配（区分大小写）。

### Q: 搜索结果不准确？
A: Tavily 免费版有一定限制，可考虑升级付费版本获得更好效果。

### Q: 如何修改分析的热搜数量？
A: 编辑 `weibo_agent.py` 中的 `[:20]` 改为需要的数量。

### Q: 报告保存在哪里？
A: 默认保存在 `./reports/` 目录，可通过 `OUTPUT_DIR` 环境变量修改。

## License

MIT
