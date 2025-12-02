import os
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.tech_surveillance.state import GraphState, ReportSchema

from .prompts import INITIAL_SCHEMA_PROMPTS 

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=1.7,
)

def initial_schema_node(state: GraphState):
    print("📝 GENERANDO ESQUEMA CONCEPTUAL INICIAL...")

    # 1. Extracción segura de datos del estado
    # Obtenemos el resumen de la convocatoria
    report_call = state.get("presentation_summary", "Información de convocatoria no disponible.")
    
    # Obtenemos los componentes del reporte (Estructura Pydantic)
    report_components = state.get("report_components")
    
    # Inicializamos valores por defecto
    project_title = "Título no definido"
    project_description = "Descripción no definida"
    framework_body = "Marco teórico no disponible"

    # Verificamos y extraemos datos si existen
    if report_components:
        if report_components.general_info:
            project_title = report_components.general_info.project_title or project_title
            project_description = report_components.general_info.project_description or project_description
        
        if report_components.theoretical_framework:
            framework_body = report_components.theoretical_framework.body or framework_body

    # 2. Formatear el prompt
    # NOTA: Las claves dentro del .format() deben coincidir con las del string INITIAL_SCHEMA_PROMPTS
    formatted_prompt = INITIAL_SCHEMA_PROMPTS.format(
        call_info=report_call,
        theoretical_framework=framework_body,
        project_title=project_title,
        project_description=project_description
    )

    # 3. Invocar al LLM
    try:
        response = llm.invoke(formatted_prompt)
        schema_content = response.content
    except Exception as e:
        print(f"Error invocando al LLM: {e}")
        schema_content = "Error al generar el esquema. Por favor revise los inputs."

    # 4. Retornar actualización del estado
    # Guardamos el resultado en 'initial_schema' y añadimos un mensaje al historial
    return {
        "messages": [AIMessage(content="Esquema conceptual inicial generado exitosamente.")],
        "initial_schema": schema_content
    }