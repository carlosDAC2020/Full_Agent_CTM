import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from langchain.tools import tool
from tavily import TavilyClient
from langchain_community.tools import BraveSearch
from langchain_community.tools import DuckDuckGoSearchResults



@tool
async def tavily_search(query: str, max_results: int = 5) -> str:
    """
    Perform an advanced web search optimized for technical and academic content using Tavily.

    This tool is best suited for finding high-quality, up-to-date information from reliable sources.
    It filters for content relevant to research, development, and technical analysis.

    Args:
        query (str): The search query string. Be specific for better results.
        max_results (int, optional): The maximum number of search results to return. Defaults to 5.

    Returns:
        str: A formatted string containing the search results, including titles, URLs, snippets, and relevance scores.
    """
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    
    def sync_search():
        return client.search(query, max_results=max_results, search_depth="advanced")
    
    results = await asyncio.to_thread(sync_search)
    
    formatted_results = []
    for item in results.get('results', []):
        formatted_results.append(
            f"🌐 **Title**: {item.get('title', 'N/A')}\n"
            f"🔗 **URL**: {item.get('url', 'N/A')}\n"
            f"📝 **Snippet**: {item.get('content', 'N/A')[:400]}...\n"
            f"⭐ **Score**: {item.get('score', 'N/A')}"
        )
    
    return "\n\n" + "="*80 + "\n\n".join(formatted_results)


@tool
async def brave_search(query: str, max_results: int = 5) -> str:
    """
    Perform a search using the Brave Search API, focusing on scholarly and academic sources.

    This tool is useful for finding papers, articles, and technical reports.

    Args:
        query (str): The search query.
        max_results (int, optional): The number of results to retrieve. Defaults to 5.

    Returns:
        str: The raw JSON string response from the Brave Search API, or an error message.
    """
    try:
        api_key = os.environ.get("BRAVE_API_KEY")
        tool = BraveSearch.from_api_key(
            api_key=api_key, 
            search_kwargs={"count": 5}
        )
        result = await tool.arun(query)
        return result
    except Exception as e:
        return f"Error during BraveSearch: {e}"

@tool
async def duckduckgo_search(query: str, max_results: int = 5) -> str:
    """
    Perform a general web search using DuckDuckGo.

    Good for broad searches, news, and general knowledge gathering.

    Args:
        query (str): The search query.
        max_results (int, optional): The maximum number of results. Defaults to 5.

    Returns:
        str: The search results as a string, or an error message on failure.
    """
    try:
        tool = DuckDuckGoSearchResults(max_results=max_results)
        result = await tool.arun(query)
        return result
    except Exception as e:
        return f"Error during DuckDuckGo search: {e}"

@tool
async def fetch_url_content(url: str) -> str:
    """
    Fetch and extract the main text content from a given URL.

    This tool downloads the HTML content of a webpage and uses BeautifulSoup to extract the text.
    It is useful for reading the full content of a specific article or documentation page found via search.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The extracted text content of the page, or an error message if fetching fails.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return f"Error: HTTP {response.status} when fetching {url}"
                html = await response.text()
                
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text(separator='\n', strip=True)
        
        # Basic cleanup of multiple newlines
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:10000] # Limit content length to avoid context overflow
        
    except Exception as e:
        return f"Error fetching URL content: {e}"


# Lista de herramientas
research_tools = [
    tavily_search,
    brave_search,
    duckduckgo_search,
    fetch_url_content
]