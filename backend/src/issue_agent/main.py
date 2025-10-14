"""
主程序入口和示例数据

本模块提供 Issue 分诊 Agent 的命令行接口和示例数据。
用户可以通过命令行参数选择不同类型的示例 Issue 进行测试。
"""

import json
import argparse
from typing import Any

# 导入 Agent
from .agent import get_agent


# 示例 Issue 数据常量

SAMPLE_BUG_ISSUE = {
    "title": "应用启动时崩溃",
    "body": """
当我尝试启动应用时，它立即崩溃并显示以下错误：

```
TypeError: Cannot read property 'map' of undefined
at App.render (App.js:45)
```

复现步骤：
1. 打开应用
2. 应用立即崩溃

环境：
- 版本: 1.2.3
- 操作系统: Windows 11
    """,
    "number": 123,
    "author": "user123"
}

SAMPLE_FEATURE_ISSUE = {
    "title": "添加暗色模式支持",
    "body": """
希望应用能够支持暗色模式。

建议：
- 添加主题切换按钮
- 自动跟随系统主题
- 保存用户偏好设置

这将大大提升夜间使用体验。
    """,
    "number": 124,
    "author": "user456"
}

SAMPLE_QUESTION_ISSUE = {
    "title": "如何配置数据库连接？",
    "body": """
我是新用户，想知道如何正确配置数据库连接。

我尝试了以下配置但不工作：
```
DB_HOST=localhost
DB_PORT=5432
```

文档中没有找到详细说明，能否提供帮助？
    """,
    "number": 125,
    "author": "user789"
}


def format_result(messages: list) -> dict[str, Any]:
    """格式化 Agent 执行结果
    
    从 Agent 的消息列表中提取关键信息，包括分类和分配人。
    
    Args:
        messages: Agent 执行后返回的消息列表
        
    Returns:
        包含 category 和 assigned_to 的字典
        如果无法提取信息，返回空字典
    """
    result = {
        "category": None,
        "assigned_to": None,
        "raw_output": None
    }
    
    # 获取最后一条消息（Agent 的最终输出）
    if messages:
        final_message = messages[-1]
        if hasattr(final_message, 'content'):
            result["raw_output"] = final_message.content
            
            # 尝试从输出中提取分类和分配人
            content = final_message.content
            
            # 提取 Issue 类型
            if "Issue 类型:" in content or "Issue类型:" in content:
                lines = content.split('\n')
                for line in lines:
                    if "Issue 类型:" in line or "Issue类型:" in line:
                        # 提取冒号后的内容
                        category = line.split(':', 1)[1].strip()
                        result["category"] = category
                        break
            
            # 提取分配人
            if "分配给:" in content or "分配给：" in content:
                lines = content.split('\n')
                for line in lines:
                    if "分配给:" in line or "分配给：" in line:
                        # 提取冒号后的内容
                        assigned = line.split(':', 1)[1].strip()
                        # 移除可能的引号
                        assigned = assigned.strip('"\'')
                        result["assigned_to"] = assigned
                        break
    
    return result


def print_agent_process(messages: list) -> None:
    """打印 Agent 的思考过程和工具调用
    
    遍历消息列表，展示 Agent 的每一步操作，包括：
    - 工具调用
    - 工具返回结果
    - Agent 的思考过程
    
    Args:
        messages: Agent 执行过程中的消息列表
    """
    print("\n" + "="*80)
    print("Agent 执行过程")
    print("="*80 + "\n")
    
    step_count = 0
    
    for msg in messages:
        # 检查消息类型
        msg_type = type(msg).__name__
        
        if hasattr(msg, 'type'):
            msg_type = msg.type
        
        # 处理 AI 消息（Agent 的思考和决策）
        if msg_type == 'ai' or 'AI' in msg_type:
            # 检查是否有工具调用
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    step_count += 1
                    print(f"步骤 {step_count}: 调用工具")
                    print(f"  工具名称: {tool_call.get('name', 'unknown')}")
                    print(f"  工具参数: {json.dumps(tool_call.get('args', {}), ensure_ascii=False, indent=4)}")
                    print()
            
            # 如果有文本内容且不是工具调用
            elif hasattr(msg, 'content') and msg.content and not hasattr(msg, 'tool_calls'):
                step_count += 1
                print(f"步骤 {step_count}: Agent 响应")
                print(f"  {msg.content}")
                print()
        
        # 处理工具消息（工具返回结果）
        elif msg_type == 'tool' or 'Tool' in msg_type:
            if hasattr(msg, 'content'):
                print(f"  工具返回: {msg.content[:200]}{'...' if len(msg.content) > 200 else ''}")
                print()
    
    print("="*80 + "\n")


def run_triage(issue_data: dict) -> None:
    """运行 Issue 分诊流程

    接收 Issue JSON 数据，调用 Agent 进行分诊，
    并打印完整的执行过程和最终结果。

    Args:
        issue_data: Issue 的 JSON 数据字典
    """
    print("\n" + "="*80)
    print("开始 Issue 分诊")
    print("="*80)

    # 打印输入的 Issue 信息
    print(f"\nIssue #{issue_data.get('number', 'N/A')}")
    print(f"标题: {issue_data.get('title', 'N/A')}")
    print(f"作者: {issue_data.get('author', 'N/A')}")
    print("\n正文预览:")
    body = issue_data.get('body', 'N/A')
    body_preview = body[:200] + "..." if len(body) > 200 else body
    print(body_preview)
    print()

    try:
        # 获取 Agent 实例
        print("正在初始化 Agent...")
        agent = get_agent()
        print("Agent 初始化成功！\n")

        # 调用 Agent 进行分诊
        print("正在执行分诊流程...\n")

        # 将 Issue 数据转换为 JSON 字符串作为用户消息
        issue_json = json.dumps(issue_data, ensure_ascii=False)

        # 调用 Agent
        result = agent.invoke({
            "messages": [("user", issue_json)]
        })

        # 打印 Agent 思考过程
        if "messages" in result:
            print_agent_process(result["messages"])

        # 格式化并打印最终结果
        print("="*80)
        print("分诊结果")
        print("="*80 + "\n")

        formatted_result = format_result(result.get("messages", []))

        if formatted_result["category"] and formatted_result["assigned_to"]:
            print(f"✓ Issue 类型: {formatted_result['category']}")
            print(f"✓ 分配给: {formatted_result['assigned_to']}")

            # 根据类型建议优先级
            priority_map = {
                "Bug": "高",
                "Feature Request": "中",
                "Question": "低"
            }
            priority = priority_map.get(formatted_result['category'], "中")
            print(f"✓ 建议优先级: {priority}")
        else:
            print("完整输出:")
            if formatted_result["raw_output"]:
                print(formatted_result["raw_output"])
            else:
                print("无法提取结构化结果")

        print("\n" + "="*80)
        print("分诊完成！")
        print("="*80 + "\n")

    except ValueError as e:
        print(f"\n错误：{e}")
        print("\n请确保已设置以下环境变量之一：")
        print("  - OPENAI_API_KEY")
        print("  - ANTHROPIC_API_KEY")
        print()
    except (RuntimeError, IOError, KeyError) as e:
        print(f"\n执行过程中发生错误：{e}")
        print()


def main():
    """主函数：解析命令行参数并运行分诊流程"""
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="GitHub Issue 自动分诊 Agent - 演示程序",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  python -m issue_agent.main --type bug        # 测试 Bug Issue
  python -m issue_agent.main --type feature    # 测试 Feature Request
  python -m issue_agent.main --type question   # 测试 Question Issue

环境变量：
  需要设置以下环境变量之一：
  - OPENAI_API_KEY: OpenAI API 密钥
  - ANTHROPIC_API_KEY: Anthropic API 密钥
        """
    )
    
    parser.add_argument(
        "--type",
        choices=["bug", "feature", "question"],
        default="bug",
        help="选择要测试的 Issue 类型 (默认: bug)"
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 根据参数选择示例数据
    issue_map = {
        "bug": SAMPLE_BUG_ISSUE,
        "feature": SAMPLE_FEATURE_ISSUE,
        "question": SAMPLE_QUESTION_ISSUE,
    }
    
    selected_issue = issue_map[args.type]
    
    # 打印欢迎信息
    print("\n" + "="*80)
    print("GitHub Issue 自动分诊 Agent")
    print("="*80)
    print(f"\n测试类型: {args.type.upper()}")
    
    # 运行分诊
    run_triage(selected_issue)


if __name__ == "__main__":
    main()
