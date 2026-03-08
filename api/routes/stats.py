"""
统计信息 API 路由
提供系统统计和概览数据

@author LiuHuiYu
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter()


@router.get("/", response_model=schemas.StatsResponse, summary="获取统计信息")
def get_statistics(db: Session = Depends(get_db)):
    """获取系统统计信息"""
    stats = crud.get_stats(db=db)
    return schemas.StatsResponse(**stats)


@router.get("/recent", response_model=list, summary="最近的知识条目")
def get_recent_knowledge(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取最近添加的知识条目"""
    recent = crud.get_knowledge_list(db=db, skip=0, limit=limit)
    return [k.to_dict() for k in recent]


@router.get("/popular/tags", response_model=list, summary="热门标签")
def get_popular_tags(db: Session = Depends(get_db)):
    """获取使用频率最高的标签"""
    from sqlalchemy import func
    from models import Knowledge, Tag, knowledge_tags
    
    # 查询标签使用次数
    tag_counts = db.query(
        Tag.id,
        Tag.name,
        Tag.color,
        func.count(knowledge_tags.c.knowledge_id).label('count')
    ).join(
        knowledge_tags,
        Tag.id == knowledge_tags.c.tag_id
    ).group_by(
        Tag.id, Tag.name, Tag.color
    ).order_by(
        func.count(knowledge_tags.c.knowledge_id).desc()
    ).limit(10).all()
    
    return [
        {
            'id': t.id,
            'name': t.name,
            'color': t.color,
            'count': t.count
        }
        for t in tag_counts
    ]
