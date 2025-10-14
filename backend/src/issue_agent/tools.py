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
    IssueClassificationOutput,
    CATEGORY_DESCRIPTIONS
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
        格式化的 Issue 内容（JSON 格式）
    """
    # 构建 Issue 数据字典，保持结构清晰
    issue_content = {
        "title": title,
        "body": body
    }
    
    return json.dumps(issue_content, ensure_ascii=False, indent=2)


def _build_classification_prompt() -> str:
    """动态构建分类 prompt，基于 CATEGORY_DESCRIPTIONS 配置。
    
    这样可以确保当添加新分类时，prompt 会自动更新，提高可维护性。
    
    Returns:
        完整的分类 prompt 模板字符串
    """
    # 构建分类描述部分
    category_sections = []
    for idx, (category, info) in enumerate(CATEGORY_DESCRIPTIONS.items(), 1):
        features = "\n   ".join(f"- {feature}" for feature in info["features"])
        section = f"{idx}. {info['name']} - {info['description']}\n   特征：\n   {features}"
        category_sections.append(section)
    
    categories_text = "\n\n".join(category_sections)
    
    # 构建完整 prompt
    prompt_template = f"""你是一个 GitHub Issue 分类专家。请根据以下 Issue 内容，将其分类为以下类型之一：

{categories_text}

Issue 内容：
{{text_content}}

请仔细分析 Issue 的标题和正文内容，根据上述特征进行分类。"""
    
    return prompt_template


# 动态生成分类 prompt
CLASSIFICATION_PROMPT = _build_classification_prompt()


@tool("categorize_issue", args_schema=CategorizeIssueInput, return_direct=False)
def categorize_issue(text_content: str) -> str:
    """对 Issue 内容进行智能分类。

    此工具使用 LLM 分析 Issue 的文本内容，根据内容特征判断 Issue 的类型。
    支持的分类类型在 CATEGORY_DESCRIPTIONS 中定义。这是分诊流程中的核心工具。

    Args:
        text_content: Issue 的文本内容，应包含标题和正文信息

    Returns:
        分类结果字符串，包含类别和分类理由
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
        category: Issue 分类类型

    Returns:
        被分配开发者的名称
    """
    return config.get_assignee(category)
