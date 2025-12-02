import os
import re
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_agent
from agents.tech_surveillance.state import GraphState
from .prompts import SYSTEM_PROMPT, CONTENT_PROMPT_TEMPLATE, MARP_HEADER

from .tools import research_tools
from .utils import create_marp_from_text,  convert_marp_to_formats


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
    
        # 3. Extraer texto final
        last_message = result["messages"][-1]

        text_response = last_message.content[0]['text'] + last_message.content[-1]
        
        print(f"✅ Agente finalizado. Longitud respuesta: {len(text_response)} caracteres")
        print(text_response)
        # 4. Ensamblaje seguro en Python (Marp)
        final_marp = create_marp_from_text(text_response, call_info.title or "Presentación")
        
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

        return {
            "messages": [AIMessage(content=msg_content)],
            "random_response": final_marp,
            "presentation_summary": text_response
        }

    except Exception as e:
        print(f"❌ Error crítico en nodo: {e}")
        return {"random_response": f"Error: {e}"}


