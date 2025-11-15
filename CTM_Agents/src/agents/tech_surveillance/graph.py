from __future__ import annotations
import os
from typing import List, Literal, Optional
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

from pydantic import BaseModel, Field

# --- 1. Modelos Pydantic para Salida Estructurada ---
# Usamos Pydantic para forzar al LLM a que nos dé la respuesta en el formato que necesitamos.



class ProjectInfo(BaseModel):
    """Información extraída de la descripción de un proyecto."""
    title: str = Field(description="Un título conciso y descriptivo para el proyecto.")
    description: str = Field(description="Una descripción de una sola frase que resuma el objetivo principal del proyecto.")

# --- 2. Definir el Estado del Grafo (Más Completo) ---
# Este es el nuevo "cerebro" de nuestro agente.



# --- 3. Inicializar los Modelos ---
# Usaremos el mismo modelo base pero con diferentes "capacidades".

# Modelo base para chat general
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Corregido para usar el nombre correcto
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True # Necesario para algunos modelos de Gemini
)

# Modelo "aumentado" para la tarea de enrutamiento
router_llm = chat_model.with_structured_output(RouteQuery)

# Modelo "aumentado" para la tarea de extracción de información
extraction_llm = chat_model.with_structured_output(ProjectInfo)

# --- 4. Definir los Nodos del Grafo ---



def ingestion_node(state: GraphState) -> dict:
    """
    Se activa cuando se detecta un nuevo proyecto. Extrae título y descripción.
    """
    print("--- Ejecutando Nodo: Ingesta de Proyecto ---")
    last_message = state["messages"][-1]
    
    prompt = f"""Eres un asistente experto en análisis de proyectos. Del siguiente texto, extrae un título conciso y una descripción de una frase.
    
    Texto del proyecto: "{last_message['content']}"
    
    Responde únicamente en el formato JSON solicitado.
    """
    
    try:
        # Llama al LLM de extracción
        project_info = extraction_llm.invoke(prompt)

        confirmation_text = (
            f"Proyecto registrado con éxito:\n\n"
            f"**Título:** {project_info.title}\n\n"
            f"**Descripción:** {project_info.description}\n\n"
            f"He recibido {len(state.get('document_urls', []))} documento(s) adjunto(s).\n\n"
            "¿Cómo podemos continuar?"
        )
        
        # --- CAMBIO CLAVE AQUÍ ---
        # Añadimos el mensaje de confirmación a la clave "messages" para que se envíe al cliente.
        return {
            "project_title": project_info.title,
            "project_description": project_info.description,
            "messages": [AIMessage(content=confirmation_text)]
        }
        # --- FIN DEL CAMBIO ---
    except Exception as e:
        print(f"--- Error en el Nodo de Ingesta: {e} ---")
        error_message = AIMessage(
            content="No pude procesar la descripción de tu proyecto. Por favor, sé más detallado y describe claramente los objetivos. "
                    "Por ejemplo: 'Quiero crear un informe sobre el impacto de la IA en la agricultura...'"
        )
        return {"messages": [error_message]}

def chat_node(state: GraphState) -> dict:
    """
    Maneja la conversación general. Es consciente del contexto del proyecto si ya existe.
    """
    print("--- Ejecutando Nodo: Chat General ---")
    messages = state["messages"]
    project_title = state.get("project_title")
    
    system_prompt = "Eres un asistente conversacional útil."
    if project_title:
        system_prompt = (
            f"Actualmente estás trabajando en el proyecto titulado '{project_title}'. "
            "Usa este contexto para responder las preguntas del usuario."
        )

    # Prepara los mensajes para el modelo, añadiendo el contexto del sistema
    messages_with_context = [SystemMessage(content=system_prompt)] + messages
    response = chat_model.invoke(messages_with_context)
    
    # --- CAMBIO CLAVE AQUÍ ---
    # Nos aseguramos de que la respuesta del chat también se retorne en la clave "messages".
    return {"messages": [response]}
    # --- FIN DEL CAMBIO ---

# --- 5. Construir el Grafo ---

workflow = StateGraph(GraphState)

# Añadimos los nodos
workflow.add_node("router", router_node)
workflow.add_node("ingest", ingestion_node)
workflow.add_node("chat", chat_node)

# El punto de entrada es siempre el enrutador
workflow.set_entry_point("router")

# Añadimos la arista condicional
workflow.add_conditional_edges(
    "router",
    # La función lambda simplemente lee la decisión que el enrutador guardó en el estado
    lambda state: state["route_decision"],
    {
        "PROYECTO": "ingest",
        "CHAT": "chat"
    }
)

# Definimos los puntos finales
workflow.add_edge("ingest", END)
workflow.add_edge("chat", END)

# Compilamos el grafo
agent = workflow.compile()