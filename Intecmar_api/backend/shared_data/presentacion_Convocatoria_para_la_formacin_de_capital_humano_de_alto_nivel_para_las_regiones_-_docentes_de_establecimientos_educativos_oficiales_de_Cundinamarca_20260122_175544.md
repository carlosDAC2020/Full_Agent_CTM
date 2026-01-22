---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  /* --- COLORES COTECMAR --- */
  :root {
    --primary: #003366;
    --secondary: #FFC000;
    --accent: #004d99;
    --text: #333;
    --bg-header: #003366;
  }

  /* --- AJUSTES DE ESPACIO GENERAL --- */
  section {
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
  }

  /* --- HEADER (LOGO COTECMAR A LA DERECHA) --- */
  header {
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
  }

  section.title-slide {
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
  }

  /* Efecto de brillo sutil */
  section.title-slide::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: subtle-glow 8s ease-in-out infinite;
  }

  @keyframes subtle-glow {
    0%, 100% { transform: translate(0, 0); opacity: 0.3; }
    50% { transform: translate(10%, 10%); opacity: 0.6; }
  }

  section.title-slide h1 { 
    color: white; 
    font-size: 2.8em; 
    margin-bottom: 20px; 
    text-shadow: 2px 2px 5px rgba(0,0,0,0.4);
    position: relative;
    z-index: 1;
  }
  
  section.title-slide h3 { 
    color: var(--secondary);
    font-size: 1.5em;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    position: relative;
    z-index: 1;
  }

  /* --- COMPONENTES --- */
  h1 { color: var(--primary); font-size: 1.6em; margin-bottom: 15px; }
  h2 { color: var(--accent); border-bottom: 2px solid var(--secondary); padding-bottom: 5px; font-size: 1.3em; margin-top: 0; margin-bottom: 15px; }
 
  /* CLASE PARA TEXTO DENSO */
  section.compact { font-size: 17px; }
  section.compact h2 { font-size: 1.2em; }
  section.compact li { margin-bottom: 2px; }

  /* TARJETAS */
  .card { background: #f8f9fa; border-left: 5px solid var(--primary); padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px; }
  .card.warning { border-left: 5px solid var(--secondary); background: #fffdf0; }
 
  /* COLUMNAS */
  .col-2 { columns: 2; column-gap: 40px; }
  .col-2 li { break-inside: avoid; }
  /* TABLAS COMPACTAS */
  table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
  th, td { padding: 6px 10px; border-bottom: 1px solid #ddd; }
  th { background: var(--primary); color: white; }
---
<!-- _class: title-slide -->
<!-- _header: "" -->
<!-- _paginate: false -->

# Convocatoria para la formación de capital humano de alto nivel para las regiones - docentes de establecimientos educativos oficiales de Cundinamarca

### Informe de Inteligencia de Convocatoria

---

<!-- header: '1. DATOS GENERALES' -->
<div class="card warning">
  <h3>📅 Información Clave</h3>
  <ul>
  <li><strong>Entidad:</strong> Ministerio de Ciencia, Tecnología e Innovación (Minciencias)</li>
  <li><strong>Número:</strong> 973</li>
  <li><strong>Apertura:</strong> jueves 20 noviembre 2025</li>
  <li><strong>Cierre:</strong> martes 16 diciembre 2025 04:00 pm</li>
  <li><strong>Resumen:</strong> Esta convocatoria de Minciencias busca incrementar la disponibilidad de capital humano con capacidades de investigación en prácticas pedagógicas, dirigido a docentes de establecimientos educativos oficiales del Departamento de Cundinamarca. El objetivo es potenciar sus habilidades y liderazgo a través de formación de alto nivel (maestrías), preparándolos para un impacto significativo en el futuro de la educación regional mediante propuestas de innovación educativa.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Incrementar la disponibilidad de capital humano con capacidades de investigación en prácticas pedagógicas en establecimientos educativos oficiales del Departamento de Cundinamarca.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> Docentes de aula de preescolar, básica o media, con asignación académica en matemáticas, lenguaje, ciencias naturales o ciencias sociales (incluyendo filosofía), de establecimientos educativos oficiales en el Departamento de Cundinamarca. Deben estar nombrados en propiedad o en periodo de prueba y contar con admisión a uno de los programas de maestría financiables.</li>
  <li><strong>Alianzas Obligatorias:</strong> No se exige un consorcio para la presentación individual del docente. Sin embargo, la participación implica la admisión a programas de maestría ofertados por Instituciones de Educación Superior (IES) aliadas.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>No ser docente de aula en un establecimiento educativo oficial del Departamento de Cundinamarca.</li>
      <li>No estar nombrado en propiedad o en periodo de prueba en el establecimiento educativo.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria está focalizada geográficamente en el Departamento de Cundinamarca.</p>
<ul>
  <li>Establecimientos educativos oficiales del Departamento de Cundinamarca.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>Las propuestas de investigación, desarrollo tecnológico y/o innovación deben estar enfocadas en la solución de problemas del ámbito académico en las aulas y relacionadas con los focos priorizados del PAED de Cundinamarca y las Misiones de la Política de Investigación e Innovación Orientada por Misiones:</p>
<ul>
  <li><strong>Línea 1: Agropecuario y Agroindustrial:</strong> Investigación aplicada a prácticas pedagógicas que aborden desafíos y oportunidades en los sectores agropecuario y agroindustrial de Cundinamarca.</li>
  <li><strong>Línea 2: Educación – Desarrollo Social y Comunitario:</strong> Proyectos que busquen mejorar las metodologías pedagógicas para impulsar el desarrollo social, la cohesión comunitaria y la resolución de problemáticas educativas en la región.</li>
  <li><strong>Línea 3: Medio Ambiente y Minas – Energía:</strong> Enfoque en la integración de la investigación pedagógica con la sostenibilidad ambiental y la gestión eficiente de los recursos minero-energéticos.</li>
  <li><strong>Línea 4: Salud y Soberanía Sanitaria:</strong> Desarrollo de capacidades de investigación en educación que promuevan la salud pública, el bienestar y la autonomía en la generación de conocimiento y tecnologías sanitarias.</li>
  <li><strong>Línea 5: Bioeconomía y Territorio / Ciencia para la Paz:</strong> Investigación pedagógica orientada a potenciar el desarrollo territorial sostenible mediante el conocimiento y aprovechamiento de la biodiversidad, y a fomentar la convivencia pacífica a través de soluciones tecnológicas y sociales.</li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> Se espera que las propuestas de investigación inicien en un nivel de madurez tecnológica TRL 2-3 (formulación del concepto tecnológico/aplicación) y culminen en TRL 4-5 (validación en laboratorio/entorno relevante), dada la naturaleza de los trabajos de grado de maestría.</li>
  <li><strong>Componentes Obligatorios:</strong> La realización de propuestas de investigación, desarrollo tecnológico y/o innovación como trabajo de grado es obligatoria. Estas propuestas deben estar enfocadas en la solución de problemas del ámbito académico en las aulas y alineadas con los focos priorizados del PAED de Cundinamarca y las Misiones de la Política de Investigación e Innovación Orientada por Misiones.</li>
  <li><strong>Duración:</strong> La duración de la ejecución corresponde al tiempo establecido para la culminación de los programas de maestría, típicamente dos (2) años, iniciando después de la publicación de resultados definitivos.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  Clasifica los entregables obligatorios (derivados de la investigación de maestría):
<ul>
  <li><strong>Generación de Conocimiento:</strong> Tesis de maestría (que contengan propuestas de investigación, desarrollo tecnológico y/o innovación), artículos científicos, ponencias en eventos académicos.</li>
  <li><strong>Desarrollo Tecnológico:</strong> Prototipos educativos, herramientas pedagógicas innovadoras, software educativo, nuevas metodologías de enseñanza-aprendizaje resultantes de las investigaciones.</li>
  <li><strong>Apropiación Social:</strong> Implementación y validación de nuevas prácticas pedagógicas en el aula, talleres de socialización de resultados con la comunidad educativa, manuales o guías didácticas, eventos de divulgación.</li>
  <li><strong>Infraestructura:</strong> No se contempla la generación de infraestructura física como entregable directo de los docentes. Sin embargo, podría incluir la adecuación o mejora de recursos didácticos o tecnológicos existentes en los establecimientos educativos.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li>Directrices éticas para la investigación científica y pedagógica (Minciencias).</li>
      <li>Normas de citación y publicación académica (ej. APA, ICONTEC, Vancouver, según la disciplina y el programa de maestría).</li>
      <li>Estándares de calidad para programas de posgrado en Colombia (Ministerio de Educación Nacional).</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong> No se especifican requisitos mínimos de hardware o software por parte de la convocatoria. Las especificaciones dependerán de las necesidades particulares de cada proyecto de investigación y de los requerimientos de los programas de maestría.</li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li>Resolución 1452 de 2024 del Ministerio de Ciencia, Tecnología e Innovación (que adopta las Misiones de la Política de Investigación e Innovación).</li>
      <li>Normatividad educativa colombiana aplicable a docentes y establecimientos educativos oficiales.</li>
      <li>Reglamentación interna de Minciencias para la ejecución y seguimiento de proyectos de formación de capital humano.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria tiene un impacto directo en el Departamento de Cundinamarca, buscando fortalecer el capital humano docente y las capacidades de investigación en sus establecimientos educativos oficiales, contribuyendo al desarrollo regional a través de la educación.</li>
  <li><strong>Enfoque Diferencial:</strong> El Anexo 4 ("Enfoque diferencial e interseccional y autorización de tratamiento de datos personales") sugiere la consideración de enfoques diferenciales e interseccionales en las propuestas. Esto implica la inclusión y atención a las particularidades de diversas poblaciones (mujeres, grupos étnicos, personas con discapacidad, víctimas del conflicto, etc.) en el diseño y ejecución de la investigación pedagógica.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <ul>
  <li><strong>Director/Gerente:</strong> No aplica para la presentación individual del docente. El docente es el beneficiario y ejecutor principal de su proceso de formación e investigación.</li>
  <li><strong>Investigadores:</strong> Docentes de aula de preescolar, básica o media, con asignación académica en matemáticas, lenguaje, ciencias naturales o ciencias sociales (incluyendo filosofía), nombrados en propiedad o en periodo de prueba, y admitidos a un programa de maestría.</li>
  <li><strong>Técnicos:</strong> No se especifica un equipo técnico de apoyo directo para la propuesta individual del docente. Sin embargo, se espera que los programas de maestría y las instituciones educativas brinden el soporte académico y técnico necesario para el desarrollo de las investigaciones.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  Lista tipo checklist de los documentos más críticos:
<ul>
  <li>Términos de Referencia de la Convocatoria.</li>
  <li>Anexo 1: Certificación emitida por la secretaría de educación departamental o municipal.</li>
  <li>Anexo 2: Carta aval del establecimiento educativo oficial.</li>
  <li>Anexo 3: Carta de compromiso, conocimiento y aceptación del candidato para desarrollar la propuesta de investigación, desarrollo tecnológico y/o innovación.</li>
  <li>Anexo 4: Enfoque diferencial e interseccional y autorización de tratamiento de datos personales.</li>
  <li>Anexo 6: Documento científico - técnico (propuesta de investigación).</li>
  <li>Anexo 7: Acuerdo de propiedad intelectual.</li>
  <li>Resolución 1473 de 2025 (Reglamento de la convocatoria).</li>
  <li>Documento de admisión a uno de los programas de maestría financiables.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> $877.800.000 (Ochocientos setenta y siete millones ochocientos mil pesos colombianos).</li>
  <li><strong>Tope por Proyecto:</strong> No se especifica un tope individual por proyecto o beca en la información disponible, pero el monto total se destina a la financiación de programas de maestría para los docentes seleccionados.</li>
  <li><strong>Contrapartida:</strong> No se exige una contrapartida financiera directa del docente beneficiario. Se infiere un compromiso institucional por parte del establecimiento educativo oficial (aval) y un compromiso del docente con la permanencia y aplicación del conocimiento en la región.</li>
  <li><strong>Rubros Financiables:</strong> Principalmente costos asociados a la matrícula, derechos académicos y, potencialmente, sostenimiento para los docentes beneficiarios de los programas de maestría.</li>
</ul>
  </div>
</div>


---
<!-- _class: compact -->
<!-- header: '13. MAPA DE RIESGOS' -->
<h2>🛡️ Matriz de Riesgos</h2>
<!-- Si la tabla es muy larga, reduce fuente -->
<div style="font-size: 0.8em;">
  <ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li>Desalineación de las propuestas de investigación con los focos priorizados del PAED de Cundinamarca o con las Misiones de la Política de Investigación e Innovación.</li>
      <li>Baja pertinencia o calidad científica de las propuestas de investigación pedagógica presentadas por los docentes.</li>
      <li>Dificultades en la implementación de las innovaciones pedagógicas resultantes en el entorno educativo real.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li>Baja participación de docentes elegibles o que cumplan con todos los requisitos de la convocatoria.</li>
      <li>Retrasos en los cronogramas académicos de los programas de maestría o en la culminación de los trabajos de grado.</li>
      <li>Rotación de personal docente en los establecimientos educativos o incumplimiento de los compromisos de permanencia post-formación.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li>Insuficiencia de fondos para cubrir la totalidad de cupos o el sostenimiento de todos los beneficiarios si los costos de los programas de maestría exceden las previsiones.</li>
      <li>Riesgo de ejecución presupuestal, donde los recursos no se desembolsen o utilicen de manera eficiente según el cronograma.</li>
    </ul>
  </li>
</ul>
</div>

