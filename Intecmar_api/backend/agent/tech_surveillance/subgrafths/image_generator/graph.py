from __future__ import annotations

import os
from langgraph.graph import END, StateGraph

from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from google import genai
from google.genai import types
from PIL import Image, ImageDraw
from io import BytesIO
from datetime import datetime

from backend.agent.tech_surveillance.state import GraphState, ReportSchema, DocsPaths
from .prompts import template_image_prompt

from backend.app.services.core.storage import storage_service

# Cliente de Google Genai para generación de imágenes
genai_client = genai.Client(api_key=os.environ.get("NANO_BANANA_API_KEY"))

print("\n🚀 [VERSION 1.2] GRAPH.PY LOADED - TIMESTAMP LOGIC ENABLED\n")

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
    print(" 🎨 Generando prompt para la portada del proyecto")
    # --- LEER DESDE report_components ---
    report_components = state.get("report_components") or ReportSchema()
    
    # Safe access using Pydantic models
    project_title = "proyecto tecnológico"
    project_description = "un proyecto innovador"
    
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "proyecto tecnológico"
        project_description = report_components.general_info.project_description or "un proyecto innovador"
    
    # --- REVISAR SOBREESCRITURA DE PROMPT ---
    gen_config = state.get("generation_config")
    if isinstance(gen_config, dict):
        try:
            from backend.agent.tech_surveillance.state import GenerationConfig
            gen_config = GenerationConfig(**gen_config)
        except:
            pass
            
    override_prompt = getattr(gen_config, "poster_prompt_override", None) if gen_config else None
    
    # --- COMPROBAR SI YA EXISTE PÓSTER ---
    docs_paths = state.get("docs_paths") or DocsPaths()
    if isinstance(docs_paths, dict):
        docs_paths = DocsPaths(**docs_paths)
    
    existing_poster = docs_paths.poster_image_path
    
    # --- LEER CONFIGURACIÓN DE REGENERACIÓN ---
    override_base = getattr(gen_config, "base_image_path", None) if gen_config else None
    
    # ===== CASE 1: HISTORIAL SELECCIONADO =====
    # Si el usuario eligió una imagen del historial, NO generamos prompt ni IA.
    # Solo señalamos al siguiente nodo que use esa base y aplique logos.
    if override_base:
        print(f"📂 [CASE 1] Usuario seleccionó imagen histórica: {override_base[-40:]}")
        return {
            "messages": [AIMessage(content="Usando imagen del historial seleccionada.")],
            "image_prompt": None,
            "use_historical_base": override_base  # Señal para generator_image_node
        }
    
    # ===== CASE 2: FEEDBACK / REFINAMIENTO =====
    # Si hay feedback del usuario, generamos un nuevo prompt refinado y luego IA.
    if override_prompt:
        print("🚀 [CASE 2] Refinando prompt de póster con feedback del usuario.")

        from .prompts import template_image_refinement_prompt
        
        prompt_template = PromptTemplate(
            input_variables=["title", "description", "user_feedback"],
            template=template_image_refinement_prompt
        )
        
        chain = prompt_template | chat_model
        
        try:
            result = chain.invoke({
                "title": project_title,
                "description": project_description,
                "user_feedback": override_prompt
            })
            
            generated_prompt = result.content
            message = AIMessage(
                content="✓ Prompt de póster refinado con tu feedback, manteniendo las directrices de diseño."
            )
            return {
                "messages": [message],
                "image_prompt": generated_prompt,
                "use_historical_base": None,  # CLEAR: Forzar generación con IA
                "use_current_base": None      # CLEAR: No reusar base anterior
            }
        except Exception as e:
            print(f"⚠️ Error refinando prompt: {e}")
            return {
                "messages": [AIMessage(content="⚠ Error en refinamiento, usando feedback directo.")],
                "image_prompt": override_prompt,
                "use_historical_base": None,
                "use_current_base": None
            }

    # ===== CASE 3: BASE ACTUAL (poster existe, sin feedback ni historial) =====
    # El usuario quiere regenerar otras secciones pero mantener la base visual.
    # Sin embargo, los logos pueden haber cambiado, así que señalamos re-aplicar logos.
    if existing_poster and gen_config:
        print("🔄 [CASE 3] Base actual seleccionada. Re-aplicando logos actuales.")
        # Necesitamos la ruta de la imagen BASE, no la FINAL (con logos).
        # La obtenemos del último item del historial.
        current_history = state.get("generation_history", []) or []
        base_to_use = None
        if current_history:
            last_item = current_history[-1]
            base_to_use = last_item.base_image_path if hasattr(last_item, 'base_image_path') else (
                last_item.get('base_image_path') if isinstance(last_item, dict) else None
            )
        
        if not base_to_use:
            # Fallback: si no hay base guardada, usamos el poster final existente
            base_to_use = existing_poster
            print(f"   ⚠️ No se encontró base en historial, usando póster final: {base_to_use[-40:]}")
        
        return {
            "messages": [AIMessage(content="Re-aplicando logos a la base actual.")],
            "image_prompt": None,
            "use_current_base": base_to_use  # Señal para generator_image_node
        }

    # ===== CASE 4: PRIMERA VEZ (no existe póster) =====
    # Generamos un prompt nuevo desde cero.
    print("🆕 [CASE 4] Primera generación de póster. Creando prompt nuevo.")
    
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


# --- HELPER FUNCTIONS FOR IMAGE PROCESSING ---

def remove_background(logo_img, threshold=30):
    """
    Elimina el fondo blanco/claro de un logo automáticamente.
    - Detecta el color de fondo muestreando las esquinas
    - Hace transparentes todos los píxeles similares al fondo
    """
    # Convertir a RGBA si no lo está
    if logo_img.mode != 'RGBA':
        logo_img = logo_img.convert('RGBA')
    
    # Obtener datos de píxeles
    data = logo_img.getdata()
    
    # Muestrear las 4 esquinas para detectar el color de fondo
    width, height = logo_img.size
    corners = [
        logo_img.getpixel((0, 0)),
        logo_img.getpixel((width-1, 0)),
        logo_img.getpixel((0, height-1)),
        logo_img.getpixel((width-1, height-1))
    ]
    
    # Calcular el color de fondo promedio (asumiendo que las esquinas son fondo)
    bg_r = sum(c[0] for c in corners) // 4
    bg_g = sum(c[1] for c in corners) // 4
    bg_b = sum(c[2] for c in corners) // 4
    
    # Si el fondo es muy claro (blanco/gris claro), eliminarlo
    if bg_r > 200 and bg_g > 200 and bg_b > 200:
        new_data = []
        for item in data:
            # Calcular diferencia de color con el fondo
            diff = abs(item[0] - bg_r) + abs(item[1] - bg_g) + abs(item[2] - bg_b)
            
            # Si es muy similar al fondo, hacerlo transparente
            if diff < threshold:
                new_data.append((item[0], item[1], item[2], 0))
            else:
                new_data.append(item)
        
        logo_img.putdata(new_data)
    
    return logo_img

def apply_logos_to_image(img: Image.Image, report_components: ReportSchema, logo_default_path: str):
    """
    Aplica los logos a la imagen base siguiendo la jerarquía y estilos definidos.
    """
    # Copiar imagen para no modificar la original si se pasa por referencia
    img_with_logos = img.copy()
    
    # Definir categorías con sus tamaños relativos (jerarquía)
    # EJECUTOR: 100%, CO-EJECUTORES: 80%, COLABORADORES: 65%
    categories = []
    
    # 1. Ejecutor (tamaño base = 1.0)
    if report_components.general_info and report_components.general_info.executor_entity_logo:
        categories.append({
            "role": "EJECUTOR",
            "sources": [report_components.general_info.executor_entity_logo],
            "size_factor": 1.0
        })
    elif not (report_components.general_info and (report_components.general_info.coejecutors_entities_logos or report_components.general_info.collaborators_entities_logos)):
        categories.append({
            "role": "EJECUTOR",
            "sources": [logo_default_path],
            "size_factor": 1.0
        })
        
    # 2. Co-ejecutores (80% del tamaño del ejecutor)
    if report_components.general_info and report_components.general_info.coejecutors_entities_logos:
        categories.append({
            "role": "CO-EJECUTOR",
            "sources": report_components.general_info.coejecutors_entities_logos,
            "size_factor": 0.80
        })

    # 3. Colaboradores (65% del tamaño del ejecutor)
    if report_components.general_info and report_components.general_info.collaborators_entities_logos:
        categories.append({
            "role": "COLABORADOR",
            "sources": report_components.general_info.collaborators_entities_logos,
            "size_factor": 0.65
        })

    # Cargar y procesar logos manteniendo colores originales
    all_logos = []
    
    for cat in categories:
        base_height = int(img_with_logos.height * 0.12)  # 12% de altura base - MUY VISIBLE
        target_height = int(base_height * cat["size_factor"])
        
        for src in cat["sources"]:
            try:
                pil_logo = None
                if src.startswith("http"):
                    import requests
                    resp = requests.get(src, timeout=10)
                    if resp.status_code == 200:
                        pil_logo = Image.open(BytesIO(resp.content)).convert("RGBA")
                elif os.path.exists(src):
                    pil_logo = Image.open(src).convert("RGBA")
                elif "/" in src:
                    if src.startswith("/api/minio_agent/"):
                        src = src.replace("/api/minio_agent/", "")
                    print(f"   ⬇️ Descargando logo de MinIO Key: {src}")
                    data = storage_service.download_file(src)
                    if data:
                        pil_logo = Image.open(BytesIO(data)).convert("RGBA")
                    elif os.path.exists(src):
                        pil_logo = Image.open(src).convert("RGBA")
                
                if pil_logo:
                    # ✨ ELIMINAR FONDO AUTOMÁTICAMENTE
                    pil_logo = remove_background(pil_logo, threshold=40)
                    
                    # Redimensionar manteniendo proporción y colores originales
                    aspect = pil_logo.width / pil_logo.height
                    new_w = int(target_height * aspect)
                    resized = pil_logo.resize((new_w, target_height), Image.Resampling.LANCZOS)
                    
                    all_logos.append({
                        "image": resized,
                        "role": cat["role"],
                        "width": new_w,
                        "height": target_height
                    })
                    
            except Exception as e:
                print(f"Error cargando logo {src}: {e}")

    if all_logos:
        try:
            # --- Configuración de Layout ---
            padding_x = int(img_with_logos.width * 0.025)  # Espacio entre logos
            left_margin = int(img_with_logos.width * 0.04)  # Margen izquierdo
            bottom_margin = int(img_with_logos.height * 0.04)  # Margen inferior
            
            # Calcular ancho total
            total_width = sum(l["width"] for l in all_logos) + (len(all_logos) - 1) * padding_x
            
            # Altura máxima de logo
            max_logo_height = max(l["height"] for l in all_logos)
            
            # --- Posicionamiento (Esquina inferior izquierda) ---
            base_y = img_with_logos.height - max_logo_height - bottom_margin
            current_x = left_margin
            
            # --- Pegar Logos DIRECTAMENTE (sin fondo blanco) ---
            for logo_data in all_logos:
                logo_img = logo_data["image"]
                # Centrar verticalmente cada logo según su altura
                y_offset = base_y + (max_logo_height - logo_data["height"]) // 2
                
                # Pegar con transparencia
                img_with_logos.paste(logo_img, (current_x, y_offset), logo_img)
                current_x += logo_data["width"] + padding_x
                
            print(f"✅ {len(all_logos)} logos (tamaño 12%) integrados sin fondo - alineados izquierda.")
            
        except Exception as e:
            print(f"Error en composición de logos: {e}")
            import traceback
            traceback.print_exc()
            
    return img_with_logos


def generator_image_node(state: GraphState):
    """
    Genera un póster vertical usando Gemini 3  (capacidad nativa de imagen).
    Maneja 4 casos según las señales del nodo prompt_generator:
    1. use_historical_base: Cargar base del historial, aplicar logos.
    2. use_current_base: Cargar base actual, re-aplicar logos (alianzas cambiaron).
    3. image_prompt presente: Generar nueva imagen con IA.
    4. Ninguno: Skip completo.
    """
    print(" 🛠️ Procesando póster del proyecto")
    
    # --- LEER SEÑALES DEL NODO ANTERIOR ---
    image_prompt = state.get("image_prompt")
    use_historical_base = state.get("use_historical_base")  # Case 1
    use_current_base = state.get("use_current_base")  # Case 3
    
    session_id = state.get("session_id", "default_session")
    user_email = state.get("user_email", "unknown_user")
    
    # ===== EARLY EXIT: SKIP COMPLETO =====
    if not image_prompt and not use_historical_base and not use_current_base:
        print("⏭️ [SKIP] No hay prompt ni señal de usar base. Salto completo.")
        return {
            "messages": [AIMessage(content="Generación de imagen omitida.")]
        }

    report_components = state.get("report_components") or ReportSchema()
    
    # Nombre del proyecto para el archivo
    project_title = "proyecto_tecnologico"
    if report_components.general_info:
        project_title = report_components.general_info.project_title or "proyecto_tecnologico"
    
    # --- DETERMINAR QUÉ BASE USAR ---
    # Prioridad: use_historical_base > use_current_base > generar nueva
    override_base_path = use_historical_base or use_current_base
    
    img_base = None
    base_image_key = None
    
    # Si vamos a usar una base (Case 1 o 3), recuperamos el prompt anterior para el historial
    if override_base_path and not image_prompt:
        last_history = state.get("generation_history", []) or []
        if last_history:
            last_item = last_history[-1]
            image_prompt = last_item.prompt_used if hasattr(last_item, 'prompt_used') else (
                last_item.get('prompt_used') if isinstance(last_item, dict) else None
            )
        if not image_prompt:
            image_prompt = "Reutilización de imagen base del proyecto."

    # 1. Definir carpeta
    base_path = os.getenv("SHARED_DATA_PATH", "generated_images")

    output_dir = os.path.join(base_path, "posters")
    os.makedirs(output_dir, exist_ok=True)

    # Buscamos en /app/static/
    # En Docker, Intecmar_api suele montarse en /app, así que static está en /app/static
    logo_path = "/app/static/images/CotecmarLogo_white.png"
    
    if not os.path.exists(logo_path):
        # Fallback para entorno local (asumiendo ejecución desde backend/)
        # Subimos niveles: backend/agent/tech_surveillance/subgrafths/image_generator/graph.py
        # Necesitamos ir a: static/images/
        # base del proyecto
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")) 
        logo_path = os.path.join(base_dir, "static", "images", "CotecmarLogo_white.png")

    print(f"Buscando logo en: {logo_path}")
    
    try:
        if override_base_path:
            print(f"🔄 [IMAGE GEN] Usando imagen base histórica: {override_base_path}")
            # Limpiar prefijo si existe
            base_key = override_base_path.split("MinioContent/")[-1] if "MinioContent/" in override_base_path else override_base_path
            base_key = base_key.replace("/api/minio_agent/", "")
            
            data = storage_service.download_file(base_key)
            if data:
                img_base = Image.open(BytesIO(data)).convert("RGBA")
                base_image_key = base_key
                print("   ✅ Imagen base histórica cargada correctamente.")
            else:
                print(f"   ⚠️ No se pudo descargar {base_key}, se intentará generar una nueva.")

        # 1. GENERACIÓN IA (Solo si no hay base override o falló la descarga)
        if not img_base:
            if not image_prompt:
                return {"messages": [AIMessage(content="✗ No hay prompt para generar imagen.")]}
                
            print("🎨 Generando nueva imagen con IA...")
            response = genai_client.models.generate_content(
                model=os.environ.get("NANO_BANANA_MODEL", "gemini-2.5-flash-image"),
                contents=[image_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["Image"], 
                    image_config=types.ImageConfig(
                        aspect_ratio="3:4" 
                    )
                )
            )

            # Procesar la respuesta para obtener img_base
            for part in response.parts:
                if part.inline_data:
                    image_bytes = part.inline_data.data
                    img_base = Image.open(BytesIO(image_bytes)).convert("RGBA")
                    break
            
            if not img_base:
                 return {"messages": [AIMessage(content="⚠ La API respondió pero no se encontró imagen.")]}

        # 2. PROCESAMIENTO COMÚN (Logo Overlay & Storage)
        sanitized_title = "".join(x for x in project_title if x.isalnum() or x in " _-").replace(" ", "_").lower()
        timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Guardar imagen base (si es generada nueva, para mantener el historial de bases)
        if not override_base_path:
            base_filename = f"{sanitized_title}_base_{timestamp_str}.png"
            full_base_path = os.path.join(output_dir, base_filename)
            img_base.save(full_base_path)
            minio_folder_base = f"{user_email}/Agent_Sessions/{session_id}/generated_images/base"
            base_image_key = storage_service.upload_file(full_base_path, f"{minio_folder_base}/{base_filename}", remove_after_upload=True)
            print(f"   ✅ Nueva imagen base guardada: {base_image_key}")
        
        # APLICAR LOGOS
        img_final = apply_logos_to_image(img_base, report_components, logo_path)
        
        # GUARDAR IMAGEN FINAL
        img_final_rgb = img_final.convert("RGB") 
        final_filename = f"{sanitized_title}_final_{timestamp_str}.png"
        full_final_path = os.path.join(output_dir, final_filename)
        img_final_rgb.save(full_final_path)
        
        print("   ☁️ Subiendo póster FINAL a MinIO...")
        minio_folder_final = f"{user_email}/Agent_Sessions/{session_id}/generated_images/final"
        minio_key = storage_service.upload_file(full_final_path, f"{minio_folder_final}/{final_filename}", remove_after_upload=False)
        
        image_path = full_final_path
        
        if image_path:
             # Actualizando estado
            
            # --- Historial ---
            from backend.agent.tech_surveillance.state import GenerationItem
            
            new_history_item = GenerationItem(
                timestamp=datetime.now().isoformat(),
                poster_path=minio_key if minio_key else image_path,
                base_image_path=base_image_key if base_image_key else full_base_path,
                prompt_used=image_prompt
            )
            
            current_history = state.get("generation_history", []) or []
            current_history.append(new_history_item)

            # --- DEBUG LOGGING REQUESTED BY USER ---
            print("\n" + "="*50)
            print(f"🧐 DEBUG HISTORIAL (Total versiones: {len(current_history)})")
            for idx, item in enumerate(current_history):
                try:
                    ts = item.get('timestamp') if isinstance(item, dict) else item.timestamp
                    p = item.get('poster_path') if isinstance(item, dict) else item.poster_path
                    b = item.get('base_image_path') if isinstance(item, dict) else getattr(item, 'base_image_path', 'N/A')
                    print(f"   [{idx+1}] TS: {ts} | FINAL: {p[-30:] if p else 'None'} | BASE: {b[-30:] if b else 'None'}")
                except Exception as e:
                    print(f"   [{idx+1}] Error imprimiendo item: {e}")
            print("="*50 + "\n")

            docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
            if isinstance(docs_paths, dict):
                docs_paths = DocsPaths(**docs_paths)
            
            # Guardamos la KEY de MinIO si existe, o la ruta local como fallback
            docs_paths.poster_image_path = minio_key if minio_key else image_path
            
            # También devolvemos la ruta local en 'generated_image_path' para que el nodo
            # de reporte PDF pueda encontrarla rápidamente sin descargarla de MinIO
            return {
                "messages": [AIMessage(content=f"✓ Póster generado: {image_path}")],
                "generated_image_path": image_path, # Ruta LOCAL para uso inmediato en PDF
                "docs_paths": docs_paths, # Retornamos objeto para que TypedDict lo valide
                "generation_history": current_history
            }
        else:
            return {"messages": [AIMessage(content="⚠ La API respondió pero no se encontró imagen.")]}
            
    except Exception as e:
        import traceback
        traceback.print_exc()
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