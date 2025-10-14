"""
GitHub Issue 自动分诊 Agent

这个模块提供了一个基于 LangChain 和 LangGraph 的自动化 Issue 分诊系统。
系统使用 ReAct Agent 模式，通过定义的工具函数自主完成 Issue 的读取、分类和分配。

主要组件:
- agent: 主 Agent 实现
- tools: 工具函数（read_issue_content, categorize_issue, assign_developer）
- config: 分类和分配配置
- models: 数据模型定义
- main: 主程序入口和示例

使用示例:
    from issue_agent.agent import agent
    from issue_agent.main import SAMPLE_BUG_ISSUE
    
    result = agent.invoke({"messages": [("user", str(SAMPLE_BUG_ISSUE))]})
"""

__version__ = "0.1.0"

from .agent import get_agent, create_triage_agent, create_llm_model

__all__ = [
    "get_agent",
    "create_triage_agent",
    "create_llm_model",
]
