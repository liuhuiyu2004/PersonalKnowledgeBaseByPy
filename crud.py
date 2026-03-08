"""
CRUD 操作 - 数据访问层
封装对数据库的基本操作

@author LiuHuiYu
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from typing import List, Optional, Dict, Any
import json

from models import Knowledge, Tag, Source, SearchHistory
import schemas


# ============ 知识条目 CRUD ============
def create_knowledge(db: Session, knowledge: schemas.KnowledgeCreate) -> Knowledge:
    """创建新的知识条目"""
    db_knowledge = Knowledge(
        title=knowledge.title,
        content=knowledge.content,
        summary=knowledge.summary,
        source_type=knowledge.source_type,
        source_url=knowledge.source_url,
    )
    
    # 关联标签
    if knowledge.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(knowledge.tag_ids)).all()
        db_knowledge.tags = tags
    
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


def get_knowledge(db: Session, knowledge_id: int) -> Optional[Knowledge]:
    """获取单个知识条目"""
    return db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()


def get_knowledge_list(
    db: Session, 
    skip: int = 0, 
    limit: int = 20,
    tag_ids: Optional[List[int]] = None,
    source_type: Optional[str] = None
) -> List[Knowledge]:
    """获取知识条目列表"""
    query = db.query(Knowledge)
    
    # 按标签筛选
    if tag_ids:
        query = query.join(Knowledge.tags).filter(Tag.id.in_(tag_ids))
    
    # 按来源类型筛选
    if source_type:
        query = query.filter(Knowledge.source_type == source_type)
    
    # 按创建时间倒序排序
    results = query.order_by(Knowledge.created_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()
    
    # 确保标签被加载 (使用 list() 强制执行查询)
    for item in results:
        _ = list(item.tags)
    
    return results


def update_knowledge(
    db: Session, 
    knowledge_id: int, 
    update_data: schemas.KnowledgeUpdate
) -> Optional[Knowledge]:
    """更新知识条目"""
    db_knowledge = get_knowledge(db, knowledge_id)
    if not db_knowledge:
        return None
    
    # 更新字段
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    # 特殊处理 tag_ids
    if 'tag_ids' in update_dict and update_dict['tag_ids'] is not None:
        tags = db.query(Tag).filter(Tag.id.in_(update_dict['tag_ids'])).all()
        db_knowledge.tags = tags
        del update_dict['tag_ids']
    
    # 更新其他字段
    for field, value in update_dict.items():
        setattr(db_knowledge, field, value)
    
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


def delete_knowledge(db: Session, knowledge_id: int) -> bool:
    """删除知识条目"""
    db_knowledge = get_knowledge(db, knowledge_id)
    if not db_knowledge:
        return False
    
    db.delete(db_knowledge)
    db.commit()
    return True


def search_knowledge(
    db: Session, 
    query: str,
    skip: int = 0,
    limit: int = 20,
    tag_ids: Optional[List[int]] = None,
    source_type: Optional[str] = None
) -> tuple[List[Knowledge], int]:
    """搜索知识条目 (全文搜索)"""
    # 构建查询条件
    conditions = or_(
        Knowledge.title.ilike(f'%{query}%'),
        Knowledge.content.ilike(f'%{query}%'),
        Knowledge.summary.ilike(f'%{query}%')
    )
    
    db_query = db.query(Knowledge).filter(conditions)
    
    # 按标签筛选
    if tag_ids:
        db_query = db_query.join(Knowledge.tags).filter(Tag.id.in_(tag_ids))
    
    # 按来源类型筛选
    if source_type:
        db_query = db_query.filter(Knowledge.source_type == source_type)
    
    # 获取总数
    total = db_query.count()
    
    # 获取结果
    results = db_query.order_by(Knowledge.created_at.desc())\
                      .offset(skip)\
                      .limit(limit)\
                      .all()
    
    # 确保标签被加载
    for item in results:
        _ = list(item.tags)
    
    return results, total


# ============ 标签 CRUD ============
def create_tag(db: Session, tag: schemas.TagCreate) -> Tag:
    """创建新标签"""
    db_tag = Tag(name=tag.name, color=tag.color)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_or_create_tag(db: Session, name: str, color: str = '#3498db') -> Tag:
    """获取或创建标签"""
    tag = db.query(Tag).filter(Tag.name == name).first()
    if not tag:
        tag = Tag(name=name, color=color)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag


def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
    """获取单个标签"""
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_all_tags(db: Session) -> List[Tag]:
    """获取所有标签"""
    return db.query(Tag).order_by(Tag.name).all()


def delete_tag(db: Session, tag_id: int) -> bool:
    """删除标签"""
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return False
    
    db.delete(db_tag)
    db.commit()
    return True


# ============ 来源记录 CRUD ============
def create_source(db: Session, source_data: Dict[str, Any]) -> Source:
    """创建来源记录"""
    db_source = Source(**source_data)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


# ============ 搜索历史 CRUD ============
def record_search(db: Session, query: str, results_count: int):
    """记录搜索历史"""
    search_history = SearchHistory(
        query=query,
        results_count=results_count
    )
    db.add(search_history)
    db.commit()


def get_search_history(db: Session, limit: int = 20) -> List[SearchHistory]:
    """获取最近的搜索历史"""
    return db.query(SearchHistory)\
             .order_by(SearchHistory.searched_at.desc())\
             .limit(limit)\
             .all()


# ============ 统计信息 ============
def get_stats(db: Session) -> Dict[str, int]:
    """获取统计信息"""
    total_knowledge = db.query(Knowledge).count()
    total_tags = db.query(Tag).count()
    total_sources = db.query(Source).count()
    
    # 最近 7 天的新增数量
    from datetime import datetime, timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_count = db.query(Knowledge)\
                    .filter(Knowledge.created_at >= seven_days_ago)\
                    .count()
    
    return {
        'total_knowledge': total_knowledge,
        'total_tags': total_tags,
        'total_sources': total_sources,
        'recent_count': recent_count
    }
