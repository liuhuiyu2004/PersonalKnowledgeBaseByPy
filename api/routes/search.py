"""
搜索 API 路由
提供知识搜索功能

@author LiuHuiYu
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import schemas
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.SearchResponse, summary="搜索知识")
def search_knowledge(
    search_request: schemas.SearchRequest,
    db: Session = Depends(get_db)
):
    """
    搜索知识库
    
    - **query**: 搜索关键词
    - **page**: 页码
    - **page_size**: 每页数量
    - **tag_ids**: 按标签筛选 (可选)
    - **source_type**: 按来源类型筛选 (可选)
    """
    skip = (search_request.page - 1) * search_request.page_size
    
    results, total = crud.search_knowledge(
        db=db,
        query=search_request.query,
        skip=skip,
        limit=search_request.page_size,
        tag_ids=search_request.tag_ids,
        source_type=search_request.source_type
    )
    
    # 记录搜索历史
    crud.record_search(db=db, query=search_request.query, results_count=total)
    
    return schemas.SearchResponse(
        query=search_request.query,
        total=total,
        page=search_request.page,
        page_size=search_request.page_size,
        results=results
    )


@router.get("/history", response_model=List[dict], summary="获取搜索历史")
def get_search_history(db: Session = Depends(get_db)):
    """获取最近的搜索历史"""
    history = crud.get_search_history(db=db)
    return [
        {
            'query': h.query,
            'results_count': h.results_count,
            'searched_at': h.searched_at.isoformat()
        }
        for h in history
    ]
