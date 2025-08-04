"""博查 AI 网页检索工具
提供基于博查 AI API 的网页搜索功能
"""
import os
import requests
import json
from typing import Dict, List, Any
from loguru import logger
from smolagents import Tool
from dotenv import load_dotenv


load_dotenv()

BOCHA_API_KEY = os.getenv('BOCHA_API_KEY')
BOCHA_API_URL = os.getenv('BOCHA_API_URL')


class BochaWebSearch(Tool):
    """博查 AI 网页检索工具类"""
    
    name = "bocha_web_search"
    description = "使用博查 AI 进行网页搜索，获取最新的网络信息。支持不同时效性的搜索结果。"
    inputs = {
        "query": {
            "type": "string",
            "description": "搜索查询字符串，描述您要搜索的内容"
        }
    }
    output_type = "string"
    
    def __init__(
        self, 
        api_key: str = BOCHA_API_KEY, 
        base_url: str = BOCHA_API_URL
    ):
        """
        初始化博查 AI 网页检索工具
        
        Args:
            api_key: 博查 AI API 密钥，如果不提供将从环境变量 BOCHA_API_KEY 获取
            base_url: API 基础 URL
        """
        super().__init__()
        
        self.api_key = api_key
        self.base_url = base_url
        self.search_endpoint = f"{base_url}/ai-search"
        
        if self.api_key:
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        else:
            self.headers = None
    
    def forward(self, query: str) -> str:
        """
        执行网页搜索并返回格式化的结果
        
        Args:
            query: 搜索查询字符串
            
        Returns:
            格式化的搜索结果字符串
        """
        freshness = "noLimit"
        max_results = 5
        
        if not self.api_key or not self.headers:
            return "错误：未设置 BOCHA_API_KEY，请设置环境变量或在初始化时提供 API 密钥"
        
        try:
            results = self.search_simple(query, freshness, max_results)
            
            if not results:
                return f"未找到关于 '{query}' 的搜索结果"
            
            # 格式化搜索结果
            formatted_output = f"## 搜索结果：{query}\n\n"
            formatted_output += f"**搜索时效性：** {freshness}\n"
            formatted_output += f"**找到 {len(results)} 条结果：**\n\n"
            
            for result in results:
                formatted_output += f"### {result['rank']}. {result['title']}\n"
                formatted_output += f"**链接：** {result['url']}\n"
                formatted_output += f"**摘要：** {result['snippet']}\n\n"
            
            return formatted_output
            
        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            return f"搜索失败：{str(e)}"
    
    def search(
        self,
        query: str,
        freshness: str = "noLimit",
        answer: bool = False,
        stream: bool = False,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        执行网页搜索
        
        Args:
            query: 搜索查询字符串
            freshness: 搜索结果时效性 ("noLimit", "day", "week", "month", "year")
            answer: 是否返回 AI 生成的答案
            stream: 是否使用流式响应
            timeout: 请求超时时间（秒）
            
        Returns:
            搜索结果字典
            
        Raises:
            requests.RequestException: 网络请求异常
            ValueError: 参数错误
        """
        if not query or not query.strip():
            raise ValueError("搜索查询不能为空")
        
        # 验证 freshness 参数
        valid_freshness = ["noLimit", "day", "week", "month", "year"]
        if freshness not in valid_freshness:
            raise ValueError(f"freshness 参数必须是以下值之一: {valid_freshness}")
        
        payload = {
            "query": query.strip(),
            "freshness": freshness,
            "answer": answer,
            "stream": stream
        }
        
        try:
            logger.info(f"开始搜索: {query}")
            response = requests.post(
                self.search_endpoint,
                headers=self.headers,
                json=payload,
                timeout=timeout
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            result = response.json()
            
            # 解析博查 AI 的响应格式
            parsed_results = self._parse_bocha_response(result)
            logger.info(f"搜索完成，返回 {len(parsed_results)} 条结果")
            
            # 返回标准格式
            return {
                'results': parsed_results,
                'raw_response': result
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"搜索请求超时: {query}")
            raise requests.RequestException(f"搜索请求超时 ({timeout}秒)")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 错误: {e.response.status_code} - {e.response.text}")
            raise requests.RequestException(f"HTTP 错误: {e.response.status_code}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求异常: {str(e)}")
            raise
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析错误: {str(e)}")
            raise ValueError("响应格式错误，无法解析 JSON")
    
    def _parse_bocha_response(self, response: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        解析博查 AI 的响应格式

        Args:
            response: 博查 AI 的原始响应
            
        Returns:
            标准化的搜索结果列表
        """
        results = []
        
        try:
            # 检查响应状态
            if response.get('code') != 200:
                logger.warning(f"API 返回非 200 状态码: {response.get('code')}")
                return results
            
            # 从 messages 中提取搜索结果
            messages = response.get('messages', [])
            for message in messages:
                if message.get('type') == 'source' and message.get('content_type') == 'webpage':
                    content = message.get('content', '')
                    if content:
                        try:
                            # 解析 content 中的 JSON 数据
                            import json
                            content_data = json.loads(content)
                            web_results = content_data.get('value', [])
                            
                            for item in web_results:
                                result = {
                                    'title': item.get('name', ''),
                                    'url': item.get('url', ''),
                                    'snippet': item.get('snippet', ''),
                                    'displayUrl': item.get('displayUrl', ''),
                                    'id': item.get('id', '')
                                }
                                results.append(result)
                                
                        except json.JSONDecodeError as e:
                            logger.warning(f"解析 content JSON 失败: {e}")
                            continue
            
            return results
            
        except Exception as e:
            logger.error(f"解析博查 AI 响应失败: {e}")
            return results
    
    def search_simple(self, query: str, freshness: str = "noLimit", max_results: int = 10) -> List[Dict[str, str]]:
        """
        简化的搜索接口，返回格式化的搜索结果
        
        Args:
            query: 搜索查询
            freshness: 搜索结果时效性
            max_results: 最大结果数量
            
        Returns:
            格式化的搜索结果列表，每个结果包含 title, url, snippet
        """
        try:
            result = self.search(query, freshness=freshness, answer=False)
            
            # 提取并格式化搜索结果
            formatted_results = []
            results = result.get('results', [])
            
            for i, item in enumerate(results[:max_results]):
                formatted_result = {
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('snippet', ''),
                    'rank': i + 1
                }
                formatted_results.append(formatted_result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"简化搜索失败: {str(e)}")
            return []
    
    def search_with_answer(self, query: str) -> Dict[str, Any]:
        """
        带 AI 答案的搜索
        
        Args:
            query: 搜索查询
            
        Returns:
            包含 AI 答案和搜索结果的字典
        """
        try:
            result = self.search(query, answer=True)
            
            return {
                'answer': result.get('answer', ''),
                'results': result.get('results', []),
                'query': query
            }
            
        except Exception as e:
            logger.error(f"带答案搜索失败: {str(e)}")
            return {
                'answer': '',
                'results': [],
                'query': query,
                'error': str(e)
            }


def create_bocha_search_tool(api_key: str) -> BochaWebSearch:
    """
    创建博查 AI 搜索工具实例
    
    Args:
        api_key: 博查 AI API 密钥
        
    Returns:
        BochaWebSearch 实例
    """
    return BochaWebSearch(api_key)
