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

    INSTRUCCIONES CRÍTICAS:
    1. **FECHAS (important_dates)**: Busca específicamente la "Fecha de Apertura" y la "Fecha de Cierre" en el REPORTE. 
       - Si las encuentras, actualiza 'important_dates' con un formato claro (ej: 'Apertura: 20 Nov 2025 | Cierre: 29 Ene 2026'). 
       - PRIORIZA las fechas del reporte sobre las actuales si el reporte es más específico.
    2. **FINANCIAMIENTO (funding)**: Extrae montos máximos, porcentajes de financiación y si es no dilutiva.
    3. **OBJETIVO (objective)**: Refina el objetivo si el reporte describe mejor para qué sirve la convocatoria.
    4. **DOCS Y URL**: Mantén los documentos de contexto ('context_docs') e 'url' intactos si ya existen.
    6. **LÍNEAS TEMÁTICAS (thematic_lines)**: EXTRAE solo las líneas de investigación explícitas. <strong>REGLA DE ORO: NO INFIERAS LINEAS NO EXISTENTES.</strong>
    7. **ENFOQUE METODOLÓGICO (methodology)**: Identifica el marco metodológico requerido (ej: MGA WEB, SMART).
    
    IMPORTANTE: El campo 'thematic_lines' debe ser una lista con solo las líneas reales encontradas. No inventes para llenar cupos.
     El campo 'methodology' debe ser una descripción breve focalizada en el marco de trabajo (SMART, MGA, etc.).
    
    El resultado debe ser un objeto CallInfo completo, profesional y refinado.
    """

    max_retries = 3
    for attempt in range(max_retries):
        try:
            refined_info = await extraction_llm.ainvoke(prompt)
            
            # Llenamos ambos campos para evitar problemas de compatibilidad
            if refined_info.important_dates:
                refined_info.dates = refined_info.important_dates
            elif refined_info.dates:
                refined_info.important_dates = refined_info.dates
            
            # Preservar datos técnicos que no cambian
            if hasattr(current_call_info, "context_docs") and current_call_info.context_docs:
                refined_info.context_docs = current_call_info.context_docs
            if hasattr(current_call_info, "url") and current_call_info.url and not refined_info.url:
                refined_info.url = current_call_info.url
            if hasattr(current_call_info, "presentation_history") and current_call_info.presentation_history:
                refined_info.presentation_history = current_call_info.presentation_history
            
            # Asegurar que thematic_lines y methodology no se pierdan si el LLM falla en este intento pero existían
            if not refined_info.thematic_lines and hasattr(current_call_info, "thematic_lines"):
                refined_info.thematic_lines = current_call_info.thematic_lines
            if not refined_info.methodology and hasattr(current_call_info, "methodology"):
                refined_info.methodology = current_call_info.methodology

            print(f"✅ [REFINER] Información refinada:")
            print(f"   - Título: {refined_info.title}")
            print(f"   - Fechas Extraídas: {refined_info.important_dates or refined_info.dates}")
            print(f"   - Líneas Temáticas: {refined_info.thematic_lines}")
            print(f"   - Metodología (snippet): {refined_info.methodology[:100] if refined_info.methodology else 'VACÍO'}...")
            
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
