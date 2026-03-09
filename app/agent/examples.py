"""
Agent 模块使用示例
演示如何使用 agent 包进行 AI 文本处理
"""

# ============================================
# 示例 1: 基本导入和使用
# ============================================

from agent import AIProcessor, agent, get_agent, create_agent

# 方法 1: 使用全局单例 agent（推荐）
async def use_global_agent():
    """使用全局 agent 实例"""
    summary = await agent.summarize("这是一段测试文本...")
    tags = await agent.extract_tags("这是另一段文本...")
    return summary, tags

# 方法 2: 通过 get_agent() 获取实例
async def use_get_agent():
    """通过函数获取 agent 实例"""
    ai = get_agent()
    result = await ai.process("文本内容", task="summarize")
    return result

# 方法 3: 创建自定义实例
async def use_custom_agent():
    """创建带自定义 API 密钥的 agent"""
    custom_ai = create_agent(api_key="your-api-key-here")
    category = await custom_ai.categorize(
        "文本内容", 
        categories=["技术", "生活", "工作"]
    )
    return category

# 方法 4: 直接实例化 AIProcessor
async def use_ai_processor_class():
    """直接使用 AIProcessor 类"""
    processor = AIProcessor()
    if processor.initialized:
        summary = await processor.summarize("长文本...", max_length=100)
        return summary
    return None


# ============================================
# 示例 2: 在 FastAPI 路由中使用
# ============================================

from fastapi import APIRouter, Depends
from agent import AIProcessor

router = APIRouter()

@router.post("/summarize")
async def summarize_endpoint(text: str):
    """生成文本摘要"""
    # 每次请求创建新实例（或使用全局实例）
    processor = AIProcessor()
    summary = await processor.summarize(text, max_length=200)
    return {"summary": summary}

@router.post("/extract-tags")
async def extract_tags_endpoint(text: str):
    """提取关键词标签"""
    processor = AIProcessor()
    tags = await processor.extract_tags(text, max_tags=5)
    return {"tags": tags}

@router.post("/categorize")
async def categorize_endpoint(text: str, categories: list[str]):
    """文本分类"""
    processor = AIProcessor()
    category = await processor.categorize(text, categories=categories)
    return {"category": category}


# ============================================
# 示例 3: 使用通用处理接口
# ============================================

async def process_with_task(text: str, task_type: str):
    """使用通用处理接口"""
    options = {
        "max_length": 200,
        "max_tags": 5,
        "categories": ["技术", "生活", "工作"],
        "language": "zh"
    }
    
    result = await agent.process(text, task=task_type, options=options)
    return result

# 使用示例
# await process_with_task("文本内容", "summarize")
# await process_with_task("文本内容", "extract_tags")
# await process_with_task("文本内容", "categorize")


# ============================================
# 示例 4: 检查 AI 状态
# ============================================

def check_agent_status():
    """检查 AI 处理器是否可用"""
    processor = AIProcessor()
    
    print(f"初始化状态：{processor.initialized}")
    print(f"使用的模型：{processor.model}")
    print(f"API 密钥配置：{'已配置' if processor.api_key else '未配置'}")
    
    if processor.initialized:
        print("✓ AI 功能已启用")
    else:
        print("⚠ 未配置 API 密钥，将使用降级方案")
    
    return processor.initialized


# ============================================
# 示例 5: 批量处理
# ============================================

import asyncio

async def batch_process(texts: list[str], task: str):
    """批量处理多个文本"""
    processor = AIProcessor()
    tasks = []
    
    for text in texts:
        if task == "summarize":
            tasks.append(processor.summarize(text))
        elif task == "extract_tags":
            tasks.append(processor.extract_tags(text))
    
    # 并发执行
    results = await asyncio.gather(*tasks)
    return results

# 使用示例
# texts = ["文本 1", "文本 2", "文本 3"]
# results = await batch_process(texts, "summarize")


# ============================================
# 示例 6: 依赖注入（FastAPI）
# ============================================

from fastapi import Depends

def get_ai_processor() -> AIProcessor:
    """依赖注入：获取 AI 处理器实例"""
    return get_agent()

@router.post("/process")
async def process_text(
    text: str,
    processor: AIProcessor = Depends(get_ai_processor)
):
    """使用依赖注入的 AI 处理器"""
    summary = await processor.summarize(text)
    return {"summary": summary}


# ============================================
# 完整示例：在 main.py 中集成
# ============================================

"""
from fastapi import FastAPI
from agent import agent, AIProcessor

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    '''应用启动时检查 AI 状态'''
    print(f"AI 处理器已初始化：{agent.initialized}")
    if agent.initialized:
        print(f"使用模型：{agent.model}")

@app.post("/api/ai/summarize")
async def api_summarize(text: str):
    '''API 端点：生成摘要'''
    summary = await agent.summarize(text)
    return {"success": True, "summary": summary}

@app.get("/api/ai/status")
async def api_status():
    '''API 端点：检查 AI 状态'''
    return {
        "available": agent.initialized,
        "model": agent.model if agent.initialized else None
    }
"""
