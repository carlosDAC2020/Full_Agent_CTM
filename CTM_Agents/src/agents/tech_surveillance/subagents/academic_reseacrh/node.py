import os
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.tech_surveillance.state import GraphState
from langchain_core.messages import AIMessage, HumanMessage
from .tools import research_tools
from .prompts import RESEARCH_PROMPT_TEMPLATE

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
    """Nodo que invoca el agente de investigación académica"""
    
    project_title = state.get("project_title", "Unknown topic")
    project_desc = state.get("project_description", "")

    # Format the prompt template with project data
    system_content = RESEARCH_PROMPT_TEMPLATE.format(
        project_title=project_title,
        project_desc=project_desc
    )
    
    # Pass everything in ONE message - this becomes the system instruction
    initial_message = HumanMessage(
        content=system_content
    )
    
    result = await academic_research_agent.ainvoke({
        "messages": [initial_message]
    })

    # Extract final response
    messages = result.get("messages", [])
    
    final_report = ""
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            final_report = message.content
            break
    
    final_report_str = ""
    for i, chunk in enumerate(final_report):
        if type(chunk) == dict:
            final_report_str += chunk.get("text","")
        
        if i == len(final_report)-1:
            final_report_str+= chunk

    return {
        "messages": [AIMessage(content="Reporte de investigación académica generado")],  
        "academic_research_results": final_report_str
    }