import os
import re
import html
from datetime import datetime
from pathlib import Path

# Importaciones de ReportLab
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

# Asumiendo que estas importaciones existen en tu proyecto
from agents.tech_surveillance.state import GraphState, ReportSchema

REPORTS_DIR = "generated_reports"

# --- Colores y Estilos ---
COTECMAR_BLUE = colors.HexColor('#0066CC')
COTECMAR_DARK_BLUE = colors.HexColor('#003366')
COTECMAR_GRAY = colors.HexColor('#4A4A4A')

def get_custom_styles():
    """Crea una hoja de estilos personalizada."""
    styles = getSampleStyleSheet()
    # (Tus estilos originales se mantienen igual, aseguramos que existan)
    if 'H1' not in styles:
        styles.add(ParagraphStyle(name='H1', fontSize=18, fontName='Helvetica-Bold', textColor=COTECMAR_DARK_BLUE, spaceAfter=14, alignment=TA_LEFT))
    if 'H2' not in styles:
        styles.add(ParagraphStyle(name='H2', fontSize=14, fontName='Helvetica-Bold', textColor=COTECMAR_BLUE, spaceBefore=12, spaceAfter=10, alignment=TA_LEFT))
    if 'H3' not in styles:
        styles.add(ParagraphStyle(name='H3', fontSize=12, fontName='Helvetica-Bold', textColor=COTECMAR_GRAY, spaceBefore=10, spaceAfter=8, alignment=TA_LEFT))
    if 'Body' not in styles:
        styles.add(ParagraphStyle(name='Body', fontSize=10, fontName='Helvetica', leading=14, alignment=TA_JUSTIFY, spaceAfter=6))
    if 'CustomBullet' not in styles:
        styles.add(ParagraphStyle(name='CustomBullet', parent=styles['Body'], leftIndent=20, spaceBefore=2, spaceAfter=2))
    if 'TableHeader' not in styles:
        styles.add(ParagraphStyle(name='TableHeader', fontSize=9, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_CENTER))
    if 'TableCell' not in styles:
        styles.add(ParagraphStyle(name='TableCell', fontSize=8, fontName='Helvetica', leading=10, alignment=TA_LEFT))
    return styles

def clean_text(text):
    """Escapa caracteres XML y convierte Markdown básico a etiquetas ReportLab."""
    if not text:
        return ""
    # 1. Escapar caracteres XML primero (importante para evitar crashes con & < >)
    text = html.escape(text, quote=False)
    
    # 2. Convertir Markdown a etiquetas XML soportadas por ReportLab
    # Negrita: **texto** -> <b>texto</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Cursiva: *texto* -> <i>texto</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    return text

def process_table(table_text, styles):
    """Convierte texto de tabla Markdown a un objeto Table de ReportLab."""
    lines = table_text.strip().split('\n')
    data = []
    
    for line in lines:
        # Omitir la línea separadora (ej: |---|---|)
        if '---' in line:
            continue
        
        # Dividir por la tubería y limpiar espacios
        # [1:-1] elimina el primer y último elemento vacío que genera split('|')
        row_raw = [cell.strip() for cell in line.split('|')]
        
        # Filtrar celdas vacías generadas por los bordes de la tabla
        row_cleaned = [cell for cell in row_raw if cell]
        
        # Si la fila está vacía después de limpiar, continuar
        if not row_cleaned:
            continue

        # Convertir texto de celda a Paragraphs para permitir wrap de texto
        row_flowables = []
        for i, cell_text in enumerate(row_cleaned):
            style = styles['TableHeader'] if len(data) == 0 else styles['TableCell']
            row_flowables.append(Paragraph(clean_text(cell_text), style))
        
        data.append(row_flowables)

    if not data:
        return None

    # Calcular anchos de columna de forma inteligente
    num_cols = len(data[0])
    available_width = 17*cm  # Ancho disponible en la página (ajustado para márgenes)
    
    # Estrategia de anchos según número de columnas
    if num_cols == 4:
        # Para tablas de 4 columnas (como Cronograma): 
        # Columna 1 (Fase) más estrecha, Columna 2 (Actividad) más ancha
        col_widths = [3*cm, 7*cm, 4*cm, 3*cm]
    elif num_cols == 5:
        # Para tablas de 5 columnas (como Matriz de Riesgos):
        # Distribuir más proporcionalmente
        col_widths = [1.5*cm, 5*cm, 2.5*cm, 2.5*cm, 5.5*cm]
    else:
        # Distribución uniforme para otras tablas
        col_width = available_width / num_cols
        col_widths = [col_width] * num_cols
    
    t = Table(data, colWidths=col_widths)
    
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COTECMAR_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('WORDWRAP', (0, 0), (-1, -1), True),  # Importante: habilitar word wrap
    ]))
    return t

def markdown_to_flowables(markdown_text, styles):
    """Parsea el markdown completo y devuelve una lista de Flowables."""
    flowables = []
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 1. Detección de Tabla
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and (lines[i].strip().startswith('|') or lines[i].strip() == ""):
                if lines[i].strip(): # Solo agregar si tiene contenido
                    table_lines.append(lines[i])
                i += 1
            
            table = process_table('\n'.join(table_lines), styles)
            if table:
                flowables.append(table)
                flowables.append(Spacer(1, 0.5*cm))
            continue # El índice ya avanzó
            
        # 2. Encabezados
        if line.startswith('### '):
            # Limpieza especial: evitar duplicidad visual si el texto también tiene **
            clean_line = line[4:].replace('**', '').strip()
            flowables.append(Paragraph(clean_text(clean_line), styles['H3']))
        elif line.startswith('## '):
            clean_line = line[3:].replace('**', '').strip()
            flowables.append(Paragraph(clean_text(clean_line), styles['H2']))
        elif line.startswith('# '):
            clean_line = line[2:].replace('**', '').strip()
            flowables.append(Paragraph(clean_text(clean_line), styles['H1']))
            
        # 3. Listas
        elif line.startswith('* ') or line.startswith('- '):
            item_text = line[2:]
            flowables.append(Paragraph(f'• {clean_text(item_text)}', styles['CustomBullet']))
            
        # 4. Párrafos normales
        elif line:
            flowables.append(Paragraph(clean_text(line), styles['Body']))
        
        # Espaciado entre párrafos (simple)
        if line:
             flowables.append(Spacer(1, 0.2*cm))
             
        i += 1
        
    return flowables

# --- Plantilla de Página (Sin cambios, asumiendo que funciona) ---
class PageTemplate:
    def __init__(self, page_size=letter):
        self.page_width, self.page_height = page_size
        self.left_margin = 2 * cm
        self.right_margin = 2 * cm
        self.bottom_margin = 2.5 * cm

    def on_first_page(self, canvas, doc):
        self.draw_footer(canvas, doc)

    def on_later_pages(self, canvas, doc):
        self.draw_footer(canvas, doc)

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

# --- Nodo Principal ---

def report_node(state: GraphState):
    print("--- Ejecutando Nodo: Generación de Reporte PDF ---")
    
    report_components = state.get("report_components")
    if not report_components:
        return {}

    # Convertir a objeto si es dict
    if isinstance(report_components, dict):
        # Usamos un truco simple si ReportSchema da problemas, o usamos el schema real
        try:
            data = ReportSchema(**report_components)
        except:
            # Fallback: crear una clase simple al vuelo o usar diccionario
            class Data: pass
            data = Data()
            for k, v in report_components.items():
                setattr(data, k, v)
    else:
        data = report_components

    # --- Extracción de Datos (Soporte para Pydantic y Dict) ---
    
    # Helper para obtener atributos de forma segura (sea dict o objeto)
    def get_field(obj, field, default=None):
        if isinstance(obj, dict):
            return obj.get(field, default)
        return getattr(obj, field, default)

    # Helper para obtener el contenido de una sección (string o None)
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

    # Construcción del Markdown
    full_markdown_report = f"""
# {title}

## 1. Resumen Ejecutivo
{exec_summary}

## 2. Generalidades del Proyecto
*   **Descripción:** {desc}
*   **Palabras Clave:** {', '.join(kws) if kws else 'N/A'}

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

    # Limpieza de contenido repetitivo conocido (Hack para arreglar el output del LLM)
    # Elimina subtítulos repetidos como "### **1. Resumen Ejecutivo**" que vienen después del H2
    full_markdown_report = re.sub(r'## (\d+\..+)\n+### \*\*\1\*\*', r'## \1', full_markdown_report)
    full_markdown_report = re.sub(r'## (\d+\..+)\n+## \1', r'## \1', full_markdown_report)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    sanitized_title = re.sub(r'[\s/:]+', '_', title).lower()[:50]
    file_name = f"{sanitized_title}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    file_path = os.path.join(REPORTS_DIR, file_name)

    try:
        doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=2*cm, leftMargin=2*cm, topMargin=2.5*cm, bottomMargin=2.5*cm)
        styles = get_custom_styles()
        pt = PageTemplate()
        
        story = []
        
        # Si tienes una imagen en el estado:
        image_path = state.get("generated_image_path") 
        if image_path and os.path.exists(image_path):
            img = Image(image_path, width=15*cm, height=10*cm, kind='proportional') # Kind proportional evita deformación
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 1*cm))

        story.extend(markdown_to_flowables(full_markdown_report, styles))

        doc.build(story, onFirstPage=pt.on_first_page, onLaterPages=pt.on_later_pages)
        print(f"   ✅ Reporte PDF generado: {file_path}")

        # guardar un markdown con el tetxo del reporte 
        markdown_file_path = os.path.join(REPORTS_DIR, f"{sanitized_title}_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(full_markdown_report)
        print(f"   ✅ Reporte Markdown generado: {markdown_file_path}")
        
        return {"final_report": file_path}

    except Exception as e:
        print(f"   ❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        return {"final_report": f"Error: {e}"}