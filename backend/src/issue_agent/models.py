"""
数据模型和类型定义

本模块定义了 Issue 分诊系统中使用的数据结构和类型。
使用 Pydantic 提供数据验证、类型检查和自动转换，确保数据结构的一致性和类型安全。
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# 类型定义
# ============================================================================

# 支持的 Issue 分类类型
CategoryType = Literal["Bug", "Feature Request", "Question"]

# Issue 分类的详细描述和特征
# 用于 LLM 分类时的 prompt 生成，确保分类标准的一致性和可维护性
CATEGORY_DESCRIPTIONS = {
    "Bug": {
        "name": "Bug",
        "description": "软件错误或缺陷",
        "features": [
            "错误信息、异常堆栈、崩溃报告",
            "非预期行为、功能不工作、失败",
            "包含关键词：错误、bug、crash、崩溃、不工作、失败、异常、报错等",
            "通常包含复现步骤、环境信息、错误日志"
        ]
    },
    "Feature Request": {
        "name": "Feature Request",
        "description": "新功能请求或改进建议",
        "features": [
            "建议添加新功能或改进现有功能",
            "包含关键词：希望、建议、应该添加、改进、增强、新功能、支持等",
            "描述期望的功能或行为",
            "通常包含使用场景和预期效果"
        ]
    },
    "Question": {
        "name": "Question",
        "description": "使用问题或疑问",
        "features": [
            "询问如何使用、为什么、怎样操作",
            "包含关键词：如何、为什么、怎样、怎么、询问、不理解、求助、请问等",
            "寻求帮助或澄清疑问",
            "通常是对功能或文档的疑问"
        ]
    }
}

# Issue 分类到开发者的分配映射
# 注意: 此字典的键必须与 CategoryType 中定义的分类保持一致
CATEGORY_ASSIGNMENTS = {
    "Bug": "张三",
    "Feature Request": "李四",
    "Question": "王五",
}

# 默认分配人(当分类不在上述映射中时使用)
DEFAULT_ASSIGNEE = "项目负责人"


# ============================================================================
# 工具输入模型定义
# ============================================================================

class AssignDeveloperInput(BaseModel):
    """assign_developer 工具的输入模型
    
    用于根据 Issue 分类分配负责的开发者。
    这是一个确定性工具：给定分类，返回对应的开发者。
    
    Attributes:
        category: Issue 分类类型
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
    )
    
    category: CategoryType = Field(
        ...,
        description="Issue 分类类型"
    )


# ============================================================================
# LLM 输出模型定义
# ============================================================================

class IssueClassificationOutput(BaseModel):
    """LLM 返回的分类结果模型
    
    用于 Agent 中的结构化输出，让 LLM 直接进行分类推理。
    不通过工具调用，而是通过 with_structured_output 实现。
    
    Attributes:
        category: Issue 分类类型
        reasoning: 分类的理由说明
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
    )
    
    category: CategoryType = Field(
        ...,
        description="Issue 分类类型"
    )
    
    reasoning: str = Field(
        ...,
        description="分类的理由，解释为什么将 Issue 归类为该类型"
    )
