import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

from .tools import research_tools
from .prompts import RESEARCH_PROMPT_TEMPLATE
from backend.agent.tech_surveillance.state import GraphState, ReportSchema, TheoreticalFramework

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
    
    current_report = state.get("report_components") or ReportSchema()
    general_info = current_report.general_info
    
    # Validación defensiva
    if not general_info:
        project_title = "Unknown Topic"
        project_desc = ""
        keywords = []
    else:
        project_title = general_info.project_title or "Unknown topic"
        project_desc = general_info.project_description or ""
        keywords = general_info.keywords or []

    system_content = RESEARCH_PROMPT_TEMPLATE.format(
        project_title=project_title,
        project_desc=project_desc,
        keywords=', '.join(keywords)
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


