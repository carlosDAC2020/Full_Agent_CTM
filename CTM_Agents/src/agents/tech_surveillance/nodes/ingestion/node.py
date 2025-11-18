import os 

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from .squemas import ProjectInfo
from .prompts import template

from agents.tech_surveillance.state import GraphState

# Modelo base para chat general
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", # Corregido para usar el nombre correcto
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True # Necesario para algunos modelos de Gemini
)

# Modelo "aumentado" para la tarea de extracción de información
extraction_llm = chat_model.with_structured_output(ProjectInfo)


def ingestion_node(state: GraphState) -> dict:
    """
    Se activa cuando se detecta un nuevo proyecto. Extrae título y descripción.
    """
    print("--- Ejecutando Nodo: Ingesta de Proyecto ---")
    last_message = state["messages"][-1]
    
    prompt_template = PromptTemplate.from_template(template, partial_variables={"last_message": last_message})

    prompt = prompt_template.format()
    
    try:
        # Llama al LLM de extracción
        project_info = extraction_llm.invoke(prompt)

        confirmation_text = (
            f"Proyecto registrado con éxito:\n\n"
            f"**Título:** {project_info.title}\n\n"
            f"**Descripción:** {project_info.description}\n\n"
            f"He recibido {len(state.get('document_urls', []))} documento(s) adjunto(s).\n\n"
            "¿Cómo podemos continuar?"
        )
        
        # --- CAMBIO CLAVE AQUÍ ---
        # Añadimos el mensaje de confirmación a la clave "messages" para que se envíe al cliente.
        return {
            "project_title": project_info.title,
            "project_description": project_info.description,
            "messages": [AIMessage(content=confirmation_text)]
        }
        # --- FIN DEL CAMBIO ---
    except Exception as e:
        print(f"--- Error en el Nodo de Ingesta: {e} ---")
        error_message = AIMessage(
            content="No pude procesar la descripción de tu proyecto. Por favor, sé más detallado y describe claramente los objetivos. "
                    "Por ejemplo: 'Quiero crear un informe sobre el impacto de la IA en la agricultura...'"
        )
        return {"messages": [error_message]}