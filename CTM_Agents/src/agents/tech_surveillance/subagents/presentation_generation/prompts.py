SYSTEM_PROMPT = """\
Eres un Consultor Experto en Licitaciones y Vigilancia Tecnológica.

TU MISIÓN:
1. Investigar a fondo la convocatoria usando tus herramientas (tavily, brave, url_fetch). No te conformes con información superficial.
2. Rellenar los 13 bloques de información solicitados con precisión técnica.
3. Estructurar el contenido visualmente usando HTML básico para asegurar una presentación impecable.

PROTOCOLOS DE INVESTIGACIÓN:
- Si falta un dato (ej: "Matriz de Riesgos" o "Estándares Técnicos"), BÚSCALO activamente en anexos o términos de referencia usando las herramientas.
- Si la información no es explícita, infiérela profesionalmente basada en estándares del sector (ej: ISO 27001 para software, Retie para eléctricos).
- Prioriza fuentes oficiales (.gov, sitios de la entidad).

REGLAS DE FORMATO DE SALIDA (CRÍTICO):
- NO uses Markdown para listas (guiones `-` o asteriscos `*`).
- USA EXCLUSIVAMENTE HTML para dar formato dentro de los bloques:
  * Listas: <ul> <li>Elemento</li> </ul>
  * Negritas: <strong>Texto importante</strong>
  * Párrafos: <p>Texto</p>
  * Saltos: <br>
- NO escribas introducciones ni conclusiones fuera de los bloques.
- NO generes la estructura completa del documento (html/head/body), SOLO el contenido interno de los bloques.
- Limítate estrictamente a los separadores `[SECCION]...[/SECCION]`.
"""

CONTENT_PROMPT_TEMPLATE = """\
Analiza la siguiente información de la convocatoria:

TÍTULO: {title}
OBJETIVO: {objective}
FINANCIACIÓN: {funding} {funding_status}
FECHAS: {important_dates} {dates_status}
URL: {url}

Eres un Consultor Senior en Licitaciones Públicas. Tu trabajo no es solo copiar y pegar, sino INVESTIGAR A FONDO y SINTETIZAR técnicamente.

---
🚀 PROTOCOLO DE INVESTIGACIÓN (OBLIGATORIO)
1. Si un dato técnico (como "Riesgos" o "Estándares") no está en la info inicial, USA TUS HERRAMIENTAS para buscar: "Términos de referencia {title}", "Anexo técnico convocatoria {title}", "Matriz de riesgos {title}".
2. Si no encuentras una sección específica (ej: Riesgos), DEBES INFERIRLA basándote en la naturaleza del proyecto (ej: "Riesgo de sobrecostos tecnológicos", "Riesgo de importación de equipos").
3. NO uses frases cortas. Sé descriptivo y técnico.
---

⚠️ REGLA DE FORMATO VISUAL (CRÍTICA):
Para evitar errores de visualización en las diapositivas, NO uses listas con guiones de Markdown (- elemento).
USA ETIQUETAS HTML SIMPLES PARA LISTAS Y NEGRITAS:
- Usa <ul> y <li> para listas.
- Usa <strong> para resaltar textos importantes.
- Usa <br> para saltos de línea.

Ejemplo de formato esperado:
<ul>
  <li><strong>Requisito A:</strong> Descripción detallada...</li>
  <li><strong>Requisito B:</strong> Descripción detallada...</li>
</ul>

---

Genera el reporte llenando los siguientes 13 bloques con los separadores EXACTOS:

[DATOS_GENERALES]
<ul>
  <li><strong>Entidad:</strong> [Nombre exacto]</li>
  <li><strong>Número:</strong> [Código de convocatoria]</li>
  <li><strong>Apertura:</strong> [Fecha y HORA exacta]</li>
  <li><strong>Cierre:</strong> [Fecha y HORA exacta]</li>
  <li><strong>Resumen:</strong> [Párrafo de 3-4 líneas explicando el "core" de la convocatoria]</li>
</ul>
[/DATOS_GENERALES]

[OBJETIVO]
<p>[Escribe el objetivo general textual. Si es muy largo, resúmelo sin perder el alcance técnico.]</p>
[/OBJETIVO]

[DIRIGIDO_A]
<ul>
  <li><strong>Ejecutor:</strong> ¿Quién debe presentar la propuesta? (IES, Empresa, etc.)</li>
  <li><strong>Alianzas Obligatorias:</strong> ¿Se exige consorcio? ¿Con quién?</li>
  <li><strong>Inhabilidades:</strong> Menciona 2 condiciones que excluyen la participación.</li>
</ul>
[/DIRIGIDO_A]

[DEMANDAS]
<p>Detalla la focalización geográfica. ¿Hay departamentos, ciudades o zonas PDET específicas?</p>
<ul>
  <li>[Lista los lugares específicos si los hay]</li>
</ul>
[/DEMANDAS]

[LINEAS]
<p>Desglosa las líneas temáticas o ejes de investigación (Mínimo 5 si existen, sé detallado):</p>
<ul>
  <li><strong>Línea 1:</strong> [Descripción]</li>
  <li><strong>Línea 2:</strong> [Descripción]</li>
  <li><strong>Línea 3:</strong> [Descripción]</li>
  <li><strong>Línea 4:</strong> [Descripción]</li>
  <li><strong>Línea 5:</strong> [Descripción]</li>
</ul>
[/LINEAS]

[ALCANCE]
<ul>
  <li><strong>TRL Esperado:</strong> ¿En qué nivel de madurez tecnológica debe iniciar y terminar?</li>
  <li><strong>Componentes Obligatorios:</strong> ¿Qué actividades NO pueden faltar?</li>
  <li><strong>Duración:</strong> Tiempo máximo de ejecución.</li>
</ul>
[/ALCANCE]

[PRODUCTOS]
Clasifica los entregables obligatorios (busca en anexos técnicos):
<ul>
  <li><strong>Generación de Conocimiento:</strong> (Artículos, libros, tesis)</li>
  <li><strong>Desarrollo Tecnológico:</strong> (Prototipos, software, patentes)</li>
  <li><strong>Apropiación Social:</strong> (Talleres, eventos, manuales)</li>
  <li><strong>Infraestructura:</strong> (Adecuaciones, equipos)</li>
</ul>
[/PRODUCTOS]

[TECNICAS]
Investiga estándares técnicos específicos. NO digas "No especificado" sin buscar "Anexo Técnico".
<ul>
  <li><strong>Estándares:</strong> (Ej: Normas ISO, Tier III, Retie, HIPAA, etc.)</li>
  <li><strong>Hardware/Software:</strong> (Especificaciones mínimas de servidores, lenguajes, etc.)</li>
  <li><strong>Normatividad:</strong> (Leyes específicas que rigen el proyecto)</li>
</ul>
[/TECNICAS]

[ENFOQUES]
<ul>
  <li><strong>Enfoque Territorial:</strong> ¿Cómo impacta a la región?</li>
  <li><strong>Enfoque Diferencial:</strong> ¿Exige inclusión de mujeres, víctimas o minorías?</li>
</ul>
[/ENFOQUES]

[TALENTO]
Detalla el equipo mínimo requerido (Busca en "Condiciones Habilitantes"):
<ul>
  <li><strong>Director/Gerente:</strong> (Perfil, formación y años de experiencia)</li>
  <li><strong>Investigadores:</strong> (Nivel educativo requerido: PhD, Maestría)</li>
  <li><strong>Técnicos:</strong> (Perfiles de apoyo)</li>
</ul>
[/TALENTO]

[DOCUMENTOS]
Lista tipo checklist de los documentos más críticos para no ser descartado:
<ul>
  <li>[Documento Jurídico 1]</li>
  <li>[Documento Financiero 1]</li>
  <li>[Certificaciones específicas]</li>
  <li>[Avales institucionales]</li>
  <li>[Cartas de intención]</li>
</ul>
[/DOCUMENTOS]

[FINANCIACION]
<ul>
  <li><strong>Monto Total de la Bolsa:</strong> [Cifra exacta]</li>
  <li><strong>Tope por Proyecto:</strong> [Cifra exacta]</li>
  <li><strong>Contrapartida:</strong> [ % exigido en efectivo y especie]</li>
  <li><strong>Rubros Financiables:</strong> (Personal, equipos, salidas de campo, etc.)</li>
</ul>
[/FINANCIACION]

[RIESGOS]
Si no hay matriz de riesgos explícita, INFIERELOS basados en proyectos similares de tecnología/ciencia:
<ul>
  <li><strong>Riesgo Técnico:</strong> (Ej: Obsolescencia tecnológica, fallos en integración)</li>
  <li><strong>Riesgo Operativo:</strong> (Ej: Retrasos en importaciones, rotación de personal)</li>
  <li><strong>Riesgo Financiero:</strong> (Ej: Fluctuación del dólar, recortes presupuestales)</li>
</ul>
[/RIESGOS]
"""

# --- 3. PLANTILLA MARP ---

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

  /* --- AJUSTES DE ESPACIO --- */
  section {{
    background-color: white;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: var(--text);
    padding: 30px 50px;
    padding-top: 100px; /* Espacio para el header */
    font-size: 20px;
    display: block;
    /* Opcional: Marca de agua sutil del logo en el centro de las diapositivas normales */
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/2/22/Escudo_Cotecmar.png');
    background-repeat: no-repeat;
    background-position: center;
    background-size: 15%;
    background-blend-mode: overlay; /* Mezcla sutil */
  }}

  /* --- HEADER (LOGO COTECMAR A LA DERECHA) --- */
  header {{
    position: absolute; top: 0; left: 0; width: 100%; height: 80px;
    background: var(--bg-header); color: white; display: flex; align-items: center;
    padding-left: 40px; font-size: 20px; font-weight: bold;
    
    /* AQUI ESTA EL CAMBIO DEL LOGO */
    background-image: url('https://atmos.com.co/wp-content/uploads/2024/02/COTECMAR.png'); 
    
    /* Ubicación: Derecha, margen de 30px, centrado verticalmente */
    background-repeat: no-repeat; 
    background-position: right 80px center; 
    background-size: contain; /* Ajusta el logo para que quepa en el header */
    background-origin: content-box;
    padding-right: 30px; /* Protege el espacio del logo */
    
    border-bottom: 4px solid var(--secondary);
    z-index: 100;
  }}

  /* --- PORTADA (IMAGEN NAVAL/INDUSTRIAL) --- */
  section.title-slide {{
    padding: 0;
    /* Fondo alusivo a astilleros/mar con filtro azul corporativo */
    background-image: linear-gradient(rgba(0,51,102,0.85), rgba(0,51,102,0.95)), url('https://www.eluniversal.com.co/resizer/v2/cotecmar-QEK2D7TQ4ZGULICGMXZ2RNIZLM.png?auth=74a50ac10fc6fb408afed0d3916930f19cb1c6943836db1ce3e682380ac2e0f8&smart=true&width=1200&height=800&quality=70');
    background-size: cover; 
    background-position: center;
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    align-items: center; 
    text-align: center;
    
    /* CORRECCIÓN DE TEXTO INVISIBLE */
    color: white; 
  }}

  section.title-slide h1 {{ 
    color: white; 
    font-size: 2.8em; 
    margin-bottom: 20px; 
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  }}
  
  /* Estilo para el subtítulo (###) en la portada */
  section.title-slide h3 {{ 
    color: var(--secondary); /* Amarillo Cotecmar */
    font-size: 1.5em;
    font-weight: normal;
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