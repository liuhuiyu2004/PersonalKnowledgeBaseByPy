# 快速开始指南

## 🎯 5 分钟快速上手

### 第一步：安装依赖

双击运行 `install.bat`,或手动执行:

```bash
pip install -r requirements.txt
```

### 第二步：配置 (可选)

如果需要 AI 功能，编辑 `.env` 文件添加 OpenAI API 密钥:

```ini
openai_api_key=sk-xxxxxxxxxxxxxxx
```

**不配置也可以正常使用**,系统会自动使用规则基础的降级方案。

### 第三步：启动服务

双击运行 `start.bat`,或执行:

```bash
python main.py
```

看到以下信息表示成功:
```
🚀 Personal Knowledge Base 启动成功!
📊 API 文档：http://127.0.0.1:8000/docs
🌐 Web 界面：http://127.0.0.1:8000/
```

### 第四步：开始使用

打开浏览器访问：**http://127.0.0.1:8000**

## 📱 主要功能使用

### 1️⃣ 创建第一个知识条目

1. 点击顶部菜单"新建知识"
2. 填写标题和内容
3. 添加标签 (可直接输入新标签名称)
4. 点击"保存"

### 2️⃣ 从网页采集知识

1. 点击"网络采集"
2. 选择"网页抓取"标签页
3. 输入文章 URL
4. 勾选"自动保存"和"AI 生成摘要"
5. 点击"开始抓取"

系统会自动:
- 提取网页主要内容
- 过滤广告和导航
- 生成摘要
- 保存到知识库

### 3️⃣ 搜索相关知识

1. 点击"搜索"
2. 输入关键词
3. 可使用高级筛选 (标签、来源类型)
4. 查看搜索结果

### 4️⃣ 使用 AI 功能

#### 自动生成摘要
在编辑知识时:
1. 输入内容后
2. 点击"🤖 AI 生成摘要"按钮
3. 等待几秒即可得到智能摘要

#### 网络搜索并保存
1. 点击"网络采集"
2. 选择"网络搜索"标签页
3. 输入想了解的 topic
4. 勾选"自动保存结果"
5. 系统会搜索并保存前 3 条结果

### 5️⃣ 查看统计信息

点击"统计"查看:
- 知识总数
- 标签数量
- 最近 7 天新增
- 热门标签
- 最近添加的知识

## 🔌 API 使用示例

如果你喜欢用命令行或写脚本:

### 创建知识
```bash
curl -X POST "http://127.0.0.1:8000/api/knowledge/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 学习",
    "content": "Python 是一门优雅的编程语言...",
    "tag_ids": []
  }'
```

### 搜索
```bash
curl -X POST "http://127.0.0.1:8000/api/search/" \
  -H "Content-Type: application/json" \
  -d '{"query": "Python"}'
```

### 抓取网页
```bash
curl -X POST "http://127.0.0.1:8000/api/web/fetch" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://zh.wikipedia.org/wiki/Python",
    "auto_save": true
  }'
```

更多 API 文档请访问：**http://127.0.0.1:8000/docs**

## 💡 使用技巧

### 标签管理技巧
1. **颜色编码**: 给不同类别的标签设置不同颜色
   - 技术类：蓝色 (#3498db)
   - 生活类：绿色 (#2ecc71)
   - 工作类：橙色 (#e67e22)

2. **标签层次**: 使用前缀创建层次
   - Python/基础
   - Python/进阶
   - JavaScript/框架

### 搜索技巧
1. 使用简短关键词
2. 利用标签筛选精确范围
3. 可以按来源类型筛选 (只查网页采集的内容)

### 内容组织建议
1. **原子化**: 每条知识聚焦一个主题
2. **结构化**: 使用标题、列表等格式
3. **关联**: 通过标签建立知识间的联系
4. **定期整理**: 删除过时内容，合并相似内容

## ⚙️ 常见问题

### Q: 没有 OpenAI API 密钥能用吗？
**A**: 可以！系统会使用基于规则的智能算法:
- 自动摘要：提取关键句子
- 关键词提取：词频统计 + 停用词过滤
- 虽然不如 AI 强大，但基本够用

### Q: 数据库在哪里？如何备份？
**A**: 数据库文件在项目根目录:
- `knowledge_base.db`
- 直接复制这个文件即可备份

### Q: 如何修改服务端口？
**A**: 编辑 `.env` 文件:
```ini
port=8080
```

### Q: 爬虫抓取失败怎么办？
**A**: 可能原因:
1. 网站有反爬机制
2. 网络连接问题
3. URL 无效

解决方法:
- 换个网站试试
- 检查 URL 是否正确
- 手动复制内容创建知识

### Q: 支持 Markdown 吗？
**A**: 当前版本支持纯文本，Markdown 渲染将在后续版本添加。

## 🎨 自定义

### 修改主题颜色
编辑 `static/css/style.css`:
```css
.stat-card {
    background: linear-gradient(135deg, #你的颜色 0%, #你的颜色 100%);
}
```

### 添加新的 AI 功能
编辑 `ai_processor.py`,添加新方法:
```python
async def translate(self, text: str, target_lang: str = 'en'):
    # 实现翻译逻辑
    pass
```

## 📚 下一步

- 阅读完整文档：[README.md](README.md)
- 了解系统架构：[ARCHITECTURE.md](ARCHITECTURE.md)
- 查看 API 文档：http://127.0.0.1:8000/docs

---

**开始构建你的知识库吧！** 🚀
