"""
FastAPI 应用主文件
配置 CORS、中间件、路由等

@author LiuHuiYu
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from config import settings
from models import init_db
from api.routes import knowledge, tags, search, web, ai, stats

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    description="个人知识库系统 - 支持 Web 界面和 API 交互",
    version="1.0.0"
)

# 配置 CORS (允许前端访问)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    init_db()
    print(f"🚀 {settings.app_name} 启动成功!")
    print(f"📊 API 文档：http://{settings.host}:{settings.port}/docs")
    print(f"🌐 Web 界面：http://{settings.host}:{settings.port}/")


# 挂载静态文件目录 (用于前端页面)
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


# 注册路由
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识管理"])
app.include_router(tags.router, prefix="/api/tags", tags=["标签管理"])
app.include_router(search.router, prefix="/api/search", tags=["搜索"])
app.include_router(web.router, prefix="/api/web", tags=["网络爬虫"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI 处理"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计信息"])


# 根路径 - 返回前端页面
@app.get("/", response_class=HTMLResponse)
async def root():
    """返回前端页面"""
    try:
        with open(os.path.join(static_path, "index.html"), "r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>欢迎使用个人知识库系统</h1><p>请访问 /docs 查看 API 文档</p>")


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug
        )
    except ImportError:
        print("❌ 未安装 uvicorn，请运行：pip install uvicorn[standard]")
