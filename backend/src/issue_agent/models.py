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

class ReadIssueInput(BaseModel):
    """read_issue_content 工具的输入模型
    
    用于从 GitHub Issue 数据中提取标题和描述内容。
    
    Attributes:
        title: Issue 标题（必需，非空字符串）
        body: Issue 描述正文（必需，非空字符串）
    """
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )
    
    title: str = Field(
        ...,
        min_length=1,
        description="Issue 标题"
    )
    
    body: str = Field(
        ...,
        min_length=1,
        description="Issue 描述正文"
    )


class CategorizeIssueInput(BaseModel):
    """categorize_issue 工具的输入模型
    
    用于将 Issue 内容分类为 Bug、Feature Request 或 Question。
    
    Attributes:
        text_content: Issue 的文本内容，应包含标题和正文（必需，非空字符串）
    """
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )
    
    text_content: str = Field(
        ...,
        min_length=1,
        description="Issue 的文本内容，包含标题和正文"
    )


class AssignDeveloperInput(BaseModel):
    """assign_developer 工具的输入模型
    
    用于根据 Issue 分类分配负责的开发者。
    
    Attributes:
        category: Issue 分类，必须是 "Bug"、"Feature Request" 或 "Question" 之一（必需）
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
    )
    
    category: CategoryType = Field(
        ...,
        description="Issue 分类"
    )


class IssueClassificationOutput(BaseModel):
    """LLM 返回的分类结果模型
    
    用于 categorize_issue 工具中，表示 LLM 的结构化输出。
    
    Attributes:
        category: Issue 分类，必须是 "Bug"、"Feature Request" 或 "Question" 之一（必需）
        reasoning: 分类的理由说明（可选）
    """
    
    model_config = ConfigDict(
        validate_assignment=True,
    )
    
    category: CategoryType = Field(
        ...,
        description="Issue 分类，必须是 Bug、Feature Request 或 Question 之一"
    )
    
    reasoning: Optional[str] = Field(
        default=None,
        description="分类的理由（可选）"
    )
