"""
知识管理 API 路由
提供知识条目的 CRUD 操作

@author LiuHuiYu
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import schemas
from models import Knowledge
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.KnowledgeResponse, summary="创建知识条目")
def create_knowledge(knowledge: schemas.KnowledgeCreate, db: Session = Depends(get_db)):
    """
    创建新的知识条目
    
    - **title**: 标题
    - **content**: 内容
    - **summary**: 摘要 (可选)
    - **tag_ids**: 关联的标签 ID 列表
    """
    return crud.create_knowledge(db=db, knowledge=knowledge)


@router.get("/", response_model=List[schemas.KnowledgeResponse], summary="获取知识列表")
def get_knowledge_list(
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(20, ge=1, le=100, description="返回数量"),
    tag_ids: Optional[List[int]] = Query(None, description="按标签筛选"),
    source_type: Optional[str] = Query(None, description="按来源类型筛选"),
    db: Session = Depends(get_db)
):
    """获取知识条目列表"""
    return crud.get_knowledge_list(
        db=db, 
        skip=skip, 
        limit=limit,
        tag_ids=tag_ids,
        source_type=source_type
    )


@router.get("/{knowledge_id}", response_model=schemas.KnowledgeResponse, summary="获取单个知识条目")
def get_single_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    """获取指定 ID 的知识条目"""
    knowledge = crud.get_knowledge(db=db, knowledge_id=knowledge_id)
    if not knowledge:
        raise HTTPException(status_code=404, detail="知识条目不存在")
    return knowledge


@router.put("/{knowledge_id}", response_model=schemas.KnowledgeResponse, summary="更新知识条目")
def update_knowledge(
    knowledge_id: int,
    update_data: schemas.KnowledgeUpdate,
    db: Session = Depends(get_db)
):
    """更新知识条目"""
    knowledge = crud.update_knowledge(
        db=db,
        knowledge_id=knowledge_id,
        update_data=update_data
    )
    if not knowledge:
        raise HTTPException(status_code=404, detail="知识条目不存在")
    return knowledge


@router.delete("/{knowledge_id}", response_model=schemas.MessageResponse, summary="删除知识条目")
def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    """删除知识条目"""
    success = crud.delete_knowledge(db=db, knowledge_id=knowledge_id)
    if not success:
        raise HTTPException(status_code=404, detail="知识条目不存在")
    return schemas.MessageResponse(message="删除成功", success=True)


@router.post("/batch/delete", response_model=schemas.MessageResponse, summary="批量删除知识条目")
def batch_delete_knowledge(
    knowledge_ids: List[int],
    db: Session = Depends(get_db)
):
    """批量删除知识条目"""
    count = 0
    for kid in knowledge_ids:
        if crud.delete_knowledge(db=db, knowledge_id=kid):
            count += 1
    
    return schemas.MessageResponse(
        message=f"成功删除 {count}/{len(knowledge_ids)} 个条目",
        success=True
    )
