import os

from agents.tech_surveillance.state import GraphState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from agents.tech_surveillance.routes.manager.squemas import RouteQuery
from agents.tech_surveillance.routes.manager.prompts import template

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
    print("--- Ejecutando Nodo: Enrutador ---")
    last_message = state["messages"][-1]
    
    report_components = state.get("report_components") or {}
    general_info = report_components.get("general_info") or {}
    project_title = general_info.get("project_title", "N/A")
    project_description = general_info.get("project_description", "N/A")

    prompt_template = PromptTemplate.from_template(
        template, 
        partial_variables={
            "last_message": str(last_message.content), 
            "context_summary": f"""
            project_title: {project_title} 
            project_description: {project_description}
            """
        })
    
    prompt = prompt_template.format()

    # Llama al LLM de enrutamiento
    decision_result = router_llm.invoke(prompt)
    
    print(f"--- Decisión del Enrutador: {decision_result.decision} ---")
    
    # Actualiza el estado con la decisión para que la arista condicional pueda leerla
    return {
            "route_decision":decision_result.decision
        }