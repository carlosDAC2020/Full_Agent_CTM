import os
import re 
import datetime

from backend.agent.tech_surveillance.state import GraphState, DocsPaths
from langchain_core.messages import AIMessage

from .utils import create_marp_from_text,  convert_marp_to_formats

from backend.app.services.core.storage import storage_service

# Usar variable de entorno si existe (Docker), sino carpeta local
OUTPUT_DIR = os.getenv("SHARED_DATA_PATH", "generated_presentations") 
os.makedirs(OUTPUT_DIR, exist_ok=True)

def presentation_generation_docs_node(state: GraphState):
    print(" NODO de generacion de documentos de presentacion INVOCADO")
    presentation_summary = state.get("presentation_summary")
    call_info = state.get("call_info")
    # Obtener session_id del estado 
    session_id = state.get("session_id", "unknown_session")
    user_email = state.get("user_email", "unknown_user")

    if not presentation_summary or not call_info:
        message = AIMessage(content="Error: Sin datos de entrada")
        return {"messages": [message]}

     # 4. Ensamblaje seguro en Python (Marp)
    final_marp = create_marp_from_text(presentation_summary, call_info.title or "Presentación")
    
    # 5. Guardar archivo
    title_safe = re.sub(r'[^a-zA-Z0-9_-]', '', call_info.title.replace(' ', '_')) if call_info.title else 'sin_titulo'
    filename = os.path.join(OUTPUT_DIR, f"presentacion_{title_safe}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_marp)
            
    print(f"💾 Archivo Markdown guardado: {filename}")
    
    # --- NUEVO PASO: CONVERSIÓN AUTOMÁTICA ---
    pdf_path, pptx_path = convert_marp_to_formats(filename)
    
    msg_content = "Presentación generada en Markdown."
    if pdf_path and pptx_path:
        msg_content += f"\n✅ Exportada a PDF: {os.path.basename(pdf_path)}"
        msg_content += f"\n✅ Exportada a PPTX: {os.path.basename(pptx_path)}"
    else:
        msg_content += "\n⚠️ No se pudo exportar a PDF/PPTX (Verificar Node.js)."

    # ---  SUBIDA A MINIO ---
    print("☁️ Subiendo archivos a la nube (MinIO)...")
    
    # Construir ruta de carpeta organizada
    minio_folder = f"{user_email}/Agent_Sessions/{session_id}/presentation"
    
    # MD siempre existe si llegamos aquí
    md_key = storage_service.upload_file(filename, f"{minio_folder}/{os.path.basename(filename)}", remove_after_upload=True)
    
    # PDF y PPTX son opcionales (dependen de la conversión)
    pdf_key = None
    if pdf_path and os.path.exists(pdf_path):
        pdf_key = storage_service.upload_file(pdf_path, f"{minio_folder}/{os.path.basename(pdf_path)}", remove_after_upload=True)
    
    pptx_key = None
    if pptx_path and os.path.exists(pptx_path):
        pptx_key = storage_service.upload_file(pptx_path, f"{minio_folder}/{os.path.basename(pptx_path)}", remove_after_upload=True)
    
    # Actualizamos el estado con las KEYS de MinIO, no las rutas locales
    docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
    
    # Guardamos las keys de S3 en el objeto
    docs_paths.presentation_oath_md = md_key
    docs_paths.presentation_oath_pdf = pdf_key
    docs_paths.presentation_oath_pptx = pptx_key
    
    # --- NUEVO: Actualizar historial en CallInfo ---
    if not hasattr(call_info, "presentation_history") or call_info.presentation_history is None:
        call_info.presentation_history = []
    
    # Crear entrada de historial (usaremos la key de MinIO, que el API firmará después)
    history_entry = {
        "name": f"Presentación {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "url": pdf_key or md_key, # Link principal al PDF, o MD si falló
        "pdf": pdf_key,
        "pptx": pptx_key,
        "md": md_key,
        "date": datetime.datetime.now().isoformat(),
        "type": "presentation"
    }
    
    # Evitar duplicados si por alguna razón se re-ejecuta el mismo archivo (poco probable por el timestamp)
    call_info.presentation_history.append(history_entry)

    return {
        "messages": [AIMessage(content=msg_content)],
        "random_response": final_marp,
        "docs_paths": docs_paths,
        "call_info": call_info
    }
    