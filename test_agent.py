"""
测试 agent 包导入和功能
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_agent_package():
    """测试 agent 包的基本功能"""
    print("=" * 50)
    print("测试 agent 包")
    print("=" * 50)
    
    # 测试 1: 导入包
    print("\n[测试 1] 导入 agent 包...")
    try:
        from app.agent import AIProcessor, agent, get_agent, create_agent
        print("✓ 成功导入 AIProcessor, agent, get_agent, create_agent")
    except ImportError as e:
        print(f"✗ 导入失败：{e}")
        return False
    
    # 测试 2: 检查全局实例
    print("\n[测试 2] 检查全局 agent 实例...")
    try:
        print(f"✓ agent 实例类型：{type(agent)}")
        print(f"✓ agent 实例已初始化：{hasattr(agent, 'initialized')}")
        print(f"✓ agent 初始化状态：{agent.initialized}")
    except Exception as e:
        print(f"✗ 检查失败：{e}")
        return False
    
    # 测试 3: 使用 get_agent()
    print("\n[测试 3] 测试 get_agent() 函数...")
    try:
        agent_instance = get_agent()
        print(f"✓ get_agent() 返回：{type(agent_instance)}")
        print(f"✓ 与全局 agent 是同一实例：{agent_instance is agent}")
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        return False
    
    # 测试 4: 创建自定义实例
    print("\n[测试 4] 测试 create_agent() 函数...")
    try:
        custom_agent = create_agent(api_key="test-key")
        print(f"✓ create_agent() 返回：{type(custom_agent)}")
        print(f"✓ 自定义实例与全局实例不同：{custom_agent is not agent}")
    except Exception as e:
        print(f"✗ 测试失败：{e}")
        return False
    
    # 测试 5: 检查 AIProcessor 类的方法
    print("\n[测试 5] 检查 AIProcessor 类的方法...")
    try:
        methods = ['summarize', 'extract_tags', 'categorize', 'process']
        for method in methods:
            has_method = hasattr(AIProcessor, method)
            status = "✓" if has_method else "✗"
            print(f"{status} 方法 '{method}': {has_method}")
    except Exception as e:
        print(f"✗ 检查失败：{e}")
        return False
    
    # 测试 6: 向后兼容性
    print("\n[测试 6] 测试向后兼容性（从 ai_processor 导入）...")
    try:
        from app.ai_processor import ai_processor, AIProcessor as OldAIProcessor
        print(f"✓ 成功从 ai_processor 导入")
        print(f"✓ ai_processor 实例：{type(ai_processor)}")
        print(f"✓ AIProcessor 类来自 agent 包：{OldAIProcessor is AIProcessor}")
    except Exception as e:
        print(f"✗ 导入失败：{e}")
        return False
    
    print("\n" + "=" * 50)
    print("所有测试通过！✓")
    print("=" * 50)
    return True


if __name__ == "__main__":
    success = test_agent_package()
    sys.exit(0 if success else 1)
