import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

from backend.agent.tech_surveillance.tools import academic_research
from .prompts import RESEARCH_PROMPT_TEMPLATE
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, TheoreticalFramework

# Lista de herramientas
research_tools = [
    academic_research.search_arxiv,
    academic_research.search_pubmed,
    academic_research.academic_search,
    academic_research.search_semantic_scholar 
]

# Initialize model 
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

# Apply structured output BEFORE passing to create_agent
model_with_structure = model.with_structured_output(TheoreticalFramework)

# Create agent with the structured model
academic_research_agent = create_agent(
    model=model,  
    tools=research_tools,
)

async def academic_research_node(state: GraphState):
    """Much simpler node—structured output handles formatting."""
    print("--- Ejecutando Nodo: Investigación Académica ---")
    
    # --- REHIDRATACIÓN DEFENSIVA ---
    current_report = state.get("report_components") or ReportSchema()
    if isinstance(current_report, dict):
        try:
            current_report = ReportSchema(**current_report)
        except Exception as e:
            print(f"⚠️ Error rehidratando ReportSchema: {e}")
            current_report = ReportSchema()

    general_info = current_report.general_info
    
    # --- LÓGICA DE FALLBACK ROBUSTA ---
    # Intentamos obtener la información del reporte, si no, de la idea seleccionada, si no, de la convocatoria
    project_title = "Unknown Topic"
    project_desc = ""
    keywords = []

    if general_info and (general_info.project_title or general_info.project_description):
        print("✅ Usando información de general_info (ReportSchema)")
        project_title = general_info.project_title or "Unknown Topic"
        project_desc = general_info.project_description or ""
        keywords = general_info.keywords or []
    else:
        # Fallback 1: selected_idea
        selected_idea = state.get("selected_idea")
        if selected_idea:
            print("🔍 Fallback 1: Usando información de selected_idea")
            project_title = selected_idea.idea_title or "Unknown Topic"
            project_desc = selected_idea.idea_description or ""
            # Si es un objeto Pydantic o dict
            if hasattr(selected_idea, "idea_objectives"):
                 # añadir objetivos a la descripción para más contexto
                 project_desc += "\n\nObjetivos:\n" + "\n".join(selected_idea.idea_objectives or [])
        else:
            # Fallback 2: call_info
            call_info = state.get("call_info")
            if call_info:
                print("🔍 Fallback 2: Usando información de call_info")
                project_title = getattr(call_info, "title", "Unknown Topic")
                project_desc = getattr(call_info, "objective", "")
                keywords = getattr(call_info, "keywords", [])

    print(f"DEBUG: Título proyecto para investigación: {project_title}")

    system_content = RESEARCH_PROMPT_TEMPLATE.format(
        project_title=project_title,
        project_desc=project_desc,
        keywords=', '.join(keywords) if isinstance(keywords, list) else keywords
    )
    
    try:
        # Invoke agent
        result = await academic_research_agent.ainvoke(
            {"messages": [HumanMessage(content=system_content)]}
        )
        print(f"Full Agent Result: \n {result}")
        # Extrae el último mensaje (la respuesta del agente)
        last_message = result["messages"][-1]
        print(f"Last Message Content: \n {last_message}")

        text_response = f" {last_message.content[0]['text']} {last_message.content[-1]}"
        
        print(f"Raw Agent Response: \n {text_response}")
        # Invoca el modelo estructurado solo con la respuesta final
        theoretical_framework = await model_with_structure.ainvoke(
            [HumanMessage(content=text_response)]
        )
        
        print(f"Type: {type(theoretical_framework)}")  # TheoreticalFramework
        print(f"Body: {theoretical_framework.body}")
        print(f"References: {theoretical_framework.references_apa}")
        
        updated_report = current_report.model_copy(
            update={"theoretical_framework": theoretical_framework}
        )
        
        return { 
            "messages": [AIMessage(content="He completado la investigación académica...")],
            "report_components": updated_report,
        }
    except Exception as e:
        message_error = f"Error during academic research node execution: {str(e)}"
        return{
            "messages": [AIMessage(content=message_error)],
        }


