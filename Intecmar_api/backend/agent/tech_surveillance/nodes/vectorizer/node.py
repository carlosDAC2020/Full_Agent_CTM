import os
import shutil
import tempfile
import time
from typing import List
import chromadb
from langchain_chroma import Chroma
# ... rest of imports ...
from langchain_community.document_loaders import (
    PyPDFLoader, 
    Docx2txtLoader, 
    UnstructuredExcelLoader, 
    TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.agent.tech_surveillance.state import GraphState
from backend.app.services.tech_surveillance.storage import MinioService

from tenacity import retry, stop_after_attempt, wait_exponential

# Definimos una función con reintentos para agregar documentos
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    reraise=True
)
def add_documents_with_retry(vectorstore, splits):
    return vectorstore.add_documents(documents=splits)


async def vectorizer_node(state: GraphState):
    """
    Nodo para vectorizar documentos de contexto de la convocatoria.
    """
    print("\n🔮 [VECTORIZER] INICIANDO NODO DE VECTORIZACIÓN DE DOCUMENTOS...")
    
    call_info = state.get("call_info")
    session_id = state.get("session_id")
    
    if not call_info or not session_id:
        print("⚠️ [VECTORIZER] No hay información de convocatoria o session_id. Saltando vectorización.")
        return state

    context_docs = getattr(call_info, "context_docs", []) if hasattr(call_info, "context_docs") else call_info.get("context_docs", [])
    
    if not context_docs:
        print("📝 [VECTORIZER] No hay documentos de contexto para vectorizar. Saltando.")
        return state

    print(f"📂 [VECTORIZER] Se encontraron {len(context_docs)} documentos para procesar.")

    storage_service = MinioService()
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004", 
        google_api_key=os.environ.get("GEMINI_API_KEY")
    )
    
    chroma_host = os.getenv("CHROMA_HOST", "chromadb")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
    
        # Conectar a ChromaDB y guardar
        print(f"🚀 [VECTORIZER] Conectando a ChromaDB collection: session_{session_id}")
        
        client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        collection_name = f"session_{session_id}"
        
        # Identificar documentos ya procesados para evitar redundancia
        existing_sources = set()
        try:
            collection = client.get_collection(name=collection_name)
            results = collection.get(include=["metadatas"])
            if results and results.get("metadatas"):
                for meta in results["metadatas"]:
                    if "source" in meta:
                        source_base = os.path.basename(meta["source"])
                        existing_sources.add(source_base)
            print(f"🔍 [VECTORIZER] Encontrados {len(existing_sources)} documentos ya indexados.")
        except Exception:
            print(f"ℹ️ [VECTORIZER] Colección nueva. Se creará al insertar.")

        # Descargar y cargar solo documentos nuevos
        documents = []
        for obj_key in context_docs:
            filename = os.path.basename(obj_key)
            if filename in existing_sources:
                print(f"⏩ [VECTORIZER] Saltando {filename} (ya indexado).")
                continue

            local_path = os.path.join(temp_dir, filename)
            try:
                print(f"📥 [VECTORIZER] Descargando {obj_key} de MinIO...")
                storage_service.s3_client.download_file(
                    storage_service.bucket_name, 
                    obj_key, 
                    local_path
                )
                
                # Cargar según extensión
                ext = os.path.splitext(filename)[1].lower()
                loader = None
                if ext == ".pdf":
                    loader = PyPDFLoader(local_path)
                elif ext in [".docx", ".doc"]:
                    loader = Docx2txtLoader(local_path)
                elif ext in [".xlsx", ".xls"]:
                    loader = UnstructuredExcelLoader(local_path)
                elif ext in [".md", ".txt"]:
                    loader = TextLoader(local_path)
                
                if loader:
                    loaded_docs = loader.load()
                    documents.extend(loaded_docs)
                    print(f"✅ [VECTORIZER] Cargado: {filename} ({len(loaded_docs)} páginas/secciones)")
                else:
                    print(f"⚠️ [VECTORIZER] Formato no soportado: {filename}")
                    
            except Exception as e:
                print(f"❌ [VECTORIZER] Error procesando {obj_key}: {e}")

        if not documents:
            if existing_sources:
                print("✅ [VECTORIZER] Todo el contenido ya estaba indexado. Nada que hacer.")
                return state
            else:
                print("⚠️ [VECTORIZER] No se pudieron cargar documentos válidos.")
                return state

        # Dividir en chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)
        print(f"✂️ [VECTORIZER] Nuevos documentos divididos en {len(splits)} chunks.")
        
        vectorstore = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings
        )
        
        # Estrategia de Batching
        batch_size = 20
        total_chunks = len(splits)
        print(f"🚀 [VECTORIZER] Indexando {total_chunks} nuevos chunks en batches de {batch_size}...")
        
        for i in range(0, total_chunks, batch_size):
            batch = splits[i : i + batch_size]
            print(f"📦 [VECTORIZER] Enviando batch {i//batch_size + 1} ({len(batch)} chunks)...")
            add_documents_with_retry(vectorstore, batch)
            
            if i + batch_size < total_chunks:
                time.sleep(1)
        
        print(f"✅ [VECTORIZER] Vectorización completada con éxito.")
        
        # Pequeña espera de cortesía antes del siguiente nodo
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ [VECTORIZER] Error crítico en vectorización: {e}")
    finally:
        shutil.rmtree(temp_dir)

    return state