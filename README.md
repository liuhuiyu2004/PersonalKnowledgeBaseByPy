# 个人知识库系统

一个功能完整的本地知识库管理系统，支持 Web 界面和 API 交互，可自动从网络采集信息并使用 AI 整理。

## ✨ 特性

- 📚 **知识管理** - 创建、编辑、删除知识条目
- 🏷️ **标签系统** - 灵活的标签分类和管理
- 🔍 **全文搜索** - 快速检索知识库内容
- 🌐 **网络采集** - 抓取网页内容并自动保存
- 🔎 **网络搜索** - 在网络上搜索相关信息
- 🤖 **AI 处理** - 自动生成摘要、提取标签、文本分类
- 📊 **统计分析** - 查看知识库使用情况
- 🎨 **美观界面** - 现代化的 Web UI
- 🔌 **RESTful API** - 支持程序化调用

## 🚀 快速开始

### 1. 安装依赖

**方式一：使用安装脚本 (推荐)**
```bash
install.bat
```

**方式二：手动安装**
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

复制配置文件模板:
```bash
copy .env.example .env
```

编辑 `.env` 文件，根据需要修改配置:
```ini
# OpenAI API 密钥 (可选，用于 AI 功能)
openai_api_key=your_api_key_here
openai_model=gpt-3.5-turbo

# 服务配置
host=127.0.0.1
port=8000
```

### 3. 启动服务

**方式一：使用启动脚本**
```bash
start.bat
```

**方式二：手动启动**
```bash
python main.py
```

或使用 uvicorn:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 4. 访问

- **Web 界面**: http://127.0.0.1:8000
- **API 文档**: http://127.0.0.1:8000/docs
- **健康检查**: http://127.0.0.1:8000/health

## 📖 使用说明

### Web 界面

1. **知识列表** - 查看所有知识条目，支持分页
2. **新建知识** - 手动添加知识，可使用 AI 生成摘要
3. **搜索** - 关键词搜索，支持标签和来源筛选
4. **网络采集** - 
   - 网页抓取：输入 URL 自动抓取内容
   - 网络搜索：搜索相关信息并保存
5. **统计** - 查看知识库统计数据

### API 使用示例

#### 创建知识条目
```bash
curl -X POST "http://127.0.0.1:8000/api/knowledge/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 基础知识",
    "content": "Python 是一种高级编程语言...",
    "tag_ids": [1, 2]
  }'
```

#### 搜索知识
```bash
curl -X POST "http://127.0.0.1:8000/api/search/" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python",
    "page": 1,
    "page_size": 20
  }'
```

#### 抓取网页
```bash
curl -X POST "http://127.0.0.1:8000/api/web/fetch" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "auto_save": true,
    "generate_summary": true
  }'
```

#### AI 生成摘要
```bash
curl -X POST "http://127.0.0.1:8000/api/ai/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "这是一段很长的文本...",
    "max_length": 200
  }'
```

## 🗂️ 项目结构

```
Py/
├── main.py              # 应用主入口
├── config.py            # 配置管理
├── models.py            # 数据库模型
├── schemas.py           # Pydantic 数据模型
├── crud.py              # 数据库操作
├── crawler.py           # 网络爬虫
├── ai_processor.py      # AI 处理
├── database.py          # 数据库模块
├── requirements.txt     # Python 依赖
├── .env.example         # 配置模板
├── api/                 # API 路由
│   ├── routes/
│   │   ├── knowledge.py
│   │   ├── tags.py
│   │   ├── search.py
│   │   ├── web.py
│   │   ├── ai.py
│   │   └── stats.py
└── static/              # 前端静态文件
    ├── css/
    │   └── style.css
    ├── js/
    │   ├── app.js
    │   └── components/
    │       ├── knowledge-list.js
    │       ├── knowledge-editor.js
    │       ├── search-view.js
    │       ├── web-crawler.js
    │       └── statistics.js
    └── index.html
```

## 💡 功能详解

### 1. 知识管理
- 支持 Markdown 格式内容
- 可关联多个标签
- 记录来源信息 (手动/网页/API)
- 自动记录创建和更新时间

### 2. 标签系统
- 自定义标签名称和颜色
- 支持一对多关系
- 热门标签统计

### 3. 搜索功能
- 全文搜索 (标题、内容、摘要)
- 按标签筛选
- 按来源类型筛选
- 搜索历史记录

### 4. 网络采集
- 智能网页内容提取
- 支持 DuckDuckGo 和 Bing 搜索
- 自动去噪和格式化
- 批量保存搜索结果

### 5. AI 功能
- **摘要生成**: 自动总结长文本
- **标签提取**: 从内容提取关键词
- **文本分类**: 自动归类到预定义类别
- **降级方案**: 无 API 密钥时使用规则基础方法

## ⚙️ 配置说明

### 必需配置
- `database_url`: 数据库连接字符串 (默认 SQLite)
- `storage_path`: 文件存储目录

### 可选配置
- `openai_api_key`: OpenAI API 密钥 (启用高级 AI 功能)
- `openai_model`: 使用的模型名称
- `host`, `port`: 服务监听地址
- `debug`: 调试模式开关

## 🔧 开发指南

### 添加新的 API 路由

1. 在 `api/routes/` 目录创建新文件
2. 定义路由和处理函数
3. 在 `api/routes.py` 中注册路由
4. 在 `main.py` 中包含路由器

### 扩展 AI 功能

在 `ai_processor.py` 中添加新的处理方法:
```python
async def new_task(self, text: str, options: dict) -> dict:
    # 实现你的逻辑
    return {'result': '...'}
```

## 📝 常见问题

### Q: AI 功能无法使用？
A: 检查是否正确配置 `openai_api_key`,或接受使用降级方案。

### Q: 网络爬虫抓取失败？
A: 某些网站可能有反爬机制，尝试更换目标网站或调整爬虫设置。

### Q: 如何备份知识库？
A: 备份 `knowledge_base.db` 文件和 `data/` 目录即可。

### Q: 可以部署到服务器吗？
A: 可以，建议使用 Nginx + Gunicorn + FastAPI 的组合部署。

## 🛠️ 技术栈

- **后端**: FastAPI + SQLAlchemy
- **前端**: Vue 3 + Element Plus
- **数据库**: SQLite
- **爬虫**: httpx + BeautifulSoup4
- **AI**: LangChain + OpenAI API

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📧 联系方式

如有问题请提交 Issue 或联系开发者。

---

**祝你使用愉快！** 🎉
