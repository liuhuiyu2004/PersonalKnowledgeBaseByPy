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
from agent import AIProcessor
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
            raise HTTPException(status_code=400, detail=f"无法获取网页内容，请检查 URL 是否正确或网站是否可访问。URL: {request.url}")
        
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
        # 打印详细错误信息
        import traceback
        print(f"网页抓取失败：{request.url}")
        print(f"错误详情：{str(e)}")
        print(traceback.format_exc())
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
    - **engine**: 搜索引擎（duckduckgo 或 bing）
    - **auto_save**: 是否自动保存结果到知识库
    """
    searcher = WebSearcher()
    
    # 执行搜索
    results = await searcher.search(
        query=request.query,
        num_results=request.num_results,
        engine=request.engine or 'duckduckgo'  # 使用前端传递的 engine 参数
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


@router.post("/preview", response_model=schemas.WebPreviewResponse, summary="预览并分析网页")
async def preview_webpage(
    request: schemas.WebPreviewRequest,
    db: Session = Depends(get_db)
):
    """
    抓取网页内容并使用 agent 进行分析
    - 提取富文本内容
    - 生成摘要
    - 提取建议标签
    - 根据已有标签进行分类
    
    降级策略：
    1. 优先使用爬虫获取完整内容
    2. 如果失败，使用搜索引擎的摘要信息
    3. 最后返回基本信息
    """
    searcher = WebSearcher()
    ai = AIProcessor()
    
    try:
        print(f"[Preview] 开始分析 URL: {request.url}")
        
        # 策略 1: 尝试爬取网页
        page_data = await searcher.fetch_and_parse(request.url)
        print(f"[Preview] 网页抓取结果：{page_data is not None}")
        
        if page_data:
            # 爬取成功，使用完整功能
            title = page_data.get('title', '无标题')
            content = page_data.get('content', page_data.get('text', ''))
            html_content = page_data.get('html', '')
            
            print(f"[Preview] 网页标题：{title}")
            print(f"[Preview] 内容长度：{len(content)}")
            
            # 使用 agent 生成摘要
            print(f"[Preview] 开始生成摘要...")
            summary = await ai.summarize(content, max_length=300)
            print(f"[Preview] 摘要生成完成：{summary is not None}")
            
            # 使用 agent 提取关键词标签
            print(f"[Preview] 开始提取标签...")
            suggested_tags = await ai.extract_tags(content, max_tags=5)
            print(f"[Preview] 标签提取完成：{suggested_tags}")
            
            # 从数据库获取已有标签，进行分类
            from crud import get_all_tags
            existing_tags = get_all_tags(db)
            tag_names = [tag.name for tag in existing_tags]
            print(f"[Preview] 已有标签：{tag_names}")
            
            category = None
            if tag_names:
                print(f"[Preview] 开始分类...")
                category = await ai.categorize(content, categories=tag_names)
                print(f"[Preview] 分类结果：{category}")
            
            result = schemas.WebPreviewResponse(
                title=title,
                content=content,
                html_content=html_content if html_content else content,
                summary=summary or '',
                suggested_tags=suggested_tags,
                category=category,
                url=request.url,
                source_type='web'
            )
            
            print(f"[Preview] 返回结果：成功（完整模式）")
            return result
        
        # 策略 2: 爬取失败，使用搜索引擎获取基本信息
        print(f"[Preview] 爬取失败，尝试使用搜索引擎...")
        try:
            from crawler import WebSearcher as Searcher
            search_engine = Searcher()
            # 从 URL 提取域名作为搜索关键词
            from urllib.parse import urlparse
            parsed = urlparse(request.url)
            search_query = f"{parsed.path.replace('/', ' ').strip()}"
            
            if not search_query:
                search_query = parsed.netloc
            
            # 搜索相关信息
            search_results = await search_engine.search_duckduckgo(search_query, num_results=3)
            
            if search_results:
                # 找到第一个匹配的 URL
                for result in search_results:
                    if request.url in result.get('url', '') or result.get('url', '') in request.url:
                        print(f"[Preview] 找到匹配结果：{result['title']}")
                        
                        # 使用摘要信息
                        content = result.get('snippet', '')
                        summary = await ai.summarize(content, max_length=200) if content else '无摘要'
                        suggested_tags = await ai.extract_tags(content, max_tags=3) if content else []
                        
                        return schemas.WebPreviewResponse(
                            title=result.get('title', '无标题'),
                            content=content,
                            html_content=f"<p>来自搜索引擎的摘要：</p><blockquote>{content}</blockquote><p>完整内容：<a href='{request.url}' target='_blank'>{request.url}</a></p>",
                            summary=summary or '无摘要',
                            suggested_tags=suggested_tags,
                            category=None,
                            url=request.url,
                            source_type='web'
                        )
        except Exception as search_error:
            print(f"[Preview] 搜索引擎也失败了：{search_error}")
        
        # 策略 3: 所有方法都失败，返回基本信息
        print(f"[Preview] 所有方法失败，返回降级信息")
        return schemas.WebPreviewResponse(
            title=f"无法访问的网页",
            content=f"无法获取网页内容，可能是由于：\n1. 网站有反爬虫机制（如知乎、微信等）\n2. URL 不正确\n3. 网络连接问题\n\n建议：\n- 尝试其他网站（如博客园、CSDN、简书等）\n- 手动复制网页内容到新建知识中\n- 访问：<a href='{request.url}' target='_blank'>{request.url}</a>",
            html_content=f"<p>无法获取网页内容，请手动访问：<a href='{request.url}' target='_blank'>{request.url}</a></p>",
            summary='无法生成摘要（网页无法访问）',
            suggested_tags=[],
            category=None,
            url=request.url,
            source_type='web'
        )
        
    except Exception as e:
        import traceback
        error_detail = f"网页预览分析失败：{request.url}"
        print(error_detail)
        print(f"错误详情：{str(e)}")
        print(traceback.format_exc())
        # 即使是异常也返回降级方案
        return schemas.WebPreviewResponse(
            title=f"分析失败",
            content=f"分析过程中出错：{str(e)}\n\n建议尝试其他网页。",
            html_content=f"<p>分析失败，请手动访问：<a href='{request.url}' target='_blank'>{request.url}</a></p>",
            summary='无法生成摘要',
            suggested_tags=[],
            category=None,
            url=request.url,
            source_type='web'
        )


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
