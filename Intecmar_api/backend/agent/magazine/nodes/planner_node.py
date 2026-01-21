from ..state import AgentState
from .common import llm
from ..prompts.planner_prompts import build_planner_prompt


def nodo_planificador(state: AgentState) -> AgentState:
    print("--- 🧠 PLANIFICANDO ---")
    prompt = build_planner_prompt(state["tema"])
    response = llm.invoke(prompt)
    consultas = response.content.strip().split('\n')
    return {"plan": "Plan generado con éxito.", "consultas_busqueda": consultas}
