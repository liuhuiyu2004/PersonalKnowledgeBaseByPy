"""
应用配置文件

@author LiuHuiYu
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    app_name: str = "Personal Knowledge Base"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    
    # 数据库配置
    database_url: str = "sqlite:///./knowledge_base.db"
    
    # AI 配置 (可选)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # 爬虫配置
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    search_timeout: int = 10
    max_pages_to_fetch: int = 5
    
    # 文件存储配置
    storage_path: str = "./data"
    upload_max_size: int = 10485760  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 创建全局配置实例
settings = Settings()

# 确保存储目录存在
os.makedirs(settings.storage_path, exist_ok=True)
