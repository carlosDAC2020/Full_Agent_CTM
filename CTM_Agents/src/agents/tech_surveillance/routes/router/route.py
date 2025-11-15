from langchain_google_genai import ChatGoogleGenerativeAI

# Modelo base para chat general
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Corregido para usar el nombre correcto
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True # Necesario para algunos modelos de Gemini
)

# Modelo "aumentado" para la tarea de enrutamiento
router_llm = chat_model.with_structured_output(RouteQuery)

def router_node(state: GraphState) -> dict:
    """
    Clasifica la intención del último mensaje del usuario para decidir la ruta a seguir.
    """
    print("--- Ejecutando Nodo: Enrutador ---")
    last_message = state["messages"][-1]
    
    prompt = f"""Eres un clasificador de intenciones experto. Tu tarea es analizar el siguiente mensaje de un usuario y decidir si está:
    (A) Describiendo un nuevo proyecto (intención 'PROYECTO').
    (B) Haciendo una pregunta general o continuando una conversación (intención 'CHAT').

    Mensaje del usuario: "{last_message['content']}"

    Responde únicamente con la intención.
    """
    
    # Llama al LLM de enrutamiento
    decision_result = router_llm.invoke(prompt)
    
    print(f"--- Decisión del Enrutador: {decision_result.decision} ---")
    
    # Actualiza el estado con la decisión para que la arista condicional pueda leerla
    return {"route_decision": decision_result.decision}