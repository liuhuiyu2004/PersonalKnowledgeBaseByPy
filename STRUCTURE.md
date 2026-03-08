# 🏗️ 个人知识库系统 - 完整项目结构

## 📊 目录树视图

```
Py/                                    # 项目根目录
│
├── 🔧 核心应用文件
│   ├── main.py                        # ⭐ FastAPI 应用入口
│   ├── config.py                      # ⚙️ 配置管理
│   ├── models.py                      # 💾 数据库模型
│   ├── schemas.py                     # ✅ 数据验证
│   ├── crud.py                        # 🔄 CRUD 操作
│   ├── database.py                    # 🔌 数据库工具
│   ├── crawler.py                     # 🕷️ 网络爬虫
│   └── ai_processor.py                # 🤖 AI 处理
│
├── 🌐 API 路由模块
│   └── api/
│       ├── __init__.py
│       ├── routes.py                  # 路由注册
│       └── routes/
│           ├── knowledge.py           # 📚 知识管理 API
│           ├── tags.py                # 🏷️ 标签管理 API
│           ├── search.py              # 🔍 搜索 API
│           ├── web.py                 # 🌐 网络采集 API
│           ├── ai.py                  # 🤖 AI 处理 API
│           └── stats.py               # 📊 统计信息 API
│
├── 🎨 Web 前端
│   └── static/
│       ├── index.html                 # 🏠 主页面
│       ├── css/
│       │   └── style.css              # 🎨 样式表
│       └── js/
│           ├── app.js                 # 🚀 Vue 主应用
│           └── components/
│               ├── knowledge-list.js   # 📋 列表组件
│               ├── knowledge-editor.js # ✏️ 编辑器组件
│               ├── search-view.js      # 🔍 搜索组件
│               ├── web-crawler.js      # 🕷️ 爬虫组件
│               └── statistics.js       # 📊 统计组件
│
├── 📖 文档
│   ├── README.md                      # 📘 项目说明
│   ├── QUICKSTART.md                  # 🏃 快速开始
│   ├── ARCHITECTURE.md                # 🏛️ 架构设计
│   ├── PROJECT_FILES.md               # 📁 文件清单
│   └── COMPLETION_SUMMARY.md          # ✅ 完成总结
│
├── ⚙️ 配置与脚本
│   ├── requirements.txt               # 📦 Python 依赖
│   ├── .env.example                   # 📝 配置模板
│   ├── .gitignore                     # 🚫 Git 忽略
│   ├── install.bat                    # 📥 安装脚本
│   ├── start.bat                      # ▶️ 启动脚本
│   └── test_system.py                 # 🧪 测试脚本
│
└── 📂 运行时生成 (首次运行后)
    ├── knowledge_base.db              # 💾 SQLite 数据库
    ├── .env                           # ⚙️ 实际配置
    ├── data/                          # 📁 存储目录
    └── __pycache__/                   # 💾 Python 缓存
```

## 📈 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户界面                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Web 浏览器   │  │  API 客户端  │  │  移动设备     │       │
│  │              │  │              │  │              │       │
│  │  Vue 3 +     │  │  curl /      │  │  iOS /       │       │
│  │  Element+    │  │  Postman     │  │  Android     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI 应用层                            │
│                                                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │              API 路由层 (api/routes/)               │     │
│  │                                                    │     │
│  │  Knowledge │ Tags │ Search │ Web │ AI │ Stats    │       │
│  └────────────────────────────────────────────────────┘     │
│                            │                                │
│                            ▼                                │
│  ┌────────────────────────────────────────────────────┐     │
│  │              业务逻辑层                             │     │
│  │                                                    │     │
│  │   CRUD Operations │ Web Crawler │ AI Processor     │     │
│  └────────────────────────────────────────────────────┘     │
│                            │                                │
│                            ▼                                │
│  ┌────────────────────────────────────────────────────┐     │
│  │              数据访问层 (SQLAlchemy)                │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼ SQL
┌─────────────────────────────────────────────────────────────┐
│                    数据存储层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  SQLite DB   │  │  File System │  │  Memory Cache│       │
│  │              │  │              │  │              │       │
│  │  • Knowledge │  │  • Uploads   │  │  • Session   │       │
│  │  • Tags      │  │  • Data/     │  │  • Results   │       │
│  │  • Sources   │  │              │  │              │       │
│  │  • History   │  │              │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 数据流图

### 创建知识流程
```
User Input
    │
    ▼
Web Form / API Request
    │
    ▼
Pydantic Validation (schemas.py)
    │
    ├─✓ Valid ──► CRUD Operation (crud.py)
    │                  │
    │                  ▼
    │            SQLAlchemy ORM
    │                  │
    │                  ▼
    │            Database Insert
    │                  │
    │                  ▼
    └──────────── Response JSON
                      │
                      ▼
                 User Display
```

### 搜索流程
```
Search Query
    │
    ▼
POST /api/search/
    │
    ▼
Validation
    │
    ▼
crud.search_knowledge()
    │
    ├─► Build LIKE Query
    │        │
    │        ▼
    │   SQL Execution
    │        │
    │        ▼
    │   Load Results + Tags
    │        │
    │        ▼
    └──► Format Response
             │
             ▼
        Display Results
```

### 网络采集流程
```
User Provides URL
    │
    ▼
POST /api/web/fetch
    │
    ▼
WebScraper.fetch_page()
    │
    ├─► HTTP Request
    │        │
    │        ▼
    │   Get HTML
    │        │
    │        ▼
    │   BeautifulSoup Parse
    │        │
    │        ▼
    │   Extract Content
    │
    ▼
AIProcessor.summarize() (可选)
    │
    ├─► OpenAI API (如有密钥)
    │        │
    │        ▼
    │   GPT Summary
    │
    └─► Rule-based (降级方案)
             │
             ▼
        Extract Key Sentences
    │
    ▼
crud.create_knowledge()
    │
    ▼
Save to Database
```

## 🔢 模块依赖关系

```
main.py
│
├── config.py
│   └── pydantic-settings
│
├── models.py
│   ├── sqlalchemy
│   └── config.py
│
├── schemas.py
│   └── pydantic
│
├── crud.py
│   ├── models.py
│   ├── schemas.py
│   └── sqlalchemy
│
├── crawler.py
│   ├── httpx
│   ├── beautifulsoup4
│   └── config.py
│
├── ai_processor.py
│   ├── openai (可选)
│   └── config.py
│
└── api/routes/
    ├── crud.py
    ├── schemas.py
    ├── crawler.py
    └── ai_processor.py
```

## 📊 数据库 ER 图

```
┌─────────────────┐       ┌─────────────────┐
│   Knowledge     │       │      Tag        │
│─────────────────│       │─────────────────│
│ PK id           │◄────┐ │ PK id           │
│    title        │     │ │    name         │
│    content      │     └─┤    color        │
│    summary      │       │    created_at   │
│    source_type  │         └─────────────────┘
│    source_url   │               
│    created_at   │       ┌─────────────────┐
│    updated_at   │       │  knowledge_tags │
└─────────────────┘       │─────────────────│
        ▲                 │ PK knowledge_id │
        │                 │ PK tag_id       │
        │                 └─────────────────┘
        │                       
        │                 ┌─────────────────┐
        │                 │    Source       │
        │                 │─────────────────│
        └─────────────────│ PK id           │
                          │ FK knowledge_id │
                          │    url          │
                          │    source_type  │
                          │    metadata     │
                          │    fetched_at   │
                          └─────────────────┘

┌─────────────────┐
│ Search_History  │
│─────────────────│
│ PK id           │
│    query        │
│    results_cnt  │
│    searched_at  │
└─────────────────┘
```

## 🎨 前端组件层次

```
App (app.js)
│
├── Header (导航栏)
│
├── Main Content Area
│   │
│   ├── KnowledgeList (知识列表)
│   │   └── KnowledgeCard (知识卡片)
│   │
│   ├── KnowledgeEditor (编辑器)
│   │   └── Form (表单)
│   │       ├── Title Input
│   │       ├── Content Textarea
│   │       ├── Tag Select
│   │       └── Summary Input
│   │
│   ├── SearchView (搜索)
│   │   ├── SearchBox (搜索框)
│   │   ├── AdvancedFilter (筛选器)
│   │   └── SearchResult (结果列表)
│   │
│   ├── WebCrawler (爬虫)
│   │   ├── FetchTab (抓取)
│   │   └── SearchTab (搜索)
│   │
│   └── Statistics (统计)
│       ├── StatCards (统计卡)
│       ├── PopularTags (热门标签)
│       └── RecentKnowledge (最近知识)
│
└── Footer (页脚)
```

## 🚀 部署架构图

```
开发环境 (当前)
┌─────────────────────────┐
│   Windows / Linux / Mac │
│                         │
│   ┌─────────────────┐  │
│   │   Python venv   │  │
│   │                 │  │
│   │  FastAPI App    │  │
│   │                 │  │
│   │  SQLite DB      │  │
│   └─────────────────┘  │
│                         │
│   直接运行：python      │
└─────────────────────────┘

生产环境 (推荐)
┌─────────────────────────┐
│      Nginx (反向代理)   │
│           │             │
│           ▼             │
│   ┌─────────────────┐  │
│   │   Gunicorn      │  │
│   │   (WSGI Server) │  │
│   │        │        │  │
│   │        ▼        │  │
│   │  FastAPI App    │  │
│   │  (多进程)       │  │
│   └─────────────────┘  │
│                         │
│   PostgreSQL / MySQL    │
│   Redis (缓存)          │
└─────────────────────────┘
```

## 📦 技术栈总览

```
┌─────────────────────────────────────────┐
│              前端层                      │
│  Vue 3 │ Element Plus │ Axios │ CSS3   │
└─────────────────────────────────────────┘
              │
              ▼ REST API
┌─────────────────────────────────────────┐
│              后端层                      │
│  FastAPI │ Pydantic │ SQLAlchemy        │
└─────────────────────────────────────────┘
              │
              ▼ SQL
┌─────────────────────────────────────────┐
│              数据层                      │
│  SQLite │ File System │ Memory Cache    │
└─────────────────────────────────────────┘
              │
              ▼ Integration
┌─────────────────────────────────────────┐
│           外部服务                       │
│  OpenAI API │ DuckDuckGo │ Bing         │
└─────────────────────────────────────────┘
```

---

**版本**: 1.0.0  
**更新日期**: 2026-03-07  
**状态**: ✅ 已完成
