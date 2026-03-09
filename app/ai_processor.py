"""
AI 处理模块（兼容层）
此模块已迁移至 agent 包，此处保留以维持向后兼容性

使用新的 agent 包：
    from agent import AIProcessor, agent, get_agent, create_agent

@author LiuHuiYu
"""
from agent import AIProcessor, get_agent, create_agent

# 向后兼容：保持原有的全局实例名称
ai_processor = get_agent()
