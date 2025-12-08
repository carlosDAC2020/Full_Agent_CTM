import os
import re 
import datetime

from agents.tech_surveillance.state import GraphState, DocsPaths
from langchain_core.messages import AIMessage

from .utils import create_marp_from_text,  convert_marp_to_formats


def presentation_generation_docs_node(state: GraphState):
    print(" NODO de generacion de documentos de presentacion INVOCADO")
    presentation_summary = state.get("presentation_summary")
    call_info = state.get("call_info")

    if not presentation_summary or not call_info:
        message = AIMessage(content="Error: Sin datos de entrada")
        return {"messages": [message]}

     # 4. Ensamblaje seguro en Python (Marp)
    final_marp = create_marp_from_text(presentation_summary, call_info.title or "Presentación")
    
    # 5. Guardar archivo
    os.makedirs("generated_presentations", exist_ok=True)
    title_safe = re.sub(r'[^a-zA-Z0-9_-]', '', call_info.title.replace(' ', '_')) if call_info.title else 'sin_titulo'
    filename = f"generated_presentations/presentacion_{title_safe}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
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

    # Actualizando rutas de documentos en el estado
    docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
    docs_paths.presentation_oath_md = filename
    docs_paths.presentation_oath_pdf = pdf_path
    docs_paths.presentation_oath_pptx = pptx_path
    
    return {
        "messages": [AIMessage(content=msg_content)],
        "random_response": final_marp,
        "docs_paths": docs_paths
    }
    
    