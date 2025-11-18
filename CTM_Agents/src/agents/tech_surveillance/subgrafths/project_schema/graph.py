# subgraph.py

from __future__ import annotations
import os 
from langgraph.graph import END, StateGraph
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos el estado y los prompts
from agents.tech_surveillance.state import GraphState, ProjectPlan
from .prompts import SMART_OBJECTIVES_PROMPT, ACTIVITY_SCHEDULE_PROMPT, RISK_MATRIX_PROMPT


# --- Inicialización del LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

# --- Implementación de los Nodos del Subgrafo ---

def generate_smart_objectives(state: GraphState):
    """
    Genera objetivos SMART basados en el título y descripción del proyecto.
    """
    print("---GENERANDO OBJETIVOS SMART---")
    title = state.get("project_title", "No especificado")
    description = state.get("project_description", "No especificado")
    
    # 1. Formatear el prompt
    prompt = SMART_OBJECTIVES_PROMPT.format(title=title, description=description)
    
    # 2. Invocar al LLM para generar el contenido
    response = llm.invoke(prompt)
    generated_objectives = response.content
    
    # 3. Mensaje de confirmación para el historial
    message = AIMessage(content="Objetivos SMART generados. Procediendo a crear el cronograma.")
    
    # 4. Actualizar el estado
    return {
        "messages": [message],
        "smart_objectives": generated_objectives
    }

def create_activity_schedule(state: GraphState):
    """
    Crea un cronograma de actividades para el proyecto.
    """
    print("---CREANDO CRONOGRAMA DE ACTIVIDADES---")
    title = state.get("project_title", "No especificado")
    description = state.get("project_description", "No especificado")

    prompt = ACTIVITY_SCHEDULE_PROMPT.format(title=title, description=description)
    response = llm.invoke(prompt)
    generated_schedule = response.content
    
    message = AIMessage(content="Cronograma de actividades creado. Procediendo a construir la matriz de riesgos.")

    return {
        "messages": [message],
        "activity_schedule": generated_schedule
    }

def build_risk_matrix(state: GraphState):
    """
    Construye la matriz de riesgos del proyecto.
    """
    print("---CONSTRUYENDO MATRIZ DE RIESGOS---")
    title = state.get("project_title", "No especificado")
    description = state.get("project_description", "No especificado")

    prompt = RISK_MATRIX_PROMPT.format(title=title, description=description)
    response = llm.invoke(prompt)
    generated_matrix = response.content
    
    message = AIMessage(content="Matriz de riesgos construida. Compilando el plan de proyecto.")

    return {
        "messages": [message],
        "risk_matrix": generated_matrix
    }

def compile_project_plan(state: GraphState):
    """
    Nodo final que consolida los resultados en el esquema ProjectPlan.
    """
    print("---COMPILANDO PLAN DE PROYECTO ESTRUCTURADO---")
    
    project_plan: ProjectPlan = {
        "smart_objectives": state.get("smart_objectives", "No generado"),
        "activity_schedule": state.get("activity_schedule", "No generado"),
        "risk_matrix": state.get("risk_matrix", "No generado")
    }
    
    message = AIMessage(content="Plan de proyecto final compilado y estructurado en el estado.")
    
    return {
        "messages": [message],
        "project_plan": project_plan
    }


# --- Ensamblaje del Grafo ---

workflow = StateGraph(GraphState)

# Añadir los nodos al workflow
workflow.add_node("generate_objectives", generate_smart_objectives)
workflow.add_node("activity_schedule", create_activity_schedule)
workflow.add_node("risk_matrix", build_risk_matrix)
workflow.add_node("compile_plan", compile_project_plan) 

# Definir el flujo de trabajo
workflow.set_entry_point("generate_objectives")
workflow.add_edge("generate_objectives", "activity_schedule")
workflow.add_edge("activity_schedule", "risk_matrix")
workflow.add_edge("risk_matrix", "compile_plan")
workflow.add_edge("compile_plan", END)

# Compilar el grafo para que sea ejecutable
project_schema_subgraph = workflow.compile()

