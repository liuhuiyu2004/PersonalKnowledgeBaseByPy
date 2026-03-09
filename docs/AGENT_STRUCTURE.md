# Agent 模块结构图

## 📁 完整的目录结构

```
Py/
├── app/
│   ├── agent/                    # ⭐ 新增：Agent 模块包
│   │   ├── __init__.py           # 包入口，导出公共接口
│   │   ├── core.py               # 全局实例和工厂函数
│   │   ├── processor.py          # AIProcessor 类实现
│   │   ├── examples.py           # 使用示例代码
│   │   └── README.md             # 详细文档
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── ai.py             # ✅ 更新：使用 from agent import
│   │   │   └── web.py            # ✅ 更新：使用 from agent import
│   │   └── ...
│   │
│   ├── ai_processor.py           # ✅ 重构：兼容层（薄封装）
│   ├── config.py
│   ├── main.py
│   └── ...
│
├── AGENT_REFACTORING.md          # 📋 重构说明文档
├── test_agent.py                 # 🧪 Agent 包测试
└── ...
```

## 🔄 导入关系图

```
┌─────────────────────────────────────────────────────────┐
│                    外部调用代码                           │
│                  (API Routes, Tests)                     │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐      ┌──────────────────┐
│   agent 包    │      │ ai_processor.py  │
│  (推荐使用)   │      │   (兼容层)        │
└──────┬───────┘      └───────┬──────────┘
       │                     │
       ├─────────────────────┤
       │                     │
       ▼                     ▼
┌─────────────────────────────────┐
│      agent/__init__.py          │
│  导出：AIProcessor, agent       │
└─────────────┬───────────────────┘
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
┌───────────┐  ┌────────────┐
│  core.py  │  │processor.py│
│  - agent  │  │ AIProcessor│
│  - factory│  │   Class    │
└───────────┘  └────────────┘
```

## 🎯 模块依赖关系

```
app/api/routes/ai.py
    ↓
app/agent/__init__.py
    ↓
app/agent/processor.py
    ↓
app/config.py
```

```
app/api/routes/web.py
    ↓
app/agent/__init__.py
    ↓
app/agent/processor.py
    ↓
app/config.py
```

## 📦 包的组成

### `__init__.py` - 包入口
```python
"""
Agent 模块包
提供 AI 智能体功能
"""
from .processor import AIProcessor
from .core import agent

__all__ = ['AIProcessor', 'agent']
```

### `core.py` - 核心抽象层
```python
"""Agent 核心模块"""
from .processor import AIProcessor

# 全局单例
agent = AIProcessor()

def get_agent() -> AIProcessor:
    """获取全局实例"""
    return agent

def create_agent(api_key=None) -> AIProcessor:
    """创建自定义实例"""
    return AIProcessor(api_key=api_key)
```

### `processor.py` - 实现层
```python
"""AI 处理器核心实现"""
from config import settings

class AIProcessor:
    """AI 处理器 - 智能文本处理代理"""
    
    def __init__(self, api_key=None):
        # 初始化逻辑
        
    async def summarize(self, text, ...):
        # 摘要逻辑
        
    async def extract_tags(self, text, ...):
        # 标签提取逻辑
        
    async def categorize(self, text, categories, ...):
        # 分类逻辑
        
    async def process(self, content, task, options):
        # 通用处理接口
```

## 🔀 使用流程

### 场景 1: 直接使用全局实例
```
用户代码
    ↓
from agent import agent
    ↓
agent.summarize(text)
    ↓
AIProcessor.summarize()
    ↓
OpenAI API 或 降级方案
```

### 场景 2: 在 FastAPI 中使用
```
API Route (ai.py)
    ↓
from agent import AIProcessor
    ↓
processor = AIProcessor()
    ↓
processor.summarize(text)
    ↓
返回结果
```

### 场景 3: 依赖注入
```
FastAPI Depends
    ↓
get_ai_processor()
    ↓
get_agent()
    ↓
返回全局 agent 实例
    ↓
路由处理函数使用
```

## 📊 文件大小对比

```
重构前:
  ai_processor.py (233 行，单一文件)

重构后:
  agent/__init__.py     (11 行)
  agent/core.py         (35 行)
  agent/processor.py    (242 行)
  agent/examples.py     (197 行)
  agent/README.md       (181 行)
  ai_processor.py       (14 行，兼容层)
  
总计：680 行 (包含文档和示例)
核心代码：~290 行
```

## 🎨 设计模式应用

### 1. 单例模式 (Singleton)
```python
# core.py
agent = AIProcessor()  # 全局唯一实例
```

### 2. 工厂模式 (Factory)
```python
# core.py
def create_agent(api_key=None):
    return AIProcessor(api_key=api_key)
```

### 3. 外观模式 (Facade)
```python
# __init__.py
# 简化接口，隐藏内部实现
__all__ = ['AIProcessor', 'agent']
```

### 4. 兼容层模式 (Compatibility Layer)
```python
# ai_processor.py
# 保持向后兼容的薄封装
from agent import AIProcessor, get_agent
ai_processor = get_agent()
```

## 🚀 扩展性

未来可以在 `agent/` 包中添加：

```
agent/
├── __init__.py
├── core.py
├── processor.py
├── strategies/          # 不同的 AI 策略
│   ├── openai.py
│   ├── anthropic.py
│   └── local.py
├── prompts/            # Prompt 模板
│   ├── summarize.py
│   ├── extract.py
│   └── categorize.py
├── cache/              # 缓存机制
│   └── memory.py
└── utils/              # 工具函数
    └── text.py
```

这样的结构使得：
- ✅ 易于添加新的 AI 提供商
- ✅ 易于定制 Prompt
- ✅ 易于添加缓存功能
- ✅ 代码职责清晰
- ✅ 便于测试和维护
