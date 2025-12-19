import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage

# Importamos los esquemas y el estado
from backend.agent.tech_surveillance.state import GraphState, proposalIdeaResponse

from .prompts import propose_ideas_template

# Configuración del modelo (igual que tenías)
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.2, # Un poco de temperatura ayuda a la creatividad de las ideas
    convert_system_message_to_human=True
)

# Configuramos la salida estructurada
extraction_llm = chat_model.with_structured_output(proposalIdeaResponse)

def propose_ides_node(state: GraphState) -> dict:
    """
    Propone 5 ideas de proyecto iniciales basadas en la convocatoria detectada.
    """
    print("--- Ejecutando Nodo: Generación de Ideas de Proyecto ---")

    # 1. Obtener info de la convocatoria del estado
    call_info = state.get("call_info")
    
    # Validación de seguridad
    if not call_info:
        return {
            "messages": [AIMessage(content="⚠️ Error: No se encontró información de la convocatoria para generar ideas.")]
        }

    # 2. Extraer datos para el prompt (manejo de nulos seguro)
    data_for_prompt = {
        "title": call_info.title or "N/A",
        "objective": call_info.objective or "N/A",
        "funding": call_info.funding or "N/A",
        "keywords": ", ".join(call_info.keywords) if call_info.keywords else "N/A",
        "important_dates": call_info.important_dates or "N/A",
        "benefits": ", ".join(call_info.benefits) if call_info.benefits else "N/A"
    }

    # 3. Preparar el Prompt
    # (Asegúrate de importar 'propose_ideas_template' donde lo hayas definido)
    prompt_template = PromptTemplate(
        template=propose_ideas_template, 
        input_variables=["title", "objective", "funding", "keywords", "important_dates", "benefits"]
    )
    
    formatted_prompt = prompt_template.format(**data_for_prompt)

    try:
        # 4. Invocar al LLM
        # Al usar with_structured_output, 'response' ya será un objeto 'proposalIdeaResponse'
        response: proposalIdeaResponse = extraction_llm.invoke(formatted_prompt)
        
        # 5. Generar mensaje de feedback para el chat
        summary_msg = f"✅ He generado **{len(response.ideas)} ideas de proyecto** basadas en la convocatoria '{data_for_prompt['title']}'.\n\n"
        for i, idea in enumerate(response.ideas, 1):
            summary_msg += f"**{i}. {idea.idea_title}**\n"
        
        summary_msg += "\n¿Te interesa desarrollar alguna de estas en profundidad?"

        # 6. Retornar actualización del estado
        # NOTA: La clave en GraphState es 'proposal_ideas', no 'proposal_idea_response'
        return {
            "proposal_ideas": response,
            "messages": [AIMessage(content=summary_msg)]
        }

    except Exception as e:
        print(f"--- Error generando ideas: {e} ---")
        return {
            "messages": [AIMessage(content="Lo siento, hubo un error al intentar generar las ideas de proyecto.")]
        }