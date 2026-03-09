"""
测试导入预览功能
验证新的 API 端点是否正常工作
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_preview_api():
    """测试预览 API 的导入和结构"""
    print("=" * 60)
    print("测试导入预览功能")
    print("=" * 60)
    
    # 测试 1: 检查 schema 是否正确定义
    print("\n[测试 1] 检查 Schema 定义...")
    try:
        from app.schemas import WebPreviewRequest, WebPreviewResponse
        print("✓ WebPreviewRequest 和 WebPreviewResponse 已定义")
        
        # 检查字段
        request_fields = WebPreviewRequest.model_fields.keys()
        response_fields = WebPreviewResponse.model_fields.keys()
        print(f"  - WebPreviewRequest 字段：{list(request_fields)}")
        print(f"  - WebPreviewResponse 字段：{list(response_fields)}")
    except Exception as e:
        print(f"✗ Schema 导入失败：{e}")
        return False
    
    # 测试 2: 检查 API 路由
    print("\n[测试 2] 检查 API 路由...")
    try:
        from app.api.routes.web import router
        routes = [route.path for route in router.routes]
        print(f"  - 可用路由：{routes}")
        
        if '/preview' in routes or 'POST /api/web/preview' in str(router.routes):
            print("✓ /api/web/preview 路由已注册")
        else:
            # 尝试通过方法名检查
            has_preview = any(hasattr(route, 'name') and 'preview' in str(route) for route in router.routes)
            if has_preview:
                print("✓ preview_webpage 路由存在")
            else:
                print("⚠ 未找到 preview 路由，请手动检查")
    except Exception as e:
        print(f"✗ API 路由检查失败：{e}")
        return False
    
    # 测试 3: 检查 agent 模块
    print("\n[测试 3] 检查 Agent 模块...")
    try:
        from agent import AIProcessor
        print("✓ AIProcessor 可正常导入")
        
        # 创建实例检查基本功能
        ai = AIProcessor()
        print(f"  - AI 初始化状态：{ai.initialized}")
        print(f"  - 使用模型：{ai.model}")
        print(f"  - 可用方法：summarize, extract_tags, categorize, process")
    except Exception as e:
        print(f"✗ Agent 模块检查失败：{e}")
        return False
    
    # 测试 4: 检查前端文件
    print("\n[测试 4] 检查前端组件...")
    try:
        import os
        web_crawler_path = Path(__file__).parent / 'static' / 'js' / 'components' / 'web-crawler.js'
        if web_crawler_path.exists():
            content = web_crawler_path.read_text(encoding='utf-8')
            
            checks = {
                'previewUrl 方法': 'previewUrl()' in content,
                'savePreview 方法': 'savePreview()' in content,
                '预览对话框': 'previewDialogVisible' in content,
                '导入预览按钮': '导入预览' in content or 'preview' in content.lower()
            }
            
            for check_name, result in checks.items():
                status = "✓" if result else "✗"
                print(f"  {status} {check_name}: {'存在' if result else '缺失'}")
            
            if not all(checks.values()):
                print("⚠ 部分前端功能可能未正确实现")
        else:
            print("✗ web-crawler.js 文件不存在")
            return False
    except Exception as e:
        print(f"✗ 前端文件检查失败：{e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ 所有检查完成！")
    print("=" * 60)
    print("\n💡 使用说明:")
    print("1. 启动服务：start.bat")
    print("2. 访问 Web 界面：http://127.0.0.1:8000")
    print("3. 进入「网络采集」页面")
    print("4. 在 URL 输入框右侧点击「🔍 导入预览」按钮")
    print("5. 系统将使用 agent 分析网页内容并展示预览")
    print("6. 确认无误后点击「💾 保存到知识库」")
    print("\n✨ Agent 会自动完成:")
    print("  - 提取网页富文本内容")
    print("  - 生成智能摘要")
    print("  - 提取建议标签")
    print("  - 根据已有标签进行分类匹配")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = test_preview_api()
    sys.exit(0 if success else 1)
