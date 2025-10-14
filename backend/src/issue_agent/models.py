"""
数据模型和类型定义

本模块定义了 Issue 分诊系统中使用的数据结构和类型。
使用 TypedDict 提供类型提示，确保数据结构的一致性和类型安全。
"""

from typing import Optional, TypedDict


class IssueData(TypedDict, total=False):
    """GitHub Issue 数据结构
    
    表示从 GitHub API 或其他来源获取的 Issue 数据。
    title 和 body 是必需字段，其他字段为可选。
    
    Attributes:
        title: Issue 标题（必需）
        body: Issue 描述正文（必需）
        number: Issue 编号（可选）
        author: Issue 作者用户名（可选）
        labels: 现有标签列表（可选）
        created_at: Issue 创建时间（可选，ISO 8601 格式）
    
    Example:
        >>> issue: IssueData = {
        ...     "title": "应用启动时崩溃",
        ...     "body": "当我尝试启动应用时，它立即崩溃...",
        ...     "number": 123,
        ...     "author": "user123",
        ...     "labels": ["bug"],
        ...     "created_at": "2024-01-15T10:30:00Z"
        ... }
    """
    title: str
    body: str
    number: Optional[int]
    author: Optional[str]
    labels: Optional[list[str]]
    created_at: Optional[str]


class TriageResult(TypedDict, total=False):
    """Issue 分诊结果数据结构
    
    表示 Agent 完成分诊后的结果，包含分类、分配和相关元数据。
    category 和 assigned_to 是必需字段，其他字段为可选。
    
    Attributes:
        issue_number: 对应的 Issue 编号（可选）
        category: Issue 分类，必须是 "Bug"、"Feature Request" 或 "Question" 之一（必需）
        assigned_to: 被分配的开发者名称（必需）
        confidence: 分类置信度描述，如 "high"、"medium"、"low"（可选）
        reasoning: 分类的理由说明（可选）
    
    Example:
        >>> result: TriageResult = {
        ...     "issue_number": 123,
        ...     "category": "Bug",
        ...     "assigned_to": "张三",
        ...     "confidence": "high",
        ...     "reasoning": "Issue 包含错误堆栈信息和崩溃报告"
        ... }
    """
    issue_number: Optional[int]
    category: str
    assigned_to: str
    confidence: Optional[str]
    reasoning: Optional[str]
