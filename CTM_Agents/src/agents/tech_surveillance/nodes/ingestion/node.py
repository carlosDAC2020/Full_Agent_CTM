import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from .squemas import IngestionResult
from .prompts import template

# Importamos los nuevos esquemas del estado
from agents.tech_surveillance.state import GraphState, ReportSchema, GeneralInfo, CallInfo

# ... (definición de chat_model y extraction_llm sin cambios) ...
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True
)
extraction_llm = chat_model.with_structured_output(IngestionResult)


def ingestion_node(state: GraphState) -> dict:
    """
    Se activa cuando se detecta un nuevo proyecto o convocatoria. 
    Extrae la información, detecta si es convocatoria y estructura el estado.
    """
    print("--- Ejecutando Nodo: Ingesta de Proyecto/Convocatoria ---")
    last_message = state["messages"][-1].content
    
    prompt_template = PromptTemplate.from_template(template, partial_variables={"last_message": last_message})
    prompt = prompt_template.format()
    
    try:
        # 1. Llama al LLM para extraer la información (Call + Project)
        ingestion_result: IngestionResult = extraction_llm.invoke(prompt)
        
        project_info = ingestion_result.project_info
        call_info_data = ingestion_result.call_info
        
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
        
        # 4. Prepara el mensaje de confirmación
        confirmation_text = ""
        
        if call_info_data:
            confirmation_text += f"✅ **Convocatoria Detectada:** {call_info_data.title}\n"
            if call_info_data.url:
                confirmation_text += f"🔗 **URL:** {call_info_data.url}\n"
            confirmation_text += "\n"
            
        if ingestion_result.is_generated_project:
            confirmation_text += (
                f"✨ **Proyecto Generado:** Como no proporcionaste una descripción específica, he diseñado un proyecto alineado con la convocatoria:\n\n"
                f"📌 **Título:** {project_info.title}\n"
                f"📝 **Descripción:** {project_info.description}\n\n"
            )
        else:
            confirmation_text += (
                f"📋 **Proyecto Registrado:**\n\n"
                f"**Título:** {project_info.title}\n"
                f"**Descripción:** {project_info.description}\n\n"
            )
            
        confirmation_text += f"🏷️ **Palabras Clave:** {', '.join(project_info.keywords)}\n\n"
        confirmation_text += "Ahora, procederé a realizar una investigación académica y a planificar el proyecto."

        # 5. Devuelve la nueva estructura del estado
        return {
            "report_components": report_components_schema,
            "call_info": call_info_data, # Guardamos la info de la convocatoria en el estado
            "messages": [AIMessage(content=confirmation_text)]
        }

    except Exception as e:
        print(f"--- Error en el Nodo de Ingesta: {e} ---")
        error_message = AIMessage(
            content="Hubo un problema procesando tu solicitud. Por favor, intenta nuevamente con más detalles sobre la convocatoria o tu proyecto."
        )
        return {"messages": [error_message]}