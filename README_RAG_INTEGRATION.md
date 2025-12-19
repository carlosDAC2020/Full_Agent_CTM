# Guía de Integración RAG - Contexto de Documentos

Esta guía detalla los pasos manuales para integrar un sistema de búsqueda en documentos (RAG) utilizando **ChromaDB** y **Gemini Embeddings** en tu flujo actual de `api_agent`.

## 1. Actualización del Estado (`state.py`)
Añade un campo para almacenar las rutas de los documentos de contexto en `CallInfo`.

```python
# api_agent/backend/src/agents/tech_surveillance/state.py

class CallInfo(BaseModel):
    # ... campos existentes ...
    context_docs: Optional[List[str]] = Field(default=[], description="Rutas de archivos de soporte para contexto")
```

## 2. Captura de Archivos en el Frontend (`step1.js` y `agent.js`)
Actualmente el frontend no envía los archivos. Debes modificar `ingestCall` para usar `FormData`.

### En `api/agent.js`:
```javascript
export async function ingestCall(text, files = []) {
    const formData = new FormData();
    formData.append('text', text);
    files.forEach(file => formData.append('files', file));

    const response = await fetch('/api/agent/ingest', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            // Nota: No poner 'Content-Type', el navegador pondrá boundary automáticamente
        },
        body: formData
    });
    return await response.json();
}
```

### En `ui/steps/step1.js`:
```javascript
const fileInput = document.getElementById('file-upload');
const files = fileInput ? Array.from(fileInput.files) : [];
const { task_id, session_id } = await ingestCall(store.selectedCallText, files);
```

## 3. Manejo de Archivos en el Backend (`agent.py`)
Cambia el endpoint `/ingest` para recibir archivos y guardarlos localmente antes de iniciar Celery.

```python
# api_agent/backend/src/routers/agent.py
from fastapi import UploadFile, File, Form

@router.post("/ingest")
async def start_ingest(
    text: str = Form(...),
    files: List[UploadFile] = File([]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_id = str(uuid.uuid4())
    context_path = f"storage/sessions/{session_id}/context"
    os.makedirs(context_path, exist_ok=True)

    saved_paths = []
    for file in files:
        file_path = os.path.join(context_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_paths.append(file_path)

    # Iniciar Celery pasando las rutas de los archivos
    task = task_process_agent_step.delay(
        session_id=session_id, 
        input_data={"text": text, "context_docs": saved_paths}, 
        step_type="ingest"
    )
    return {"task_id": task.id, "session_id": session_id}
```

## 4. Creación del Nodo de Indexación (`ingestion/node.py`)
El agente debe procesar estos archivos y guardarlos en Chroma.

### Recomendación de Modelos:
- **Embeddings**: `models/embedding-001` de Google (es nativo de Gemini y gratuito dentro de ciertos límites).
- **Base de Datos**: ChromaDB local.

### Lógica del Nodo:
```python
# Nuevo nodo o extensión de ingestion_node
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

def process_context_docs(paths, session_id):
    docs = []
    for path in paths:
        if path.endswith('.pdf'): loader = PyPDFLoader(path)
        elif path.endswith('.docx'): loader = Docx2txtLoader(path)
        elif path.endswith('.xlsx'): loader = UnstructuredExcelLoader(path)
        docs.extend(loader.load())
    
    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(docs)
    
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        persist_directory=f"storage/sessions/{session_id}/vdb"
    )
    return vectorstore
```

## 5. Integración de la Herramienta en el Subagente (`tools.py`)
Crea una herramienta que el agente de presentación pueda usar para consultar la base de datos vectorial de la sesión actual.

```python
# api_agent/backend/src/agents/tech_surveillance/subagents/presentation_generation/tools.py

@tool
def query_session_context(query: str, session_id: str):
    """Consulta los documentos de soporte del usuario para obtener contexto sobre la convocatoria."""
    vdb = Chroma(
        persist_directory=f"storage/sessions/{session_id}/vdb",
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    )
    results = vdb.similarity_search(query, k=3)
    return "\n\n".join([r.page_content for r in results])
```

## 6. Actualización del Nodo de Presentación (`node.py`)
Asegúrate de que el agente tenga acceso a la herramienta y que el `SYSTEM_PROMPT` le indique que consulte los documentos si la información no está en la descripción básica.

1. Importa `all_tools` (incluyendo la nueva).
2. Pasa el `session_id` al agente en el mensaje de entrada para que la herramienta sepa dónde buscar.

---
**Nota sobre Formatos**: Para Excel, te recomiendo instalar `pip install openpyxl` o `pandas`. LangChain usa `UnstructuredExcelLoader` que suele requerir dependencias adicionales del sistema.
