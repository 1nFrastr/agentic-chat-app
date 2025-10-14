"""
工具函数定义

本模块包含 Issue 分诊 Agent 使用的所有工具函数。
每个工具都使用 LangChain 的 @tool 装饰器定义，提供清晰的描述和类型注解。
"""

import os
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 导入配置模块
from src.issue_agent.config import config


@tool
def read_issue_content(issue_data: dict) -> str:
    """从 GitHub Issue 数据中提取标题和描述内容。
    
    此工具用于解析 Issue JSON 对象，提取关键信息并格式化为
    便于后续分析的文本格式。这是分诊流程的第一步。
    
    Args:
        issue_data: Issue 的 JSON 数据字典，应包含 'title' 和 'body' 字段。
                   其他字段（如 number, author, labels）是可选的。
        
    Returns:
        格式化的 Issue 内容字符串，包含标题和正文。
        格式为: "Title: [标题]\n\nBody: [正文]"
        如果字段缺失或为空，将使用 "N/A" 作为占位符。
        如果输入无效，返回错误信息。
        
    Example:
        >>> issue = {
        ...     "title": "Bug: App crashes on startup",
        ...     "body": "When I click the start button, the app crashes immediately."
        ... }
        >>> content = read_issue_content(issue)
        >>> print(content)
        Title: Bug: App crashes on startup
        
        Body: When I click the start button, the app crashes immediately.
        
    Example with missing body:
        >>> issue = {"title": "Test Issue"}
        >>> content = read_issue_content(issue)
        >>> print(content)
        Title: Test Issue
        
        Body: N/A
    """
    # 输入验证：检查是否为字典类型
    if not isinstance(issue_data, dict):
        return f"错误：issue_data 必须是字典类型，当前类型为 {type(issue_data).__name__}"
    
    # 检查必需字段是否存在
    if "title" not in issue_data:
        return "错误：Issue 数据缺少必需字段 'title'"
    
    if "body" not in issue_data:
        return "错误：Issue 数据缺少必需字段 'body'"
    
    # 提取字段值，处理空值情况
    title = issue_data.get("title")
    body = issue_data.get("body")
    
    # 处理 None 或空字符串的情况
    if not title or (isinstance(title, str) and title.strip() == ""):
        title = "N/A"
    else:
        title = str(title).strip()
    
    if not body or (isinstance(body, str) and body.strip() == ""):
        body = "N/A"
    else:
        body = str(body).strip()
    
    # 格式化输出
    formatted_content = f"Title: {title}\n\nBody: {body}"
    
    return formatted_content


# 分类 Prompt 模板
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

请仔细分析 Issue 的标题和正文内容，根据上述特征进行分类。
只返回分类名称（Bug、Feature Request 或 Question），不要包含其他内容或解释。"""


@tool
def categorize_issue(text_content: str) -> str:
    """将 Issue 内容分类为 Bug、Feature Request 或 Question。

    此工具使用 LLM 分析 Issue 的文本内容，根据内容特征判断
    Issue 的类型。这是分诊流程中的核心工具。

    分类标准：
    - Bug: 报告软件错误、异常、崩溃或非预期行为
      特征包括错误信息、堆栈跟踪、复现步骤等
    - Feature Request: 建议新功能、改进或增强
      特征包括功能建议、改进提议、新特性需求等
    - Question: 询问使用方法、寻求帮助或澄清疑问
      特征包括如何使用、为什么、怎样操作等疑问

    Args:
        text_content: Issue 的文本内容（通常来自 read_issue_content 工具）
                     应包含标题和正文信息

    Returns:
        分类结果，必须是以下之一: "Bug", "Feature Request", "Question"
        如果分类失败或结果无效，默认返回 "Question"
        如果发生错误，返回错误信息字符串

    Example:
        >>> content = "Title: App crashes on startup\\n\\nBody: Stack trace..."
        >>> category = categorize_issue(content)
        >>> print(category)
        Bug

    Example with feature request:
        >>> content = "Title: Add dark mode\\n\\nBody: It would be great to have..."
        >>> category = categorize_issue(content)
        >>> print(category)
        Feature Request
    """
    # 输入验证
    if not text_content or not isinstance(text_content, str):
        return "错误：text_content 必须是非空字符串"

    if text_content.strip() == "":
        return "错误：text_content 不能为空"

    # 有效的分类列表
    VALID_CATEGORIES = ["Bug", "Feature Request", "Question"]

    try:
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
                return "错误：未找到 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 环境变量"

        # 构建完整的 prompt
        prompt = CLASSIFICATION_PROMPT.format(text_content=text_content)

        # 调用 LLM 进行分类
        response = llm.invoke(prompt)

        # 提取分类结果
        category = response.content.strip()

        # 验证分类结果是否有效
        if category not in VALID_CATEGORIES:
            # 尝试模糊匹配（处理 LLM 可能返回的变体）
            category_lower = category.lower()
            if "bug" in category_lower:
                category = "Bug"
            elif "feature" in category_lower or "request" in category_lower:
                category = "Feature Request"
            elif "question" in category_lower:
                category = "Question"
            else:
                # 无效分类，默认为 Question
                print(f"警告：LLM 返回了无效的分类 '{category}'，默认使用 'Question'")
                category = "Question"

        return category

    except Exception as e:
        # LLM 调用失败，返回错误信息
        error_msg = f"错误：分类失败 - {str(e)}"
        print(error_msg)
        return error_msg


@tool
def assign_developer(category: str) -> str:
    """根据 Issue 分类分配负责的开发者。

    此工具根据预定义的分配规则，为不同类型的 Issue 分配
    合适的开发者或团队成员。这是分诊流程的最后一步。

    分配规则：
    - Bug -> 张三（负责 Bug 修复）
    - Feature Request -> 李四（负责新功能开发）
    - Question -> 王五（负责技术支持）
    - 未知分类 -> 项目负责人（默认分配人）

    Args:
        category: Issue 分类（通常来自 categorize_issue 工具）
                 应该是 "Bug", "Feature Request", "Question" 之一

    Returns:
        被分配开发者的名称字符串
        如果分类未知，返回默认分配人 "项目负责人"
        如果输入无效，返回错误信息

    Example:
        >>> developer = assign_developer("Bug")
        >>> print(developer)
        张三

    Example with feature request:
        >>> developer = assign_developer("Feature Request")
        >>> print(developer)
        李四

    Example with unknown category:
        >>> developer = assign_developer("Unknown Type")
        >>> print(developer)
        项目负责人
    """
    # 输入验证：检查是否为字符串类型
    if not isinstance(category, str):
        return f"错误：category 必须是字符串类型，当前类型为 {type(category).__name__}"

    # 检查是否为空字符串
    if category.strip() == "":
        return "错误：category 不能为空字符串"

    # 清理输入（去除首尾空白）
    category = category.strip()

    # 使用配置模块的 get_assignee 方法获取分配人
    try:
        assignee = config.get_assignee(category)
        return assignee
    except Exception as e:
        # 处理意外错误
        error_msg = f"错误：分配开发者失败 - {str(e)}"
        print(error_msg)
        # 返回默认分配人作为降级策略
        return config.default_assignee
