from langchain_core.messages import AIMessage
from agents.tech_surveillance.state import GraphState

def proyect_idea_node(state : GraphState) -> dict:

    call_info = state.get("call_info")
    title = call_info.title if call_info else "Sin título"
    objective = call_info.objective if call_info else "Sin objetivo"    

    mesage = AIMessage(
        content=f"idea de proyecto registrada correctamente.\n para la convocatoria:\n Título: {title}\n Objetivo: {objective}"
    )
    return {
        "messages": [mesage]
    }