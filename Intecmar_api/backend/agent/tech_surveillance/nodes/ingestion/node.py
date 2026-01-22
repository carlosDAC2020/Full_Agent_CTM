
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from .prompts import template

# Importamos los nuevos esquemas del estado
from backend.agent.tech_surveillance.state import GraphState, CallInfo

# ... (definición de chat_model y extraction_llm sin cambios) ...
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.0, # Reduced temperature for more deterministic extraction
    convert_system_message_to_human=True
)
extraction_llm = chat_model.with_structured_output(CallInfo)

def ingestion_node(state: GraphState) -> dict:
    """
    Se activa cuando se detecta un nuevo proyecto o convocatoria. 
    Extrae la información de la convocatoria y estructura el estado.
    """
    print("--- Ejecutando Nodo: Ingesta de Convocatoria ---")
    last_message = state["messages"][-1].content
    
    prompt_template = PromptTemplate.from_template(template, partial_variables={"last_message": last_message})
    prompt = prompt_template.format()
    
    try:
        # 1. Llama al LLM para extraer la información (Call Info Only)
        ingestion_result: CallInfo = extraction_llm.invoke(prompt)
        print(f"DEBUG: Ingestion Result: {ingestion_result}")
        
        # 2. Prepara el mensaje de confirmación
        if ingestion_result:
            # --- LOGICA DE FALLBACK ROBUSTA ---
            # Si el objetivo está vacío pero la descripción tiene texto, usamos la descripción
            if (not ingestion_result.objective or ingestion_result.objective.strip() == "") and ingestion_result.description:
                ingestion_result.objective = ingestion_result.description
            
            # Si la descripción está vacía pero el objetivo tiene texto, usamos el objetivo
            if (not ingestion_result.description or ingestion_result.description.strip() == "") and ingestion_result.objective:
                ingestion_result.description = ingestion_result.objective

            # Asegurar compatibilidad de fechas
            if ingestion_result.important_dates:
                ingestion_result.dates = ingestion_result.important_dates
            elif ingestion_result.dates:
                ingestion_result.important_dates = ingestion_result.dates

            # 2. Prepara el mensaje de confirmación detallado
            confirmation_text = f"TÍTULO: {ingestion_result.title}\n" \
                                f"        DESCRIPCIÓN: {ingestion_result.description}\n" \
                                f"        OBJETIVO: {ingestion_result.objective}\n" \
                                f"        FINANCIACIÓN: {ingestion_result.funding}\n" \
                                f"        FECHAS: {ingestion_result.important_dates}\n" \
                                f"        FUENTE: {ingestion_result.url}\n" \
                                f"        KEYWORDS: {ingestion_result.keywords}\n\n" \
                                f"✅ **Convocatoria Detectada.** He cargado los detalles. ¿Qué deseas hacer a continuación?"
        else:
            confirmation_text = "No he detectado información clara sobre una convocatoria. Por favor, proporciona más detalles."

        # 3. Preservar documentos de contexto e historial si ya existen en el estado
        old_call_info = state.get("call_info")
        if old_call_info and ingestion_result:
            # Context Docs
            if hasattr(old_call_info, "context_docs") and old_call_info.context_docs:
                ingestion_result.context_docs = old_call_info.context_docs
            elif isinstance(old_call_info, dict) and old_call_info.get("context_docs"):
                ingestion_result.context_docs = old_call_info["context_docs"]
            
            # Presentation History
            if hasattr(old_call_info, "presentation_history") and old_call_info.presentation_history:
                ingestion_result.presentation_history = old_call_info.presentation_history
            elif isinstance(old_call_info, dict) and old_call_info.get("presentation_history"):
                ingestion_result.presentation_history = old_call_info["presentation_history"]

        # 4. Devuelve la nueva estructura del estado
        return {
            "call_info": ingestion_result, # Guardamos la info de la convocatoria en el estado
            "messages": [AIMessage(content=confirmation_text)]
        }

    except Exception as e:
        print(f"--- Error en el Nodo de Ingesta: {e} ---")
        error_message = AIMessage(
            content="Hubo un problema procesando la información de la convocatoria."
        )
        return {"messages": [error_message]}
