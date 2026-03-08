# 项目结构说明

## 📁 目录结构

```
Py/
├──  核心文件
│   └── app/                  # 应用核心代码目录 ⭐
│       ├── main.py           # FastAPI 应用入口
│       ├── config.py         # 配置管理
│       ├── database.py       # 数据库连接
│       ├── models.py         # 数据库模型
│       ├── schemas.py        # Pydantic 数据模型
│       ├── crud.py           # 数据库操作
│       ├── crawler.py        # 网络爬虫
│       ├── ai_processor.py   # AI 处理模块
│       ├── __init__.py       # 包初始化
│       └── api/              # API 路由
│           ├── __init__.py
│           ├── routes.py     # 路由汇总
│           └── routes/
│               ├── __init__.py
│               ├── ai.py     # AI 相关接口
│               ├── knowledge.py  # 知识管理接口
│               ├── search.py     # 搜索接口
│               ├── stats.py      # 统计接口
│               ├── tags.py       # 标签管理接口
│               └── web.py        # 网络采集接口
│
├──  工具脚本
│   ├── init_tags.py        # 初始化标签数据
│   ├── test_import.py      # 测试导入功能
│   └── test_system.py      # 系统测试
│
├──  数据目录
│   └── data/               # 应用数据 ⭐
│       └── knowledge_base.db # SQLite 数据库
│
├──  启动脚本
│   ├── start.bat           # 启动服务
│   ├── install.bat         # 安装依赖
│   ├── download_libs.bat   # 下载前端依赖（CMD）
│   └── download_libs.ps1   # 下载前端依赖（PowerShell）
│
├──  配置文件
│   ├── .env.example        # 环境变量示例
│   ├── .gitignore          # Git 忽略配置
│   └── requirements.txt    # Python 依赖
│
└──  文档
    ├── README.md           # 项目说明
    ├── QUICKSTART.md       # 快速开始
    └── PROJECT_STRUCTURE.md # 项目结构（本文件）
```

## 🎯 核心模块说明

### 1️⃣ 后端核心 (Backend Core)

**main.py** - 应用入口
- FastAPI 应用配置
- CORS 设置
- 路由注册
- 中间件配置

**config.py** - 配置管理
- 环境变量读取
- 数据库配置
- AI 服务配置

**database.py** - 数据库
- SQLite 连接管理
- Session 工厂创建

### 2️⃣ 数据层 (Data Layer)

**models.py** - 数据库模型
- Knowledge (知识)
- Tag (标签)
- 多对多关系表

**schemas.py** - 数据验证模型
- 请求模型 (Create/Update)
- 响应模型 (Response)
- 数据验证规则

**crud.py** - 数据库操作
- 知识的增删改查
- 标签管理
- 全文搜索

### 3️⃣ 功能模块 (Feature Modules)

**crawler.py** - 网络爬虫
- 网页抓取
- 搜索引擎集成 (DuckDuckGo, Bing)
- HTML 解析

**ai_processor.py** - AI 处理
- 文本摘要
- 内容分类
- 标签提取

### 4️⃣ API 路由 (API Routes)

**api/routes/knowledge.py** - 知识管理
- GET /api/knowledge/ - 获取列表
- POST /api/knowledge/ - 创建知识
- PUT /api/knowledge/{id} - 更新知识
- DELETE /api/knowledge/{id} - 删除知识

**api/routes/tags.py** - 标签管理
- GET /api/tags/ - 获取标签
- POST /api/tags/ - 创建标签
- PUT /api/tags/{id} - 更新标签
- DELETE /api/tags/{id} - 删除标签

**api/routes/search.py** - 搜索功能
- GET /api/search/ - 全文搜索
- GET /api/search/advanced - 高级搜索

**api/routes/web.py** - 网络采集
- POST /api/web/fetch - 抓取网页
- POST /api/web/search - 网络搜索

**api/routes/ai.py** - AI 功能
- POST /api/ai/summarize - 生成摘要
- POST /api/ai/process - AI 处理

**api/routes/stats.py** - 统计信息
- GET /api/stats/ - 获取统计数据

### 5️⃣ 前端组件 (Frontend Components)

**static/index.html** - 主页面
- Vue 3 应用容器
- Element Plus UI
- 路由入口

**static/js/app.js** - 主逻辑
- Vue 应用初始化
- 路由管理
- 全局状态

**组件说明：**
- **knowledge-list.js** - 知识列表视图
- **knowledge-editor.js** - 知识编辑（支持富文本）
- **search-view.js** - 搜索界面
- **web-crawler.js** - 网络采集（网页抓取 + 搜索）
- **tag-manager.js** - 标签管理
- **knowledge-graph.js** - 知识图谱可视化
- **statistics.js** - 统计图表

## 🚀 快速开始

### 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 下载前端依赖（二选一）
.\download_libs.bat      # CMD
.\download_libs.ps1      # PowerShell
```

### 配置环境变量

```bash
# 复制环境变量示例
copy .env.example .env

# 编辑 .env 文件，配置必要参数
# - DATABASE_URL (可选，默认使用 SQLite)
# - OPENAI_API_KEY (可选，AI 功能需要)
```

### 启动服务

```bash
# 使用启动脚本
.\start.bat

# 或手动启动
python main.py
```

访问 http://localhost:8000

## 📊 技术栈

### 后端
- **FastAPI** - Web 框架
- **SQLAlchemy** - ORM
- **SQLite** - 数据库
- **Pydantic** - 数据验证

### 前端
- **Vue 3** - 前端框架
- **Element Plus** - UI 组件库
- **Axios** - HTTP 请求
- **ECharts** - 数据可视化
- **WangEditor** - 富文本编辑器

### AI 集成
- **LangChain** - AI 应用框架
- **OpenAI API** - AI 服务（可选）

## 📝 开发规范

### 目录命名
- Python 文件：小写 + 下划线
- JS 文件：小写 + 连字符
- 组件文件：小写 + 连字符

### 代码组织
- 每个功能模块独立文件
- 组件按功能分类
- 样式统一管理

### 依赖管理
- Python 依赖：requirements.txt
- 前端依赖：本地化存储
- 定期更新依赖版本

---

**@author LiuHuiYu**  
**Last Updated:** 2026-03-08
