import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

from .tools import research_tools
from .prompts import RESEARCH_PROMPT_TEMPLATE
from agents.tech_surveillance.state import GraphState, ReportSchema, TheoreticalFramework

# Initialize model globally
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

academic_research_agent = create_agent(
    model=model,
    tools=research_tools
)



async def academic_research_node(state: GraphState):
    """
    Invoca al agente de investigación académica, procesa su salida,
    y actualiza el estado con el marco teórico y las referencias por separado.
    """
    print("--- Ejecutando Nodo: Investigación Académica ---")
    
    # 1. Acceder a la información del proyecto desde la nueva estructura del estado
    report_components = state.get("report_components", {})
    general_info = report_components.get("general_info", {})
    
    project_title = general_info.get("project_title", "Unknown topic")
    project_desc = general_info.get("project_description", "")
    keywords = general_info.get("keywords", [])

    # 2. Formatear el prompt mejorado
    system_content = RESEARCH_PROMPT_TEMPLATE.format(
        project_title=project_title,
        project_desc=project_desc,
        keywords=', '.join(keywords) # Unimos las keywords en un string
    )
    
    initial_message = HumanMessage(content=system_content)
    
    # 3. Invocar al agente
    result = await academic_research_agent.ainvoke({"messages": [initial_message]})

    # 4. Extraer la respuesta final 
    final_report_content = ""
    
    # Extract final response
    messages = result.get("messages", [])
    
    final_report = ""
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            final_report = message.content
            break
    
    for i, chunk in enumerate(final_report):
        if type(chunk) == dict:
            final_report_content += chunk.get("text","")
        
        if i == len(final_report)-1:
            final_report_content+= chunk

    # 5. Separar el cuerpo de las referencias
    report_body, report_references = separate_body_and_references(final_report_content)
    
    # 6. Construir el objeto TheoreticalFramework y actualizar el estado
    theoretical_framework_schema = TheoreticalFramework(
        body=report_body,
        references_apa=report_references
    )
    
    # Actualización segura del estado
    current_report_schema = state.get("report_components", ReportSchema())
    current_report_schema['theoretical_framework'] = theoretical_framework_schema
    
    print("--- Marco Teórico y Referencias generados y guardados en el estado. ---")

    return {
        "messages": [AIMessage(content="He completado la investigación académica y he generado el Marco Teórico.")],  
        "report_components": current_report_schema
    }


def separate_body_and_references(full_report: str) -> tuple[str, str]:
    """
    Separa el contenido principal del reporte de la sección de referencias bibliográficas.
    Busca la sección que comienza con '### 9. Referencias Bibliográficas'.
    """
    separator = "### 9. Referencias Bibliográficas"
    parts = full_report.split(separator)
    
    if len(parts) > 1:
        body = parts[0].strip()
        # Tomamos todo lo que sigue al separador como las referencias
        references = separator + parts[1]
        return body.strip(), references.strip()
    else:
        # Si no encuentra el separador, devuelve todo como cuerpo y las referencias vacías
        return full_report.strip(), "No se encontraron referencias en el formato esperado."