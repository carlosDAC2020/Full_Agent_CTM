from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

# Definimos el esquema del estado de nuestro grafo
class AgentState(TypedDict):
    convocatoria_titulo: str
    project_ideas: List[Dict]
    selected_project: Dict
    final_status: str

# --- NODOS DEL GRAFO ---

def generate_ideas_node(state: AgentState):
    """Simula la creación de 5 ideas SMART basadas en la convocatoria"""
    titulo_conv = state.get("convocatoria_titulo", "General")
    
    # Generamos datos "dummy" pero estructurados
    ideas = []
    for i in range(1, 6):
        ideas.append({
            "id": i,
            "title": f"Idea Innovadora {i} para {titulo_conv[:15]}...",
            "description": f"Propuesta tecnológica basada en IA para optimizar procesos en el contexto de {titulo_conv}. Enfoque en eficiencia.",
            "objectives": [
                f"S (Específico): Implementar módulo {i}.",
                "M (Medible): Reducir tiempos en un 20%.",
                "A (Alcanzable): Usando tecnología open source.",
                "R (Relevante): Alineado con la convocatoria.",
                "T (Temporal): Ejecución en 6 meses."
            ]
        })
    
    return {"project_ideas": ideas}

def analyze_project_node(state: AgentState):
    """Simula un análisis exhaustivo del proyecto final"""
    # Aquí en la vida real llamarías a un LLM para evaluar el proyecto
    return {"final_status": "APPROVED_WITH_HONORS"}

# --- CONSTRUCCIÓN DEL GRAFO ---

workflow = StateGraph(AgentState)

# Añadimos los nodos
workflow.add_node("generator", generate_ideas_node)
workflow.add_node("analyzer", analyze_project_node)

# Definimos el flujo (en este caso desconectado, lo usaremos como herramientas sueltas por simplicidad en app.py)
# Pero para cumplir, hacemos una conexión directa
workflow.set_entry_point("generator")
workflow.add_edge("generator", "analyzer")
workflow.add_edge("analyzer", END)

# Compilamos
dummy_graph = workflow.compile()