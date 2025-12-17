yo 
    q retreaver me funciona paraq un modelo me de respuestas a base de un docuemno ya sea de tipo pdf word , .md ecel etc 

LANGCHAIN bot 
**Sí, un retriever en LangChain funciona perfectamente para que un modelo responda preguntas basándose en documentos como PDF, Word, Markdown, Excel y más formatos.**

Usa **Document Loaders** para cargar archivos de diferentes tipos, luego los divides en chunks con **Text Splitters**, los conviertes en embeddings y los almacenas en un **Vector Store**. El retriever busca los chunks más relevantes para tu pregunta y el LLM genera la respuesta usando ese contexto (RAG).

```python
# 1. Instalar loaders específicos
# pip install pypdf langchain-openai chromadb unstructured[all-docs]

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

# 2. Cargar documentos (PDF, Word, Excel, MD, etc.)
loaders = [
    PyPDFLoader("mi_documento.pdf"),           # PDF
    Docx2txtLoader("mi_documento.docx"),       # Word
    UnstructuredExcelLoader("mi_archivo.xlsx"), # Excel
    # TextLoader("documento.md"),             # Markdown (texto plano)
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

# 3. Dividir en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# 4. Crear vector store con embeddings
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()                # Necesitas OPENAI_API_KEY
)

# 5. Crear retriever y usarlo con LLM
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Ejemplo: Preguntar al modelo
query = "resumir el contenido del PDF"
docs_relevantes = retriever.get_relevant_documents(query)
```

## Loaders por formato común

```python
# PDF
from langchain_community.document_loaders import PyPDFLoader

# Word (.docx)
from langchain_community.document_loaders import Docx2txtLoader

# Excel (.xlsx)
from langchain_community.document_loaders import UnstructuredExcelLoader

# Markdown/Texto
from langchain_community.document_loaders import TextLoader

# Múltiples archivos
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader("mi_carpeta/", glob="**/*")  # Todos los archivos
```

**Para RAG completo con LLM:**
```python
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

llm = ChatOpenAI(model="gpt-4o-mini")
chain = create_retrieval_chain(retriever, llm)
respuesta = chain.invoke({"input": "Tu pregunta aquí"})
print(respuesta["answer"])
```

yo
    se pdria incluir esta funcion al mi agente de investigacion aca el codoigo actual import os
import re
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_agent

from src.agents.tech_surveillance.state import GraphState, DocsPaths
from .prompts import SYSTEM_PROMPT, CONTENT_PROMPT_TEMPLATE

from .tools import research_tools


# --- 1. CONFIGURACIÓN DEL MODELO ---
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7
)

# Creamos el agente con herramientas
academic_research_agent = create_agent(
    model=model,  
    tools=research_tools,
    system_prompt=SYSTEM_PROMPT
)


# --- NODO PRINCIPAL ---
async def presentation_generation_node(state: GraphState):
    """
    Nodo para la generacion de los documentos de presentacion
    """
    print("🎨 INICIANDO AGENTE DE INVESTIGACIÓN Y PRESENTACIÓN...")
    
    call_info = state.get("call_info")
    if not call_info:
        return {"final_report": "Error: Sin datos de entrada"}

    # 1. Calcular estado de los datos para guiar al agente
    # Si falta info, le ponemos una etiqueta explícita para que use las Tools
    funding_status = "(⚠️ FALTANTE - BUSCAR MONTO EXACTO)" if not call_info.funding or call_info.funding == "N/A" else ""
    dates_status = "(⚠️ FALTANTE - BUSCAR CRONOGRAMA)" if not call_info.important_dates or call_info.important_dates == "N/A" else ""
    title_status = "(⚠️ FALTANTE - BUSCAR TÍTULO)" if not call_info.title else ""

    prompt_content = CONTENT_PROMPT_TEMPLATE.format(
        title=call_info.title or "Sin título",
        title_status=title_status,
        objective=call_info.objective or "N/A",
        funding=call_info.funding or "N/A",
        funding_status=funding_status,
        important_dates=call_info.important_dates or "N/A",
        dates_status=dates_status,
        url=call_info.url or "N/A"
    )

    try:
        # 2. Invocar al Agente con Herramientas
        # El agente decidirá si llamar a 'tavily_search' basándose en los status FALTANTE
        result = await academic_research_agent.ainvoke(
            {"messages": [HumanMessage(content=prompt_content)]}
        )

        last_message = result["messages"][-1]
        print(f"📝 Mensaje final del agente recibido. Procesando...")

        # 3. Extraer texto final
        # Lógica de extracción segura para Gemini/LangChain
        text_response = ""
        
        if isinstance(last_message.content, str):
            # Caso A: Respuesta es texto plano
            text_response = last_message.content
        elif isinstance(last_message.content, list):
            # Caso B: Respuesta es lista de bloques (Multimodal)
            # Iteramos y unimos todos los bloques que sean de tipo 'text'
            parts = []
            for block in last_message.content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text", ""))
            text_response = "\n".join(parts)
        else:
            # Caso C: Fallback
            text_response = str(last_message.content)
        
        
        print(f"✅ Agente finalizado. Longitud respuesta: {len(text_response)} caracteres")
        
        message = AIMessage(content="✅ Resumen de presentación generado correctamente.")
        
        return {
            "messages": [message],
            "presentation_summary": text_response,
        }

    except Exception as e:
        print(f"❌ Error crítico en nodo: {e}")
        return {
            "messages": [
                AIMessage(content=f"❌ Error crítico en nodo: {e}")
                ]
            }


**Sí, puedes integrar fácilmente la funcionalidad RAG/retriever a tu agente de investigación.** Aquí te muestro cómo agregar un **RAG Tool** que cargue documentos locales (PDF, Word, Excel, etc.) y los use para responder preguntas específicas.

## 1. Primero, crea el RAG Tool (nuevo archivo `tools/rag_tool.py`)

```python
# tools/rag_tool.py
import os
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader, TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.tools import tool
from langchain_core.documents import Document

@tool
def rag_search_documents(
    query: str, 
    docs_folder: str = "docs/", 
    top_k: int = 3
) -> str:
    """
    Busca información relevante en documentos locales (PDF, Word, Excel, MD).
    
    Args:
        query: Pregunta específica sobre los documentos
        docs_folder: Carpeta con documentos (default: "docs/")
        top_k: Número de documentos relevantes a retornar
    
    Úsalo cuando necesites información precisa de documentos internos.
    """
    try:
        # 1. Cargar documentos automáticamente según extensión
        docs_folder = os.path.abspath(docs_folder)
        if not os.path.exists(docs_folder):
            return f"❌ Carpeta no encontrada: {docs_folder}"
        
        documents: List[Document] = []
        
        # Extensiones soportadas
        for ext, loader_class in [
            (".pdf", PyPDFLoader),
            (".docx", Docx2txtLoader),
            (".xlsx", UnstructuredExcelLoader),
            (".md", TextLoader),
            (".txt", TextLoader),
        ]:
            for file in os.listdir(docs_folder):
                if file.lower().endswith(ext):
                    file_path = os.path.join(docs_folder, file)
                    try:
                        loader = loader_class(file_path)
                        docs = loader.load()
                        documents.extend(docs)
                        print(f"✅ Cargado: {file}")
                    except Exception as e:
                        print(f"⚠️ Error cargando {file}: {e}")
        
        if not documents:
            return "❌ No se encontraron documentos en la carpeta especificada"
        
        # 2. Dividir en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        # 3. Embeddings y Vector Store (en memoria)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
        
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=None  # En memoria para velocidad
        )
        
        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        
        # 4. Buscar documentos relevantes
        relevant_docs = retriever.get_relevant_documents(query)
        
        if not relevant_docs:
            return f"❌ No se encontraron documentos relevantes para: '{query}'"
        
        # 5. Formatear respuesta con contexto
        context = "\n\n".join([
            f"📄 [{doc.metadata.get('source', 'Desconocido')}]:\n{doc.page_content[:500]}..."
            for doc in relevant_docs
        ])
        
        return f"""**RESULTADOS RAG** (Top {top_k} documentos relevantes):

**Pregunta:** {query}

**Documentos relevantes encontrados:**

{context}

**Fuentes:** {', '.join(set(doc.metadata.get('source', '') for doc in relevant_docs))}"""
        
    except Exception as e:
        return f"❌ Error en RAG: {str(e)}"
```

## 2. Actualiza tu archivo `tools/__init__.py`

```python
# tools/__init__.py
from .research_tools import research_tools  # Tus tools existentes
from .rag_tool import rag_search_documents

# Combinar tools existentes + nuevo RAG tool
all_research_tools = research_tools + [rag_search_documents]
```

## 3. Actualiza tu agente principal

```python
# En tu archivo actual, cambia esta línea:
from .tools import all_research_tools  # ← CAMBIO AQUÍ

# Y actualiza la creación del agente:
academic_research_agent = create_agent(
    model=model,  
    tools=all_research_tools,  # ← Ahora incluye RAG
    system_prompt=SYSTEM_PROMPT
)
```

## 4. Actualiza tu `SYSTEM_PROMPT` para guiar al agente

Agrega al final de tu `SYSTEM_PROMPT`:

```
**NUEVAS HERRAMIENTAS DISPONIBLES:**
• rag_search_documents: Busca información en documentos locales (PDF, DOCX, Excel, MD)
  - Úsalo cuando la pregunta requiera datos específicos de documentos internos
  - Ejemplo: "Busca en docs/ el cronograma de convocatorias" → rag_search_documents

**INSTRUCCIONES:**
1. Si falta información específica (monto, fechas, requisitos), usa primero las tools de búsqueda web
2. Si necesitas datos de documentos internos, usa rag_search_documents("docs/")
3. Siempre cita la fuente (web o documento) en tu respuesta final
```

## 5. Crea la carpeta `docs/` con tus documentos

```
tu_proyecto/
├── docs/                 # ← Nueva carpeta
│   ├── convocatoria.pdf
│   ├── requisitos.docx
│   ├── cronograma.xlsx
│   └── manual.md
├── src/
│   └── agents/
└── ...
```

## 6. Uso del agente actualizado

Ahora tu agente **automáticamente decidirá** cuándo usar RAG:

```
Usuario: "Genera presentación de convocatoria X con cronograma exacto"

Agente pensará:
1. "Falta cronograma → usar tools web primero"
2. "Si no encuentro → buscar en docs/ con rag_search_documents"
3. "Combinar info web + documentos → generar presentación"
```

**Ejemplo de salida del RAG tool:**
```
**RESULTADOS RAG** (Top 3 documentos relevantes):

**Pregunta:** cronograma convocatoria

**Documentos relevantes encontrados:**
📄 [docs/cronograma.xlsx]:
Fase 1: 01/03/2025 - 15/04/2025 (Presentación)
Fase 2: 16/04/2025 - 30/05/2025 (Evaluación)...

**Fuentes:** docs/cronograma.xlsx, docs/convocatoria.pdf
```

## 🚀 Ventajas de esta integración:

1. **Automático**: El agente decide cuándo usar RAG vs web search
2. **Multi-formato**: PDF, Word, Excel, Markdown automáticamente
3. **En memoria**: Rápido (no persiste, se recrea cada llamada)
4. **Compatible**: Usa tu Gemini embedding model existente
5. **Escalable**: Solo agrega `docs_folder="mi_carpeta/"` al tool

**¿Listo para probar?** Crea la carpeta `docs/`, pon tus archivos y ejecuta. ¡Tu agente ahora tendrá memoria documental! 📚✨

