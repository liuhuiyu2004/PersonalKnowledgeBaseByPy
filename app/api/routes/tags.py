"""
标签管理 API 路由
提供标签的 CRUD 操作

@author LiuHuiYu
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db
from models import Tag

router = APIRouter()


@router.post("/", response_model=schemas.TagResponse, summary="创建标签")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    """
    创建新标签
    
    - **name**: 标签名称
    - **color**: 标签颜色 (十六进制格式，如 #3498db)
    """
    # 检查是否已存在
    existing = db.query(Tag).filter_by(name=tag.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="标签已存在")
    
    return crud.create_tag(db=db, tag=tag)


@router.get("/", response_model=List[schemas.TagResponse], summary="获取所有标签")
def get_all_tags(db: Session = Depends(get_db)):
    """获取所有标签"""
    return crud.get_all_tags(db=db)


@router.get("/{tag_id}", response_model=schemas.TagResponse, summary="获取单个标签")
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """获取指定 ID 的标签"""
    tag = crud.get_tag(db=db, tag_id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@router.delete("/{tag_id}", response_model=schemas.MessageResponse, summary="删除标签")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """删除标签"""
    success = crud.delete_tag(db=db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="标签不存在")
    return schemas.MessageResponse(message="删除成功", success=True)


@router.put("/{tag_id}", response_model=schemas.TagResponse, summary="更新标签")
def update_tag(tag_id: int, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    """
    更新标签信息
    
    - **name**: 新的标签名称
    - **color**: 新的标签颜色 (十六进制格式)
    """
    # 检查标签是否存在
    existing_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not existing_tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    # 检查新名称是否已被其他标签使用
    name_exists = db.query(Tag).filter(Tag.name == tag.name, Tag.id != tag_id).first()
    if name_exists:
        raise HTTPException(status_code=400, detail="标签名称已存在")
    
    # 更新标签
    existing_tag.name = tag.name
    existing_tag.color = tag.color
    db.commit()
    db.refresh(existing_tag)
    
    return existing_tag
