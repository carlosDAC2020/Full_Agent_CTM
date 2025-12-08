
import os
import re
from datetime import datetime
from langchain_core.messages import AIMessage
from reportlab.platypus import Spacer, PageBreak, Paragraph
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from agents.tech_surveillance.state import GraphState, DocsPaths
from agents.tech_surveillance.utils.pdf_generation import get_custom_styles, PageTemplate, markdown_to_flowables, ReportDocTemplate, COTECMAR_BLUE, COTECMAR_DARK_BLUE

# Carpeta de esquemas iniciales
INITIAL_SCHEMAS_DIR = "generated_initial_schemas"

def initial_schema_proyect_doc_node(state: GraphState) -> dict:
    """
    Nodo para la generacion de los documentos iniciales del esquema del proyecto.
    Genera tanto .md como .pdf.
    """
    print("--- Nodo: generando el documento de esquema inicial de la idea del proyecto ---")

    # Obtenemos el esquema inicial del proyecto
    initial_schema = state.get("initial_schema") or "No se encontró el esquema inicial."
    
    # Obtenemos el título del proyecto desde selected_idea o report_components
    selected_idea = state.get("selected_idea")
    report_components = state.get("report_components")
    
    if selected_idea and hasattr(selected_idea, 'idea_title'):
        project_title = selected_idea.idea_title or "Proyecto Sin Título"
    elif report_components:
        gen_info = getattr(report_components, 'general_info', None)
        if gen_info:
            project_title = getattr(gen_info, 'project_title', "Proyecto Sin Título")
        else:
            project_title = "Proyecto Sin Título"
    else:
        project_title = "Proyecto Sin Título"

    # Creamos la carpeta donde se guardarán los documentos si no existe
    os.makedirs(INITIAL_SCHEMAS_DIR, exist_ok=True)

    # Sanitizamos el título para usar en nombres de archivo
    sanitized_title = re.sub(r'[\s/:]+', '_', project_title).lower()[:50]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # ========================================
    # GENERAR ARCHIVO MARKDOWN
    # ========================================
    md_filename = f"initial_schema_{sanitized_title}_{timestamp}.md"
    md_filepath = os.path.join(INITIAL_SCHEMAS_DIR, md_filename)
    
    # Contenido del markdown
    markdown_content = f"""# Esquema Inicial del Proyecto

**Título del Proyecto:** {project_title}

**Fecha de Generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{initial_schema}
"""
    
    # Guardar el archivo markdown
    try:
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"   ✅ Esquema inicial Markdown generado: {md_filepath}")
    except Exception as e:
        print(f"   ❌ Error generando archivo Markdown: {e}")
        return {"messages": [AIMessage(content=f"Error generando Markdown: {e}")]}

    # ========================================
    # GENERAR ARCHIVO PDF
    # ========================================
    pdf_filename = f"initial_schema_{sanitized_title}_{timestamp}.pdf"
    pdf_filepath = os.path.join(INITIAL_SCHEMAS_DIR, pdf_filename)

    try:
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
        # PORTADA
        # ========================================
        story.append(Spacer(1, 4*cm))
        
        # Título de la portada
        cover_title_style = styles['H1'].__class__(
            name='CoverTitle',
            fontSize=24,
            fontName='Helvetica-Bold',
            leading=30,
            alignment=TA_CENTER,
            textColor=COTECMAR_DARK_BLUE,
            spaceAfter=20
        )
        
        story.append(Paragraph("Esquema Inicial del Proyecto", cover_title_style))
        story.append(Spacer(1, 1*cm))
        
        # Título del proyecto
        project_title_style = styles['H1'].__class__(
            name='ProjectTitle',
            fontSize=18,
            fontName='Helvetica-Bold',
            leading=24,
            alignment=TA_CENTER,
            textColor=COTECMAR_BLUE,
            spaceAfter=10
        )
        
        story.append(Paragraph(project_title, project_title_style))
        story.append(Spacer(1, 8*cm))
        
        # Información adicional centrada
        footer_style = styles['H1'].__class__(
            name='CoverFooter',
            fontSize=10,
            fontName='Helvetica',
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
        )
        
        story.append(Paragraph(f"COTECMAR - {datetime.now().strftime('%B %Y')}", footer_style))
        story.append(PageBreak())
        
        # ========================================
        # CONTENIDO DEL ESQUEMA
        # ========================================
        story.extend(markdown_to_flowables(initial_schema, styles))
        
        # Generar PDF con callbacks personalizados
        doc.multiBuild(
            story,
            onFirstPage=pt.on_first_page,
            onLaterPages=pt.on_later_pages
        )
        
        print(f"   ✅ Esquema inicial PDF generado: {pdf_filepath}")
        
    except Exception as e:
        print(f"   ❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        return {
            "messages": [AIMessage(content=f"Error generando PDF: {e}")],
            "docs_paths": state.get("docs_paths") or DocsPaths()
        }

    # ========================================
    # ACTUALIZAR RUTAS EN EL ESTADO
    # ========================================
    docs_paths: DocsPaths = state.get("docs_paths") or DocsPaths()
    docs_paths.proyect_proposal_initial_schema_md = md_filepath
    docs_paths.proyect_proposal_initial_schema_pdf = pdf_filepath

    message = AIMessage(
        content=f"✓ Esquema inicial Markdown generado: {md_filepath}\n✓ Esquema inicial PDF generado: {pdf_filepath}"
    )

    return {
        "messages": [message],
        "docs_paths": docs_paths
    }
