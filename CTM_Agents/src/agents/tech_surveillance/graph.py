
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
EXECUTION_SCOPE = os.environ.get("CTM_EXECUTION_SCOPE", "ALL").upper()
EXECUTION_STRATEGY = os.environ.get("CTM_EXECUTION_STRATEGY", "SEQUENTIAL").upper()

print(f"--- CONFIGURACIÓN DE GRAFO ---")
print(f"SCOPE: {EXECUTION_SCOPE}")
print(f"STRATEGY: {EXECUTION_STRATEGY}")

# --- Construir el Grafo ---

workflow = StateGraph(GraphState)

# Añadimos los nodos
workflow.add_node("router", router_node)
workflow.add_node("ingest", ingestion_node)
workflow.add_node("chat", chat_node)
workflow.add_node("report", report_node)

# Añadimos sub agentes como nodos 
workflow.add_node("academic_research", academic_research_node)
workflow.add_node("presentation_generator", presentation_generation_node)

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

# --- Lógica de Conexión Dinámica ---

if EXECUTION_SCOPE == "ALL":
    if EXECUTION_STRATEGY == "PARALLEL":
        # Ejecución Semi-Paralela Optimizada:
        # 1. Ingestión -> Investigación (Secuencial para contexto)
        # 2. Investigación -> Esquema Y Imagen (Paralelo)
        # 3. Ambos -> Reporte (Convergencia)
        
        workflow.add_edge("ingest", "academic_research")
        
        # Bifurcación después de la investigación
        workflow.add_edge("academic_research", "project_schemas")
        workflow.add_edge("academic_research", "images_generator")
        workflow.add_edge("academic_research", "presentation_generatior")
        
        # Convergencia (El reporte se ejecutará dos veces, la segunda será la completa)
        workflow.add_edge("project_schemas", "report")
        workflow.add_edge("images_generator", "report")
        workflow.add_edge("presentation_generator", "report")
        
    else:
        # Ejecución Secuencial (Default y Recomendada)
        workflow.add_edge("ingest", "academic_research")
        workflow.add_edge("academic_research", "project_schemas")
        workflow.add_edge("project_schemas", "images_generator")
        workflow.add_edge("images_generator", "report")
        # Presentación antes del reporte
        #workflow.add_edge("images_generator", "presentation_generator")
        #workflow.add_edge("presentation_generator", "report")

elif EXECUTION_SCOPE == "ACADEMIC":
    workflow.add_edge("ingest", "academic_research")
    workflow.add_edge("academic_research", "report")

elif EXECUTION_SCOPE == "SCHEMA":
    workflow.add_edge("ingest", "project_schemas")
    workflow.add_edge("project_schemas", "report")

elif EXECUTION_SCOPE == "IMAGE":
    workflow.add_edge("ingest", "images_generator")
    workflow.add_edge("images_generator", "report")

elif EXECUTION_SCOPE == "PRESENTATION":
    workflow.add_edge("ingest", "presentation_generator")
    workflow.add_edge("presentation_generator", "report")
else:
    # Fallback seguro: Secuencial completa
    print(f"⚠️ Scope desconocido '{EXECUTION_SCOPE}'. Usando configuración por defecto (ALL SEQUENTIAL).")
    workflow.add_edge("ingest", "academic_research")
    workflow.add_edge("academic_research", "project_schemas")
    workflow.add_edge("project_schemas", "images_generator")
    workflow.add_edge("images_generator", "presentation_generator")
    workflow.add_edge("presentation_generator", "report")

# Finalización
workflow.add_edge("report", END)
workflow.add_edge("chat", END)

# Compilamos el grafo
agent = workflow.compile()