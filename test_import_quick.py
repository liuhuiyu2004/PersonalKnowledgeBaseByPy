"""
快速测试 agent 包导入
"""
import sys
from pathlib import Path

# 确保项目根目录在路径中
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 50)
print("测试 agent 包导入")
print("=" * 50)

try:
    print("\n[1] 测试从 agent.processor 导入...")
    from app.agent.processor import AIProcessor
    print("✓ 成功导入 AIProcessor")
    
    print("\n[2] 测试从 agent.core 导入...")
    from app.agent.core import agent, get_agent, create_agent
    print("✓ 成功导入 agent, get_agent, create_agent")
    
    print("\n[3] 测试从 agent 包导入...")
    from app.agent import AIProcessor, agent
    print("✓ 成功从包级别导入")
    
    print("\n[4] 测试 ai_processor 兼容层...")
    from app.ai_processor import ai_processor, AIProcessor as OldAI
    print("✓ 兼容层导入成功")
    
    print("\n[5] 检查全局实例...")
    print(f"   - agent 类型：{type(agent)}")
    print(f"   - agent.initialized: {agent.initialized}")
    print(f"   - agent.model: {agent.model}")
    
    print("\n" + "=" * 50)
    print("所有导入测试通过！✓")
    print("=" * 50)
    
except Exception as e:
    print(f"\n✗ 导入失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
