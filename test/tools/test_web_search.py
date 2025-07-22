import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.tools.web_search import DuckDuckGoSearchAPIWrapper, visit_webpage, web_search


class TestDuckDuckGoSearchAPIWrapper(unittest.TestCase):
    """测试DuckDuckGoSearchAPIWrapper类"""

    def setUp(self):
        """设置测试环境"""
        self.search_wrapper = DuckDuckGoSearchAPIWrapper()

    def test_default_initialization(self):
        """测试默认初始化参数"""
        self.assertEqual(self.search_wrapper.region, "wt-wt")
        self.assertEqual(self.search_wrapper.safesearch, "moderate")
        self.assertEqual(self.search_wrapper.time, "y")
        self.assertEqual(self.search_wrapper.max_results, 5)
        self.assertEqual(self.search_wrapper.backend, "auto")
        self.assertEqual(self.search_wrapper.source, "text")

    def test_custom_initialization(self):
        """测试自定义初始化参数"""
        custom_wrapper = DuckDuckGoSearchAPIWrapper(
            region="us-en",
            safesearch="strict",
            time="w",
            max_results=10,
            backend="html",
            source="news"
        )
        self.assertEqual(custom_wrapper.region, "us-en")
        self.assertEqual(custom_wrapper.safesearch, "strict")
        self.assertEqual(custom_wrapper.time, "w")
        self.assertEqual(custom_wrapper.max_results, 10)
        self.assertEqual(custom_wrapper.backend, "html")
        self.assertEqual(custom_wrapper.source, "news")

    @patch('ddgs.DDGS')
    def test_ddgs_text_search(self, mock_ddgs):
        """测试文本搜索功能"""
        # 模拟搜索结果
        mock_results = [
            {"body": "测试结果1", "title": "标题1", "href": "http://example1.com"},
            {"body": "测试结果2", "title": "标题2", "href": "http://example2.com"}
        ]
        
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = mock_results
        mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
        
        results = self.search_wrapper._ddgs_text("测试查询")
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["body"], "测试结果1")
        self.assertEqual(results[1]["body"], "测试结果2")
        
        # 验证DDGS被正确调用
        mock_ddgs_instance.text.assert_called_once_with(
            "测试查询",
            region="wt-wt",
            safesearch="moderate",
            timelimit="y",
            max_results=5,
            backend="auto"
        )

    @patch('ddgs.DDGS')
    def test_ddgs_news_search(self, mock_ddgs):
        """测试新闻搜索功能"""
        mock_results = [
            {"body": "新闻1", "title": "新闻标题1", "url": "http://news1.com", "date": "2024-01-01", "source": "新闻源1"},
            {"body": "新闻2", "title": "新闻标题2", "url": "http://news2.com", "date": "2024-01-02", "source": "新闻源2"}
        ]
        
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.news.return_value = mock_results
        mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
        
        results = self.search_wrapper._ddgs_news("新闻查询")
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["body"], "新闻1")
        self.assertEqual(results[1]["body"], "新闻2")

    @patch('ddgs.DDGS')
    def test_ddgs_images_search(self, mock_ddgs):
        """测试图片搜索功能"""
        mock_results = [
            {
                "title": "图片1",
                "thumbnail": "http://thumb1.com",
                "image": "http://image1.com",
                "url": "http://url1.com",
                "height": 100,
                "width": 200,
                "source": "图片源1"
            }
        ]
        
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.images.return_value = mock_results
        mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
        
        results = self.search_wrapper._ddgs_images("图片查询")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "图片1")
        self.assertEqual(results[0]["height"], 100)

    @patch.object(DuckDuckGoSearchAPIWrapper, '_ddgs_text')
    def test_run_text_search(self, mock_text_search):
        """测试run方法的文本搜索"""
        mock_text_search.return_value = [
            {"body": "搜索结果1"},
            {"body": "搜索结果2"}
        ]
        
        result = self.search_wrapper.run("测试查询")
        
        self.assertEqual(result, "搜索结果1 搜索结果2")
        mock_text_search.assert_called_once_with("测试查询")

    @patch.object(DuckDuckGoSearchAPIWrapper, '_ddgs_text')
    def test_run_no_results(self, mock_text_search):
        """测试run方法无搜索结果的情况"""
        mock_text_search.return_value = []
        
        result = self.search_wrapper.run("测试查询")
        
        self.assertEqual(result, "No good DuckDuckGo Search Result was found")

    @patch.object(DuckDuckGoSearchAPIWrapper, '_ddgs_text')
    def test_results_text_search(self, mock_text_search):
        """测试results方法的文本搜索"""
        mock_text_search.return_value = [
            {"body": "搜索结果1", "title": "标题1", "href": "http://example1.com"},
            {"body": "搜索结果2", "title": "标题2", "href": "http://example2.com"}
        ]
        
        results = self.search_wrapper.results("测试查询", max_results=2)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["snippet"], "搜索结果1")
        self.assertEqual(results[0]["title"], "标题1")
        self.assertEqual(results[0]["link"], "http://example1.com")

    @patch.object(DuckDuckGoSearchAPIWrapper, '_ddgs_news')
    def test_results_news_search(self, mock_news_search):
        """测试results方法的新闻搜索"""
        mock_news_search.return_value = [
            {"body": "新闻1", "title": "新闻标题1", "url": "http://news1.com", "date": "2024-01-01", "source": "新闻源1"}
        ]
        
        results = self.search_wrapper.results("新闻查询", max_results=1, source="news")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["snippet"], "新闻1")
        self.assertEqual(results[0]["title"], "新闻标题1")
        self.assertEqual(results[0]["link"], "http://news1.com")
        self.assertEqual(results[0]["date"], "2024-01-01")
        self.assertEqual(results[0]["source"], "新闻源1")

    @patch.object(DuckDuckGoSearchAPIWrapper, '_ddgs_images')
    def test_results_images_search(self, mock_images_search):
        """测试results方法的图片搜索"""
        mock_images_search.return_value = [
            {
                "title": "图片1",
                "thumbnail": "http://thumb1.com",
                "image": "http://image1.com",
                "url": "http://url1.com",
                "height": 100,
                "width": 200,
                "source": "图片源1"
            }
        ]
        
        results = self.search_wrapper.results("图片查询", max_results=1, source="images")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "图片1")
        self.assertEqual(results[0]["thumbnail"], "http://thumb1.com")
        self.assertEqual(results[0]["image"], "http://image1.com")
        self.assertEqual(results[0]["url"], "http://url1.com")
        self.assertEqual(results[0]["height"], 100)
        self.assertEqual(results[0]["width"], 200)
        self.assertEqual(results[0]["source"], "图片源1")

    def test_results_invalid_source(self):
        """测试results方法无效源的情况"""
        results = self.search_wrapper.results("测试查询", max_results=1, source="invalid")
        
        self.assertEqual(len(results), 0)

    @patch('ddgs.DDGS')
    def test_results_empty_return(self, mock_ddgs):
        """测试results方法返回空结果的情况"""
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = []
        mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance
        
        results = self.search_wrapper.results("测试查询", max_results=1)
        
        self.assertEqual(len(results), 0)


class TestVisitWebpage(unittest.TestCase):
    """测试visit_webpage函数"""

    @patch('requests.get')
    def test_visit_webpage_success(self, mock_get):
        """测试成功访问网页的情况"""
        # 模拟HTML响应
        mock_response = MagicMock()
        mock_response.text = "<html><body><h1>测试标题</h1><p>测试内容</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 模拟markdownify转换
        with patch('markdownify.markdownify') as mock_markdownify:
            mock_markdownify.return_value = "# 测试标题\n\n测试内容\n\n"
            
            result = visit_webpage("http://example.com")
            
            # 验证结果
            self.assertIn("测试标题", result)
            self.assertIn("测试内容", result)
            
            # 验证请求被正确调用
            mock_get.assert_called_once_with("http://example.com")

    @patch('requests.get')
    def test_visit_webpage_request_exception(self, mock_get):
        """测试请求异常的情况"""
        mock_get.side_effect = Exception("网络错误")
        
        result = visit_webpage("http://example.com")
        
        self.assertIn("Error fetching the webpage", result)
        self.assertIn("网络错误", result)

    @patch('requests.get')
    def test_visit_webpage_http_error(self, mock_get):
        """测试HTTP错误的情况"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response
        
        result = visit_webpage("http://example.com")
        
        self.assertIn("Error fetching the webpage", result)
        self.assertIn("404 Not Found", result)

    @patch('requests.get')
    def test_visit_webpage_remove_multiple_linebreaks(self, mock_get):
        """测试移除多余换行符的功能"""
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>内容1</p><p>内容2</p><p>内容3</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with patch('markdownify.markdownify') as mock_markdownify:
            # 模拟包含多个换行符的markdown内容
            mock_markdownify.return_value = "内容1\n\n\n\n\n内容2\n\n\n内容3\n\n\n\n\n"
            
            result = visit_webpage("http://example.com")
            
            # 验证多余的换行符被移除
            self.assertNotIn("\n\n\n\n", result)
            self.assertIn("\n\n", result)


class TestWebSearch(unittest.TestCase):
    """测试web_search函数"""

    @patch('src.tools.web_search.DuckDuckGoSearchAPIWrapper')
    @patch('src.tools.web_search.visit_webpage')
    def test_web_search_success(self, mock_visit_webpage, mock_wrapper_class):
        """测试web_search成功的情况"""
        # 模拟搜索结果
        mock_results = [
            {"link": "http://example1.com"},
            {"link": "http://example2.com"}
        ]
        
        # 模拟DuckDuckGoSearchAPIWrapper实例
        mock_wrapper = MagicMock()
        mock_wrapper.results.return_value = mock_results
        mock_wrapper_class.return_value = mock_wrapper
        
        # 模拟网页访问结果
        mock_visit_webpage.side_effect = [
            "网页内容1" * 20,  # 超过100字符
            "网页内容2" * 20   # 超过100字符
        ]
        
        result = web_search("测试查询")
        
        # 验证结果
        self.assertIn("网页内容1", result)
        self.assertIn("网页内容2", result)
        
        # 验证调用
        mock_wrapper.results.assert_called_once_with("测试查询", max_results=10)
        self.assertEqual(mock_visit_webpage.call_count, 2)

    @patch('src.tools.web_search.DuckDuckGoSearchAPIWrapper')
    def test_web_search_no_results(self, mock_wrapper_class):
        """测试web_search无搜索结果的情况"""
        # 模拟空搜索结果
        mock_wrapper = MagicMock()
        mock_wrapper.results.return_value = []
        mock_wrapper_class.return_value = mock_wrapper
        
        result = web_search("测试查询")
        
        # 验证结果为空字符串
        self.assertEqual(result, "")

    @patch('src.tools.web_search.DuckDuckGoSearchAPIWrapper')
    @patch('src.tools.web_search.visit_webpage')
    def test_web_search_content_truncation(self, mock_visit_webpage, mock_wrapper_class):
        """测试web_search内容截断功能"""
        # 模拟搜索结果
        mock_results = [
            {"link": "http://example.com"}
        ]
        
        mock_wrapper = MagicMock()
        mock_wrapper.results.return_value = mock_results
        mock_wrapper_class.return_value = mock_wrapper
        
        # 模拟长网页内容
        long_content = "这是一个很长的网页内容" * 20  # 超过100字符
        mock_visit_webpage.return_value = long_content
        
        result = web_search("测试查询")
        
        # 验证内容被截断到100字符
        self.assertEqual(len(result), 100)
        self.assertIn("这是一个很长的网页内容", result)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
