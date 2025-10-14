"""
测试 Issue Agent 的简单脚本
直接运行 issue_agent 并打印每个消息
"""

from src.issue_agent.agent import agent

# 测试 Issue 数据
test_issue = {
    "title": "应用崩溃无法启动",
    "body": "我在启动应用时遇到了错误，显示 TypeError: Cannot read property 'map' of undefined。请帮忙解决这个问题。"
}

print("=" * 60)
print("开始测试 Issue Agent")
print("=" * 60)
print(f"\n测试 Issue:")
print(f"标题: {test_issue['title']}")
print(f"描述: {test_issue['body']}")
print("\n" + "=" * 60)
print("Agent 执行过程:")
print("=" * 60 + "\n")

# 调用 agent
initial_message = f"请分析以下 Issue:\n标题: {test_issue['title']}\n描述: {test_issue['body']}"

try:
    # 使用 stream 方法逐步打印消息
    for event in agent.stream(
        {"messages": [{"role": "user", "content": initial_message}]},
        stream_mode="values"
    ):
        messages = event.get("messages", [])
        if messages:
            last_message = messages[-1]
            
            # 打印消息类型和内容
            print(f"\n[消息 #{len(messages)}]")
            print(f"类型: {type(last_message).__name__}")
            
            # 如果是 AIMessage，打印内容和工具调用
            if hasattr(last_message, "content") and last_message.content:
                print(f"内容: {last_message.content}")
            
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                print(f"工具调用:")
                for tool_call in last_message.tool_calls:
                    print(f"  - {tool_call['name']}: {tool_call['args']}")
            
            # 如果是 ToolMessage，打印工具结果
            if hasattr(last_message, "name"):
                print(f"工具名称: {last_message.name}")
                if hasattr(last_message, "content"):
                    print(f"工具结果: {last_message.content}")
            
            print("-" * 60)

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ 发生错误: {type(e).__name__}")
    print(f"错误信息: {str(e)}")
    import traceback
    print("\n完整错误堆栈:")
    traceback.print_exc()
