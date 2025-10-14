"""
主 Agent 逻辑

本模块实现 Issue 分诊 Agent 的核心逻辑。
使用 LangGraph 的 StateGraph 构建工作流，结合 LLM 进行推理决策。
每个工具作为独立节点，Agent 可以展示思考过程。
"""

from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# 导入工具
from src.issue_agent.tools import read_issue_content, categorize_issue, assign_developer
# 导入 LLM 创建函数
from src.issue_agent.llm import create_llm_model


class AgentState(TypedDict):
    """Agent 状态定义

    Attributes:
        messages: 消息历史列表，包含 Agent 的思考过程
    """
    messages: Annotated[list[BaseMessage], add_messages]


# Agent System Prompt
# 专注于工作流程指导，具体的分类标准由工具的 prompt 处理
SYSTEM_PROMPT = """你是一个 GitHub Issue 自动分诊助手。你的任务是分析 Issue 并完成以下流程：

工作流程（必须按顺序执行）：
1. 使用 read_issue_content 工具读取 Issue 的标题和描述
2. 使用 categorize_issue 工具对 Issue 进行分类
3. 使用 assign_developer 工具根据分类结果分配合适的开发者

重要说明：
- 必须按照上述顺序依次调用三个工具
- 每个工具的输出是下一个工具的输入
- 在调用每个工具前，简要说明你要做什么
- 在收到工具结果后，简要总结结果

输出格式：
完成所有工具调用后，请总结分诊结果，格式如下：

分诊完成！
- Issue 类型: [分类]
- 分配给: [开发者名称]

请开始执行分诊流程。"""


def call_model(state: AgentState) -> AgentState:
    """调用 LLM 进行推理和决策

    这是 Agent 的核心节点，负责：
    1. 分析当前状态
    2. 决定下一步行动（调用哪个工具）
    3. 生成思考过程

    Args:
        state: 当前 Agent 状态

    Returns:
        更新后的状态，包含 LLM 的响应
    """
    messages = state["messages"]

    # 添加系统提示（如果是第一次调用）
    if len(messages) == 1:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    # 创建 LLM 实例并绑定工具
    llm = create_llm_model()
    tools = [read_issue_content, categorize_issue, assign_developer]
    llm_with_tools = llm.bind_tools(tools)

    # 调用 LLM
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """决定是否继续执行工具调用

    检查最后一条消息是否包含工具调用。
    如果有，继续执行工具；否则结束流程。

    Args:
        state: 当前 Agent 状态

    Returns:
        "tools" 或 "end"
    """
    messages = state["messages"]
    last_message = messages[-1]

    # 如果 LLM 调用了工具，继续执行
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # 否则结束
    return "end"


def create_triage_agent():
    """创建 Issue 分诊 Agent

    使用 StateGraph 构建工作流：
    1. agent 节点：LLM 进行推理和决策
    2. tools 节点：执行工具调用
    3. 条件边：根据 LLM 的决策选择下一步

    Returns:
        编译后的 Agent 图
    """
    # 创建工具节点
    tool_node = ToolNode([read_issue_content, categorize_issue, assign_developer])

    # 创建 StateGraph
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    # 添加边
    workflow.add_edge(START, "agent")

    # 添加条件边：根据 agent 的决策选择下一步
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )

    # 工具执行后返回 agent 继续思考
    workflow.add_edge("tools", "agent")

    # 编译图
    return workflow.compile()


# 创建 Agent 实例供 LangGraph 使用
agent = create_triage_agent()
