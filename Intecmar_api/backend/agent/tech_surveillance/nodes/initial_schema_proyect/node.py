
import os
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.agent.tech_surveillance.state import GraphState, ProposalIdea, GeneralInfo, ReportSchema

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
    selected_idea = state.get("selected_idea")
    
    # Validaciones de seguridad y rehidratación de emergencia
    if not selected_idea:
        print("⚠️ [NODE] Error: selected_idea no encontrado en el estado.")
        return {
            "messages": [AIMessage(content="⚠️ Error: No hay una idea seleccionada para generar el esquema.")]
        }

    # Si es un objeto, intentamos obtener atributos. Si es un dict, usamos get.
    if isinstance(selected_idea, dict):
        idea_title = selected_idea.get("idea_title") or selected_idea.get("title")
        idea_description = selected_idea.get("idea_description") or selected_idea.get("desc")
        idea_objectives = selected_idea.get("idea_objectives") or selected_idea.get("objectives") or []
    else:
        idea_title = getattr(selected_idea, "idea_title", None) or getattr(selected_idea, "title", None)
        idea_description = getattr(selected_idea, "idea_description", None) or getattr(selected_idea, "desc", None)
        idea_objectives = getattr(selected_idea, "idea_objectives", []) or getattr(selected_idea, "objectives", []) or []

    # Final Fallback: Si sigue vacío, buscar en report_components (que acabamos de reforzar en tasks.py)
    if not idea_title or idea_title == "Título no definido":
        rc = state.get("report_components")
        if rc and hasattr(rc, "general_info") and rc.general_info:
            idea_title = rc.general_info.project_title or idea_title
            idea_description = rc.general_info.project_description or idea_description

    if not idea_title: idea_title = "Título no definido"
    if not idea_description: idea_description = "Descripción no disponible"

    print(f"📌 [NODE] Procesando Idea: {idea_title}")
    
    # Convertimos la lista de objetivos a un string con viñetas
    idea_objectives_str = "\n".join([f"- {obj}" for obj in idea_objectives])


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
Extract the general information of the project from the following conceptual schema.
The project MUST be titled and focused on the user's selected idea: "{idea_title}".

Conceptual Schema:
{schema_content}

Strictly retrieve the following fields based on the schema and the project's identity:
- Title (should match or be a refined version of "{idea_title}")
- Description
- Duration
- Keywords
- Main Entity
- Collaborating Entities
"""
            )
        # Fix: Ensure input is a list of messages
        general_info : GeneralInfo = ll_estructured.invoke([message_by_get_general_info])

        # --- LÓGICA DE ENRIQUECIMIENTO HÍBRIDO ---
        # 1. Conservamos la identidad exacta de la idea seleccionada (Manual)
        general_info.project_title = idea_title
        general_info.project_description = idea_description
        
        # 2. El resto de campos (keywords, duration, entities, etc.) vienen enriquecidos por el LLM 
        # desde el esquema generado.
        print(f"✅ GeneralInfo enriquecido. Título forzado: {general_info.project_title}")
        print(f"   Keywords detectadas: {general_info.keywords}")
            
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
            "report_components": report_components,
            "selected_idea": selected_idea  # ← CRÍTICO: Preservar para pasos posteriores
        }
    
    except Exception as e:
        print(f"Error invocando al LLM en initial_schema_node: {e}")
        return {
            "messages": [AIMessage(content="Error generando el esquema conceptual inicial.")]
        }