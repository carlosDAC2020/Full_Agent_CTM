import os
import chromadb
from typing import List, Optional
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools import tool

@tool
def rag_search_documents(query: str, session_id: str) -> str:
    """
    Busca información relevante en los documentos de contexto subidos por el usuario para esta sesión.
    Úsalo cuando necesites detalles específicos de la convocatoria, cronogramas, requisitos o cualquier
    documento adjunto que no sea público en la web.
    
    Args:
        query: La pregunta o término de búsqueda relacionado con los documentos.
        session_id: El ID de la sesión actual (proporcionado en el estado).
    """
    try:
        chroma_host = os.getenv("CHROMA_HOST", "chromadb")
        chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
        
        client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        
        # Verificar si existe la colección
        collection_name = f"session_{session_id}"
        try:
            client.get_collection(name=collection_name)
        except Exception:
            return "❌ No se encontraron documentos de referencia para esta sesión. Por favor, usa herramientas de búsqueda web."

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.environ.get("GEMINI_API_KEY")
        )

        vectorstore = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings
        )

        # Realizar búsqueda
        results = vectorstore.similarity_search(query, k=4)
        
        if not results:
            return f"❌ No se encontró información relevante en los documentos para la consulta: '{query}'"

        # Formatear respuesta
        context_parts = []
        sources = set()
        
        for i, doc in enumerate(results):
            source = os.path.basename(doc.metadata.get("source", "Documento desconocido"))
            sources.add(source)
            context_parts.append(f"--- Fragmento {i+1} (Fuente: {source}) ---\n{doc.page_content}")

        context_text = "\n\n".join(context_parts)
        
        return f"""📚 Información encontrada en los documentos locales:

{context_text}

Fuentes consultadas: {', '.join(sources)}
"""

    except Exception as e:
        return f"❌ Error al consultar los documentos locales: {str(e)}"
