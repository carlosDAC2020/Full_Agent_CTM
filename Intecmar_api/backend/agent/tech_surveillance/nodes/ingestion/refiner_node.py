import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.agent.tech_surveillance.state import GraphState, CallInfo

# Configuramos el modelo para extracción estructurada
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.0,
    max_retries=6
)
extraction_llm = model.with_structured_output(CallInfo)

async def call_info_refiner_node(state: GraphState):
    """
    Nodo que refina la información de la convocatoria (CallInfo) 
    utilizando el reporte detallado generado por el agente de investigación.
    """
    print("🧹 [REFINER] REFINANDO INFORMACIÓN DE LA CONVOCATORIA...")
    
    presentation_summary = state.get("presentation_summary")
    current_call_info = state.get("call_info")
    
    if not presentation_summary or not current_call_info:
        print("⚠️ [REFINER] No hay reporte o CallInfo para refinar. Saltando.")
        return state

    prompt = f"""
    Eres un experto en extracción de datos. Tu tarea es actualizar el objeto 'CallInfo' usando la información 
    más detallada encontrada en el siguiente REPORTE DE INVESTIGACIÓN.

    INFORMACIÓN ACTUAL (Puede estar incompleta):
    - Título: {current_call_info.title}
    - Fechas: {current_call_info.important_dates}
    - Financiamiento: {current_call_info.funding}

    REPORTE DE INVESTIGACIÓN DETALLADO:
    {presentation_summary}

    INSTRUCCIONES:
    1. Si el reporte contiene fechas exactas, montos de financiamiento detallados o un objetivo más preciso que los actuales, ACTUALÍZALOS.
    2. Mantén los documentos de contexto ('context_docs') y la URL intactos si ya existen.
    3. Asegúrate de extraer palabras clave relevantes y beneficios si se mencionan en el reporte.
    4. El resultado debe ser un objeto CallInfo completo y refinado.
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            refined_info = await extraction_llm.ainvoke(prompt)
            
            # Preservar datos técnicos que no cambian
            if hasattr(current_call_info, "context_docs") and current_call_info.context_docs:
                refined_info.context_docs = current_call_info.context_docs
            if hasattr(current_call_info, "url") and current_call_info.url and not refined_info.url:
                refined_info.url = current_call_info.url

            print(f"✅ [REFINER] Información refinada con éxito: {refined_info.title}")
            return {"call_info": refined_info}
            
        except Exception as e:
            error_str = str(e)
            is_rate_limit = "429" in error_str or "RESOURCE_EXHAUSTED" in error_str
            is_overloaded = "503" in error_str or "UNAVAILABLE" in error_str
            
            if (is_rate_limit or is_overloaded) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 10
                print(f"⚠️ [REFINER] API ocupada ({'429' if is_rate_limit else '503'}). Reintentando en {wait_time}s...")
                time.sleep(wait_time)
                continue
                
            print(f"❌ [REFINER] Error refinando información: {e}")
            return state
