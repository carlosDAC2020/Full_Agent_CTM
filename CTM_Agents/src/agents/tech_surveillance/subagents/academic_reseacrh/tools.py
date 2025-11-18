import os
import asyncio
from langchain.tools import tool
from langchain_community.retrievers import ArxivRetriever, PubMedRetriever, WikipediaRetriever
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from tavily import TavilyClient

# 1. Búsqueda en ArXiv (papers científicos)
@tool
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
    
    Usage tips:
    - Use specific technical terms: "LangGraph agent architecture" works better than "AI agents"
    - Include key concepts: "ReAct reasoning" or "chain-of-thought prompting"
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


# 2. Búsqueda en PubMed (medicina/biología)
@tool
async def search_pubmed(query: str, max_results: int = 5) -> str:
    """Search PubMed for biomedical and life sciences research papers.
    
    Best for:
    - AI applications in healthcare, medical imaging, drug discovery
    - Bioinformatics and computational biology
    - Neuroscience and cognitive science (relevant for AI cognition)
    
    Args:
        query: Medical/biological search terms
        max_results: Number of articles to retrieve (default: 5)
    
    Returns:
        Formatted list of medical research articles.
    
    Usage tips:
    - Only use if the research topic intersects with medicine/biology
    - For pure AI/ML topics, prefer ArXiv instead
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


# 3. Búsqueda en Wikipedia
@tool
async def search_wikipedia(query: str, lang: str = "en") -> str:
    """Search Wikipedia for general background information and concept definitions.
    
    Best for:
    - Understanding basic concepts and terminology
    - Historical context and evolution of technologies
    - Quick overviews before diving into academic papers
    
    Args:
        query: Topic to search (e.g., "multi-agent system", "reinforcement learning")
        lang: Language code ("en" for English, "es" for Spanish)
    
    Returns:
        Wikipedia article excerpts (first 500 chars per article).
    
    Usage tips:
    - Use this FIRST to understand unfamiliar terms
    - Not a primary source - always verify with academic papers
    - Good for context but cite academic sources in the final report
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


# 4. Búsqueda académica con Tavily
@tool
async def academic_search(query: str, max_results: int = 5) -> str:
    """Perform advanced web search optimized for academic and technical content.
    
    Best for:
    - Recent blog posts from AI research labs (OpenAI, Anthropic, DeepMind, Meta AI)
    - Technical documentation and tutorials
    - Conference proceedings not yet in ArXiv
    - Industry applications and case studies
    - GitHub repositories with research implementations
    
    Args:
        query: Search query with specific terms
        max_results: Number of results (default: 5, max: 10)
    
    Returns:
        Search results with URLs, titles, and content snippets.
    
    Usage tips:
    - Great for finding the latest developments not yet published as papers
    - Use to discover practical implementations and code repositories
    - Complements ArXiv by finding grey literature and industry insights
    - Add terms like "2024", "2025" for recent content
    """
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    def sync_search():
        return client.search(
            query,
            max_results=max_results,
            search_depth="advanced"
        )
    
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
async def search_semantic_scholar(query: str, max_results: int = 5) -> str:
    """Search Semantic Scholar for AI/ML research papers with citation context.
    
    Best for:
    - Finding highly-cited papers and their impact
    - Understanding research genealogy and influence
    - Discovering papers cited by key works
    - Comprehensive academic literature overview
    
    Args:
        query: Research topic (e.g., "multi-agent reinforcement learning")
        max_results: Number of papers (default: 5)
    
    Returns:
        Formatted list of papers with citation counts and influence.
    """
    tool = SemanticScholarQueryRun()
    results = await tool.ainvoke(query)
    return results


# Lista de herramientas
research_tools = [
    search_arxiv,
    search_pubmed,
    search_wikipedia,
    academic_search,
    search_semantic_scholar 
]