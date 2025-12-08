
import os
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.tech_surveillance.state import GraphState, ProposalIdea, GeneralInfo, ReportSchema

# Asegúrate de importar el nuevo prompt
from .prompts import INITIAL_SCHEMA_PROMPTS 

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.8, 
)

ll_estructured = llm.with_structured_output(GeneralInfo)

def initial_schema_node(state: GraphState):
    print("📝 GENERANDO ESQUEMA CONCEPTUAL INICIAL BASADO EN LA IDEA SELECCIONADA...")

    # 1. Extracción de datos del estado
    call_info_summary = state.get("presentation_summary", "Información de convocatoria no disponible.")
    selected_idea: ProposalIdea = state.get("selected_idea")
    
    # Validaciones de seguridad
    if not selected_idea:
        return {
            "messages": [AIMessage(content="⚠️ Error: No hay una idea seleccionada para generar el esquema.")]
        }

    # Datos de la idea
    idea_title = selected_idea.idea_title or "Título no definido"
    idea_description = selected_idea.idea_description or "Descripción no disponible"
    # Convertimos la lista de objetivos a un string con viñetas
    idea_objectives_str = "\n".join([f"- {obj}" for obj in (selected_idea.idea_objectives or [])])

    # 2. Formatear el prompt
    formatted_prompt = INITIAL_SCHEMA_PROMPTS.format(
        call_info=call_info_summary,
        idea_title=idea_title,
        idea_description=idea_description,
        idea_objectives=idea_objectives_str
    )

    # 3. Invocar al LLM
    try:
        # obtenemos el esquema inicial del proyecto 
        response = llm.invoke(formatted_prompt)
        schema_content = response.content

        # segun el esquema obtenido sacamos la informacion general del proyetco 
        message_by_get_general_info = HumanMessage(
            content=f"""
Extract the general information of the project from the following conceptual schema:\n\n
            {schema_content}"""
            )
        # Fix: Ensure input is a list of messages
        general_info : GeneralInfo = ll_estructured.invoke([message_by_get_general_info])

        # actualizamos en el estado 
        current_components = state.get("report_components")
        
        if current_components is None:
            # Si no existe, creamos una nueva instancia de la clase Pydantic
            report_components = ReportSchema()
        elif isinstance(current_components, dict):
            # Si es un dict, lo convertimos a la clase Pydantic
            report_components = ReportSchema(**current_components)
        else:
            # Si ya es objeto, lo usamos tal cual
            report_components = current_components
            
        # Ahora sí podemos usar notación de punto con seguridad
        report_components.general_info = general_info
        # -----------------------------

        # 4. Retornar actualización del estado
        return {
            "messages": [AIMessage(content=f"✅ Esquema conceptual generado para: {idea_title}")],
            "initial_schema": schema_content,
            "report_components": report_components
        }
    
    except Exception as e:
        print(f"Error invocando al LLM en initial_schema_node: {e}")
        return {
            "messages": [AIMessage(content="Error generando el esquema conceptual inicial.")]
        }