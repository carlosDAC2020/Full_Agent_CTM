import os
import asyncio
import functools
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from langchain.tools import tool
from langchain_community.retrievers import (
    ArxivRetriever,
    PubMedRetriever,
    WikipediaRetriever
)
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from tavily import TavilyClient

# ============================================================================
# RATE LIMITING DECORATOR - Aplica a TODAS las tools
# ============================================================================

class RateLimiter:
    """Control rate limiting across multiple API services"""
    
    def __init__(self):
        self.last_request_time = {}
        self.min_intervals = {
            'arxiv': 3,           # 3 segundos entre solicitudes
            'pubmed': 2,          # 2 segundos
            'wikipedia': 1,       # 1 segundo
            'tavily': 1,          # 1 segundo
            'semantic_scholar': 2 # 2 segundos
        }
        self.lock = asyncio.Lock()
    
    async def wait_if_needed(self, service: str):
        """Esperar si es necesario antes de hacer una solicitud"""
        async with self.lock:
            now = time.time()
            last_time = self.last_request_time.get(service, 0)
            elapsed = now - last_time
            min_interval = self.min_intervals.get(service, 1)
            
            if elapsed < min_interval:
                wait_time = min_interval - elapsed
                print(f"⏳ Rate limit: esperando {wait_time:.2f}s para {service}...")
                await asyncio.sleep(wait_time)
            
            self.last_request_time[service] = time.time()

# Instancia global del rate limiter
rate_limiter = RateLimiter()

def rate_limited_tool(service_name: str, max_retries: int = 3):
    """
    Decorador que aplica rate limiting + reintentos exponenciales a cualquier tool.
    
    Args:
        service_name: Nombre del servicio ('arxiv', 'pubmed', 'tavily', etc.)
        max_retries: Número máximo de reintentos (default: 3)
    
    Usage:
        @tool
        @rate_limited_tool('arxiv')
        async def search_arxiv(query: str) -> str:
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            await rate_limiter.wait_if_needed(service_name)
            return await func(*args, **kwargs)
        
        # Aplicar reintentos con backoff exponencial
        wrapper = retry(
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type((
                Exception,  # Captura cualquier excepción
            )),
            reraise=True
        )(wrapper)
        
        return wrapper
    
    return decorator

# 1. Búsqueda en ArXiv (papers científicos)
@tool
@rate_limited_tool('arxiv', max_retries=3)
async def search_arxiv(query: str, max_results: int = 5) -> str:
    """Search for academic papers in ArXiv across computer science, AI/ML, mathematics, and physics.
    
    Best for:
    - AI agent architectures, neural networks, machine learning algorithms
    - Cutting-edge research and preprints (often before peer review)
    - Computer science and mathematical foundations
    
    Args:
        query: Search terms (e.g., "multi-agent reinforcement learning", "transformer architectures")
        max_results: Number of papers to retrieve (default: 5, max recommended: 10)
    
    Returns:
        Formatted list of papers with titles, authors, publication dates, and abstracts.
    """
    retriever = ArxivRetriever(top_k_results=max_results)
    docs = await retriever.ainvoke(query)
    
    results = []
    for doc in docs:
        results.append(
            f"📄 **Title**: {doc.metadata.get('Title', 'N/A')}\n"
            f"👥 **Authors**: {doc.metadata.get('Authors', 'N/A')}\n"
            f"📅 **Published**: {doc.metadata.get('Published', 'N/A')}\n"
            f"📝 **Abstract**: {doc.page_content[:400]}...\n"
            f"🔗 **ArXiv ID**: {doc.metadata.get('entry_id', 'N/A')}"
        )
    return "\n\n" + "="*80 + "\n\n".join(results)


@tool
@rate_limited_tool('pubmed', max_retries=3)
async def search_pubmed(query: str, max_results: int = 5) -> str:
    """Search PubMed for biomedical and life sciences research papers.
    
    Best for:
    - AI applications in healthcare, medical imaging, drug discovery
    - Bioinformatics and computational biology
    - Neuroscience and cognitive science
    
    Args:
        query: Medical/biological search terms
        max_results: Number of articles to retrieve (default: 5)
    
    Returns:
        Formatted list of medical research articles.
    """
    retriever = PubMedRetriever(top_k_results=max_results)
    docs = await retriever.ainvoke(query)
    
    results = []
    for doc in docs:
        results.append(
            f"🏥 **Title**: {doc.metadata.get('Title', 'N/A')}\n"
            f"📝 **Summary**: {doc.page_content[:400]}...\n"
            f"🔗 **PMID**: {doc.metadata.get('uid', 'N/A')}"
        )
    return "\n\n" + "="*80 + "\n\n".join(results)


@tool
@rate_limited_tool('wikipedia', max_retries=2)
async def search_wikipedia(query: str, lang: str = "en") -> str:
    """Search Wikipedia for general background information and concept definitions.
    
    Best for:
    - Understanding basic concepts and terminology
    - Historical context and evolution of technologies
    - Quick overviews before diving into academic papers
    
    Args:
        query: Topic to search
        lang: Language code ("en" for English, "es" for Spanish)
    
    Returns:
        Wikipedia article excerpts.
    """
    retriever = WikipediaRetriever(lang=lang, top_k_results=2)
    docs = await retriever.ainvoke(query)
    
    results = []
    for doc in docs:
        results.append(
            f"📚 **Wikipedia**: {doc.metadata.get('title', 'N/A')}\n"
            f"📝 {doc.page_content[:500]}...\n"
        )
    return "\n\n" + "="*80 + "\n\n".join(results)


@tool
@rate_limited_tool('tavily', max_retries=3)
async def academic_search(query: str, max_results: int = 5) -> str:
    """Perform advanced web search optimized for academic and technical content.
    
    Best for:
    - Recent blog posts from AI research labs
    - Technical documentation and tutorials
    - Conference proceedings
    - Industry applications and case studies
    - GitHub repositories with research implementations
    
    Args:
        query: Search query with specific terms
        max_results: Number of results (default: 5)
    
    Returns:
        Search results with URLs, titles, and content snippets.
    """
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    
    def sync_search():
        return client.search(query, max_results=max_results, search_depth="basic")
    
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
@rate_limited_tool('semantic_scholar', max_retries=3)
async def search_semantic_scholar(query: str, max_results: int = 5) -> str:
    """Search Semantic Scholar for AI/ML research papers with citation context.
    
    Best for:
    - Finding highly-cited papers and their impact
    - Understanding research genealogy and influence
    - Discovering papers cited by key works
    
    Args:
        query: Research topic
        max_results: Number of papers (default: 5)
    
    Returns:
        Formatted list of papers with citation counts.
    """
    tool_instance = SemanticScholarQueryRun()
    results = await tool_instance.ainvoke(query)
    return results


# Lista de herramientas
research_tools = [
    search_arxiv,
    search_pubmed,
    #search_wikipedia,
    academic_search,
    search_semantic_scholar 
]