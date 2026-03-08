# 个人知识库系统 - 架构设计文档

## 📐 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户界面层                                │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Web 界面    │  │  API 客户端   │  │  第三方应用  │       │
│  │  Vue3 + EP  │  │  curl/脚本   │  │  集成        │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API 网关层                                │
│                    FastAPI 应用                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  路由层 (api/routes/)                                 │  │
│  │  • knowledge.py  • tags.py     • search.py           │  │
│  │  • web.py        • ai.py       • stats.py            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      业务逻辑层                               │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  CRUD 操作   │  │  网络爬虫    │  │  AI 处理器    │       │
│  │  (crud.py)  │  │ (crawler.py) │  │(ai_proces..) │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据访问层                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SQLAlchemy ORM + Session                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据存储层                               │
│  ┌─────────────┐  ┌──────────────┐                          │
│  │  SQLite DB  │  │  文件系统    │                          │
│  │  知识/标签   │  │  上传文件    │                          │
│  └─────────────┘  └──────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ 核心模块

### 1. 数据模型层 (models.py)

**Knowledge (知识条目)**
- id, title, content, summary
- source_type, source_url
- created_at, updated_at
- tags (多对多关系)

**Tag (标签)**
- id, name, color
- knowledge_items (多对多关系)

**Source (来源记录)**
- id, knowledge_id, url
- source_type, metadata
- fetched_at

**SearchHistory (搜索历史)**
- id, query, results_count
- searched_at

### 2. 数据验证 (schemas.py)

使用 Pydantic 进行数据验证和序列化:
- TagCreate/TagResponse
- KnowledgeCreate/KnowledgeResponse
- SearchRequest/SearchResponse
- WebFetchRequest/WebSearchRequest
- AISummarizeRequest/AIProcessRequest

### 3. CRUD 操作 (crud.py)

封装所有数据库操作:
- create_knowledge / get_knowledge / update_knowledge / delete_knowledge
- create_tag / get_tag / delete_tag
- search_knowledge (全文搜索)
- record_search / get_search_history
- get_stats (统计信息)

### 4. 网络爬虫 (crawler.py)

**WebScraper 类**
- fetch_page(): 获取网页 HTML
- parse_html(): 解析 HTML，提取内容
- _extract_main_content(): 智能提取正文
- extract_metadata(): 提取元数据

**WebSearcher 类**
- search_duckduckgo(): DuckDuckGo 搜索
- search_bing(): Bing 搜索
- fetch_and_parse(): 抓取并解析

### 5. AI 处理 (ai_processor.py)

**AIProcessor 类**
- summarize(): 文本摘要
- extract_tags(): 关键词提取
- categorize(): 文本分类
- process(): 通用处理接口

**降级方案**: 无 API 密钥时使用规则基础方法

### 6. API 路由 (api/routes/)

**knowledge.py** - 知识管理
- POST / - 创建
- GET / - 列表
- GET /{id} - 详情
- PUT /{id} - 更新
- DELETE /{id} - 删除

**tags.py** - 标签管理
- POST / - 创建
- GET / - 列表
- DELETE /{id} - 删除

**search.py** - 搜索
- POST / - 搜索
- GET /history - 历史

**web.py** - 网络采集
- POST /fetch - 抓取网页
- POST /search - 网络搜索
- GET /test/{url} - 测试抓取

**ai.py** - AI 处理
- POST /summarize - 摘要
- POST /extract-tags - 标签
- POST /categorize - 分类
- GET /status - 状态检查

**stats.py** - 统计
- GET / - 总体统计
- GET /recent - 最近知识
- GET /popular/tags - 热门标签

### 7. Web 前端 (static/)

**Vue 3 组件**
- app.js - 主应用
- knowledge-list.js - 知识列表
- knowledge-editor.js - 编辑器
- search-view.js - 搜索界面
- web-crawler.js - 爬虫界面
- statistics.js - 统计界面

**Element Plus UI**
- 卡片、表单、表格、对话框
- 响应式布局
- 现代化主题

## 🔄 数据流

### 创建知识流程
```
用户 → Web 界面/API → POST /api/knowledge/ 
→ KnowledgeCreate 验证 → crud.create_knowledge() 
→ SQLAlchemy → Database
```

### 搜索流程
```
用户输入关键词 → POST /api/search/
→ SearchRequest 验证 → crud.search_knowledge()
→ SQLAlchemy LIKE 查询 → 返回结果
→ 记录搜索历史
```

### 网络采集流程
```
用户提供 URL → POST /api/web/fetch
→ WebScraper.fetch_page() → BeautifulSoup 解析
→ AIProcessor.summarize() (可选)
→ crud.create_knowledge() → 保存
```

### AI 处理流程
```
请求 AI 服务 → POST /api/ai/summarize
→ AIProcessor 检查 API 密钥
→ 有密钥：调用 OpenAI API
→ 无密钥：使用规则基础方法
→ 返回结果
```

## 🔐 配置管理 (config.py)

```python
class Settings(BaseSettings):
    # 应用配置
    app_name: str
    debug: bool
    host: str
    port: int
    
    # 数据库
    database_url: str
    
    # AI
    openai_api_key: Optional[str]
    openai_model: str
    
    # 爬虫
    user_agent: str
    search_timeout: int
    max_pages_to_fetch: int
    
    # 存储
    storage_path: str
    upload_max_size: int
```

## 📊 数据库设计

```sql
-- 知识表
CREATE TABLE knowledge (
    id INTEGER PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    source_type VARCHAR(50),
    source_url VARCHAR(2000),
    created_at DATETIME,
    updated_at DATETIME
);

-- 标签表
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    color VARCHAR(7),
    created_at DATETIME
);

-- 知识 - 标签关联表
CREATE TABLE knowledge_tags (
    knowledge_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY(knowledge_id) REFERENCES knowledge(id),
    FOREIGN KEY(tag_id) REFERENCES tags(id)
);

-- 来源表
CREATE TABLE sources (
    id INTEGER PRIMARY KEY,
    knowledge_id INTEGER,
    url VARCHAR(2000),
    source_type VARCHAR(50),
    metadata TEXT,
    fetched_at DATETIME
);

-- 搜索历史表
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY,
    query VARCHAR(500),
    results_count INTEGER,
    searched_at DATETIME
);
```

## 🛡️ 错误处理

1. **数据库异常**: try-except + rollback
2. **网络异常**: httpx timeout + 重试机制
3. **AI 服务异常**: 降级到规则基础方法
4. **验证异常**: Pydantic ValidationError
5. **HTTP 异常**: FastAPI HTTPException

## 🚀 性能优化

1. **数据库索引**: title, created_at, tags 建立索引
2. **分页查询**: limit/offset 防止大数据量
3. **异步 IO**: httpx async 爬虫
4. **连接池**: SQLAlchemy session 管理
5. **懒加载**: relationship lazy='dynamic'

## 🔧 扩展性

### 添加新功能步骤:
1. 在 models.py 添加数据模型
2. 在 schemas.py 添加验证模型
3. 在 crud.py 添加数据库操作
4. 在 api/routes/ 添加 API 端点
5. 在 static/js/components/ 添加前端组件
6. 在 main.py 注册路由

### 可扩展方向:
- 用户认证系统
- 文件上传功能
- 更多 AI 模型支持
- 全文搜索引擎 (Elasticsearch)
- 知识图谱可视化
- 数据导出/导入
- 版本控制
- 协作功能

## 📝 开发规范

### 代码风格
- 遵循 PEP 8
- 类型注解
- 文档字符串

### Git 提交
- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- refactor: 重构
- test: 测试相关

### API 设计
- RESTful 风格
- 统一响应格式
- 清晰的错误信息
- 完整的文档

---

**版本**: 1.0.0  
**更新日期**: 2026-03-07
