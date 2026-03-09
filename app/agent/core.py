"""
Agent 核心模块
提供全局 Agent 实例和高级抽象

@author LiuHuiYu
"""
from .processor import AIProcessor


# 全局 AI 处理器实例（单例模式）
agent = AIProcessor()


def get_agent() -> AIProcessor:
    """
    获取全局 AI 处理器实例
    
    Returns:
        AIProcessor 实例
    """
    return agent


def create_agent(api_key: str | None = None) -> AIProcessor:
    """
    创建自定义的 AI 处理器实例
    
    Args:
        api_key: API 密钥，不指定则使用配置中的默认值
    
    Returns:
        新创建的 AIProcessor 实例
    """
    return AIProcessor(api_key=api_key)
