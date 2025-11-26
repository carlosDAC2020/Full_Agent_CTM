import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, 
                                Table, TableStyle, PageBreak, ListFlowable, ListItem)
from reportlab.platypus.tableofcontents import TableOfContents

# --- CONFIGURACIÓN DE RUTAS ---
HEADER_LOGO_PATH = "CTM_Agents/static/CotecmarLogo.png"
COVER_IMAGE_PATH = "CTM_Agents/generated_images/detección_de_anomalías_sísmicas_con_inteligencia_artificial.png"
OUTPUT_DIR = "test_reports"

# --- COLORES ---
COLOR_PRIMARY = colors.HexColor('#003366')
COLOR_SECONDARY = colors.HexColor('#0066CC')
COLOR_ACCENT = colors.HexColor('#E6F0FF')
COLOR_TEXT = colors.HexColor('#2A2A2A')

# --- CLASE PERSONALIZADA PARA GESTIONAR LA TABLA DE CONTENIDO ---
class MecanismoTOC(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        """Detecta si se acaba de agregar un título y lo registra en el TOC."""
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'CustomH1':
                # Nivel 0 en el TOC, texto, número de página actual
                self.notify('TOCEntry', (0, text, self.page))
            elif style == 'CustomH2':
                # Nivel 1 en el TOC
                self.notify('TOCEntry', (1, text, self.page))

class ProjectReportGenerator:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        self.styles = self._create_styles()
        
    def _create_styles(self):
        styles = getSampleStyleSheet()
        
        # Títulos (H1)
        styles.add(ParagraphStyle(
            name='CustomH1', parent=styles['Heading1'],
            fontSize=18, textColor=COLOR_PRIMARY, spaceAfter=12, spaceBefore=12,
            fontName='Helvetica-Bold', borderPadding=0
        ))
        
        # Subtítulos (H2)
        styles.add(ParagraphStyle(
            name='CustomH2', parent=styles['Heading2'],
            fontSize=14, textColor=COLOR_SECONDARY, spaceAfter=10, spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Sub-subtítulos (H3) - Usando Oblique para evitar error
        styles.add(ParagraphStyle(
            name='CustomH3', parent=styles['Heading3'],
            fontSize=12, textColor=colors.HexColor('#444444'), spaceAfter=8, spaceBefore=10,
            fontName='Helvetica-BoldOblique' 
        ))

        # Cuerpo
        styles.add(ParagraphStyle(
            name='CustomBody', parent=styles['Normal'],
            fontSize=10, leading=14, alignment=TA_JUSTIFY, textColor=COLOR_TEXT,
            spaceAfter=6
        ))
        

        # Tablas
        styles.add(ParagraphStyle(
            name='CellHeader', parent=styles['Normal'],
            fontSize=9, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_CENTER
        ))
        styles.add(ParagraphStyle(
            name='CellBody', parent=styles['Normal'],
            fontSize=9, leading=11, alignment=TA_LEFT
        ))

        # --- ESTILOS PARA LA TABLA DE CONTENIDO (TOC) ---
        styles.add(ParagraphStyle(
            name='TOCHeading', parent=styles['Heading1'],
            fontSize=16, textColor=COLOR_PRIMARY, spaceAfter=10, alignment=TA_CENTER
        ))
        # Nivel 1 del TOC (Coincide con H1)
        styles.add(ParagraphStyle(
            name='TOCEntry1', parent=styles['Normal'],
            fontSize=11, fontName='Helvetica-Bold', spaceAfter=5, textColor=COLOR_PRIMARY
        ))
        # Nivel 2 del TOC (Coincide con H2)
        styles.add(ParagraphStyle(
            name='TOCEntry2', parent=styles['Normal'],
            fontSize=10, leftIndent=20, spaceAfter=2, textColor=COLOR_TEXT
        ))

            # Estilo APA Reference corregido
        styles.add(ParagraphStyle(
            name='APA_Reference', 
            parent=styles['Normal'],
            fontSize=10, 
            leading=14, 
            alignment=TA_LEFT,
            # El truco de la sangría francesa:
            leftIndent=36,        # Mueve todo el bloque a la derecha
            firstLineIndent=-36,  # Tira solo la primera línea a la izquierda
            spaceAfter=6
        ))

        return styles

    def _header_footer_layout(self, canvas, doc):
        canvas.saveState()
        page_width, page_height = letter
        margin = 2 * cm
        
        # --- ENCABEZADO CORREGIDO ---
        logo_width = 4 * cm
        logo_height = 1.5 * cm
        
        # CORRECCIÓN DE POSICIÓN: Bajamos el logo restando más cm (2.5 en vez de 1.5)
        # page_height (27.9cm) - 2.5cm deja espacio visual arriba.
        y_pos = page_height - 2.5 * cm 
        x_pos = page_width - margin - logo_width
        
        if os.path.exists(HEADER_LOGO_PATH):
            try:
                canvas.drawImage(HEADER_LOGO_PATH, x_pos, y_pos, width=logo_width, height=logo_height, mask='auto', preserveAspectRatio=True)
            except:
                pass
        else:
            # Placeholder visual si falla la carga
            canvas.setFillColor(colors.lightgrey)
            canvas.rect(x_pos, y_pos, logo_width, logo_height, fill=1)
            canvas.setFillColor(colors.black)
            canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(x_pos + logo_width/2, y_pos + logo_height/2 - 3, "[LOGO]")

        # --- PIE DE PÁGINA ---
        canvas.setStrokeColor(COLOR_SECONDARY)
        canvas.setLineWidth(0.5)
        canvas.line(margin, 2*cm, page_width - margin, 2*cm)
        
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        canvas.drawString(margin, 1.5*cm, f"Proyecto: {self.data['titulo_corto']}")
        canvas.drawRightString(page_width - margin, 1.5*cm, f"Página {doc.page}")
        
        canvas.restoreState()

    def create_table(self, data, col_widths=None, header_bg=COLOR_SECONDARY):
        formatted_data = []
        for i, row in enumerate(data):
            new_row = []
            for cell in row:
                style = self.styles['CellHeader'] if i == 0 else self.styles['CellBody']
                if isinstance(cell, str):
                    new_row.append(Paragraph(cell, style))
                else:
                    new_row.append(cell)
            formatted_data.append(new_row)

        t = Table(formatted_data, colWidths=col_widths)
        style_cmds = [
            ('BACKGROUND', (0, 0), (-1, 0), header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]
        for i in range(1, len(data)):
            bg = COLOR_ACCENT if i % 2 == 0 else colors.white
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

        t.setStyle(TableStyle(style_cmds))
        return t

    def generate(self):
        # Usamos nuestra clase personalizada MecanismoTOC en lugar de SimpleDocTemplate
        doc = MecanismoTOC(
            self.filename, pagesize=letter,
            rightMargin=2*cm, leftMargin=2*cm, topMargin=3*cm, bottomMargin=2.5*cm
        )
        
        story = []
        S = self.styles

        # --- PORTADA / TÍTULO INICIAL ---
        story.append(Paragraph("Presentacion de Proyecto", S['CustomH1']))
        story.append(Spacer(1, 1*cm))

        # --- TABLA DE CONTENIDO ---
        story.append(Paragraph("Tabla de Contenido", S['TOCHeading']))
        toc = TableOfContents()
        toc.levelStyles = [S['TOCEntry1'], S['TOCEntry2']] # Asignar estilos a niveles 0 y 1
        story.append(toc)
        story.append(PageBreak())

        # --- CONTENIDO (Sin índices numéricos en los títulos) ---

        # 1. GENERALIDADES
        story.append(Paragraph("Generalidades del Proyecto", S['CustomH1'])) # Nivel 0 TOC
        story.append(Paragraph("Información Básica", S['CustomH2']))         # Nivel 1 TOC
        
        data_gen = [
            ["Atributo", "Valor"],
            ["Código Registro", self.data['codigo']],
            ["Título", self.data['titulo_completo']],
            ["Convocatoria", self.data['convocatoria']],
            ["Programa", self.data['programa']],
            ["Entidad", self.data['entidad']],
            ["Línea Temática", self.data['linea_tematica']],
            ["Duración", f"{self.data['duracion']} Meses"],
            ["Área OCDE", self.data['area_ocde']]
        ]
        story.append(self.create_table(data_gen, col_widths=[6*cm, 11*cm]))
        story.append(Spacer(1, 0.5*cm))

        # 2. PALABRAS CLAVE
        story.append(Paragraph("Palabras Clave", S['CustomH1']))
        story.append(Paragraph(f"<b>Términos:</b> {', '.join(self.data['keywords'])}.", S['CustomBody']))
        story.append(Spacer(1, 0.5*cm))

        # 3. ENTIDADES
        story.append(Paragraph("Entidades Participantes", S['CustomH1']))
        data_ent = [["Nombre Entidad", "Rol"]] + self.data['entidades']
        story.append(self.create_table(data_ent, col_widths=[12*cm, 5*cm]))
        story.append(Spacer(1, 0.5*cm))

        # 4. EQUIPOS
        story.append(Paragraph("Equipos de Trabajo", S['CustomH1']))
        
        story.append(Paragraph("Equipo Técnico-Científico", S['CustomH2']))
        data_eq_tec = [["Entidad", "Tipo", "Rol"]] + self.data['equipo_tecnico']
        story.append(self.create_table(data_eq_tec, col_widths=[6*cm, 5*cm, 6*cm]))
        
        story.append(Paragraph("Equipo Administrativo", S['CustomH2']))
        data_eq_adm = [["Nombre", "Cédula", "Rol"]] + self.data['equipo_admin']
        story.append(self.create_table(data_eq_adm, col_widths=[7*cm, 4*cm, 6*cm]))
        story.append(PageBreak())

        # 5. DESCRIPCIONES
        story.append(Paragraph("Descripciones y Contenido", S['CustomH1']))
        
        story.append(Paragraph("Portada del Proyecto", S['CustomH2']))
        if os.path.exists(COVER_IMAGE_PATH):
            try:
                img = Image(COVER_IMAGE_PATH, width=14*cm, height=9*cm, kind='proportional')
                img.hAlign = 'CENTER'
                story.append(img)
            except:
                story.append(Paragraph("[Error visualizando imagen]", S['CustomBody']))
        else:
            story.append(Spacer(1, 0.5*cm))
            t_ph = Table([["[IMAGEN DE PORTADA]"]], colWidths=[14*cm], rowHeights=[4*cm])
            t_ph.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),1,colors.grey)]))
            story.append(t_ph)

        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("Resumen Ejecutivo", S['CustomH2']))
        story.append(Paragraph(self.data['resumen_ejecutivo'], S['CustomBody']))

        story.append(Paragraph("Justificación", S['CustomH2']))
        story.append(Paragraph(self.data['justificacion'], S['CustomBody']))
        
        # 6. OBJETIVOS
        story.append(Paragraph("Objetivos (SMART)", S['CustomH1']))
        story.append(Paragraph(f"<b>Objetivo General:</b> {self.data['obj_general']}", S['CustomBody']))
        
        for obj in self.data['obj_especificos']:
            story.append(Paragraph(f"<b>{obj['titulo']}</b>", S['CustomH3']))
            bullets = [
                ListItem(Paragraph(f"<b>Específico:</b> {obj['S']}", S['CustomBody'])),
                ListItem(Paragraph(f"<b>Medible:</b> {obj['M']}", S['CustomBody'])),
                ListItem(Paragraph(f"<b>Alcanzable:</b> {obj['A']}", S['CustomBody'])),
                ListItem(Paragraph(f"<b>Relevante:</b> {obj['R']}", S['CustomBody'])),
                ListItem(Paragraph(f"<b>Temporal:</b> {obj['T']}", S['CustomBody'])),
            ]
            story.append(ListFlowable(bullets, bulletType='bullet', start='square', leftIndent=15))

        # 8. EJECUCIÓN
        story.append(PageBreak())
        story.append(Paragraph("Plan de Ejecución", S['CustomH1']))
        
        story.append(Paragraph("Cronograma de Actividades", S['CustomH2']))
        data_crono = [["Fase", "Actividad", "Entregable", "Semanas"]] + self.data['cronograma']
        story.append(self.create_table(data_crono, col_widths=[2.5*cm, 6.5*cm, 5.5*cm, 2.5*cm]))
        
        story.append(Paragraph("Matriz de Riesgos", S['CustomH2']))
        data_riesgos = [["Riesgo", "Prob.", "Imp.", "Mitigación"]] + self.data['riesgos']
        story.append(self.create_table(data_riesgos, col_widths=[5*cm, 2*cm, 2*cm, 8*cm]))

        # 9. RESULTADOS
        story.append(Paragraph("Resultados e Impactos", S['CustomH1']))
        res_bullets = [ListItem(Paragraph(r, S['CustomBody'])) for r in self.data['resultados']]
        story.append(ListFlowable(res_bullets, bulletType='bullet', leftIndent=15))

        # 10. REFERENCIAS
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph("Referencias Bibliográficas (APA)", S['CustomH1']))
        for ref in self.data['referencias']:
            story.append(Paragraph(ref, S['APA_Reference']))

        # IMPORTANTE: Usar multiBuild para que el TOC se genere (requiere 2 pasadas)
        doc.multiBuild(story, onFirstPage=self._header_footer_layout, onLaterPages=self._header_footer_layout)
        print(f"✅ Reporte generado exitosamente: {self.filename}")

# --- DATOS DE PRUEBA ---
DUMMY_DATA = {
    "titulo_corto": "Sismología IA Rural",
    "titulo_completo": "Detección de Anomalías Sísmicas con Inteligencia Artificial en Zonas Rurales de Difícil Acceso",
    "codigo": "109755-2025",
    "convocatoria": "950-2024 COLOMBIA INTELIGENTE",
    "programa": "Ciencias de la Tierra",
    "entidad": "ESCUELA NAVAL DE CADETES",
    "linea_tematica": "Gestión del Riesgo",
    "duracion": "24",
    "area_ocde": "2. Ingeniería y Tecnología",
    "keywords": ["Sismología", "Deep Learning", "IoT", "Alerta Temprana"],
    "entidades": [
        ["Escuela Naval", "Ejecutor"],
        ["Univ. Cartagena", "Co-Ejecutor"]
    ],
    "equipo_tecnico": [
        ["Escuela Naval", "Academia", "Investigador Principal"],
        ["TechSolutions", "Privado", "Arquitecto"]
    ],
    "equipo_admin": [
        ["Juan Pérez", "1.045.XXX.XXX", "Gerente de Proyecto"]
    ],
    "resumen_ejecutivo": "Este proyecto busca democratizar el acceso a sistemas de alerta temprana...",
    "justificacion": "Las zonas rurales carecen de monitoreo...",
    "obj_general": "Desarrollar sistema de alerta temprana con IA.",
    "obj_especificos": [
        {"titulo": "Objetivo 1", "S": "Red sensores", "M": "100% operativos", "A": "LoRaWAN", "R": "Recolección", "T": "Mes 6"}
    ],
    "cronograma": [
        ["Fase 1", "Diseño", "Planos", "4"],
        ["Fase 2", "Datos", "Dataset", "8"]
    ],
    "riesgos": [
        ["Fallo Sensores", "Media", "Alto", "Redundancia"]
    ],
    "resultados": ["Prototipo TRL-6", "Software Web"],
    "referencias": [
    # Nota el uso de <i> y </i> para cursivas
        "Airlangga, G. (2024). Advanced machine learning techniques. <i>Journal of Geophysics, 45</i>(2), 112-130. https://doi.org/10.1002/jg.example",
        
        "Lin, J. (2025). Anomaly detection in seismic data. <i>Seismological Research Letters, 96</i>(1), 45-58. https://doi.org/10.1785/022024",
        
        "Wang, S., & Nishio, M. (2025). Optical flow‐based structural anomaly detection. <i>Computer-Aided Civil and Infrastructure Engineering, 38</i>, 201-215."
    ]
}

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f"Proyecto_CTM__v2_{timestamp}.pdf"
    full_path = os.path.join(OUTPUT_DIR, filename)
    print("Generando reporte...")
    report_gen = ProjectReportGenerator(full_path, DUMMY_DATA)
    report_gen.generate()