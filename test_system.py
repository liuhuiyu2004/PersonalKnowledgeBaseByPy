"""
测试脚本 - 验证知识库系统基本功能

@author LiuHuiYu
"""
import sys
import asyncio

def test_imports():
    """测试依赖导入"""
    print("=" * 50)
    print("测试 1: 检查依赖包")
    print("=" * 50)
    
    try:
        import fastapi
        print("✓ FastAPI:", fastapi.__version__)
        
        import sqlalchemy
        print("✓ SQLAlchemy:", sqlalchemy.__version__)
        
        import pydantic
        print("✓ Pydantic:", pydantic.__version__)
        
        import httpx
        print("✓ httpx:", httpx.__version__)
        
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup4: Installed")
        
        print("\n✅ 所有核心依赖安装成功!\n")
        return True
    except ImportError as e:
        print(f"\n❌ 缺少依赖：{e}")
        print("请运行：pip install -r requirements.txt\n")
        return False


def test_config():
    """测试配置加载"""
    print("=" * 50)
    print("测试 2: 检查配置")
    print("=" * 50)
    
    try:
        from app.config import settings
        
        print(f"✓ 应用名称：{settings.app_name}")
        print(f"✓ 数据库 URL: {settings.database_url}")
        print(f"✓ 主机：{settings.host}:{settings.port}")
        print(f"✓ 调试模式：{settings.debug}")
        
        if settings.openai_api_key:
            print("✓ OpenAI API 密钥：已配置")
        else:
            print("⚠ OpenAI API 密钥：未配置 (AI 功能将使用降级方案)")
        
        print("\n✅ 配置加载成功!\n")
        return True
    except Exception as e:
        print(f"\n❌ 配置加载失败：{e}\n")
        return False


def test_database():
    """测试数据库初始化"""
    print("=" * 50)
    print("测试 3: 检查数据库")
    print("=" * 50)
    
    try:
        from app.models import init_db, engine, Base
        from sqlalchemy import inspect
        
        # 创建表
        init_db()
        print("✓ 数据库表创建成功")
        
        # 检查表是否存在
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✓ 已创建的表：{', '.join(tables)}")
        
        print("\n✅ 数据库初始化成功!\n")
        return True
    except Exception as e:
        print(f"\n❌ 数据库初始化失败：{e}\n")
        return False


def test_crud():
    """测试 CRUD 操作"""
    print("=" * 50)
    print("测试 4: 测试 CRUD 操作")
    print("=" * 50)
    
    try:
        from app.database import get_db, SessionLocal
        import crud
        import schemas
        
        db = SessionLocal()
        
        # 创建测试标签
        print("  创建测试标签...")
        tag = schemas.TagCreate(name="测试标签", color="#ff6b6b")
        created_tag = crud.create_tag(db=db, tag=tag)
        print(f"  ✓ 标签 ID: {created_tag.id}, 名称：{created_tag.name}")
        
        # 创建测试知识
        print("  创建测试知识...")
        knowledge = schemas.KnowledgeCreate(
            title="测试知识条目",
            content="这是一个测试知识条目的内容。用于验证 CRUD 操作是否正常工作。",
            summary="测试摘要",
            source_type="manual",
            tag_ids=[created_tag.id]
        )
        created_knowledge = crud.create_knowledge(db=db, knowledge=knowledge)
        print(f"  ✓ 知识 ID: {created_knowledge.id}, 标题：{created_knowledge.title}")
        
        # 查询知识
        print("  查询知识...")
        retrieved = crud.get_knowledge(db=db, knowledge_id=created_knowledge.id)
        print(f"  ✓ 查询成功：{retrieved.title}")
        
        # 搜索知识
        print("  搜索知识...")
        results, total = crud.search_knowledge(db=db, query="测试")
        print(f"  ✓ 搜索结果：{total} 条")
        
        # 删除知识
        print("  删除知识...")
        crud.delete_knowledge(db=db, knowledge_id=created_knowledge.id)
        print("  ✓ 删除成功")
        
        # 删除标签
        print("  删除标签...")
        crud.delete_tag(db=db, tag_id=created_tag.id)
        print("  ✓ 删除成功")
        
        db.close()
        print("\n✅ CRUD 操作测试通过!\n")
        return True
    except Exception as e:
        print(f"\n❌ CRUD 测试失败：{e}\n")
        import traceback
        traceback.print_exc()
        return False


async def test_crawler():
    """测试爬虫功能"""
    print("=" * 50)
    print("测试 5: 测试网络爬虫")
    print("=" * 50)
    
    try:
        from app.crawler import WebScraper
        
        scraper = WebScraper()
        
        # 测试抓取简单页面
        print("  测试抓取网页...")
        html, error = await scraper.fetch_page("https://www.example.com")
        
        if error:
            print(f"  ⚠ 抓取失败：{error}")
        else:
            print("  ✓ 网页抓取成功")
            
            parsed = scraper.parse_html(html, "https://www.example.com")
            print(f"  ✓ 解析成功，标题：{parsed['title']}")
            print(f"  ✓ 内容长度：{len(parsed['text'])} 字符")
        
        print("\n✅ 爬虫功能测试完成!\n")
        return True
    except Exception as e:
        print(f"\n❌ 爬虫测试失败：{e}\n")
        return False


def test_ai_processor():
    """测试 AI 处理器"""
    print("=" * 50)
    print("测试 6: 测试 AI 处理器")
    print("=" * 50)
    
    try:
        from app.ai_processor import AIProcessor
        
        processor = AIProcessor()
        
        if processor.initialized:
            print("✓ AI 处理器已初始化")
            print(f"✓ 使用模型：{processor.model}")
        else:
            print("⚠ AI 处理器未初始化 (无 API 密钥)")
            print("  将使用基于规则的降级方案")
        
        # 测试规则基础摘要
        print("  测试摘要生成 (规则基础)...")
        test_text = "这是一段测试文本。Python 是一种高级编程语言。它语法简洁，易于学习。"
        summary = processor._rule_based_summarize(test_text, 50)
        print(f"  ✓ 生成摘要：{summary}")
        
        # 测试关键词提取
        print("  测试关键词提取...")
        tags = processor._extract_keywords_rule_based(test_text, 3)
        print(f"  ✓ 提取关键词：{tags}")
        
        print("\n✅ AI 处理器测试完成!\n")
        return True
    except Exception as e:
        print(f"\n❌ AI 测试失败：{e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n")
    print("🚀 " + "=" * 48)
    print("🚀   个人知识库系统 - 功能测试")
    print("🚀 " + "=" * 48)
    print()
    
    results = []
    
    # 运行测试
    results.append(("依赖检查", test_imports()))
    results.append(("配置加载", test_config()))
    results.append(("数据库初始化", test_database()))
    results.append(("CRUD 操作", test_crud()))
    results.append(("AI 处理器", test_ai_processor()))
    results.append(("网络爬虫", asyncio.run(test_crawler())))
    
    # 汇总结果
    print("=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
    
    print()
    print(f"总计：{passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统可以正常使用。\n")
        print("下一步:")
        print("1. 运行 start.bat 启动服务")
        print("2. 访问 http://127.0.0.1:8000 使用 Web 界面")
        print("3. 访问 http://127.0.0.1:8000/docs 查看 API 文档")
    else:
        print("\n⚠ 部分测试失败，请检查错误信息并修复。\n")
    
    print("=" * 50)
    print()


if __name__ == "__main__":
    main()
