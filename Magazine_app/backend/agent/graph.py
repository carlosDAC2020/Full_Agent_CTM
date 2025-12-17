# backend/agent/graph.py
from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    nodo_planificador,
    nodo_busqueda,
    nodo_extraccion,
    nodo_curacion,
    nodo_guardado_db,
)

# Crear el grafo
workflow = StateGraph(AgentState)

# Añadir los nodos
workflow.add_node("planificador", nodo_planificador)
workflow.add_node("busqueda", nodo_busqueda)
workflow.add_node("extraccion", nodo_extraccion)
workflow.add_node("curacion", nodo_curacion)
workflow.add_node("guardado_db", nodo_guardado_db)

# Definir el flujo (las conexiones entre nodos)
workflow.set_entry_point("planificador")
workflow.add_edge("planificador", "busqueda")
workflow.add_edge("busqueda", "extraccion")
workflow.add_edge("extraccion", "curacion")
workflow.add_edge("curacion", "guardado_db")
workflow.add_edge("guardado_db", END)

# Compilar el grafo en una aplicación ejecutable
app = workflow.compile()