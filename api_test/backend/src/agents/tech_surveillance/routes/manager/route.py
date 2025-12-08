import os

from agents.tech_surveillance.state import GraphState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from src.agents.tech_surveillance.routes.manager.squemas import RouteQuery
from src.agents.tech_surveillance.routes.manager.prompts import template

# Modelo base para chat general
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Corregido para usar el nombre correcto
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

# Modelo "aumentado" para la tarea de enrutamiento
router_llm = chat_model.with_structured_output(RouteQuery)

def router_node(state: GraphState) -> dict:
    """
    Clasifica la intención del último mensaje del usuario para decidir la ruta a seguir.
    """
    # Actualiza el estado con la decisión para que la arista condicional pueda leerla
    return {
            "route_decision":state["route_decision"]
        }