
from __future__ import annotations

from langgraph.graph import END, StateGraph

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState


# Importar los nodos 
from .nodes.justification.node import generate_justification
from .nodes.objectives.node import generate_objectives
from .nodes.methodology.node import generate_methodology
from .nodes.activity_schedule.node import create_activity_schedule
from .nodes.risk_matrix.node import build_risk_matrix
from .nodes.impacts.node import generate_impacts
from .nodes.executive_summary.node import generate_executive_summary

# --- Ensamblaje del Grafo Extendido ---
workflow = StateGraph(GraphState)

# Añadir todos los nodos al workflow
workflow.add_node("generate_justification", generate_justification)
workflow.add_node("generate_objectives", generate_objectives)
workflow.add_node("generate_methodology", generate_methodology)
workflow.add_node("create_activity_schedule", create_activity_schedule)
workflow.add_node("build_risk_matrix", build_risk_matrix)
workflow.add_node("generate_impacts", generate_impacts)
workflow.add_node("generate_executive_summary", generate_executive_summary)

# Definir el nuevo flujo de trabajo SECUENCIAL
workflow.set_entry_point("generate_justification")
workflow.add_edge("generate_justification", "generate_objectives")
workflow.add_edge("generate_objectives", "generate_methodology")
workflow.add_edge("generate_methodology", "create_activity_schedule")
workflow.add_edge("create_activity_schedule", "build_risk_matrix")
workflow.add_edge("build_risk_matrix", "generate_impacts")
workflow.add_edge("generate_impacts", "generate_executive_summary")
workflow.add_edge("generate_executive_summary", END) 

# Compilar el grafo para que sea ejecutable
project_schema_subgraph = workflow.compile()