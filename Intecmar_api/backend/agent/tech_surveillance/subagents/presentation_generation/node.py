import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_agent

from backend.agent.tech_surveillance.state import GraphState
from .prompts import SYSTEM_PROMPT, CONTENT_PROMPT_TEMPLATE

from  backend.agent.tech_surveillance.tools import web_search

# Lista de herramientas
web_research_tools = [
    web_search.tavily_search,
    web_search.brave_search,
    web_search.duckduckgo_search,
    web_search.fetch_url_content
]

# --- 1. CONFIGURACIÓN DEL MODELO ---
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7
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


