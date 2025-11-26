import subprocess
import sys
import re

from .prompts import MARP_HEADER


def convert_marp_to_formats(md_file_path: str):
    """
    Convierte el archivo MD a PDF y PPTX usando Marp CLI instalado localmente.
    """
    print(f"🔄 Iniciando conversión de: {md_file_path}")
    
    # Definir nombres de salida
    pdf_file = md_file_path.replace(".md", ".pdf")
    pptx_file = md_file_path.replace(".md", ".pptx")
    
    # --- CAMBIO IMPORTANTE AQUÍ ---
    # Al tener marp instalado, llamamos directamente al comando "marp".
    # Eliminamos "npx", "--yes" y "@marp-team/marp-cli@latest".
    cmd_pdf = ["marp", md_file_path, "--pdf", "--allow-local-files", "-o", pdf_file]
    cmd_pptx = ["marp", md_file_path, "--pptx", "--allow-local-files", "-o", pptx_file]
    
    try:
        # Detectar si es Windows para usar shell=True
        # En Windows, 'marp' suele ser un archivo .cmd, y subprocess necesita shell=True para encontrarlo fácilmente.
        is_windows = sys.platform == "win32"

        # 1. Generar PDF
        print("   📄 Generando PDF...")
        subprocess.run(cmd_pdf, check=True, shell=is_windows)
        print(f"   ✅ PDF creado: {pdf_file}")

        # 2. Generar PPTX
        print("   📊 Generando PowerPoint...")
        subprocess.run(cmd_pptx, check=True, shell=is_windows)
        print(f"   ✅ PPTX creado: {pptx_file}")
        
        return pdf_file, pptx_file

    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error en la conversión: {e}")
        return None, None
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return None, None


# --- FUNCIÓN AUXILIAR DE ENSAMBLAJE ---
def create_marp_from_text(raw_text: str, title: str) -> str:
    """Toma el texto estructurado del agente y lo envuelve en HTML/Marp."""
    
    # Mapeo: Nombre del bloque -> Plantilla HTML Específica y Optimizada
    slides = {
        "DATOS_GENERALES": """
<!-- header: '1. DATOS GENERALES' -->
<div class="card warning">
  <h3>📅 Información Clave</h3>
  {content}
</div>
""",
        "OBJETIVO": """
---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  {content}
</div>
""",
        "DIRIGIDO_A": """
---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    {content}
  </div>
</div>
""",
        "DEMANDAS": """
---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  {content}
</div>
""",
        "LINEAS": """
---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  {content}
</div>
""",
        "ALCANCE": """
---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  {content}
</div>
""",
        "PRODUCTOS": """
---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  {content}
</div>
""",
        "TECNICAS": """
---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  {content}
</div>
""",
        "ENFOQUES": """
---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
{content}
""",
        "TALENTO": """
---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  {content}
</div>
""",
        "DOCUMENTOS": """
---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  {content}
</div>
""",
        "FINANCIACION": """
---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    {content}
  </div>
</div>
""",
        "RIESGOS": """
---
<!-- _class: compact -->
<!-- header: '13. MAPA DE RIESGOS' -->
<h2>🛡️ Matriz de Riesgos</h2>
<!-- Si la tabla es muy larga, reduce fuente -->
<div style="font-size: 0.8em;">
  {content}
</div>
"""
    }

    presentation_body = ""
    found_blocks = 0
    
    # Extraer bloques (Igual que antes)
    for tag, template in slides.items():
        pattern = fr"\[{tag}\](.*?)\[/{tag}\]"
        match = re.search(pattern, raw_text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            presentation_body += template.format(content=content) + "\n"
            found_blocks += 1
            
    if found_blocks == 0:
        presentation_body = f"\n---\n<!-- header: 'Resultados' -->\n{raw_text}"

    return MARP_HEADER.format(title=title) + presentation_body