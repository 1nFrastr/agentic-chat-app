"""
工具函数定义

本模块包含 Issue 分诊 Agent 使用的工具函数。
工具应该是确定性的操作（如查询配置、调用 API），而不应包含 LLM 推理。
"""
from langchain_core.tools import tool

# 导入配置模块
from src.issue_agent.config import config
# 导入模型定义
from src.issue_agent.models import CategoryType, AssignDeveloperInput


# ============================================================================
# 工具实现函数
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
    return config.get_assignee(category)
