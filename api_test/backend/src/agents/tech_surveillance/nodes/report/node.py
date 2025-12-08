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

from src.agents.tech_surveillance.state import GraphState, ReportSchema, DocsPaths
from src.agents.tech_surveillance.utils.pdf_generation  import get_custom_styles, PageTemplate, markdown_to_flowables, ReportDocTemplate, COTECMAR_BLUE, COTECMAR_DARK_BLUE


from src.services.storage import MinioService

# Instanciamos el servicio
storage_service = MinioService()

# --- Carpeta de Reportes ---
REPORTS_DIR = "generated_reports"


def report_node(state: GraphState):
    print("--- Ejecutando Nodo: Generación de Reporte PDF ---")
    
    report_components = state.get("report_components")

    session_id = state.get("session_id", "default_session")

    if not report_components:
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
    if isinstance(kws, str): kws = [kws]
    
    # 2. Resumen Ejecutivo
    exec_summary = get_section_content(get_field(data, 'executive_summary'), 'content')

    # 3. Justificación
    justification = get_section_content(get_field(data, 'problem_statement_justification'), 'content')

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
    execution_text = f"**Cronograma de Actividades**\n\n{schedule}\n\n**Matriz de Riesgos**\n\n{risks}"

    # 8. Resultados
    results = get_section_content(get_field(data, 'results_and_impacts'), 'content')

    # Obtener datos de convocatoria
    call_info = state.get("call_info")
    
    # Construcción del Markdown
    full_markdown_report = f"""

## 1. Generalidades del Proyecto

**Título:** {title}
**Convocatoria:** {call_info.title if call_info else 'N/A'}
**Entidad/Persona:** COTECMAR
**Línea Temática:** {', '.join(call_info.keywords) if call_info and call_info.keywords else 'N/A'}


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
        # A veces la imagen puede venir como ruta relativa o absoluta
        final_img_path = None
        if image_path_raw:
            if os.path.exists(image_path_raw):
                final_img_path = image_path_raw
            else:
                # Intentar buscar dentro del shared path si viene solo el nombre
                potential_path = os.path.join(base_path, os.path.basename(image_path_raw))
                if os.path.exists(potential_path):
                    final_img_path = potential_path

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
        pdf_key = storage_service.upload_file(pdf_filepath, session_id)
        md_key = storage_service.upload_file(md_filepath, session_id)
        
        # Nota: La imagen de portada ya debería haber sido subida en su propio nodo,
        # pero si no, podrías subirla aquí también si quisieras tener el link directo.
        img_key = None
        if final_img_path:
             img_key = storage_service.upload_file(final_img_path, session_id)

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
        
        message = AIMessage(
            content=f"✓ Reporte final generado."
        )

        return {
            "messages": [message],
            "docs_paths": docs_paths
        }

    except Exception as e:
        print(f"   ❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        return {"final_report": f"Error: {e}"}