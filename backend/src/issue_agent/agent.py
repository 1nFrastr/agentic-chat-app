"""
主 Agent 逻辑

本模块实现 Issue 分诊 Agent 的核心逻辑。
使用 LangGraph 的 StateGraph 构建工作流，结合 LLM 进行推理决策。
Agent 直接分析 Issue 并分类，只使用工具查询确定性数据（如开发者分配）。
"""

import os
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# 导入模型定义
from src.issue_agent.models import (
    CategoryType, 
    AssignDeveloperInput,
    CATEGORY_ASSIGNMENTS,
    DEFAULT_ASSIGNEE
)
# 导入系统 Prompt
from src.issue_agent.prompts import SYSTEM_PROMPT


# ============================================================================
# LLM 模型创建
# ============================================================================

def create_llm_model(temperature: float = 0):
    """创建 LLM 模型实例

    使用统一的 init_chat_model 接口，支持 'provider:model' 格式。
    从环境变量读取 LLM_PROVIDER 和对应的模型名称。
    """
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    
    # 防御式编程：确保 provider 有效
    if provider not in ("openai", "anthropic"):
        raise ValueError(
            f"不支持的 LLM_PROVIDER: {provider}。请设置为 'openai' 或 'anthropic'。"
        )
    
    # 根据 provider 获取对应的模型名称
    model_env_key = f"{provider.upper()}_MODEL"
    default_models = {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-sonnet-20241022"
    }
    model = os.getenv(model_env_key, default_models[provider])
    
    # 直接拼接 model_string
    model_string = f"{provider}:{model}"
    
    return init_chat_model(model_string, temperature=temperature)


# ============================================================================
# 工具定义
# ============================================================================

@tool("assign_developer", args_schema=AssignDeveloperInput, return_direct=False)
def assign_developer(category: CategoryType) -> str:
    """根据 Issue 分类分配负责的开发者。

    此工具根据预定义的分配规则，为不同类型的 Issue 分配
    合适的开发者或团队成员。这是一个确定性操作：给定分类，
    返回对应的开发者。

    Args:
        category: Issue 分类类型

    Returns:
        被分配开发者的名称
    """
    return CATEGORY_ASSIGNMENTS.get(category, DEFAULT_ASSIGNEE)


# ============================================================================
# Agent 状态和节点定义
# ============================================================================


class AgentState(TypedDict):
    """Agent 状态定义

    Attributes:
        messages: 消息历史列表，包含 Agent 的思考过程
    """
    messages: Annotated[list[BaseMessage], add_messages]


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
