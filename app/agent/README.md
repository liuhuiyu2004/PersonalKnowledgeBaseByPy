# Agent 模块 - AI 智能体处理包

## 📦 模块结构

```
app/agent/
├── __init__.py      # 包初始化，导出公共接口
├── core.py          # 核心功能：全局实例和工厂函数
├── processor.py     # AI 处理器实现（具体业务逻辑）
└── examples.py      # 使用示例代码
```

## 🎯 主要组件

### 1. AIProcessor 类
位于 `processor.py`，提供以下核心功能：
- **文本摘要** (`summarize`)
- **关键词提取** (`extract_tags`)
- **文本分类** (`categorize`)
- **通用处理** (`process`)

### 2. 全局实例
位于 `core.py`：
- `agent` - 全局单例模式的 AI 处理器
- `get_agent()` - 获取全局实例的函数
- `create_agent(api_key=None)` - 创建自定义实例的工厂函数

## 💻 使用方法

### 基本导入

```python
from agent import AIProcessor, agent, get_agent, create_agent
```

### 使用示例

#### 1. 使用全局实例（推荐）
```python
from agent import agent

# 生成摘要
summary = await agent.summarize("长文本内容...")

# 提取标签
tags = await agent.extract_tags("文章内容...")

# 文本分类
category = await agent.categorize(
    "文本内容", 
    categories=["技术", "生活", "工作"]
)
```

#### 2. 使用 get_agent() 函数
```python
from agent import get_agent

ai_processor = get_agent()
result = await ai_processor.process("文本", task="summarize")
```

#### 3. 创建自定义实例
```python
from agent import create_agent

# 使用自定义 API 密钥
custom_agent = create_agent(api_key="your-api-key")
result = await custom_agent.summarize("文本")
```

#### 4. 直接使用 AIProcessor 类
```python
from agent import AIProcessor

processor = AIProcessor()
if processor.initialized:
    summary = await processor.summarize("文本")
```

## 🔄 向后兼容

为了保持向后兼容性，原有的 `ai_processor.py` 模块仍然可用：

```python
# 旧的导入方式仍然有效
from ai_processor import AIProcessor, ai_processor

# 但实际上这些是从新的 agent 包导入的
```

**建议**：新代码请使用 `from agent import ...` 的方式。

## ⚙️ 配置

AI 处理器从项目的配置文件中读取设置：

```python
# .env 文件
openai_api_key=sk-xxxxxxxxxxxxxxx
openai_model=gpt-3.5-turbo
```

如果没有配置 API 密钥，系统会自动使用基于规则的降级方案。

## 📝 API 路由中的使用

在 FastAPI 路由中使用 agent：

```python
from fastapi import APIRouter, Depends
from agent import AIProcessor

router = APIRouter()

@router.post("/summarize")
async def summarize(text: str):
    processor = AIProcessor()
    summary = await processor.summarize(text)
    return {"summary": summary}
```

## 🔍 检查 AI 状态

```python
from agent import AIProcessor

processor = AIProcessor()
print(f"AI 已初始化：{processor.initialized}")
print(f"使用的模型：{processor.model}")
```

## 🚀 高级用法

### 批量处理
```python
import asyncio
from agent import agent

async def batch_summarize(texts):
    tasks = [agent.summarize(text) for text in texts]
    return await asyncio.gather(*tasks)
```

### 依赖注入
```python
from fastapi import Depends
from agent import get_agent, AIProcessor

def get_ai_processor() -> AIProcessor:
    return get_agent()

@app.post("/process")
async def process_text(
    text: str,
    processor: AIProcessor = Depends(get_ai_processor)
):
    return await processor.summarize(text)
```

## 📊 错误处理

所有 AI 方法都有内置的错误处理：
- 如果 API 调用失败，会自动降级到基于规则的方法
- 返回 `None` 或默认值而不是抛出异常
- 会在控制台打印错误信息用于调试

## 🎯 最佳实践

1. **推荐使用全局实例** `agent`，避免重复初始化
2. **在 Web 请求中**可以每次创建新实例或使用依赖注入
3. **批量处理时**使用 `asyncio.gather()` 并发执行
4. **始终检查** `processor.initialized` 了解 AI 功能是否可用
5. **生产环境**建议配置 API 密钥以获得更好的效果

## 📚 更多信息

- 查看 `examples.py` 了解更多使用示例
- 查看 `processor.py` 了解方法详细参数
- 参考项目文档了解如何配置 AI 功能
