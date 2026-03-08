"""
数据库模型定义
包含知识条目、标签、来源等核心表结构

@author LiuHuiYu
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from config import settings

Base = declarative_base()


# 知识条目和标签的多对多关系表
knowledge_tags = Table(
    'knowledge_tags',
    Base.metadata,
    Column('knowledge_id', Integer, ForeignKey('knowledge.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Knowledge(Base):
    """知识条目表 - 存储核心知识内容"""
    __tablename__ = 'knowledge'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True)  # 标题
    content = Column(Text, nullable=False)  # 主要内容
    summary = Column(Text)  # AI 生成的摘要
    source_type = Column(String(50), default='manual')  # 来源类型：manual(手动), web(网页), api(API), file(文件)
    source_url = Column(String(2000))  # 原始 URL(如果是网络来源)
    created_at = Column(DateTime, default=datetime.now, index=True)  # 创建时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间
    
    # 关联字段
    tags = relationship('Tag', secondary=knowledge_tags, back_populates='knowledge_items', lazy='dynamic')
    sources = relationship('Source', back_populates='knowledge_items', lazy='dynamic')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary or '',
            'source_type': self.source_type,
            'source_url': self.source_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': [tag.to_dict() for tag in self.tags.all()],
        }


class Tag(Base):
    """标签表 - 用于知识分类"""
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    color = Column(String(7), default='#3498db')  # 标签颜色 (十六进制)
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联
    knowledge_items = relationship('Knowledge', secondary=knowledge_tags, back_populates='tags')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
        }


class Source(Base):
    """来源表 - 记录知识的详细来源信息"""
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    knowledge_id = Column(Integer, ForeignKey('knowledge.id', ondelete='CASCADE'), nullable=False)
    url = Column(String(2000))  # 来源 URL
    source_type = Column(String(50), nullable=False)  # manual, web, api, file
    extra_metadata = Column(Text)  # JSON 格式的额外元数据
    fetched_at = Column(DateTime, default=datetime.now)
    
    # 关联
    knowledge_items = relationship('Knowledge', back_populates='sources')
    
    def to_dict(self):
        return {
            'id': self.id,
            'knowledge_id': self.knowledge_id,
            'url': self.url,
            'source_type': self.source_type,
            'extra_metadata': self.extra_metadata,
            'fetched_at': self.fetched_at.isoformat() if self.fetched_at else None,
        }


class SearchHistory(Base):
    """搜索历史表 - 记录用户的搜索行为"""
    __tablename__ = 'search_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String(500), nullable=False)
    results_count = Column(Integer, default=0)
    searched_at = Column(DateTime, default=datetime.now, index=True)


# 创建数据库引擎和会话
engine = create_engine(settings.database_url, echo=settings.debug)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话的依赖注入函数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
