import os
import re
from datetime import datetime
from pathlib import Path
import html

# Importamos nuestro estado
from agents.tech_surveillance.state import GraphState

# Importaciones de ReportLab
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

REPORTS_DIR = "generated_reports"

# --- Colores y Estilos ---

COTECMAR_BLUE = colors.HexColor('#0066CC')
COTECMAR_DARK_BLUE = colors.HexColor('#003366')
COTECMAR_GRAY = colors.HexColor('#4A4A4A')

def get_custom_styles():
    """Crea una hoja de estilos personalizada."""
    styles = getSampleStyleSheet()
    
    # Verificar si el estilo ya existe antes de agregarlo
    if 'H1' not in styles:
        styles.add(ParagraphStyle(
            name='H1',
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=COTECMAR_DARK_BLUE,
            spaceAfter=14,
            alignment=TA_LEFT
        ))
    
    if 'H2' not in styles:
        styles.add(ParagraphStyle(
            name='H2',
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=COTECMAR_BLUE,
            spaceBefore=12,
            spaceAfter=10,
            alignment=TA_LEFT
        ))
    
    if 'H3' not in styles:
        styles.add(ParagraphStyle(
            name='H3',
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=COTECMAR_GRAY,
            spaceBefore=10,
            spaceAfter=8,
            alignment=TA_LEFT
        ))
    
    if 'Body' not in styles:
        styles.add(ParagraphStyle(
            name='Body',
            fontSize=10,
            fontName='Helvetica',
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ))
    
    if 'CustomBullet' not in styles:
        styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=styles['Body'],
            leftIndent=20,
            spaceBefore=2,
            spaceAfter=2
        ))
    
    if 'TableHeader' not in styles:
        styles.add(ParagraphStyle(
            name='TableHeader',
            fontSize=9,
            fontName='Helvetica-Bold',
            textColor=colors.white,
            alignment=TA_CENTER
        ))
    
    if 'TableCell' not in styles:
        styles.add(ParagraphStyle(
            name='TableCell',
            fontSize=8,
            fontName='Helvetica',
            leading=10,
            alignment=TA_LEFT
        ))
    
    return styles

def escape_xml_chars(text):
    """Escapa caracteres especiales para XML/HTML."""
    if not isinstance(text, str):
        return str(text)
    
    # Escapar caracteres XML básicos
    text = html.escape(text, quote=False)
    
    # Reemplazar saltos de línea por <br/> (auto-cerrada)
    text = text.replace('\n', '<br/>')
    
    return text

def process_table(table_text, styles):
    """Convierte una tabla markdown en un objeto Table de ReportLab."""
    lines = [line.strip() for line in table_text.split('\n') if line.strip()]
    
    # Filtrar líneas que son separadores (contienen solo |, -, y espacios)
    data_lines = [line for line in lines if not re.match(r'^[\|\s\-:]+$', line)]
    
    if not data_lines:
        return None
    
    # Procesar cada línea de la tabla
    table_data = []
    for line in data_lines:
        # Dividir por | y limpiar espacios
        cells = [cell.strip() for cell in line.split('|')]
        # Eliminar células vacías al inicio/final
        cells = [cell for cell in cells if cell]
        
        if cells:
            # Convertir cada celda a Paragraph, escapando caracteres especiales
            formatted_cells = []
            for cell in cells:
                # Escapar caracteres especiales y limpiar
                safe_cell = escape_xml_chars(cell)
                # Remover asteriscos de markdown
                safe_cell = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_cell)
                safe_cell = re.sub(r'\*(.*?)\*', r'<i>\1</i>', safe_cell)
                
                formatted_cells.append(Paragraph(safe_cell, styles['TableCell']))
            
            table_data.append(formatted_cells)
    
    if not table_data:
        return None
    
    # Crear la tabla
    try:
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COTECMAR_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        return table
    except Exception as e:
        print(f"   ⚠️ Error al crear tabla: {e}")
        return None

def markdown_to_flowables(markdown_text: str, styles):
    """Convierte un string Markdown a una lista de Flowables de ReportLab."""
    flowables = []
    lines = markdown_text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detectar inicio de tabla (línea que empieza con |)
        if line.startswith('|'):
            # Recolectar todas las líneas de la tabla
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            
            # Procesar la tabla completa
            table_text = '\n'.join(table_lines)
            table = process_table(table_text, styles)
            if table:
                flowables.append(table)
                flowables.append(Spacer(1, 0.3*cm))
            continue
        
        # Procesar líneas normales
        if line.startswith('### '):
            safe_text = escape_xml_chars(line[4:])
            safe_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_text)
            flowables.append(Paragraph(safe_text, styles['H3']))
        elif line.startswith('## '):
            safe_text = escape_xml_chars(line[3:])
            safe_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_text)
            flowables.append(Paragraph(safe_text, styles['H2']))
        elif line.startswith('# '):
            safe_text = escape_xml_chars(line[2:])
            safe_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_text)
            flowables.append(Paragraph(safe_text, styles['H1']))
        elif line.startswith('* '):
            safe_text = escape_xml_chars(line[2:])
            safe_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_text)
            flowables.append(Paragraph(f'• {safe_text}', styles['CustomBullet']))
        elif line:
            safe_text = escape_xml_chars(line)
            safe_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', safe_text)
            safe_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', safe_text)
            flowables.append(Paragraph(safe_text, styles['Body']))
        
        i += 1
    
    return flowables

# --- Plantilla de Página con Encabezado y Pie de Página ---

class PageTemplate:
    def __init__(self, page_size=letter):
        self.page_width = page_size[0]
        self.page_height = page_size[1]
        self.top_margin = 2.5 * cm
        self.bottom_margin = 2.5 * cm
        self.left_margin = 2 * cm
        self.right_margin = 2 * cm

    def on_first_page(self, canvas, doc):
        canvas.saveState()
        self.draw_footer(canvas, doc)
        canvas.restoreState()

    def on_later_pages(self, canvas, doc):
        canvas.saveState()
        self.draw_footer(canvas, doc)
        canvas.restoreState()

    def draw_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(COTECMAR_BLUE)
        canvas.setLineWidth(0.5)
        canvas.line(self.left_margin, self.bottom_margin - 0.5*cm, 
                   self.page_width - self.right_margin, self.bottom_margin - 0.5*cm)
        
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(COTECMAR_GRAY)
        canvas.drawString(self.left_margin, self.bottom_margin - 1*cm, 
                         "Documento Generado por Sistema de Vigilancia Tecnológica")
        
        canvas.drawRightString(self.page_width - self.right_margin, 
                              self.bottom_margin - 1*cm, 
                              f"Página {canvas.getPageNumber()}")
        canvas.restoreState()


# --- El Nodo Principal de Reporte ---

def report_node(state: GraphState):
    """
    Ensambla el reporte final desde el estado y lo genera como un archivo PDF.
    """
    print("--- Ejecutando Nodo: Generación de Reporte PDF ---")
    
    # 1. Extraer todos los componentes del estado
    report_components = state.get("report_components")
    if not report_components:
        print("   ⚠️ No se encontraron componentes de reporte para generar el PDF.")
        return {}

    general_info = report_components.get("general_info", {})
    theoretical_framework = report_components.get("theoretical_framework", {})
    objectives = report_components.get("objectives", {})
    execution_plan = report_components.get("execution_plan", {})

    # Extraer la ruta de la imagen
    image_path = state.get("generated_image_path")

    # 2. Ensamblar el contenido completo en Markdown
    project_title = general_info.get("project_title", "Proyecto Sin Título")
    
    full_markdown_report = f"""
# {project_title}

## 1. Resumen Ejecutivo
{report_components.get("executive_summary", "N/A")}

## 2. Generalidades del Proyecto
*   **Descripción:** {general_info.get("project_description", "N/A")}
*   **Palabras Clave:** {', '.join(general_info.get("keywords", []))}

## 3. Planteamiento del Problema y Justificación
{report_components.get("problem_statement_justification", "N/A")}

## 4. Marco Teórico y Estado del Arte
{theoretical_framework.get("body", "N/A")}

## 5. Objetivos
{objectives.get("general_objective", "N/A")}
{objectives.get("specific_objectives_smart", "N/A")}

## 6. Metodología Propuesta
{report_components.get("methodology", "N/A")}

## 7. Plan de Ejecución y Gestión
{execution_plan.get("activity_schedule", "N/A")}
{execution_plan.get("risk_matrix", "N/A")}

## 8. Resultados e Impactos Esperados
{report_components.get("results_and_impacts", "N/A")}

## 9. Referencias Bibliográficas
{theoretical_framework.get("references_apa", "N/A")}
"""
    
    # 3. Preparar para la generación del PDF
    os.makedirs(REPORTS_DIR, exist_ok=True)
    sanitized_title = re.sub(r'[\s/:]+', '_', project_title).lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"{sanitized_title}_{timestamp}.pdf"
    file_path = os.path.join(REPORTS_DIR, file_name)

    try:
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = get_custom_styles()
        page_template_handler = PageTemplate()

        story = []
        
        # Añadir la imagen de portada si existe
        if image_path and os.path.exists(image_path):
            try:
                img = Image(image_path, width=15*cm, height=15*cm)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(PageBreak())
            except Exception as e:
                print(f"   ⚠️ No se pudo cargar la imagen de portada: {e}")

        # Convertir el Markdown a Flowables
        story.extend(markdown_to_flowables(full_markdown_report, styles))

        print(f"   🔨 Construyendo PDF en: {file_path}")
        doc.build(story, onFirstPage=page_template_handler.on_first_page, 
                 onLaterPages=page_template_handler.on_later_pages)
        
        print("   ✅ Reporte PDF generado exitosamente.")
        
        return {"final_report": file_path}

    except Exception as e:
        print(f"   ❌ Error al generar el PDF: {e}")
        import traceback
        traceback.print_exc()
        return {"final_report": f"Error al generar PDF: {e}"}