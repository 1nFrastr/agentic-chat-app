"""
LLM 模型创建和管理

本模块提供统一的 LLM 模型创建接口，支持多个提供商（OpenAI、Anthropic）。
使用 LangChain 的 init_chat_model 接口，符合现代化最佳实践。
"""

import os
from langchain.chat_models import init_chat_model


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
