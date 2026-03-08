"""
测试导入是否正常

@author LiuHuiYu
"""
import sys

print("测试 1: 导入 api.routes 包...")
try:
    from api.routes import knowledge, tags, search, web, ai, stats
    print("✅ 成功导入所有路由模块!")
    print(f"   - knowledge: {knowledge}")
    print(f"   - tags: {tags}")
    print(f"   - search: {search}")
    print(f"   - web: {web}")
    print(f"   - ai: {ai}")
    print(f"   - stats: {stats}")
except ImportError as e:
    print(f"❌ 导入失败：{e}")
    sys.exit(1)

print("\n测试 2: 检查 router 对象...")
try:
    print(f"   - knowledge.router: {hasattr(knowledge, 'router')}")
    print(f"   - tags.router: {hasattr(tags, 'router')}")
    print(f"   - search.router: {hasattr(search, 'router')}")
    print(f"   - web.router: {hasattr(web, 'router')}")
    print(f"   - ai.router: {hasattr(ai, 'router')}")
    print(f"   - stats.router: {hasattr(stats, 'router')}")
except Exception as e:
    print(f"❌ 检查失败：{e}")
    sys.exit(1)

print("\n✅ 所有导入测试通过!")
