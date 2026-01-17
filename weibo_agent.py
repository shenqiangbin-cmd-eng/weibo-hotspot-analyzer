#!/usr/bin/env python3
"""
微博热搜产品创意分析 Agent
使用 Claude Agent SDK 实现云端定时执行
（简化版：不依赖网页搜索，直接基于热搜标题分析）
"""

import os
import asyncio
import json
from datetime import datetime
from typing import Any
from pathlib import Path

import httpx
from claude_agent_sdk import (
    tool,
    create_sdk_mcp_server,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)

# 环境变量
TIANAPI_KEY = os.environ.get("TIANAPI_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
ANTHROPIC_BASE_URL = os.environ.get("ANTHROPIC_BASE_URL")  # 支持自定义代理

# 输出目录
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "./reports"))


# ============ 自定义工具定义 ============

@tool("fetch_weibo_hot", "获取微博热搜榜单数据", {})
async def fetch_weibo_hot(args: dict[str, Any]) -> dict[str, Any]:
    """从天行数据 API 获取微博热搜"""
    if not TIANAPI_KEY:
        return {
            "content": [{"type": "text", "text": "错误: TIANAPI_KEY 未配置"}],
            "is_error": True
        }

    url = f"https://apis.tianapi.com/weibohot/index?key={TIANAPI_KEY}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url)
            data = response.json()

            if data.get("code") != 200:
                return {
                    "content": [{"type": "text", "text": f"API 错误: {data.get('msg', '未知错误')}"}],
                    "is_error": True
                }

            hot_list = data.get("result", {}).get("list", [])[:20]

            result_text = f"成功获取 {len(hot_list)} 条微博热搜:\n\n"
            for item in hot_list:
                result_text += f"#{item.get('index', '?')} {item.get('word', '')} (热度: {item.get('hotnum', 0)})\n"

            return {
                "content": [
                    {"type": "text", "text": result_text},
                    {"type": "text", "text": f"\n原始数据:\n```json\n{json.dumps(hot_list, ensure_ascii=False, indent=2)}\n```"}
                ]
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"请求失败: {str(e)}"}],
                "is_error": True
            }


@tool("save_report", "保存 HTML 报告到文件", {"filename": str, "content": str})
async def save_report(args: dict[str, Any]) -> dict[str, Any]:
    """保存 HTML 报告"""
    filename = args.get("filename", "")
    content = args.get("content", "")

    if not filename or not content:
        return {
            "content": [{"type": "text", "text": "错误: 文件名和内容不能为空"}],
            "is_error": True
        }

    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        file_path = OUTPUT_DIR / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "content": [{"type": "text", "text": f"报告已保存到: {file_path.absolute()}"}]
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"保存失败: {str(e)}"}],
            "is_error": True
        }


# ============ Agent 主逻辑 ============

SYSTEM_PROMPT = """你是一个专业的微博热搜产品创意分析师。

你的任务是：
1. 使用 fetch_weibo_hot 工具获取最新的微博热搜榜单（前20条）
2. 基于你的知识和对热点话题的理解，对每个话题进行分析
3. 基于有趣度(80%)和有用度(20%)对每个话题进行评分
4. 根据评分生成产品创意方案：
   - ≥80分：生成3-5个创意
   - 60-79分：生成2-3个创意
   - <60分：生成1-2个创意
5. 生成专业的 HTML 可视化报告，包含：
   - 统计概览（分析话题数、平均分、优秀/良好/一般分布）
   - 每个话题的分析（话题背景推测、社会意义）
   - 产品创意卡片（含评分、核心功能、目标用户）
   - 响应式设计和动画效果
   - 使用现代化 CSS 样式（渐变、阴影、圆角等）
6. 使用 save_report 工具保存报告

评分标准：
- 有趣度(80分)：话题吸引力(20) + 病毒传播性(20) + 情感共鸣(20) + 创意空间(20)
- 有用度(20分)：真实需求(5) + 市场规模(5) + 可行性(5) + 持续性(5)

每个产品创意需包含：
- 产品名称（2-6个字，朗朗上口）
- 核心功能（3-5个要点）
- 目标用户（具体描述）
- 创意评分（0-100）

HTML 报告设计要求：
- 颜色编码：≥80分绿色、60-79分蓝色、<60分灰色
- 卡片式布局，支持移动端响应式
- 包含进度条显示评分
- 所有 CSS 内联，不依赖外部资源

报告文件名格式：weibo_hotspot_analysis_YYYYMMDD_HHMMSS.html
"""


async def run_weibo_agent():
    """运行微博热搜分析 Agent"""

    # 创建 MCP 服务器
    weibo_tools = create_sdk_mcp_server(
        name="weibo-tools",
        version="1.0.0",
        tools=[fetch_weibo_hot, save_report]
    )

    # 配置 Agent 选项
    options = ClaudeAgentOptions(
        mcp_servers={"weibo": weibo_tools},
        allowed_tools=[
            "mcp__weibo__fetch_weibo_hot",
            "mcp__weibo__save_report"
        ],
        system_prompt=SYSTEM_PROMPT,
        max_turns=50,  # 允许足够的交互轮次
    )

    # 执行 Agent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prompt = f"""请开始执行微博热搜产品创意分析任务。

当前时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
报告文件名: weibo_hotspot_analysis_{timestamp}.html

请按照系统提示的步骤执行完整分析，最后保存 HTML 报告。
"""

    print(f"🚀 启动微博热搜分析 Agent...")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)

        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"\n📝 Claude: {block.text[:500]}...")
                    elif isinstance(block, ToolUseBlock):
                        print(f"\n🔧 使用工具: {block.name}")
            elif isinstance(message, ResultMessage):
                print(f"\n💰 总费用: ${message.total_cost_usd:.4f}")
                break

    print("\n" + "-" * 50)
    print("✅ 分析完成!")

    # 列出生成的报告
    if OUTPUT_DIR.exists():
        reports = list(OUTPUT_DIR.glob("*.html"))
        if reports:
            print(f"📊 生成的报告:")
            for report in reports:
                print(f"   - {report}")


if __name__ == "__main__":
    asyncio.run(run_weibo_agent())
