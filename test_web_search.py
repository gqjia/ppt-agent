#!/usr/bin/env python3
"""
测试网页检索工具的功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.web_search import web_search, search_news, fetch_webpage_content


def test_web_search():
    """测试网页搜索功能"""
    print("=" * 50)
    print("测试网页搜索功能")
    print("=" * 50)
    
    # 测试基本搜索
    result = web_search("Python编程", max_results=3, include_content=False)
    print(result)
    
    print("\n" + "=" * 50)
    print("测试包含内容的搜索")
    print("=" * 50)
    
    # 测试包含内容的搜索
    result_with_content = web_search("天气", max_results=2, include_content=True)
    print(result_with_content)


def test_news_search():
    """测试新闻搜索功能"""
    print("\n" + "=" * 50)
    print("测试新闻搜索功能")
    print("=" * 50)
    
    result = search_news("人工智能", max_results=3)
    print(result)


def test_webpage_fetch():
    """测试网页内容获取功能"""
    print("\n" + "=" * 50)
    print("测试网页内容获取功能")
    print("=" * 50)
    
    # 测试获取一个简单的网页
    test_url = "https://httpbin.org/html"
    content = fetch_webpage_content(test_url)
    print(f"获取网页内容 (前500字符):\n{content[:500]}...")
    
    # 测试无效URL
    print("\n测试无效URL:")
    invalid_content = fetch_webpage_content("invalid-url")
    print(invalid_content)


def main():
    """主测试函数"""
    try:
        test_web_search()
        test_news_search()
        test_webpage_fetch()
        
        print("\n" + "=" * 50)
        print("所有测试完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 