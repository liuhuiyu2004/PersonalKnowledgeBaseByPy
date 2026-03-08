"""
Pydantic 模型 - 用于 API 数据验证和序列化

@author LiuHuiYu
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ 标签相关模型 ============
class TagBase(BaseModel):
    """标签基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="标签名称")
    color: Optional[str] = Field(default='#3498db', pattern=r'^#[0-9A-Fa-f]{6}$', description="标签颜色")


class TagCreate(TagBase):
    """创建标签的请求模型"""
    pass


class TagResponse(TagBase):
    """标签响应模型"""
    id: int
    
    class Config:
        from_attributes = True


# ============ 知识条目相关模型 ============
class KnowledgeBase(BaseModel):
    """知识条目基础模型"""
    title: str = Field(..., min_length=1, max_length=500, description="标题")
    content: str = Field(..., min_length=1, description="内容")
    summary: Optional[str] = Field(default=None, description="摘要")
    source_type: Optional[str] = Field(default='manual', description="来源类型")
    source_url: Optional[str] = Field(default=None, max_length=2000, description="来源 URL")


class KnowledgeCreate(KnowledgeBase):
    """创建知识条目的请求模型"""
    tag_ids: Optional[List[int]] = Field(default=[], description="关联的标签 ID 列表")


class KnowledgeUpdate(BaseModel):
    """更新知识条目的请求模型"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    content: Optional[str] = Field(default=None, min_length=1)
    summary: Optional[str] = Field(default=None)
    source_url: Optional[str] = Field(default=None, max_length=2000)
    tag_ids: Optional[List[int]] = Field(default=None)


class KnowledgeResponse(KnowledgeBase):
    """知识条目响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []
    
    class Config:
        from_attributes = True


# ============ 搜索相关模型 ============
class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str = Field(default="", min_length=0, max_length=500, description="搜索关键词")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")
    tag_ids: Optional[List[int]] = Field(default=None, description="按标签筛选")
    source_type: Optional[str] = Field(default=None, description="按来源类型筛选")


class SearchResponse(BaseModel):
    """搜索响应模型"""
    query: str
    total: int
    page: int
    page_size: int
    results: List[KnowledgeResponse]


# ============ 网络爬虫相关模型 ============
class WebFetchRequest(BaseModel):
    """网页抓取请求模型"""
    url: str = Field(..., description="要抓取的网页 URL")
    auto_save: Optional[bool] = Field(default=True, description="是否自动保存到知识库")
    generate_summary: Optional[bool] = Field(default=True, description="是否生成 AI 摘要")


class WebSearchRequest(BaseModel):
    """网络搜索请求模型"""
    query: str = Field(..., min_length=1, max_length=500, description="搜索关键词")
    num_results: Optional[int] = Field(default=5, ge=1, le=20, description="结果数量")
    engine: Optional[str] = Field(default='duckduckgo', description="搜索引擎：duckduckgo 或 bing")
    auto_save: Optional[bool] = Field(default=False, description="是否自动保存结果到知识库")


# ============ AI 处理相关模型 ============
class AISummarizeRequest(BaseModel):
    """AI 摘要请求模型"""
    text: str = Field(..., min_length=1, description="要摘要的文本")
    max_length: Optional[int] = Field(default=200, ge=50, le=1000, description="摘要最大长度")


class AIProcessRequest(BaseModel):
    """AI 处理请求模型"""
    content: str = Field(..., description="要处理的内容")
    task: str = Field(..., description="处理任务：summarize, categorize, extract_tags, etc.")
    options: Optional[dict] = Field(default={}, description="额外选项")


# ============ 统计信息模型 ============
class StatsResponse(BaseModel):
    """统计信息响应模型"""
    total_knowledge: int
    total_tags: int
    total_sources: int
    recent_count: int  # 最近 7 天新增的数量


# ============ 通用响应模型 ============
class MessageResponse(BaseModel):
    """消息响应模型"""
    message: str
    success: bool = True
