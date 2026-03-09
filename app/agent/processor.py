"""
AI 处理器核心实现
提供文本摘要、关键词提取、文本分类等功能

@author LiuHuiYu
"""
from typing import Optional, Dict, Any, List
import json
import sys
from pathlib import Path

# 动态添加项目根目录到 Python 路径，确保可以导入 config
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent  # app/
sys.path.insert(0, str(project_root))

# 现在可以正常导入 config
from config import settings


class AIProcessor:
    """AI 处理器 - 智能文本处理代理"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 AI 处理器
        
        Args:
            api_key: API 密钥，默认从配置读取
        """
        self.api_key = api_key or settings.openai_api_key
        self.model = settings.openai_model
        self.initialized = bool(self.api_key)
        
        if self.initialized:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                print("未安装 openai 库，AI 功能将不可用")
                self.initialized = False
    
    async def summarize(
        self, 
        text: str, 
        max_length: int = 200,
        language: str = 'zh'
    ) -> Optional[str]:
        """
        生成文本摘要
        
        Args:
            text: 要摘要的文本
            max_length: 摘要最大长度
            language: 语言 ('zh' 或 'en')
        
        Returns:
            摘要文本
        """
        if not self.initialized:
            return self._rule_based_summarize(text, max_length)
        
        lang_name = "中文" if language == 'zh' else "English"
        prompt = f"""请用{lang_name}为以下文本生成一个简洁的摘要，不超过{max_length}字：

{text[:3000]}  # 限制输入长度

摘要:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that summarizes text in {lang_name}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length // 2,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI 摘要失败：{e}")
            return self._rule_based_summarize(text, max_length)
    
    def _rule_based_summarize(self, text: str, max_length: int) -> str:
        """基于规则的摘要 (当 AI 不可用时的降级方案)"""
        # 简单实现：取前几句话
        sentences = text.replace('。', '.').replace('!', '!').replace('？', '?').split('.')
        summary = ''
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and len(summary) + len(sentence) < max_length:
                summary += sentence + '。'
            if len(summary) >= max_length:
                break
        return summary[:max_length] + '...' if len(summary) > max_length else summary
    
    async def extract_tags(
        self, 
        text: str, 
        max_tags: int = 5,
        language: str = 'zh'
    ) -> List[str]:
        """
        提取关键词标签
        
        Args:
            text: 文本内容
            max_tags: 最大标签数量
            language: 语言
        
        Returns:
            标签列表
        """
        if not self.initialized:
            return self._extract_keywords_rule_based(text, max_tags)
        
        lang_name = "中文" if language == 'zh' else "English"
        prompt = f"""请从以下文本中提取{max_tags}个最重要的关键词或短语作为标签，用逗号分隔。使用{lang_name}。

{text[:2000]}

标签:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Extract keywords from text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            tags_text = response.choices[0].message.content.strip()
            tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
            return tags[:max_tags]
        except Exception as e:
            print(f"AI 提取标签失败：{e}")
            return self._extract_keywords_rule_based(text, max_tags)
    
    def _extract_keywords_rule_based(self, text: str, max_tags: int) -> List[str]:
        """基于规则的关键词提取"""
        # 简单实现：分词并统计频率 (这里简化处理)
        words = text.replace(',', ' ').replace('.', ' ').replace('\n', ' ').split()
        
        # 过滤短词和常见词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个'}
        meaningful_words = [w for w in words if len(w) > 1 and w not in stop_words]
        
        # 简单计数
        word_count = {}
        for word in meaningful_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # 排序取前 N 个
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:max_tags]]
    
    async def categorize(
        self, 
        text: str, 
        categories: List[str],
        language: str = 'zh'
    ) -> Optional[str]:
        """
        文本分类
        
        Args:
            text: 文本内容
            categories: 可选类别列表
            language: 语言
        
        Returns:
            最匹配的类别
        """
        if not self.initialized:
            return categories[0] if categories else "未分类"
        
        lang_name = "中文" if language == 'zh' else "English"
        prompt = f"""请将以下文本分类到以下类别之一：{', '.join(categories)}。只返回类别名称，使用{lang_name}。

{text[:2000]}

类别:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Classify text into categories."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0.3
            )
            
            category = response.choices[0].message.content.strip()
            return category if category in categories else categories[0]
        except Exception as e:
            print(f"AI 分类失败：{e}")
            return categories[0] if categories else "未分类"
    
    async def process(self, content: str, task: str, options: Dict[str, Any] = {}) -> Dict[str, Any]:
        """
        通用 AI 处理接口
        
        Args:
            content: 要处理的内容
            task: 任务类型 (summarize, categorize, extract_tags, etc.)
            options: 额外选项
        
        Returns:
            处理结果
        """
        if task == 'summarize':
            result = await self.summarize(
                content, 
                max_length=options.get('max_length', 200),
                language=options.get('language', 'zh')
            )
            return {'summary': result}
        
        elif task == 'extract_tags':
            tags = await self.extract_tags(
                content,
                max_tags=options.get('max_tags', 5),
                language=options.get('language', 'zh')
            )
            return {'tags': tags}
        
        elif task == 'categorize':
            categories = options.get('categories', ['技术', '生活', '工作', '学习'])
            category = await self.categorize(
                content,
                categories=categories,
                language=options.get('language', 'zh')
            )
            return {'category': category}
        
        else:
            return {'error': f'未知任务类型：{task}'}
