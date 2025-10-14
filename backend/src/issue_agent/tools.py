"""
工具函数定义

本模块包含 Issue 分诊 Agent 使用的所有工具函数。
使用 LangChain 的 StructuredTool 和 Pydantic 模型进行输入输出验证。
这样可以获得更好的类型安全和自动参数验证。
"""
import os
import json
from typing import Optional
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 导入配置模块
from src.issue_agent.config import config
# 导入模型定义
from src.issue_agent.models import (
    CategoryType,
    ReadIssueInput,
    CategorizeIssueInput,
    AssignDeveloperInput,
    IssueClassificationOutput
)


# ============================================================================
# 工具实现函数
# ============================================================================

@tool("read_issue_content", args_schema=ReadIssueInput, return_direct=False)
def read_issue_content(title: str, body: str) -> str:
    """从 GitHub Issue 数据中提取标题和描述内容。
    
    此工具用于解析 Issue JSON 对象，提取关键信息并格式化为便于后续分析的文本格式。
    这是分诊流程的第一步。
    
    Args:
        title: Issue 标题
        body: Issue 描述正文
        
    Returns:
        格式化的 Issue 内容字符串（JSON 格式）
    """
    # 构建 Issue 数据字典，保持结构清晰
    issue_content = {
        "title": title,
        "body": body
    }
    
    return json.dumps(issue_content, ensure_ascii=False, indent=2)


CLASSIFICATION_PROMPT = """你是一个 GitHub Issue 分类专家。请根据以下 Issue 内容，将其分类为以下三种类型之一：

1. Bug - 软件错误或缺陷
   特征：
   - 错误信息、异常堆栈、崩溃报告
   - 非预期行为、功能不工作、失败
   - 包含关键词：错误、bug、crash、崩溃、不工作、失败、异常、报错等
   - 通常包含复现步骤、环境信息、错误日志

2. Feature Request - 新功能请求或改进建议
   特征：
   - 建议添加新功能或改进现有功能
   - 包含关键词：希望、建议、应该添加、改进、增强、新功能、支持等
   - 描述期望的功能或行为
   - 通常包含使用场景和预期效果

3. Question - 使用问题或疑问
   特征：
   - 询问如何使用、为什么、怎样操作
   - 包含关键词：如何、为什么、怎样、怎么、询问、不理解、求助、请问等
   - 寻求帮助或澄清疑问
   - 通常是对功能或文档的疑问

Issue 内容：
{text_content}

请仔细分析 Issue 的标题和正文内容，根据上述特征进行分类。"""


@tool("categorize_issue", args_schema=CategorizeIssueInput, return_direct=False)
def categorize_issue(text_content: str) -> str:
    """将 Issue 内容分类为 Bug、Feature Request 或 Question。

    此工具使用 LLM 分析 Issue 的文本内容，根据内容特征判断 Issue 的类型。
    这是分诊流程中的核心工具。

    分类标准：
    - Bug: 报告软件错误、异常、崩溃或非预期行为
    - Feature Request: 建议新功能、改进或增强
    - Question: 询问使用方法、寻求帮助或澄清疑问

    Args:
        text_content: Issue 的文本内容，应包含标题和正文信息

    Returns:
        分类结果字符串
    """
    # 创建 LLM 实例（支持 OpenAI 和 Anthropic）
    llm = None

    # 优先使用 OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=openai_api_key
        )
    else:
        # 尝试使用 Anthropic
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_api_key:
            llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0,
                api_key=anthropic_api_key
            )
        else:
            raise ValueError("未找到 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 环境变量")

    # 使用 with_structured_output 确保 LLM 返回结构化数据
    structured_llm = llm.with_structured_output(IssueClassificationOutput)

    # 构建完整的 prompt
    prompt = CLASSIFICATION_PROMPT.format(text_content=text_content)

    # 调用 LLM 进行分类，返回结构化输出
    result: IssueClassificationOutput = structured_llm.invoke(prompt)

    # 返回分类结果（已通过 with_structured_output 和 Pydantic 验证）
    return f'Category: {result.category}\nReasoning: {result.reasoning or "N/A"}'


@tool("assign_developer", args_schema=AssignDeveloperInput, return_direct=False)
def assign_developer(category: CategoryType) -> str:
    """根据 Issue 分类分配负责的开发者。

    此工具根据预定义的分配规则，为不同类型的 Issue 分配
    合适的开发者或团队成员。这是分诊流程的最后一步。

    Args:
        category: Issue 分类（Bug、Feature Request 或 Question）

    Returns:
        被分配开发者的名称字符串
    """
    return config.get_assignee(category)
