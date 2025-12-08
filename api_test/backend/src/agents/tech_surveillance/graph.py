
from __future__ import annotations

import os
from langgraph.graph import END, StateGraph
from agents.tech_surveillance.state import GraphState

# importamos rutas
from agents.tech_surveillance.routes.manager.route import router_node

# importamos nodos 
from agents.tech_surveillance.nodes.ingestion.node import ingestion_node
from agents.tech_surveillance.nodes.chat.node import chat_node
from agents.tech_surveillance.nodes.report.node import report_node
from agents.tech_surveillance.nodes.initial_schema_proyect.node import initial_schema_node
from agents.tech_surveillance.nodes.initial_schema_proyect_doc.node import initial_schema_proyect_doc_node
from agents.tech_surveillance.nodes.ipropose_ides.node import propose_ides_node
from agents.tech_surveillance.nodes.presentation.node import presentation_generation_docs_node

# importamos subagentes 
from agents.tech_surveillance.subagents.academic_reseacrh.node import academic_research_node
from agents.tech_surveillance.subagents.presentation_generation.node import presentation_generation_node

# importamos subgrafos 
from agents.tech_surveillance.subgrafths.image_generator.graph import Image_generator_subgraph
from agents.tech_surveillance.subgrafths.project_schema.graph import project_schema_subgraph


# --- Configuración de Ejecución ---
# Leemos las variables de entorno para controlar el flujo
# CTM_EXECUTION_SCOPE: ALL, ACADEMIC, SCHEMA, IMAGE
# CTM_EXECUTION_STRATEGY: SEQUENTIAL, PARALLEL (Solo aplica para ALL)
EXECUTION_SCOPE = "IMAGE" #os.environ.get("CTM_EXECUTION_SCOPE", "ALL").upper()
EXECUTION_STRATEGY = os.environ.get("CTM_EXECUTION_STRATEGY", "SEQUENTIAL").upper()

print(f"--- CONFIGURACIÓN DE GRAFO ---")
print(f"SCOPE: {EXECUTION_SCOPE}")
print(f"STRATEGY: {EXECUTION_STRATEGY}")

# --- Construir el Grafo ---

workflow = StateGraph(GraphState)

# Añadimos los nodos
workflow.add_node("router", router_node)

# seleccion de convocatoria 
workflow.add_node("ingest", ingestion_node)
workflow.add_node("presentation_generator", presentation_generation_node)
workflow.add_node("presentation_generator_docs", presentation_generation_docs_node)

# geenracion de ideas
workflow.add_node("propose_ideas", propose_ides_node)

# seleccion y generacionde idea del proyecto
workflow.add_node("proyect_idea", initial_schema_node)
workflow.add_node("project_idea_doc", initial_schema_proyect_doc_node)

# investicacion y generacion de la propuesta de proyeto y documentos asociados 
workflow.add_node("academic_research", academic_research_node)
workflow.add_node("project_schemas", project_schema_subgraph)
workflow.add_node("images_generator", Image_generator_subgraph)
workflow.add_node("report", report_node)

# --- Lógica de Conexión Estática ---
workflow.set_entry_point("router")

# Añadimos la arista condicional
workflow.add_conditional_edges(
    "router",
    lambda state: state["route_decision"],
    {
        "ingest": "ingest",
        "proposal_ideas": "propose_ideas",
        "project_idea": "proyect_idea",
        "generate_proyect": "academic_research"
    }
)

# flujo para invetsiagcion de convocatorias
workflow.add_edge("ingest", "presentation_generator")
workflow.add_edge("presentation_generator", "presentation_generator_docs")
workflow.add_edge("presentation_generator_docs", END)

# flujo para generacion de ideas de proyecto
workflow.add_edge("propose_ideas", END)

# flujo para definicion de esquema inicial del proyecto
workflow.add_edge("proyect_idea", "project_idea_doc")
workflow.add_edge("project_idea_doc", END)

# flujo para generacion del esquema del proyecto
workflow.add_edge("academic_research", "project_schemas")
workflow.add_edge("project_schemas", "images_generator")
workflow.add_edge("images_generator", "report")
workflow.add_edge("report", END)



# Compilamos el grafo
agent = workflow.compile()