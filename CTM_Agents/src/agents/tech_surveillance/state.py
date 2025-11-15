from typing_extensions import TypedDict

class GraphState(TypedDict):
    """
    Representa el estado de nuestro grafo.

    Atributos:
      messages: Historial de la conversación.
      document_urls: Lista de URLs de los archivos subidos.
      project_title: Título del proyecto (una vez extraído).
      project_description: Descripción del proyecto (una vez extraída).
      final_report: Espacio reservado para el informe final.
      route_decision: La decisión tomada por el enrutador.
    """
    messages: List[BaseMessage]
    document_urls: Optional[List[str]] = None
    project_title: Optional[str] = None
    project_description: Optional[str] = None
    final_report: Optional[str] = None
    route_decision: Optional[str] = None