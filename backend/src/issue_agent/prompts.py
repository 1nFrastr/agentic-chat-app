"""
Prompt 模板定义

本模块负责生成 Issue 分诊 Agent 使用的各种 prompt。
所有 prompt 生成逻辑集中在此，便于管理和维护。
"""

from src.issue_agent.models import CATEGORY_DESCRIPTIONS


def build_system_prompt() -> str:
    """动态构建系统 prompt，包含分类标准
    
    根据 CATEGORY_DESCRIPTIONS 动态生成 Agent 的系统提示词。
    这样可以确保分类标准的变更自动反映到 prompt 中。
    
    Returns:
        完整的系统提示词字符串
    """
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


# 预生成系统 prompt
SYSTEM_PROMPT = build_system_prompt()
