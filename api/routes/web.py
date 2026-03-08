"""
网络爬虫 API 路由
提供网页抓取和网络搜索功能

@author LiuHuiYu
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

import crud
import schemas
from crawler import WebSearcher
from ai_processor import AIProcessor
from database import get_db

router = APIRouter()


@router.post("/fetch", response_model=schemas.KnowledgeResponse, summary="抓取网页并保存")
async def fetch_webpage(
    request: schemas.WebFetchRequest,
    db: Session = Depends(get_db)
):
    """
    抓取指定网页内容并保存到知识库
    
    - **url**: 要抓取的网页 URL
    - **auto_save**: 是否自动保存到知识库
    - **generate_summary**: 是否生成 AI 摘要
    """
    searcher = WebSearcher()
    
    try:
        # 获取网页内容
        page_data = await searcher.fetch_and_parse(request.url)
        if not page_data:
            raise HTTPException(status_code=400, detail="无法获取网页内容，请检查 URL 是否正确或网站是否可访问")
        
        # 生成摘要
        summary = None
        if request.generate_summary:
            ai = AIProcessor()
            summary = await ai.summarize(page_data['text'], max_length=300)
        
        # 保存到知识库
        knowledge_data = schemas.KnowledgeCreate(
            title=page_data.get('title', '无标题'),
            content=page_data.get('content', page_data.get('text', '')),
            summary=summary,
            source_type='web',
            source_url=request.url,
            tag_ids=[]
        )
        
        return crud.create_knowledge(db=db, knowledge=knowledge_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"抓取失败：{str(e)}")


@router.post("/search", response_model=List[dict], summary="网络搜索")
async def search_web(
    request: schemas.WebSearchRequest,
    db: Session = Depends(get_db)
):
    """
    在网络上搜索相关信息
    
    - **query**: 搜索关键词
    - **num_results**: 结果数量
    - **auto_save**: 是否自动保存结果到知识库
    """
    searcher = WebSearcher()
    
    # 执行搜索
    results = await searcher.search(
        query=request.query,
        num_results=request.num_results,
        engine='duckduckgo'
    )
    
    # 如果启用自动保存，保存前几个结果
    if request.auto_save and results:
        ai = AIProcessor()
        
        for result in results[:3]:  # 最多保存前 3 个
            try:
                # 获取详细内容
                page_data = await searcher.fetch_and_parse(result['url'])
                if page_data:
                    # 生成摘要
                    summary = await ai.summarize(page_data['text'], max_length=200)
                    
                    # 保存
                    knowledge = schemas.KnowledgeCreate(
                        title=result['title'] or page_data.get('title', '无标题'),
                        content=page_data.get('content', result.get('snippet', '')),
                        summary=summary,
                        source_type='web',
                        source_url=result['url'],
                        tag_ids=[]
                    )
                    crud.create_knowledge(db=db, knowledge=knowledge)
            except Exception as e:
                print(f"保存搜索结果失败：{e}")
                continue
    
    return results


@router.get("/test/{url:path}", summary="测试网页抓取")
async def test_fetch(url: str):
    """测试抓取指定网页 (返回解析后的内容，不保存)"""
    searcher = WebSearcher()
    page_data = await searcher.fetch_and_parse(url)
    
    if not page_data:
        raise HTTPException(status_code=400, detail="无法获取网页内容")
    
    return {
        'success': True,
        'url': url,
        'title': page_data.get('title', '无标题'),
        'content_length': len(page_data.get('content', '')),
        'text_length': len(page_data.get('text', ''))
    }
