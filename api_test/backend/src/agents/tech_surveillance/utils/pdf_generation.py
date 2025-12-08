import re
import html
from datetime import datetime
from pathlib import Path

# Importaciones de ReportLab
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, SimpleDocTemplate, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter


# --- Colores y Estilos Mejorados ---
COTECMAR_BLUE = colors.HexColor('#0066CC')
COTECMAR_DARK_BLUE = colors.HexColor('#003366')
COTECMAR_GRAY = colors.HexColor('#4A4A4A')
COLOR_ACCENT = colors.HexColor('#E6F0FF')
GOLD_ACCENT = colors.HexColor('#D4AF37')  # Dorado elegante para marcos

def get_custom_styles():
    """Crea una hoja de estilos personalizada mejorada."""
    styles = getSampleStyleSheet()
    
    if 'H1' not in styles:
        styles.add(ParagraphStyle(
            name='H1', 
            fontSize=18, 
            fontName='Helvetica-Bold', 
            textColor=COTECMAR_DARK_BLUE, 
            spaceAfter=14, 
            alignment=TA_LEFT,
            borderPadding=(0, 0, 5, 0)
        ))
    if 'H2' not in styles:
        styles.add(ParagraphStyle(
            name='H2', 
            fontSize=14, 
            fontName='Helvetica-Bold', 
            textColor=COTECMAR_BLUE, 
            spaceBefore=16, 
            spaceAfter=10, 
            alignment=TA_LEFT,
            leftIndent=0,
            borderWidth=0,
            borderColor=COTECMAR_BLUE,
            borderPadding=(0, 0, 3, 0)
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
            alignment=TA_LEFT,  # ← CAMBIO: era TA_JUSTIFY
            spaceAfter=6,
            textColor=colors.HexColor('#2C2C2C')
        ))
    if 'CustomBullet' not in styles:
        styles.add(ParagraphStyle(
            name='CustomBullet', 
            parent=styles['Body'], 
            leftIndent=20, 
            spaceBefore=2, 
            spaceAfter=2,
            bulletIndent=10
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
    
    if 'TOCHeading1' not in styles:
        styles.add(ParagraphStyle(
            name='TOCHeading1', 
            fontSize=11, 
            fontName='Helvetica-Bold', 
            leftIndent=0, 
            spaceBefore=6, 
            spaceAfter=3,
            textColor=COTECMAR_DARK_BLUE
        ))
    if 'TOCHeading2' not in styles:
        styles.add(ParagraphStyle(
            name='TOCHeading2', 
            fontSize=10, 
            fontName='Helvetica', 
            leftIndent=25, 
            spaceBefore=2, 
            spaceAfter=2
        ))
    if 'TOCHeading3' not in styles:
        styles.add(ParagraphStyle(
            name='TOCHeading3', 
            fontSize=9, 
            fontName='Helvetica-Oblique', 
            leftIndent=45, 
            spaceBefore=0, 
            spaceAfter=2,
            textColor=COTECMAR_GRAY
        ))

    return styles

def clean_text(text):
    """Escapa caracteres XML y convierte Markdown básico a etiquetas ReportLab."""
    if not text:
        return ""
    text = html.escape(text, quote=False)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    return text

def process_table(table_text, styles):
    """Convierte texto de tabla Markdown a un objeto Table de ReportLab mejorado."""
    lines = table_text.strip().split('\n')
    data = []
    
    for line in lines:
        if '---' in line:
            continue
            
        raw_cells = line.split('|')
        
        if len(raw_cells) > 2:
            row_content = raw_cells[1:-1]
        else:
            row_content = raw_cells

        row_cleaned = [cell.strip() for cell in row_content]
        
        if not any(row_cleaned):
            continue

        row_flowables = []
        for i, cell_text in enumerate(row_cleaned):
            style = styles['TableHeader'] if len(data) == 0 else styles['TableCell']
            text_content = clean_text(cell_text)
            
            if not text_content:
                text_content = "&nbsp;"
                
            row_flowables.append(Paragraph(text_content, style))
        
        data.append(row_flowables)

    if not data:
        return None

    num_cols = len(data[0])
    for row in data:
        while len(row) < num_cols:
            row.append(Paragraph("", styles['TableCell']))
            
    available_width = 17*cm 
    
    if num_cols == 4:
        col_widths = [3*cm, 7*cm, 4*cm, 3*cm]
    elif num_cols == 5:
        col_widths = [1.5*cm, 5*cm, 2.5*cm, 2.5*cm, 5.5*cm]
    else:
        col_width = available_width / num_cols
        col_widths = [col_width] * num_cols
    
    t = Table(data, colWidths=col_widths)
    
    # Estilo mejorado con sombras sutiles
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COTECMAR_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.75, colors.HexColor('#CCCCCC')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, COTECMAR_DARK_BLUE),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('WORDWRAP', (0, 0), (-1, -1), True),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_ACCENT]),
    ]))
    return t

def create_general_info_table(data_dict, styles):
    """Crea una tabla de información básica mejorada."""
    table_data = [["Atributo", "Valor"]]
    
    for key, value in data_dict.items():
        key_p = Paragraph(f"<b>{key}</b>", styles['TableCell'])
        value_p = Paragraph(str(value) if value else "N/A", styles['TableCell'])
        table_data.append([key_p, value_p])

    col_widths = [5*cm, 12*cm]
    t = Table(table_data, colWidths=col_widths)

    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), COTECMAR_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.75, colors.HexColor('#CCCCCC')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, COTECMAR_DARK_BLUE),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]

    for i in range(1, len(table_data)):
        bg_color = COLOR_ACCENT if i % 2 == 0 else colors.white
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg_color))

    t.setStyle(TableStyle(style_cmds))
    return t


class ReportDocTemplate(SimpleDocTemplate):
    """Plantilla personalizada con detección automática de encabezados para TOC."""
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'Paragraph':
            if hasattr(flowable, '_toc_level') and hasattr(flowable, '_toc_key'):
                text = flowable.getPlainText()
                level = flowable._toc_level
                key = flowable._toc_key
                self.notify('TOCEntry', (level, text, self.page, key))

def markdown_to_flowables(markdown_text, styles):
    """Parsea markdown con mejor manejo de espaciado y elementos visuales."""
    flowables = []
    lines = markdown_text.split('\n')
    i = 0
    unique_id_counter = 0 
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 1. Tablas
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and (lines[i].strip().startswith('|') or lines[i].strip() == ""):
                if lines[i].strip():
                    table_lines.append(lines[i])
                i += 1
            table = process_table('\n'.join(table_lines), styles)
            if table:
                flowables.append(Spacer(1, 0.3*cm))
                flowables.append(table)
                flowables.append(Spacer(1, 0.5*cm))
            continue
            
        # 2. Encabezados
        elif line.startswith('#'):
            clean_line = line.lstrip('#').replace('*', '').strip()
            text_content = clean_text(clean_line)
            
            bookmark_name = f"section_{unique_id_counter}"
            unique_id_counter += 1
            
            if line.startswith('#### '):
                style = styles['H3'] 
                level = 2
            elif line.startswith('### '):
                style = styles['H3']
                level = 2
            elif line.startswith('## '):
                style = styles['H2']
                level = 1
                # Agregar línea decorativa antes de H2
                flowables.append(Spacer(1, 0.3*cm))
            else:
                style = styles['H1']
                level = 0
            
            p_text = f'{text_content}<a name="{bookmark_name}"/>'
            p = Paragraph(p_text, style)
            
            p._toc_level = level
            p._toc_key = bookmark_name
            
            flowables.append(p)

        # 3. Listas
        elif line.startswith('* ') or line.startswith('- '):
            item_text = line[2:]
            bullet_style = styles['CustomBullet']
            flowables.append(Paragraph(f'<font color="{COTECMAR_BLUE}">●</font> {clean_text(item_text)}', bullet_style))
            
        # 4. Párrafos normales
        elif line:
            flowables.append(Paragraph(clean_text(line), styles['Body']))
        
        if line and not line.startswith('|'):
             flowables.append(Spacer(1, 0.2*cm))
             
        i += 1
        
    return flowables


class PageTemplate:
    """Plantilla de página con marco decorativo y pie de página mejorado."""
    def __init__(self, page_size=letter):
        self.page_width, self.page_height = page_size
        self.left_margin = 2 * cm
        self.right_margin = 2 * cm
        self.bottom_margin = 2.5 * cm
        self.top_margin = 2.5 * cm

    def draw_cover_frame(self, canvas, doc):
        """Dibuja un marco elegante alrededor de la portada."""
        canvas.saveState()
        
        # Marco exterior - dorado elegante
        canvas.setStrokeColor(GOLD_ACCENT)
        canvas.setLineWidth(3)
        margin = 0.8*cm
        canvas.rect(margin, margin, 
                   self.page_width - 2*margin, 
                   self.page_height - 2*margin)
        
        # Marco interior - azul COTECMAR
        canvas.setStrokeColor(COTECMAR_BLUE)
        canvas.setLineWidth(1.5)
        inner_margin = 1.1*cm
        canvas.rect(inner_margin, inner_margin,
                   self.page_width - 2*inner_margin,
                   self.page_height - 2*inner_margin)
        
        # Línea decorativa en la parte inferior
        canvas.setStrokeColor(COTECMAR_DARK_BLUE)
        canvas.setLineWidth(0.5)
        y_pos = 1.5*cm
        canvas.line(self.left_margin, y_pos, 
                   self.page_width - self.right_margin, y_pos)
        
        canvas.restoreState()

    def on_first_page(self, canvas, doc):
        """Primera página con marco decorativo."""
        self.draw_cover_frame(canvas, doc)

    def on_later_pages(self, canvas, doc):
        """Páginas posteriores con encabezado y pie de página."""
        self.draw_header(canvas, doc)
        self.draw_footer(canvas, doc)

    def draw_header(self, canvas, doc):
        """Dibuja encabezado en páginas interiores."""
        canvas.saveState()
        canvas.setStrokeColor(COTECMAR_BLUE)
        canvas.setLineWidth(1)
        canvas.line(self.left_margin, self.page_height - 1.5*cm,
                   self.page_width - self.right_margin, self.page_height - 1.5*cm)
        canvas.restoreState()

    def draw_footer(self, canvas, doc):
        """Dibuja pie de página mejorado."""
        canvas.saveState()
        
        # Línea decorativa superior
        canvas.setStrokeColor(COTECMAR_BLUE)
        canvas.setLineWidth(1)
        # Dibujamos la línea
        canvas.line(self.left_margin, self.bottom_margin - 0.3*cm, 
                   self.page_width - self.right_margin, self.bottom_margin - 0.3*cm)
        
        # Texto del pie (Izquierda)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(COTECMAR_GRAY)
        footer_text = f"Sistema de Vigilancia Tecnológica | {datetime.now().strftime('%B %Y')}"
        # Bajamos un poco más el texto para que respire respecto a la línea
        canvas.drawString(self.left_margin, self.bottom_margin - 1.0*cm, footer_text)
        
        # --- CORRECCIÓN AQUÍ: Número de página ---
        page_num = canvas.getPageNumber()
        
        canvas.setFillColor(COTECMAR_BLUE)
        # Ubicación X: Alineado al margen derecho
        x_pos = self.page_width - self.right_margin - 0.5*cm 
        
        # Ubicación Y: Lo bajamos más (antes era 0.8, ahora 1.2) para que no toque la línea
        y_circle = self.bottom_margin - 1.2*cm  
        
        # Dibujar círculo
        canvas.circle(x_pos, y_circle, 0.35*cm, fill=0)
        
        # Número dentro del círculo
        canvas.setFillColor(COTECMAR_DARK_BLUE)
        canvas.setFont('Helvetica-Bold', 9)
        # Ajuste fino vertical (-0.12cm centra mejor visualmente la fuente Helvetica)
        canvas.drawCentredString(x_pos, y_circle - 0.12*cm, str(page_num))
        
        canvas.restoreState()