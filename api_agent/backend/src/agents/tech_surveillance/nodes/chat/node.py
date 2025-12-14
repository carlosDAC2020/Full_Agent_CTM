import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


from src.agents.tech_surveillance.state import GraphState
from .prompts import template

# Modelo base para chat general
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)


def chat_node(state: GraphState) -> dict:
    """
    Maneja la conversación general. Es consciente del contexto del proyecto si ya existe.
    """
    print("--- Ejecutando Nodo: Chat General ---")
    
    messages = state["messages"]
    project_title = state.get("project_title")
    
    # Obtener el mensaje actual del usuario - acceder como atributo, no como dict
    current_message = messages[-1].content if messages else ""
    
    # Preparar historial (todos los mensajes excepto el último)
    message_history = messages[:-1] if len(messages) > 1 else []
    
    # Crear el prompt usando el template
    prompt_template = PromptTemplate.from_template(template, template_format="jinja2")
    prompt = prompt_template.format(
        project_title=project_title,
        message_history=message_history,
        current_message=current_message
    )
    
    # Invocar el modelo con el prompt formateado
    response = chat_model.invoke(prompt)
    
    print(f"Respuesta del modelo: {response}")
    
    return {"messages": [response]}