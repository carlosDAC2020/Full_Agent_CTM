
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from .squemas import ProjectInfo
from .prompts import template

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, GeneralInfo

# ... (definición de chat_model y extraction_llm sin cambios) ...
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True
)
extraction_llm = chat_model.with_structured_output(ProjectInfo)


def ingestion_node(state: GraphState) -> dict:
    """
    Se activa cuando se detecta un nuevo proyecto. Extrae la información inicial
    y estructura el objeto 'report_components' en el estado.
    """
    print("--- Ejecutando Nodo: Ingesta de Proyecto ---")
    last_message = state["messages"][-1].content
    
    prompt_template = PromptTemplate.from_template(template, partial_variables={"last_message": last_message})
    prompt = prompt_template.format()
    
    try:
        # 1. Llama al LLM para extraer la información
        project_info: ProjectInfo = extraction_llm.invoke(prompt)
        # 2. Construye la sección 'GeneralInfo' para nuestro nuevo estado
        general_info = GeneralInfo(
            project_title=project_info.title,
            project_description=project_info.description,
            keywords=project_info.keywords,
            duration_months=18, 
            main_entity="Nombre Entidad Ejemplo" # Ejemplo
        )

        # 3. Inicializa el esquema principal del reporte
        report_components_schema = ReportSchema(
            general_info=general_info
        )

        # 4. Crea el mensaje de confirmación para el usuario
        confirmation_text = (
            f"Proyecto registrado con éxito. He entendido lo siguiente:\n\n"
            f"**Título:** {project_info.title}\n\n"
            f"**Descripción:** {project_info.description}\n\n"
            f"**Palabras Clave:** {', '.join(project_info.keywords)}\n\n"
            f"Ahora, procederé a realizar una investigación académica y a planificar el proyecto."
        )
        
        # 5. Devuelve la nueva estructura del estado
        return {
            "report_components": report_components_schema,
            "messages": [AIMessage(content=confirmation_text)]
        }

    except Exception as e:
        print(f"--- Error en el Nodo de Ingesta: {e} ---")
        error_message = AIMessage(
            content="No pude procesar la descripción de tu proyecto. Por favor, sé más detallado y describe claramente los objetivos. "
                    "Por ejemplo: 'Quiero crear un informe sobre el impacto de la IA en la agricultura...'"
        )
        return {"messages": [error_message]}