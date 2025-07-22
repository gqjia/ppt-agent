import re
import time
import requests
from requests.exceptions import RequestException, Timeout
from urllib.parse import urlparse
from typing import Optional, Dict, Any, List

from smolagents import tool
from markdownify import markdownify
from pydantic import BaseModel, model_validator, ConfigDict
from loguru import logger


class DuckDuckGoSearchAPIWrapper(BaseModel):
    """Wrapper for DuckDuckGo Search API.

    Free and does not require any setup.
    """

    region: Optional[str] = "wt-wt"
    """
    See https://pypi.org/project/duckduckgo-search/#regions
    """
    safesearch: str = "moderate"
    """
    Options: strict, moderate, off
    """
    time: Optional[str] = "y"
    """
    Options: d, w, m, y
    """
    max_results: int = 5
    backend: str = "auto"
    """
    Options: auto, html, lite
    """
    source: str = "text"
    """
    Options: text, news, images
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Validate that python package exists in environment."""
        try:
            from ddgs import DDGS  # noqa: F401
        except ImportError:
            raise ImportError(
                "Could not import ddgs python package. "
                "Please install it with `pip install -U ddgs`."
            )
        return values

    def _ddgs_text(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo text search and return results."""
        from ddgs import DDGS

        try:
            with DDGS() as ddgs:
                ddgs_gen = ddgs.text(
                    query,
                    region=self.region,
                    safesearch=self.safesearch,
                    timelimit=self.time,
                    max_results=max_results or self.max_results,
                    backend=self.backend,
                )
                if ddgs_gen:
                    return [r for r in ddgs_gen]
        except Exception as e:
            logger.error(f"Error in DuckDuckGo text search: {e}")
        return []

    def _ddgs_news(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo news search and return results."""
        from ddgs import DDGS

        try:
            with DDGS() as ddgs:
                ddgs_gen = ddgs.news(
                    query,
                    region=self.region,
                    safesearch=self.safesearch,
                    timelimit=self.time,
                    max_results=max_results or self.max_results,
                )
                if ddgs_gen:
                    return [r for r in ddgs_gen]
        except Exception as e:
            logger.error(f"Error in DuckDuckGo news search: {e}")
        return []

    def _ddgs_images(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo image search and return results."""
        from ddgs import DDGS

        try:
            with DDGS() as ddgs:
                ddgs_gen = ddgs.images(
                    query,
                    region=self.region,
                    safesearch=self.safesearch,
                    max_results=max_results or self.max_results,
                )
                if ddgs_gen:
                    return [r for r in ddgs_gen]
        except Exception as e:
            logger.error(f"Error in DuckDuckGo image search: {e}")
        return []

    def run(self, query: str) -> str:
        """Run query through DuckDuckGo and return concatenated results."""
        if self.source == "text":
            results = self._ddgs_text(query)
        elif self.source == "news":
            results = self._ddgs_news(query)
        elif self.source == "images":
            results = self._ddgs_images(query)
        else:
            results = []

        if not results:
            return "No good DuckDuckGo Search Result was found"
        return " ".join(r["body"] for r in results)

    def results(
        self, query: str, max_results: int, source: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo and return metadata.

        Args:
            query: The query to search for.
            max_results: The number of results to return.
            source: The source to look from.

        Returns:
            A list of dictionaries with the following keys:
                snippet - The description of the result.
                title - The title of the result.
                link - The link to the result.
        """
        source = source or self.source
        if source == "text":
            results = [
                {"snippet": r["body"], "title": r["title"], "link": r["href"]}
                for r in self._ddgs_text(query, max_results=max_results)
            ]
        elif source == "news":
            results = [
                {
                    "snippet": r["body"],
                    "title": r["title"],
                    "link": r["url"],
                    "date": r["date"],
                    "source": r["source"],
                }
                for r in self._ddgs_news(query, max_results=max_results)
            ]
        elif source == "images":
            results = [
                {
                    "title": r["title"],
                    "thumbnail": r["thumbnail"],
                    "image": r["image"],
                    "url": r["url"],
                    "height": r["height"],
                    "width": r["width"],
                    "source": r["source"],
                }
                for r in self._ddgs_images(query, max_results=max_results)
            ]
        else:
            results = []

        if results is None:
            results = [{"Result": "No good DuckDuckGo Search Result was found"}]

        return results


def is_valid_url(url: str) -> bool:
    """Check if the URL is valid and accessible."""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except Exception:
        return False


def clean_content(content: str, max_length: int = 2000) -> str:
    """Clean and format the content."""
    if not content:
        return ""
    
    content = re.sub(r'\s+', ' ', content.strip())
    
    patterns_to_remove = [
        r'cookie|privacy|terms|conditions|advertisement|广告',
        r'©\s*\d{4}.*?all rights reserved',
        r'powered by.*?',
        r'loading\.\.\.',
        r'javascript:.*?',
        r'window\.|document\.|function\(',
    ]
    
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    if len(content) > max_length:
        content = content[:max_length] + "..."
    
    return content


def visit_webpage(url: str, timeout: int = 10, max_retries: int = 3) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retry attempts.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    if not is_valid_url(url):
        return f"Invalid URL: {url}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                url, 
                headers=headers, 
                timeout=timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type and 'text/plain' not in content_type:
                return f"Unsupported content type: {content_type}"
            
            if response.encoding == 'ISO-8859-1':
                response.encoding = response.apparent_encoding
            
            markdown_content = markdownify(response.text, heading_style="ATX")
            
            cleaned_content = clean_content(markdown_content)
            
            return cleaned_content

        except Timeout:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return f"Timeout error: Request to {url} timed out after {timeout} seconds"
        except RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return f"Request error fetching {url}: {str(e)}"
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return f"Unexpected error fetching {url}: {str(e)}"
    
    return f"Failed to fetch {url} after {max_retries} attempts"


@tool
def web_search(query: str, max_results: int = 5, include_content: bool = True) -> str:
    """Search the web for information and optionally fetch webpage content.
    
    Args:
        query: The search query to look for.
        max_results: Maximum number of search results to return (default: 5).
        include_content: Whether to fetch and include webpage content (default: True).
    
    Returns:
        A formatted string containing search results and optionally webpage content.
    """
    try:
        ddg = DuckDuckGoSearchAPIWrapper()
        search_results = ddg.results(query, max_results=max_results)
        
        if not search_results or len(search_results) == 0:
            return f"No search results found for: {query}"
        
        result_parts = [f"Search results for: {query}\n"]
        
        for i, result in enumerate(search_results, 1):
            title = result.get('title', 'No title')
            snippet = result.get('snippet', 'No description')
            link = result.get('link', result.get('url', 'No link'))
            
            result_parts.append(f"{i}. {title}")
            result_parts.append(f"   URL: {link}")
            result_parts.append(f"   Description: {snippet}")
            
            if include_content and link and link != 'No link':
                content = visit_webpage(link)
                if content and not content.startswith("Error") and not content.startswith("Invalid"):
                    result_parts.append(f"   Content: {content[:500]}...")
                else:
                    result_parts.append("   Content: Unable to fetch content")
            
            result_parts.append("")
        
        return "\n".join(result_parts)
        
    except Exception as e:
        logger.error(f"Error in web_search: {e}")
        return f"Error performing web search: {str(e)}"


@tool
def fetch_webpage_content(url: str) -> str:
    """Fetch and return the content of a specific webpage.
    
    Args:
        url: The URL of the webpage to fetch.
    
    Returns:
        The content of the webpage as a cleaned markdown string.
    """
    return visit_webpage(url)


if __name__ == "__main__":
    print("=== Testing Web Search ===")
    search_result = web_search("北京今天天气", max_results=3, include_content=True)
    print(search_result)
    
    print("\n=== Testing Webpage Fetch ===")
    webpage_content = fetch_webpage_content("https://httpbin.org/html")
    print(webpage_content[:500] + "...")
