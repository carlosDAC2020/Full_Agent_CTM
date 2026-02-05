import os
import re
from datetime import datetime
from langchain_core.messages import AIMessage
from reportlab.platypus import Spacer, Image, PageBreak, Paragraph
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from backend.agent.tech_surveillance.state import GraphState, ReportSchema, DocsPaths
from backend.agent.tech_surveillance.utils.pdf_generation  import get_custom_styles, PageTemplate, markdown_to_flowables, ReportDocTemplate, COTECMAR_BLUE, COTECMAR_DARK_BLUE


from backend.app.services.core.storage import storage_service

# --- Carpeta de Reportes ---
REPORTS_DIR = "generated_reports"


def report_node(state: GraphState):
    print("\n--- [REPORT_NODE] START ---")
    
    # --- DEBUG STATE ---
    curr_history = state.get("generation_history", []) or []
    curr_docs = state.get("docs_paths")
    print(f"🧐 [DEBUG REPORT_NODE] Versiones recibidas: {len(curr_history)}")
    
    # --- Restore missing variables ---
    session_id = state.get("session_id", "default_session")
    user_email = state.get("user_email", "unknown_user")
    
    report_components = state.get("report_components")
    
    if not report_components:
        print("⚠️ [REPORT_NODE] No report_components found in state!")
        return {}

    # Convertir a objeto si es dict
    if isinstance(report_components, dict):
        try:
            data = ReportSchema(**report_components)
        except:
            class Data: pass
            data = Data()
            for k, v in report_components.items():
                setattr(data, k, v)
    else:
        data = report_components

    # --- Configuración de Rutas (Docker) ---
    base_path = os.getenv("SHARED_DATA_PATH", "generated_reports")
    # Subcarpeta opcional para reportes finales
    reports_dir = os.path.join(base_path, "final_reports") 
    os.makedirs(reports_dir, exist_ok=True)

    # --- Extracción de Datos ---
    
    def get_field(obj, field, default=None):
        if isinstance(obj, dict):
            val = obj.get(field, default)
        else:
            val = getattr(obj, field, default)
        return val if val is not None else default

    def get_section_content(section_obj, field='content'):
        if not section_obj:
            return ""
        val = get_field(section_obj, field)
        return val if val else ""

    # 1. Información General
    gen_info = get_field(data, 'general_info')
    title = get_field(gen_info, 'project_title', "Proyecto Sin Título") if gen_info else "Proyecto Sin Título"
    desc = get_field(gen_info, 'project_description', "N/A") if gen_info else "N/A"
    kws = get_field(gen_info, 'keywords', []) if gen_info else []
    duration = get_field(gen_info, 'duration_months', "N/A") if gen_info else "N/A"
    thematic_line = get_field(gen_info, 'thematic_line', "N/A") if gen_info else "N/A"
    
    # Alianzas
    executor = get_field(gen_info, 'executor_entity', "COTECMAR")
    executor_logo = get_field(gen_info, 'executor_entity_logo')
    
    co_executors = get_field(gen_info, 'coejecutors_entities', [])
    co_executors_logos = get_field(gen_info, 'coejecutors_entities_logos', [])
    
    collaborators = get_field(gen_info, 'collaborators_entities', [])
    collaborators_logos = get_field(gen_info, 'collaborators_entities_logos', [])
    
    # Construir tabla de alianzas en Markdown
    alliances_table = "| Rol | Entidad |\n| :--- | :--- |\n"
    alliances_table += f"| **Ejecutor** | {executor} |\n"
    
    for ce in co_executors:
        alliances_table += f"| Co-ejecutor | {ce} |\n"
        
    for col in collaborators:
        alliances_table += f"| Colaborador | {col} |\n"

    if isinstance(kws, str): kws = [kws]
    
    # ... (rest of data extraction looks ok) ...
    # 2. Resumen Ejecutivo
    exec_summary = get_section_content(get_field(data, 'executive_summary'), 'content')

    # 3. Justificación
    justification_obj = get_field(data, 'problem_statement_justification')
    if justification_obj:
        ps = get_field(justification_obj, 'problem_statement', '')
        js = get_field(justification_obj, 'justification', '')
        justification = f"### 3.1. Planteamiento del Problema\n{ps}\n\n### 3.2. Justificación\n{js}"
    else:
        justification = ""

    # 4. Marco Teórico
    theo_frame_obj = get_field(data, 'theoretical_framework')
    theo_frame_body = get_section_content(theo_frame_obj, 'body')
    references = get_section_content(theo_frame_obj, 'references_apa')

    # 5. Objetivos
    objs_obj = get_field(data, 'objectives')
    gen_obj = get_field(objs_obj, 'general_objective', '') if objs_obj else ''
    spec_objs = get_field(objs_obj, 'specific_objectives_smart', '') if objs_obj else ''
    objectives_text = f"**Objetivo General**\n\n{gen_obj}\n\n**Objetivos Específicos**\n\n{spec_objs}"

    # 6. Metodología
    methodology = get_section_content(get_field(data, 'methodology'), 'content')

    # 7. Plan de Ejecución
    plan_obj = get_field(data, 'execution_plan')
    schedule = get_field(plan_obj, 'activity_schedule', '') if plan_obj else ''
    risks = get_field(plan_obj, 'risk_matrix', '') if plan_obj else ''
    budget = get_field(plan_obj, 'budget', '') if plan_obj else ''

    execution_text = f"{schedule}\n\n{budget}\n\n{risks}"

    # 8. Resultados
    results = get_section_content(get_field(data, 'results_and_impacts'), 'content')

    # Obtener datos de convocatoria
    call_info = state.get("call_info")
    
    # Construcción del Markdown
    full_markdown_report = f"""

## 1. Generalidades del Proyecto

**Título:** {title}
**Convocatoria:** {call_info.title if call_info else 'N/A'}
**Duración:** {duration} meses
**Línea Temática:** {thematic_line}

**Alianzas del Proyecto**
{alliances_table}

* **Descripción:** {desc}
* **Palabras Clave:** {', '.join(kws) if kws else 'N/A'}

## 2. Resumen Ejecutivo
{exec_summary}

## 3. Planteamiento del Problema y Justificación
{justification}

## 4. Marco Teórico y Estado del Arte
{theo_frame_body}

## 5. Objetivos
{objectives_text}

## 6. Metodología Propuesta
{methodology}

## 7. Plan de Ejecución y Gestión
{execution_text}

## 8. Resultados e Impactos Esperados
{results}

## 9. Referencias Bibliográficas
{references}
"""

    # Limpieza de contenido repetitivo
    full_markdown_report = re.sub(r'## (\d+\..+)\n+### \*\*\1\*\*', r'## \1', full_markdown_report)
    full_markdown_report = re.sub(r'## (\d+\..+)\n+## \1', r'## \1', full_markdown_report)

    # --- SANITIZACIÓN PARA REPORTLAB ---
    # ReportLab usa un parser XML estricto para tags como <br>. 
    # El markdown a veces genera <br> sin cerrar si hay saltos de línea forzados.
    # Reemplazamos <br> por <br/> self-closing.
    full_markdown_report = re.sub(r'<br\s*>', '<br/>', full_markdown_report)
    full_markdown_report = re.sub(r'<br\s*/?>', '<br/>', full_markdown_report) # Asegurar consistencia
    # También limpiar posibles atributos vacíos o contenido dentro de br (que no debería existir)
    full_markdown_report = re.sub(r'<br>(.*?)</br>', r'\1<br/>', full_markdown_report) 


    # Nombres de Archivo
    sanitized_title = re.sub(r'[\s/:]+', '_', title).lower()[:50]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    pdf_filename = f"{sanitized_title}_{timestamp}.pdf"
    pdf_filepath = os.path.join(reports_dir, pdf_filename)
    
    md_filename = f"{sanitized_title}_{timestamp}.md"
    md_filepath = os.path.join(reports_dir, md_filename)

    try:
        # Guardar markdown primero
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(full_markdown_report)

        # Crear documento con plantilla personalizada
        doc = ReportDocTemplate(
            pdf_filepath, 
            pagesize=letter, 
            rightMargin=2*cm, 
            leftMargin=2*cm, 
            topMargin=2.5*cm, 
            bottomMargin=2.5*cm
        )
        
        styles = get_custom_styles()
        pt = PageTemplate()
        
        story = []
        
        # ========================================
        # PÁGINA 1: PORTADA CON IMAGEN Y MARCO
        # ========================================
        image_path_raw = state.get("generated_image_path")
        # Validar si la imagen existe en el sistema de archivos local
        final_img_path = None
        if image_path_raw:
            if os.path.exists(image_path_raw):
                final_img_path = image_path_raw
            else:
                # Intentar buscar dentro del shared path si viene solo el nombre
                potential_path = os.path.join(base_path, os.path.basename(image_path_raw))
                if os.path.exists(potential_path):
                    final_img_path = potential_path

        # --- FALLBACK: Si no existe localmente, intentar descargar de MinIO ---
        if not final_img_path:
            docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
            if isinstance(docs_paths, dict):
                img_key = docs_paths.get("poster_image_path")
            else:
                img_key = getattr(docs_paths, "poster_image_path", None)
            
            if img_key and ("/" in img_key or "generated_images" in img_key):
                print(f"📥 [REPORT_NODE] Recuperando imagen de MinIO para PDF: {img_key}")
                data = storage_service.download_file(img_key)
                if data:
                    import tempfile
                    # Guardamos en un temporal que el cleanup final borrará
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        tmp.write(data)
                        final_img_path = tmp.name
                        print(f"✅ [REPORT_NODE] Imagen descargada a: {final_img_path}")

        if final_img_path:
            # El área imprimible (Frame) es aprox 17.1cm x 22.5cm debido a los márgenes.
            # Debemos hacer la imagen un poco más pequeña que eso para que entre.
            
            # Usamos 22 cm de alto como límite seguro.
            # Manteniendo ratio 3:4 -> Ancho = 22 * 0.75 = 16.5 cm
            
            img_width = 16.5 * cm
            img_height = 22.0 * cm
            
            # --- AJUSTE DE POSICIÓN ---
            # Usamos un espaciador negativo para "subir" la imagen visualmente
            # hacia el margen superior, aprovechando que la imagen ahora sí cabe.
            story.append(Spacer(1,0 * cm))
            
            # Insertar imagen
            img = Image(final_img_path, width=img_width, height=img_height, kind='proportional')
            img.hAlign = 'CENTER'
            story.append(img)
            
            story.append(PageBreak())
        else:
            # Si no hay imagen, crear portada de texto
            story.append(Spacer(1, 4*cm))
            
            # Título de la portada
            cover_title_style = ParagraphStyle(
                name='CoverTitle',
                fontSize=24,
                fontName='Helvetica-Bold',
                leading=30,
                alignment=TA_CENTER,
                textColor=COTECMAR_DARK_BLUE,
                spaceAfter=20
            )
            
            story.append(Paragraph(title, cover_title_style))
            story.append(Spacer(1, 0.8*cm))
            
            # Subtítulo de convocatoria
            cover_subtitle_style = ParagraphStyle(
                name='CoverSubtitle',
                fontSize=14,
                fontName='Helvetica',
                leading=18,
                alignment=TA_CENTER,
                textColor=COTECMAR_BLUE,
                spaceAfter=10
            )
            
            if call_info:
                story.append(Paragraph(call_info.title, cover_subtitle_style))
            
            story.append(Spacer(1, 10*cm))
            
            # Información adicional centrada
            footer_style = ParagraphStyle(
                name='CoverFooter',
                fontSize=10,
                fontName='Helvetica',
                alignment=TA_CENTER,
                textColor=colors.HexColor('#666666')
            )
            
            story.append(Paragraph(f"COTECMAR - {datetime.now().strftime('%B %Y')}", footer_style))
            story.append(PageBreak())

        # ========================================
        # PÁGINA 2: TABLA DE CONTENIDO
        # ========================================
        toc = TableOfContents()
        toc.dotsMinLevel = 0
        toc.levelStyles = [
            styles['TOCHeading1'],
            styles['TOCHeading2'],
            styles['TOCHeading3']
        ]
        
        # Título de la TOC (Estilo específico)
        toc_title_style = ParagraphStyle(
            name='TOCTitle',
            parent=styles['H1'],
            alignment=TA_CENTER
        )
        
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph("<b>Tabla de Contenido</b>", toc_title_style))
        story.append(Spacer(1, 0.8*cm))
        
        # Línea decorativa
        from reportlab.platypus import HRFlowable
        hr = HRFlowable(
            width="80%",
            thickness=2,
            color=COTECMAR_BLUE,
            spaceBefore=0,
            spaceAfter=20,
            hAlign='CENTER'
        )
        story.append(hr)
        
        story.append(toc)
        story.append(PageBreak())

        # ========================================
        # RESTO DEL CONTENIDO
        # ========================================
        story.extend(markdown_to_flowables(full_markdown_report, styles))

        # Generar PDF con callbacks personalizados
        doc.multiBuild(
            story, 
            onFirstPage=pt.on_first_page,  # Usa el marco decorativo
            onLaterPages=pt.on_later_pages  # Usa encabezado/pie estándar
        )
        
        print(f"   ✅ Reporte PDF generado: {pdf_filepath}")

        # ========================================
        # SUBIDA A MINIO
        # ========================================
        print("☁️ Subiendo reporte final a MinIO...")
        minio_folder = f"{user_email}/Agent_Sessions/{session_id}/final_project_proposal"
        pdf_key = storage_service.upload_file(pdf_filepath, f"{minio_folder}/{pdf_filename}", remove_after_upload=True)
        md_key = storage_service.upload_file(md_filepath, f"{minio_folder}/{md_filename}", remove_after_upload=True)
        
        # --- LÓGICA PARA EVITAR DOBLE SUBIDA DEL POSTER ---
        # La imagen de portada ya debería haber sido subida por el nodo 'images_generator'.
        # Verificamos si ya existe una key en docs_paths antes de intentar subir de nuevo.
        existing_docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
        img_key = existing_docs_paths.poster_image_path
        
        if img_key and "/" in img_key and not img_key.startswith("/app"):
            # Ya existe una key de MinIO válida (no es una ruta local), la reutilizamos.
            print(f"   ℹ️ Poster ya subido por images_generator: {img_key}. No se re-sube.")
        elif final_img_path:
            # No hay key previa, o la key es una ruta local. Subimos la imagen.
            print(f"   ☁️ Subiendo poster desde report_node (fallback)...")
            img_key = storage_service.upload_file(final_img_path, f"{minio_folder}/{os.path.basename(final_img_path)}", remove_after_upload=True)

        # Cleanup poster if it still exists locally (even if not uploaded in this node)
        if final_img_path and os.path.exists(final_img_path):
            try:
                os.remove(final_img_path)
                print(f"🗑️ Poster local eliminado después de generar PDF: {final_img_path}")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar el poster local {final_img_path}: {e}")

        # ========================================
        # ACTUALIZACIÓN DE ESTADO
        # ========================================
        docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
        
        # Guardamos KEYS de S3
        if pdf_key:
            docs_paths.proyect_proposal_pdf = pdf_key
        if md_key:
            docs_paths.proyect_proposal_md = md_key
        if img_key:
             docs_paths.poster_image_path = img_key # Actualizamos con la ruta nube si queremos
        
        # --- Actualizar Historial con PDF/MD ---
        current_history = state.get("generation_history", []) or []
        
        # SI EL PÓSTER SE SALTÓ (image_prompt es None), debemos CREAR un nuevo registro 
        # en el historial basado en el último póster, de lo contrario report_node 
        # sobreescribirá los campos pdf_path/md_path del registro anterior.
        image_prompt = state.get("image_prompt")
        if not image_prompt and current_history:
            print("📝 [REPORT_NODE] Creando nueva versión en el historial (preservando selección de usuario)")
            last_item = current_history[-1]
            from backend.agent.tech_surveillance.state import GenerationItem
            
            # CRITICAL: Usamos docs_paths.poster_image_path si está disponible, 
            # ya que refleja lo que el usuario seleccionó en la UI o lo que se cargó/mantuvo.
            poster_to_use = docs_paths.poster_image_path if docs_paths and docs_paths.poster_image_path else (
                last_item.poster_path if not isinstance(last_item, dict) else last_item.get('poster_path')
            )
            
            new_item = GenerationItem(
                timestamp=datetime.now().isoformat(),
                poster_path=poster_to_use,
                base_image_path=getattr(last_item, 'base_image_path', None) if not isinstance(last_item, dict) else last_item.get('base_image_path'),
                prompt_used=last_item.prompt_used if not isinstance(last_item, dict) else last_item.get('prompt_used'),
                pdf_path=pdf_key,
                md_path=md_key
            )
            current_history.append(new_item)
        elif current_history:
            # Si el póster SÍ se generó, el nodo images_generator ya creó el registro. 
            # Solo actualizamos los paths de PDF/MD.
            last_item = current_history[-1]
            
            # El estado puede venir como dict o como objeto Pydantic
            if isinstance(last_item, dict):
                if pdf_key: last_item['pdf_path'] = pdf_key
                if md_key: last_item['md_path'] = md_key
            else:
                try:
                    if pdf_key: last_item.pdf_path = pdf_key
                    if md_key: last_item.md_path = md_key
                except AttributeError:
                    # Fallback si por alguna razón no es lo que esperábamos
                    if pdf_key: last_item['pdf_path'] = pdf_key
                    if md_key: last_item['md_path'] = md_key
            
            current_history[-1] = last_item
            
        print("\n" + "="*50)
        print(f"🧐 [DEBUG REPORT_NODE] HISTORIAL FINALIZADO (Total: {len(current_history)})")
        for i, item in enumerate(current_history):
            p = item.get('poster_path') if isinstance(item, dict) else item.poster_path
            pdf = item.get('pdf_path') if isinstance(item, dict) else item.pdf_path
            print(f"   [{i+1}] Poster: {p[-30:] if p else 'None'} | PDF: {'OK' if pdf else 'Missing'}")
        print("="*50 + "\n")

        message = AIMessage(
            content=f"✓ Reporte final generado."
        )

        return {
            "messages": [message],
            "docs_paths": docs_paths,
            "generation_history": current_history
        }

    except Exception as e:
        print(f"   ❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        return {
            "generation_history": state.get("generation_history", []),
            "final_report_error": str(e)
        }