from __future__ import annotations

import os
from langgraph.graph import END, StateGraph
from agents.tech_surveillance.state import GraphState, ReportSchema
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from google import genai
from google.genai import types

from .prompts import template_image_prompt

# Cliente de Google Genai para generación de imágenes
genai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Modelo base para chat general
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.7,
    convert_system_message_to_human=True 
)

def prompt_generator_image_node(state: GraphState):
    """
    Genera un prompt optimizado para la creación de imágenes basándose
    en el título y descripción del proyecto.
    """
    # --- LEER DESDE report_components ---
    report_components = state.get("report_components") or ReportSchema()
    
    # Safe access using Pydantic models
    project_title = "proyecto tecnológico"
    project_description = "un proyecto innovador"
    
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "proyecto tecnológico"
        project_description = report_components.general_info.project_description or "un proyecto innovador"
    
    # Template para generar el prompt de imagen
    prompt_template = PromptTemplate(
        input_variables=["title", "description"],
        template=template_image_prompt
    )
    
    # Generar el prompt usando el modelo de chat
    chain = prompt_template | chat_model
    
    try:
        result = chain.invoke({
            "title": project_title,
            "description": project_description
        })
        
        generated_prompt = result.content
        
        message = AIMessage(
            content=f"✓ Prompt para generación de imágenes creado:\n\n{generated_prompt}"
        )
        
        return {
                "messages": [message],
                "image_prompt": generated_prompt 
            }
    
    except Exception as e:
        error_message = AIMessage(
            content=f"✗ Error al generar el prompt: {str(e)}"
        )
        return {
            "messages": [error_message],
            "image_prompt": None
        }


def generator_image_node(state: GraphState):
    """
    Genera una imagen usando la API de Google Generative AI y la guarda
    en una carpeta específica.
    """
    image_prompt = state.get("image_prompt")
    
    report_components = state.get("report_components") or ReportSchema()
    
    project_title = "proyecto_tecnologico"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "proyecto_tecnologico"
    
    if not image_prompt:
        error_message = AIMessage(
            content="✗ No se encontró un prompt válido para generar la imagen"
        )
        return {"messages": [error_message]}

    # 2. DEFINIR LA CARPETA DE DESTINO
    output_dir = "generated_images"
    
    try:
        # 3. ASEGURARSE DE QUE LA CARPETA EXISTA
        os.makedirs(output_dir, exist_ok=True)
        
        response = genai_client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[image_prompt],
        )
        
        image_path = None
        
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                
                # Crear un nombre de archivo más seguro
                sanitized_title = project_title.replace(" ", "_").lower()
                image_filename = f"{sanitized_title}.png"
                
                # 4. CONSTRUIR LA RUTA COMPLETA (carpeta + nombre de archivo)
                full_image_path = os.path.join(output_dir, image_filename)
                
                # Guardar la imagen en la ruta completa
                image.save(full_image_path)
                image_path = full_image_path
                
                break
        
        if image_path:
            success_message = AIMessage(
                content=f"✓ Imagen del proyecto generada exitosamente y guardada en: {image_path}\n\n"
                        f"La imagen representa visualmente el proyecto basándose en su título y descripción."
            )
            
            return {
                "messages": [success_message],
                "generated_image_path": image_path,
            }
        else:
            warning_message = AIMessage(
                content="⚠ La API respondió pero no se pudo extraer la imagen generada"
            )
            return {"messages": [warning_message]}
    
    except Exception as e:
        error_message = AIMessage(
            content=f"✗ Error al generar la imagen: {str(e)}\n\n"
                    f"Verifica que la API key de Google esté configurada correctamente."
        )
        return {"messages": [error_message]}


# Construcción del grafo
workflow = StateGraph(GraphState)

workflow.add_node("generate_prompt", prompt_generator_image_node)
workflow.add_node("generate_image", generator_image_node)

workflow.set_entry_point("generate_prompt")
workflow.add_edge("generate_prompt", "generate_image")
workflow.add_edge("generate_image", END)

Image_generator_subgraph = workflow.compile()