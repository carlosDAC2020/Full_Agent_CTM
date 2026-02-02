
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
    
    print(f"🔍 DEBUG RAW selected_idea (node): {selected_idea}")

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
- Duration (in months, as a number)
- Thematic Line (Línea Temática)
- Keywords (List)
- Main Entity (Ejecutor)
- Collaborating Entities (List of names)
"""
            )
        # Fix: Ensure input is a list of messages
        general_info : GeneralInfo = ll_estructured.invoke([message_by_get_general_info])

        # --- LÓGICA DE ENRIQUECIMIENTO HÍBRIDO ---
        # 1. Conservamos la identidad exacta de la idea seleccionada (Manual)
        general_info.project_title = idea_title
        general_info.project_description = idea_description
        
        # --- NUEVO: Propagar Alianzas y Duración desde selected_idea (Híbrido) ---
        def get_val(obj, key):
            if isinstance(obj, dict): return obj.get(key)
            return getattr(obj, key, None)

        print(f"🛠️ [ENRICHMENT] Checking selected_idea for alliances...")
        
        # Duración
        s_dur = get_val(selected_idea, "duration_time") or get_val(selected_idea, "suggested_duration_months")
        if s_dur: general_info.duration_months = int(s_dur) if str(s_dur).isdigit() else general_info.duration_months

        # Ejecutor
        s_exec = get_val(selected_idea, "executor_entity")
        if s_exec: general_info.executor_entity = s_exec
        s_exec_logo = get_val(selected_idea, "executor_entity_logo")
        if s_exec_logo: general_info.executor_entity_logo = s_exec_logo

        # Coejecutores
        s_co_ent = get_val(selected_idea, "coejecutors_entities")
        if s_co_ent: general_info.coejecutors_entities = s_co_ent
        s_co_log = get_val(selected_idea, "coejecutors_entities_logos")
        if s_co_log: general_info.coejecutors_entities_logos = s_co_log

        # Colaboradores
        s_col_ent = get_val(selected_idea, "collaborators_entities")
        if s_col_ent: general_info.collaborators_entities = s_col_ent
        s_col_log = get_val(selected_idea, "collaborators_entities_logos")
        if s_col_log: general_info.collaborators_entities_logos = s_col_log

        print(f"📊 [ENRICHMENT] Result: Exec='{general_info.executor_entity}', Co-Execs={len(general_info.coejecutors_entities or [])}")
        # -------------------------------------------------------------------------

        # 2. El resto de campos (keywords, etc.) vienen enriquecidos por el LLM 
        # desde el esquema generado, a menos que ya los tengamos.
        
        print(f"✅ GeneralInfo enriquecido. Título forzado: {general_info.project_title}")
        print(f"   Alianzas Ejecutor: {general_info.executor_entity}")

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