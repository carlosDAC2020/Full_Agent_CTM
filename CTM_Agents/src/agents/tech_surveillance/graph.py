from __future__ import annotations

from langgraph.graph import END, StateGraph
from agents.tech_surveillance.state import GraphState

# importamos rutas
from agents.tech_surveillance.routes.manager.route import router_node

# importamos nodos 
from agents.tech_surveillance.nodes.ingestion.node import ingestion_node
from agents.tech_surveillance.nodes.chat.node import chat_node
from agents.tech_surveillance.nodes.report.node import report_mode

# importamos subagentes 
from agents.tech_surveillance.subagents.academic_reseacrh.node import academic_research_node

# importamos subgrafos 
from agents.tech_surveillance.subgrafths.image_generator.graph import Image_generator_subgraph
from agents.tech_surveillance.subgrafths.project_schema.graph import project_schema_subgraph



#-----------------------------------------------------------

# --- Construir el Grafo ---

workflow = StateGraph(GraphState)

# Añadimos los nodos
workflow.add_node("router", router_node)
workflow.add_node("ingest", ingestion_node)
workflow.add_node("chat", chat_node)
workflow.add_node("report", report_mode)

# Añadimos sub agentes como nodos 
workflow.add_node("academic_research", academic_research_node)

# Añadimos los subgrafos como nodos
workflow.add_node("project_schemas", project_schema_subgraph)
workflow.add_node("images_generator", Image_generator_subgraph)

# El punto de entrada es siempre el enrutador
workflow.set_entry_point("router")

# Añadimos la arista condicional
workflow.add_conditional_edges(
    "router",
    lambda state: state["route_decision"],
    {
        "PROYECTO": "ingest",
        "CHAT": "chat",
    }
)

# Definimos los puntos finales

# ejecucion en paralelo ára la generacion de reporte 
#workflow.add_edge("ingest", "academic_research")
workflow.add_edge("ingest", "project_schemas")
#workflow.add_edge("ingest", "images_generator")

# esperamos la ejecuion de cada parte del reporte para traerla y genrar el reporte 
#workflow.add_edge("academic_research", "report")
workflow.add_edge("project_schemas", "report")
#workflow.add_edge("images_generator", "report")

workflow.add_edge("report", END)
workflow.add_edge("chat", END)

# Compilamos el grafo
agent = workflow.compile()