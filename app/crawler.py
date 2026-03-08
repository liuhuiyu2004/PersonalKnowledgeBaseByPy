"""
网络爬虫模块
负责从网页抓取内容和搜索网络信息

@author LiuHuiYu
"""
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
import re
from config import settings


class WebScraper:
    """网页爬虫类"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
        }
        self.timeout = settings.search_timeout
    
    async def fetch_page(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        获取网页内容
        
        Returns:
            Tuple[html, error]: (HTML 内容，错误信息)
        """
        try:
            async with httpx.AsyncClient(
                headers=self.headers, 
                timeout=self.timeout,
                follow_redirects=True,
                cookies={}
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # 检测编码 - httpx 使用 response.encoding
                # 如果没有设置编码，尝试从 headers 中获取
                encoding = response.encoding
                if not encoding:
                    content_type = response.headers.get('content-type', '')
                    if 'charset=' in content_type:
                        encoding = content_type.split('charset=')[-1].strip()
                    else:
                        # 默认使用 UTF-8
                        encoding = 'utf-8'
                
                # 设置编码并获取文本
                response.encoding = encoding
                
                # 检查是否被重定向或返回错误页面
                if response.status_code != 200:
                    return None, f"HTTP 错误：{response.status_code}"
                
                # 检查是否返回了反爬虫页面
                if 'robot' in response.text.lower() or 'access denied' in response.text.lower():
                    return None, "网站拒绝了访问（可能触发了反爬虫机制）"
                
                return response.text, None
        except httpx.HTTPStatusError as e:
            return None, f"HTTP 错误：{e.response.status_code} - 网站可能拒绝了请求"
        except httpx.RequestError as e:
            return None, f"请求失败：{str(e)}"
        except Exception as e:
            return None, f"获取网页失败：{str(e)}"
    
    def parse_html(self, html: str, url: str) -> Dict[str, str]:
        """
        解析 HTML 内容，提取有用信息
        
        Returns:
            Dict: {'title': 标题，'content': 正文内容，'text': 纯文本}
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取标题
        title = ''
        if soup.title:
            title = soup.title.string.strip()
        
        # 尝试提取主要内容
        content = self._extract_main_content(soup)
        
        # 提取纯文本
        text = soup.get_text(separator='\n', strip=True)
        
        return {
            'title': title,
            'content': content,
            'text': text,
            'url': url
        }
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """提取网页主要内容"""
        # 移除不需要的元素
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # 尝试查找主要内容区域
        main_content = None
        
        # 优先级顺序查找
        for tag_name in ['article', 'main']:
            main_content = soup.find(tag_name)
            if main_content:
                break
        
        # 如果没有找到，使用 class/id 查找
        if not main_content:
            for pattern in ['content', 'article', 'post', 'main']:
                main_content = soup.find(class_=re.compile(pattern, re.I))
                if main_content:
                    break
        
        # 仍然没找到就使用 body
        if not main_content:
            main_content = soup.find('body')
        
        # 最后回退到整个文档
        if not main_content:
            main_content = soup
        
        # 提取文本并清理
        content = main_content.get_text(separator='\n', strip=True)
        
        # 清理多余空白行
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return '\n'.join(lines[:500])  # 限制长度
    
    def extract_metadata(self, html: str) -> Dict[str, str]:
        """提取网页元数据"""
        soup = BeautifulSoup(html, 'lxml')
        metadata = {}
        
        # 提取 meta 标签
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        return metadata


class WebSearcher:
    """网络搜索器"""
    
    def __init__(self):
        self.scraper = WebScraper()
        self.headers = {
            'User-Agent': settings.user_agent,
        }
    
    async def search_duckduckgo(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        使用 DuckDuckGo 搜索 (无需 API 密钥)
        注意：这是一个简单实现，生产环境建议使用官方 API
        """
        results = []
        
        try:
            # DuckDuckGo HTML 搜索
            url = f"https://html.duckduckgo.com/html/?q={query}"
            
            async with httpx.AsyncClient(headers=self.headers, timeout=10, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'lxml')
                result_elements = soup.find_all('div', class_='result', limit=num_results)
                
                for result in result_elements:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text(strip=True)
                        snippet = snippet_elem.get_text(strip=True)
                        url = title_elem.get('href')
                        
                        # DuckDuckGo 的 URL 需要处理
                        if url.startswith('//'):
                            url = 'https:' + url
                        
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': url,
                            'source': 'DuckDuckGo'
                        })
        except Exception as e:
            print(f"DuckDuckGo 搜索失败：{e}")
        
        return results
    
    async def search_bing(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """
        使用 Bing 搜索
        """
        results = []
        
        try:
            url = f"https://www.bing.com/search?q={query}"
            
            async with httpx.AsyncClient(headers=self.headers, timeout=10, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'lxml')
                result_elements = soup.find_all('li', class_='b_algo', limit=num_results)
                
                for result in result_elements:
                    title_elem = result.find('h2')
                    snippet_elem = result.find('p')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text(strip=True)
                        snippet = snippet_elem.get_text(strip=True)
                        url = title_elem.find('a').get('href')
                        
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': url,
                            'source': 'Bing'
                        })
        except Exception as e:
            print(f"Bing 搜索失败：{e}")
        
        return results
    
    async def search(self, query: str, num_results: int = 5, engine: str = 'duckduckgo') -> List[Dict[str, str]]:
        """
        执行网络搜索
        
        Args:
            query: 搜索关键词
            num_results: 结果数量
            engine: 搜索引擎 ('duckduckgo' 或 'bing')
        
        Returns:
            List[Dict]: 搜索结果列表
        """
        if engine == 'bing':
            return await self.search_bing(query, num_results)
        else:
            return await self.search_duckduckgo(query, num_results)
    
    async def fetch_and_parse(self, url: str) -> Optional[Dict[str, str]]:
        """获取并解析网页"""
        print(f"正在抓取：{url}")
        html, error = await self.scraper.fetch_page(url)
        if error:
            print(f"抓取失败：{error}")
            return None
        
        print(f"抓取成功，HTML 长度：{len(html)}")
        result = self.scraper.parse_html(html, url)
        print(f"解析成功，标题：{result.get('title', '无标题')}")
        return result


# 便捷函数
async def fetch_webpage(url: str) -> Optional[Dict[str, str]]:
    """便捷函数：获取并解析网页"""
    searcher = WebSearcher()
    return await searcher.fetch_and_parse(url)


async def search_web(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """便捷函数：执行网络搜索"""
    searcher = WebSearcher()
    return await searcher.search(query, num_results)
