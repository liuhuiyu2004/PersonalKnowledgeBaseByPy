"""
Agent 模块包
提供 AI 智能体功能，包括文本摘要、关键词提取、文本分类等

@author LiuHuiYu
"""
from .processor import AIProcessor
from .core import agent, get_agent, create_agent

__all__ = ['AIProcessor', 'agent', 'get_agent', 'create_agent']
