#!/usr/bin/env python3
"""
示例：如何在smolagents中使用网页检索工具
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from smolagents import Agent
from tools.web_search import web_search, search_news, fetch_webpage_content


def create_web_search_agent():
    """创建一个使用网页检索工具的智能体"""
    
    # 定义系统提示
    system_prompt = """
    你是一个智能助手，可以使用网页检索工具来获取最新的信息。
    
    你可以使用以下工具：
    1. web_search - 搜索网页信息
    2. search_news - 搜索新闻
    3. fetch_webpage_content - 获取特定网页内容
    
    请根据用户的问题选择合适的工具来获取信息，然后提供准确、有用的回答。
    """
    
    # 创建智能体
    agent = Agent(
        system_prompt=system_prompt,
        tools=[web_search, search_news, fetch_webpage_content]
    )
    
    return agent


def main():
    """主函数"""
    print("创建智能体...")
    agent = create_web_search_agent()
    
    # 示例对话
    examples = [
        "请帮我搜索一下Python编程的最新信息",
        "搜索一下今天的人工智能相关新闻",
        "获取一下 https://www.python.org 的内容",
        "搜索一下最近的天气情况"
    ]
    
    for i, question in enumerate(examples, 1):
        print(f"\n{'='*60}")
        print(f"示例 {i}: {question}")
        print(f"{'='*60}")
        
        try:
            response = agent.run(question)
            print(f"回答: {response}")
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    main() 