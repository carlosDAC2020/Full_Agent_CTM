import os
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_agent

from backend.agent.tech_surveillance.state import GraphState
from .prompts import SYSTEM_PROMPT, CONTENT_PROMPT_TEMPLATE

from backend.agent.tech_surveillance.tools.rag import rag_search_documents
from backend.agent.tech_surveillance.tools import web_search

# Lista de herramientas
web_research_tools = [
    web_search.tavily_search,
    web_search.brave_search,
    web_search.duckduckgo_search,
    web_search.fetch_url_content,
    rag_search_documents
]

# --- 1. CONFIGURACIÓN DEL MODELO ---
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    max_retries=6
)

# Creamos el agente con herramientas
academic_research_agent = create_agent(
    model=model,  
    tools=web_research_tools,
    system_prompt=SYSTEM_PROMPT
)


# --- NODO PRINCIPAL ---
async def presentation_generation_node(state: GraphState):
    """
    Nodo para la generacion de los documentos de presentacion
    """
    print("🎨 [PRESENTATION] INICIANDO AGENTE DE INVESTIGACIÓN Y PRESENTACIÓN...")
    
    call_info = state.get("call_info")
    session_id = state.get("session_id")
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

    # Agregamos instrucción explícita sobre la sesión para RAG
    prompt_content += f"\n\nNOTA: Si necesitas consultar documentos internos de esta sesión, usa la herramienta 'rag_search_documents' con el session_id: {session_id}"

    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Espera inicial para despejar la cuota de la vectorización
            if attempt == 0:
                time.sleep(2) 
                
            # 2. Invocar al Agente con Herramientas
            result = await academic_research_agent.ainvoke(
                {"messages": [HumanMessage(content=prompt_content)]}
            )

            last_message = result["messages"][-1]
            print(f"📝 [PRESENTATION] Mensaje final del agente recibido. Procesando...")

            # 3. Extraer texto final
            text_response = ""
            if isinstance(last_message.content, str):
                text_response = last_message.content
            elif isinstance(last_message.content, list):
                parts = []
                for block in last_message.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", ""))
                text_response = "\n".join(parts)
            else:
                text_response = str(last_message.content)
            
            print(f"✅ [PRESENTATION] Agente finalizado. Longitud respuesta: {len(text_response)} caracteres")
            message = AIMessage(content="✅ Resumen de presentación generado correctamente.")
            
            return {
                "messages": [message],
                "presentation_summary": text_response,
            }

        except Exception as e:
            error_str = str(e)
            if ("429" in error_str or "RESOURCE_EXHAUSTED" in error_str) and attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 10 
                print(f"⚠️ [PRESENTATION] Cuota agotada (429). Reintentando en {wait_time}s (Intento {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
                continue
            
            print(f"❌ [PRESENTATION] Error crítico en nodo: {e}")
            return {
                "messages": [
                    AIMessage(content=f"❌ Error crítico en nodo: {e}")
                    ]
                }


