"""
AI 处理 API 路由
提供 AI 文本处理功能

@author LiuHuiYu
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from ai_processor import AIProcessor
from database import get_db

router = APIRouter()


@router.post("/summarize", response_model=dict, summary="生成摘要")
async def summarize_text(
    request: schemas.AISummarizeRequest,
    db: Session = Depends(get_db)
):
    """
    为给定文本生成摘要
    
    - **text**: 要摘要的文本
    - **max_length**: 摘要最大长度
    """
    processor = AIProcessor()
    summary = await processor.summarize(
        text=request.text,
        max_length=request.max_length
    )
    
    return {
        'success': True,
        'summary': summary,
        'original_length': len(request.text),
        'summary_length': len(summary) if summary else 0
    }


@router.post("/extract-tags", response_model=dict, summary="提取标签")
async def extract_tags(
    request: schemas.AIProcessRequest,
    db: Session = Depends(get_db)
):
    """
    从文本中提取关键词标签
    
    - **content**: 要处理的文本
    - **task**: 固定为 'extract_tags'
    - **options**: 
        - max_tags: 最大标签数量
        - language: 语言
    """
    processor = AIProcessor()
    result = await processor.extract_tags(
        text=request.content,
        max_tags=request.options.get('max_tags', 5),
        language=request.options.get('language', 'zh')
    )
    
    return {
        'success': True,
        'tags': result
    }


@router.post("/categorize", response_model=dict, summary="文本分类")
async def categorize_text(
    request: schemas.AIProcessRequest,
    db: Session = Depends(get_db)
):
    """
    将文本分类到指定类别
    
    - **content**: 要处理的文本
    - **task**: 固定为 'categorize'
    - **options**:
        - categories: 可选类别列表
        - language: 语言
    """
    processor = AIProcessor()
    categories = request.options.get('categories', ['技术', '生活', '工作', '学习'])
    
    result = await processor.categorize(
        text=request.content,
        categories=categories,
        language=request.options.get('language', 'zh')
    )
    
    return {
        'success': True,
        'category': result
    }


@router.post("/process", response_model=dict, summary="通用 AI 处理")
async def process_text(
    request: schemas.AIProcessRequest,
    db: Session = Depends(get_db)
):
    """
    通用 AI 处理接口
    
    - **content**: 要处理的内容
    - **task**: 任务类型 (summarize, categorize, extract_tags)
    - **options**: 额外选项
    """
    processor = AIProcessor()
    result = await processor.process(
        content=request.content,
        task=request.task,
        options=request.options
    )
    
    return {
        'success': True,
        'result': result
    }


@router.get("/status", response_model=dict, summary="检查 AI 状态")
async def check_ai_status():
    """检查 AI 处理器是否可用"""
    processor = AIProcessor()
    return {
        'available': processor.initialized,
        'model': processor.model if processor.initialized else None,
        'message': "AI 功能已启用" if processor.initialized else "未配置 API 密钥，使用降级方案"
    }
