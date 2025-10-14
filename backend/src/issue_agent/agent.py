"""
主 Agent 逻辑

本模块实现 Issue 分诊 Agent 的核心逻辑。
使用 LangGraph 的 StateGraph 构建工作流，结合 LLM 进行推理决策。
Agent 直接分析 Issue 并分类，只使用工具查询确定性数据（如开发者分配）。
"""

from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# 导入工具
from src.issue_agent.tools import assign_developer
# 导入 LLM 创建函数
from src.issue_agent.llm import create_llm_model
# 导入模型定义
from src.issue_agent.models import CATEGORY_DESCRIPTIONS


class AgentState(TypedDict):
    """Agent 状态定义

    Attributes:
        messages: 消息历史列表，包含 Agent 的思考过程
    """
    messages: Annotated[list[BaseMessage], add_messages]


def _build_system_prompt() -> str:
    """动态构建系统 prompt，包含分类标准"""
    # 构建分类描述部分
    category_sections = []
    for idx, (category, info) in enumerate(CATEGORY_DESCRIPTIONS.items(), 1):
        features = "\n   ".join(f"- {feature}" for feature in info["features"])
        section = f"{idx}. {info['name']} ({category}) - {info['description']}\n   特征：\n   {features}"
        category_sections.append(section)
    
    categories_text = "\n\n".join(category_sections)
    
    return f"""你是一个 GitHub Issue 自动分诊助手。

工作流程：
1. 分析 Issue 的标题和描述内容
2. 根据内容特征进行分类（以下是可用的分类）：

{categories_text}

3. 使用 assign_developer 工具查询该分类对应的开发者

请先分析 Issue 内容，直接在回复中给出分类和理由，然后调用 assign_developer 工具获取开发者信息。"""


# 动态生成系统 prompt
SYSTEM_PROMPT = _build_system_prompt()


def call_model(state: AgentState) -> AgentState:
    """调用 LLM 进行推理和工具调用

    这是 Agent 的核心节点，负责：
    1. 分析 Issue 并进行分类（在回复中展示）
    2. 决定调用 assign_developer 工具
    3. 生成最终总结

    Args:
        state: 当前 Agent 状态

    Returns:
        更新后的状态，包含 LLM 的响应
    """
    messages = state["messages"]

    # 添加系统提示（第一次调用时）
    if len(messages) == 1:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    # 创建 LLM 实例并绑定工具
    llm = create_llm_model()
    tools = [assign_developer]
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

    使用 StateGraph 构建简洁的工作流：
    1. agent 节点：LLM 分析 Issue、给出分类、调用工具
    2. tools 节点：执行工具调用（仅 assign_developer）

    Returns:
        编译后的 Agent 图
    """
    # 创建工具节点（只包含确定性工具）
    tool_node = ToolNode([assign_developer])

    # 创建 StateGraph
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("agent", call_model)   # 主节点：推理 + 工具调用
    workflow.add_node("tools", tool_node)     # 工具执行

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

    # 工具执行后返回 agent 继续（生成总结）
    workflow.add_edge("tools", "agent")

    # 编译图
    return workflow.compile()


# 创建 Agent 实例供 LangGraph 使用
agent = create_triage_agent()
