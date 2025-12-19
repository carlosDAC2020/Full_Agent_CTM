# backend/agent/state.py
import operator
from typing import TypedDict, Annotated, List

# El estado del agente. Se irá llenando a medida que el grafo avanza.
class AgentState(TypedDict):
    tema: str                                    # El tema de búsqueda inicial, ej: "IA y tecnología"
    plan: str                                    # El plan generado por el LLM
    consultas_busqueda: List[str]                # Las consultas específicas para las herramientas de búsqueda
    resultados_busqueda: Annotated[list, operator.add] # Lista de resultados (URLs, snippets)
    datos_extraidos: Annotated[list, operator.add]   # Lista de convocatorias con datos estructurados (JSON)
    contenido_curado: List[dict]                 # Lista final de convocatorias con resúmenes atractivos
    rutas_imagenes: List[str]                    # Rutas a las imágenes generadas para el magazine
    pdf_path: str                                # Ruta del PDF generado final
