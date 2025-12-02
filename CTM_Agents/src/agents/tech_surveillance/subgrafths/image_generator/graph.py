from __future__ import annotations

import os
from langgraph.graph import END, StateGraph

from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

from agents.tech_surveillance.state import GraphState, ReportSchema, DocsPaths
from .prompts import template_image_prompt

# Cliente de Google Genai para generación de imágenes
genai_client = genai.Client(api_key=os.environ.get("NANO_BANANA_API_KEY"))

# Modelo base para chat general
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=2.0,
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
    Genera un póster vertical usando Gemini 2.5 Flash (capacidad nativa de imagen).
    """
    image_prompt = state.get("image_prompt")
    report_components = state.get("report_components") or ReportSchema()
    
    # Nombre del proyecto para el archivo
    project_title = "proyecto_tecnologico"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "proyecto_tecnologico"
    
    if not image_prompt:
        return {"messages": [AIMessage(content="✗ No hay prompt para generar imagen.")]}

    # 1. Definir carpeta
    output_dir = "generated_images"
    os.makedirs(output_dir, exist_ok=True)

    # ruta del logo a insertar 
    logo_path = os.path.join("static", "CotecmarLogo_white.png")
    
    try:
        # 2. LLAMADA A LA API 
        response = genai_client.models.generate_content(
            model="gemini-3-pro-image-preview", 
            contents=[image_prompt],
            config=types.GenerateContentConfig(
                response_modalities=["Image"], 
                image_config=types.ImageConfig(
                    aspect_ratio="3:4" 
                )
            )
        )

        image_path = None

        # 3. Procesar la respuesta
        for part in response.parts:
            if part.inline_data:
                # A. Cargar imagen generada desde memoria
                image_bytes = part.inline_data.data
                img = Image.open(BytesIO(image_bytes)).convert("RGBA") # Convertir a RGBA para manejar transparencias
                
                # B. Lógica de Integración del Logo
                if os.path.exists(logo_path):
                    try:
                        logo = Image.open(logo_path).convert("RGBA")
                        
                        # --- 1. Redimensionar Logo ---
                        # El logo ocupará el 25% del ancho total del póster (aprox 216px en un ancho de 864px)
                        logo_width_ratio = 0.25 
                        target_width = int(img.width * logo_width_ratio)
                        
                        # Calcular altura manteniendo proporción (aspect ratio del logo)
                        w_percent = (target_width / float(logo.size[0]))
                        h_size = int((float(logo.size[1]) * float(w_percent)))
                        
                        logo = logo.resize((target_width, h_size), Image.Resampling.LANCZOS)
                        
                        # --- 2. Calcular Posición (Inferior Izquierda) ---
                        # Margen del 5% del ancho de la imagen (aprox 43px)
                        margin = int(img.width * 0.05)
                        
                        # Coordenada X (Izquierda): Solo el margen
                        pos_x = margin
                        
                        # Coordenada Y (Abajo): Altura total - Altura logo - Margen
                        pos_y = img.height - logo.height - margin
                        
                        # --- 3. Pegar el Logo ---
                        # El tercer parámetro 'logo' sirve como máscara para usar la transparencia del PNG
                        img.paste(logo, (pos_x, pos_y), logo)
                        
                        print(f"Logo integrado en ({pos_x}, {pos_y}) con tamaño {target_width}x{h_size}")
                        
                    except Exception as e:
                        print(f"Error al procesar el logo: {e}")
                else:
                    print(f"Advertencia: No se encontró el logo en {logo_path}")

                # C. Guardar Imagen Final
                # Convertimos a RGB antes de guardar (por si se guarda en JPG, aunque PNG soporta RGBA)
                # Si quieres mantener transparencia del fondo generado (raro en pósters), quita la conversión.
                img = img.convert("RGB") 
                
                sanitized_title = "".join(x for x in project_title if x.isalnum() or x in " _-").replace(" ", "_").lower()
                image_filename = f"{sanitized_title}_poster.png"
                full_image_path = os.path.join(output_dir, image_filename)
                
                img.save(full_image_path)
                image_path = full_image_path
                break 
        
        if image_path:
            logo_msg = " (con logo Cotecmar)" if os.path.exists(logo_path) else " (sin logo)"

            # Actualizando rutas de documentos en el estado
            docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
            docs_paths.poster_image_path = image_path
            return {
                "messages": [AIMessage(content=f"✓ Póster generado{logo_msg}: {image_path}")],
                "generated_image_path": image_path,
                "docs_paths": docs_paths
            }
        else:
            return {"messages": [AIMessage(content="⚠ La API respondió pero no se encontró imagen.")]}
            
    except Exception as e:
        return {
            "messages": [AIMessage(content=f"✗ Error generando imagen: {str(e)}")]
        }

# Construcción del grafo
workflow = StateGraph(GraphState)

workflow.add_node("generate_prompt", prompt_generator_image_node)
workflow.add_node("generate_image", generator_image_node)

workflow.set_entry_point("generate_prompt")
workflow.add_edge("generate_prompt", "generate_image")
workflow.add_edge("generate_image", END)

Image_generator_subgraph = workflow.compile()