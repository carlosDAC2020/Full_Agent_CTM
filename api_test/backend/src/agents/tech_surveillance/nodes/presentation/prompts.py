
MARP_HEADER = """---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  /* --- COLORES COTECMAR --- */
  :root {{
    --primary: #003366;
    --secondary: #FFC000;
    --accent: #004d99;
    --text: #333;
    --bg-header: #003366;
  }}

  /* --- AJUSTES DE ESPACIO GENERAL --- */
  section {{
    background-color: white;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: var(--text);
    padding: 30px 50px;
    padding-top: 100px; /* Espacio para el header */
    font-size: 20px;
    display: block;
    /* Marca de agua sutil del escudo en diapositivas normales */
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/2/22/Escudo_Cotecmar.png');
    background-repeat: no-repeat;
    background-position: center;
    background-size: 15%;
    background-blend-mode: overlay;
  }}

  /* --- HEADER (LOGO COTECMAR A LA DERECHA) --- */
  header {{
    position: absolute; top: 0; left: 0; width: 100%; height: 80px;
    background: var(--bg-header); color: white; display: flex; align-items: center;
    padding-left: 40px; font-size: 20px; font-weight: bold;
    /* Logo Cotecmar */
    background-image: url('https://atmos.com.co/wp-content/uploads/2024/02/COTECMAR.png'); 
    background-repeat: no-repeat; 
    background-position: right 80px center; 
    background-size: contain;
    background-origin: content-box;
    padding-right: 30px; 
    border-bottom: 4px solid var(--secondary);
    z-index: 100;
  }}

  section.title-slide {{
    padding: 0;
    background: linear-gradient(135deg, #001a33 0%, var(--primary) 25%, var(--accent) 60%, #0066cc 100%);
    background-image: linear-gradient(135deg, #001a33 0%, var(--primary) 25%, var(--accent) 60%, #0066cc 100%);
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    align-items: center; 
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
  }}

  /* Efecto de brillo sutil */
  section.title-slide::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: subtle-glow 8s ease-in-out infinite;
  }}

  @keyframes subtle-glow {{
    0%, 100% {{ transform: translate(0, 0); opacity: 0.3; }}
    50% {{ transform: translate(10%, 10%); opacity: 0.6; }}
  }}

  section.title-slide h1 {{ 
    color: white; 
    font-size: 2.8em; 
    margin-bottom: 20px; 
    text-shadow: 2px 2px 5px rgba(0,0,0,0.4);
    position: relative;
    z-index: 1;
  }}
  
  section.title-slide h3 {{ 
    color: var(--secondary);
    font-size: 1.5em;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    position: relative;
    z-index: 1;
  }}

  /* --- COMPONENTES --- */
  h1 {{ color: var(--primary); font-size: 1.6em; margin-bottom: 15px; }}
  h2 {{ color: var(--accent); border-bottom: 2px solid var(--secondary); padding-bottom: 5px; font-size: 1.3em; margin-top: 0; margin-bottom: 15px; }}
 
  /* CLASE PARA TEXTO DENSO */
  section.compact {{ font-size: 17px; }}
  section.compact h2 {{ font-size: 1.2em; }}
  section.compact li {{ margin-bottom: 2px; }}

  /* TARJETAS */
  .card {{ background: #f8f9fa; border-left: 5px solid var(--primary); padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px; }}
  .card.warning {{ border-left: 5px solid var(--secondary); background: #fffdf0; }}
 
  /* COLUMNAS */
  .col-2 {{ columns: 2; column-gap: 40px; }}
  .col-2 li {{ break-inside: avoid; }}
  /* TABLAS COMPACTAS */
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85em; }}
  th, td {{ padding: 6px 10px; border-bottom: 1px solid #ddd; }}
  th {{ background: var(--primary); color: white; }}
---
<!-- _class: title-slide -->
<!-- _header: "" -->
<!-- _paginate: false -->

# {title}

### Informe de Inteligencia de Convocatoria

---
"""