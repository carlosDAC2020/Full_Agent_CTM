import os
from datetime import datetime
from fpdf import FPDF
from typing import List, Dict, Any, Union
from backend.app.core.config import settings

class PDF(FPDF):
    # --- PALETA DE COLORES Y FUENTES DEL DISEÑO ---
    COLOR_HEADER = (0, 68, 136)
    COLOR_TITLE = (26, 32, 44)
    COLOR_SECTION_TITLE = (112, 128, 150)
    COLOR_BODY_TEXT = (74, 85, 104)
    COLOR_BACKGROUND_GREY = (247, 250, 252)
    FONT_SERIF = 'RobotoSlab'
    FONT_SANS = 'Roboto'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Path detection for Docker and local environments
        # This file is in: backend/app/services/magazine/pdf_engine.py
        # In Docker: /app/backend/app/services/magazine/pdf_engine.py
        # In local: <project_root>/Intecmar_api/backend/app/services/magazine/pdf_engine.py
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Detect if running in Docker (working directory is /app)
        # Go up from backend/app/services/magazine -> backend/app/services -> backend/app -> backend -> /app (root)
        potential_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..', '..'))
        
        # Check if this is Docker environment by looking for backend directory at the right level
        docker_backend = os.path.join(potential_root, 'backend')
        if os.path.isdir(docker_backend) and os.path.exists(os.path.join(docker_backend, 'app')):
            # Running in Docker: root is /app
            self.root_dir = potential_root
        else:
            # Running locally: go up 3 levels to Intecmar_api root
            self.root_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        
        # Set paths relative to root
        self.img_dir = os.path.join(self.root_dir, 'img')
        self.backend_dir = os.path.join(self.root_dir, 'backend')
        self.fonts_dir = os.path.join(self.backend_dir, 'fonts')
        
        # Load fonts from the detected fonts directory
        if os.path.isdir(self.fonts_dir):
            self._load_fonts(self.fonts_dir)
        else:
            # Fallback: try loading from backend directory directly
            self._load_fonts(self.backend_dir)
        
    def _load_fonts(self, base_path):
        """Carga las fuentes personalizadas para el diseño."""
        try:
            # We need to ensure these files exist at base_path
            self.add_font(self.FONT_SANS, '', os.path.join(base_path, 'Roboto-Regular.ttf'), uni=True)
            self.add_font(self.FONT_SANS, 'B', os.path.join(base_path, 'Roboto-Bold.ttf'), uni=True)
            self.add_font(self.FONT_SERIF, 'B', os.path.join(base_path, 'RobotoSlab-Bold.ttf'), uni=True)
        except Exception as e:
            # Fallback to standard fonts if custom ones fail, or just log
            print(f"Warning: Error cargando fuentes desde {base_path}. Detalle: {e}")

    def footer(self):
        pass
    
    def draw_section(self, icon_name, title, text, width):
        """Dibuja una sección con un icono de imagen, título y texto."""
        icon_path = os.path.join(self.img_dir, icon_name)
        y_start = self.get_y()
        x_start = self.get_x()

        if os.path.exists(icon_path):
            self.image(icon_path, x=x_start, y=y_start, w=10)

        self.set_xy(x_start + 15, y_start)
        self.set_font(self.FONT_SANS, 'B', 9)
        self.set_text_color(*self.COLOR_SECTION_TITLE)
        self.cell(width - 15, 10, title.upper())
        self.ln(15)

        self.set_x(x_start)
        self.set_font(self.FONT_SANS, '', 11)
        self.set_text_color(*self.COLOR_BODY_TEXT)
        if isinstance(text, list):
            text = '\n• ' + '\n• '.join(filter(None, text))
        self.multi_cell(width, 16, str(text))
        self.ln(10)

    def draw_call_card(self, item: dict):
        self.add_page()
        
        # --- 1. CABECERA (CON LÓGICA DINÁMICA) ---
        type_mapping = {
            'convocatoria_nacional': 'Convocatorias Nacionales',
            'convocatoria_internacional': 'Convocatorias Internacionales',
            'evento': 'Eventos'
        }
        item_type = item.get("type", "convocatoria_nacional").lower()
        header_text = type_mapping.get(item_type, 'Convocatorias')

        self.set_fill_color(*self.COLOR_HEADER)
        self.set_text_color(255, 255, 255)
        self.set_font(self.FONT_SANS, '', 18)
        self.cell(0, 30, f"   {header_text}", fill=True, align='L', new_x='LMARGIN', new_y='NEXT')
        
        icon_grid_path = os.path.join(self.img_dir, 'logo-cotecmar.png')
        if os.path.exists(icon_grid_path):
            self.image(icon_grid_path, x=self.w - self.r_margin - 66, y=self.t_margin - 34, w=84)

        self.ln(25)

        # --- 2. TÍTULO PRINCIPAL ---
        self.set_font(self.FONT_SERIF, 'B', 24)
        self.set_text_color(*self.COLOR_TITLE)
        self.multi_cell(0, 30, item.get("title", "Sin Título"))
        self.ln(25)

        # --- Definición de la geometría de las columnas ---
        y_columns_start = self.get_y()
        col_width = (self.w - self.l_margin - self.r_margin - 30) / 2
        gutter = 30
        x_col_left = self.l_margin
        x_col_right = self.l_margin + col_width + gutter

        # --- Columna Izquierda ---
        self.set_y(y_columns_start)
        self.set_x(x_col_left)
        kw_list = [kw for kw in item.get("keywords", []) if isinstance(kw, str) and "convocatoria" not in kw.lower()]
        dirigido_a = ", ".join(kw_list) or "No especificado"
        self.draw_section('icon_person.png', "DIRIGIDO A", dirigido_a, col_width)

        self.set_x(x_col_left)
        self.draw_section('icon_target.png', "OBJETIVO", item.get("description", "No especificado"), col_width)

        self.set_x(x_col_left)
        monto = item.get("monto", "No especificado")
        tipo_fin = item.get("type_financy", "No especificado")
        fin_txt = f"Monto: {monto}\nTipo: {tipo_fin}"
        self.draw_section('icon_money.png', "FINANCIAMIENTO", fin_txt, col_width)

        self.set_x(x_col_left)
        kws = item.get("keywords", [])
        kws_print = [kw for kw in kws if isinstance(kw, str)]
        self.draw_section('icon_tag.png', "KEYWORDS", ', '.join(kws_print) if kws_print else 'No especificado', col_width)
        y_left_end = self.get_y()

        # --- Columna Derecha ---
        self.set_y(y_columns_start)
        self.set_x(x_col_right)
        fecha_inicio = item.get("fecha_inicio") or item.get("inicio") or "No especificado"
        fecha_cierre = item.get("fecha_cierre") or item.get("deadline") or "No especificado"
        fechas_txt = f"Inicio: {fecha_inicio}\nCierre: {fecha_cierre}"
        self.draw_section('icon_clock.png', "FECHAS IMPORTANTES", fechas_txt, col_width)

        self.set_x(x_col_right)
        enlace = item.get("url") or item.get("source") or "No especificado"
        self.draw_section('icon_info.png', "MÁS INFORMACIÓN", enlace, col_width)

        self.set_x(x_col_right)
        self.draw_section('icon_check.png', "BENEFICIOS", item.get("beneficios", "No especificados"), col_width)

        # Colocar el cursor al final del bloque más bajo
        self.set_y(max(y_left_end, self.get_y()))

def generate_pdf(items: List[dict]) -> str:
    """Generates PDF and returns the file path."""
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_name = f"magazine_{ts}.pdf"
    output_dir = settings.OUTPUTS_DIR
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, pdf_name)

    pdf = PDF(orientation='P', unit='pt', format='A4')
    pdf.set_auto_page_break(auto=True, margin=40)
    pdf.set_margins(left=40, top=40, right=40)

    # Assets relative to the backend dir or root? 
    # Logic in PDF class init tries to find project root
    # We need to find 'assets' folder.
    # Assuming assets is in ROOT/assets
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # backend/app/services -> backend
    root_dir = os.path.dirname(backend_dir)
    assets_dir = os.path.join(root_dir, 'assets')
    
    inicio_cover = os.path.join(assets_dir, 'inicio.png')
    nacionales_cover = os.path.join(assets_dir, 'nacionales.png')
    internacionales_cover = os.path.join(assets_dir, 'internacionales.png')
    eventos_cover = os.path.join(assets_dir, 'eventos.png')
    cierre_cover = os.path.join(assets_dir, 'cierre.png')

    def add_fullpage_image(image_path: str):
        if os.path.exists(image_path):
            from PIL import Image as PILImage
            pdf.add_page()
            try:
                with PILImage.open(image_path) as im:
                    iw, ih = im.size
            except Exception:
                iw, ih = (1000, 1414)
            pw, ph = float(pdf.w), float(pdf.h)
            scale = min(pw / iw, ph / ih)
            w = iw * scale
            h = ih * scale
            x = (pw - w) / 2.0
            y = (ph - h) / 2.0
            pdf.image(image_path, x=x, y=y, w=w, h=h)

    add_fullpage_image(inicio_cover)

    nacionales = [it for it in items if str(it.get('type', 'convocatoria_nacional')).lower() == 'convocatoria_nacional']
    internacionales = [it for it in items if str(it.get('type', '')).lower() == 'convocatoria_internacional']
    eventos = [it for it in items if 'evento' in str(it.get('type', '')).lower()]

    if nacionales:
        add_fullpage_image(nacionales_cover)
        for it in nacionales:
            pdf.draw_call_card(it)

    if internacionales:
        add_fullpage_image(internacionales_cover)
        for it in internacionales:
            pdf.draw_call_card(it)

    if eventos:
        add_fullpage_image(eventos_cover)
        for it in eventos:
            pdf.draw_call_card(it)

    add_fullpage_image(cierre_cover)

    pdf.output(pdf_path)
    return pdf_path, pdf_name
