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

# CONVOCATORIA PARA EL FORTALECIMIENTO DE CAPACIDADES DE CIENCIA, TECNOLOGÍA E INNOVACIÓN EN EL DEPARTAMENTO DE CÓRDOBA ALINEADO CON LOS RETOS ESTRATÉGICOS DE CTeI DEL PLAN BIENAL 2025-2026

### Informe de Inteligencia de Convocatoria

---

<!-- header: '1. DATOS GENERALES' -->
<div class="card warning">
  <h3>📅 Información Clave</h3>
  <ul>
  <li><strong>Entidad:</strong> Ministerio de Ciencia, Tecnología e Innovación (Minciencias)</li>
  <li><strong>Número:</strong> Convocatoria 51</li>
  <li><strong>Apertura:</strong> Martes, Diciembre 30, 2025</li>
  <li><strong>Cierre:</strong> No especificado en la información pública detallada de la convocatoria.</li>
  <li><strong>Resumen:</strong> Esta convocatoria busca fortalecer las capacidades de Ciencia, Tecnología e Innovación (CTeI) en el Departamento de Córdoba. Se enfoca en el desarrollo de proyectos de convergencia regional que impulsen la productividad y competitividad, alineados con los retos estratégicos del Plan Bienal 2025-2026 y las transformaciones del Plan Nacional de Desarrollo.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer las capacidades de Ciencia, Tecnología e Innovación (CTeI) en el Departamento de Córdoba, mediante el desarrollo de proyectos de convergencia regional que impulsen la productividad y competitividad de acuerdo a las vocaciones territoriales dirigidas a atender las demandas territoriales del Reto 1. Aprovechar el conocimiento, conservación y uso sostenible de la biodiversidad, bienes y servicios ecosistémicos; Reto 2. Garantizar la soberanía alimentaria y el derecho a la alimentación; Reto 5. Poner fin a todas las formas de violencia en Colombia, y Reto 6. Asegurar la convergencia regional y el ordenamiento del territorio del plan bienal 2025-2026 y las transformaciones del Plan Nacional de Desarrollo.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> Alianzas entre entidades del Sistema Nacional de Ciencia, Tecnología e Innovación (SNCTI) y de éstas con otras entidades, conforme a lo establecido en el Decreto 1821 de 2020.</li>
  <li><strong>Alianzas Obligatorias:</strong> Las propuestas deben ser presentadas a través de una Alianza estratégica conformada, como mínimo, por:
    <ul>
      <li>Al menos una (1) Institución de Educación Superior (IES) en la zona de influencia del proyecto.</li>
      <li>Al menos una (1) entidad territorial supramunicipal, departamental o municipal.</li>
      <li>Al menos un (1) actor que agremie o agrupe empresas (Ej. Gremios empresariales, cámaras de comercio, clúster, asociaciones empresariales o empresas ancla).</li>
      <li>Al menos una (1) organización de sociedad civil con representación legal en la zona de influencia del proyecto.</li>
    </ul>
  </li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>No acreditar experiencia en mínimo dos (2) proyectos de Ciencia, Tecnología e Innovación ejecutados o en ejecución, de los cuales al menos uno (1) haya sido financiado con recursos del Sistema General de Regalías de la Asignación para la Ciencia, Tecnología e Innovación en los últimos cinco (5) años, en rol de ejecutor o aliado.</li>
      <li>No acreditar el adecuado desempeño en la medición del Departamento Nacional de Planeación (DNP), conforme a la metodología establecida, a menos que la entidad proponente no haya sido objeto de medición en los dos (2) años inmediatamente anteriores a la fecha de cierre.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria se focaliza geográficamente en el Departamento de Córdoba, buscando atender sus demandas territoriales específicas alineadas con los retos estratégicos del plan bienal 2025-2026.</p>
<ul>
  <li><strong>Departamento:</strong> Córdoba</li>
  <li><strong>Retos Territoriales Específicos:</strong>
    <ul>
      <li><strong>Reto 1:</strong> Aprovechar el conocimiento, conservación y uso sostenible de la biodiversidad, bienes y servicios ecosistémicos.</li>
      <li><strong>Reto 2:</strong> Garantizar la soberanía alimentaria y el derecho a la alimentación.</li>
      <li><strong>Reto 5:</strong> Poner fin a todas las formas de violencia en Colombia.</li>
      <li><strong>Reto 6:</strong> Asegurar la convergencia regional y el ordenamiento del territorio.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>Los proyectos deben abordar un mínimo de dos (2) de las siguientes líneas temáticas, pudiendo incluir más de una subtemática por línea:</p>
<ul>
  <li><strong>Línea temática 1:</strong> Fortalecimiento de las capacidades de ciencia, tecnología e innovación para el desarrollo productivo y competitivo. Se esperan iniciativas que desde la CTeI reconozcan los territorios para reducir brechas intra e interregionales.</li>
  <li><strong>Línea temática 2:</strong> Integración intrarregional y con el mundo para el fortalecimiento de la innovación y la productividad en los ecosistemas territoriales de ciencia, tecnología e innovación. Prioriza apuestas y cadenas de valor construidas desde los territorios, con énfasis en agricultura y producción animal (familiar, urbana, periurbana y rural) para la conservación y aprovechamiento de fuentes de alimentos con conocimiento y prácticas ancestrales.</li>
  <li><strong>Línea temática 3:</strong> Fortalecimiento de capacidades y articulación de los actores de los ecosistemas territoriales para la gobernanza territorial de la ciencia, tecnología e innovación. Centrada en mejorar la gestión descentralizada de la CTeI y promover políticas alineadas con necesidades y vocaciones territoriales.</li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> No especificado explícitamente. Sin embargo, dada la naturaleza de "fortalecimiento de capacidades" y "desarrollo de proyectos de convergencia regional", se infiere que los proyectos deben abarcar desde la investigación aplicada hasta el desarrollo y validación de tecnologías y soluciones, posiblemente entre Nivel de Madurez Tecnológica (TRL) 3 y 7.</li>
  <li><strong>Componentes Obligatorios:</strong> Los proyectos deben incluir actividades, productos e indicadores que contribuyan al desarrollo territorial a través de la promoción de la investigación científica y social para la innovación. Deben abordar un mínimo de dos (2) de las líneas temáticas definidas.</li>
  <li><strong>Duración:</strong> No especificado en la información pública disponible. Se infiere una duración típica para proyectos de CTeI de esta envergadura, que puede oscilar entre 12 y 36 meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Clasificación de entregables obligatorios (inferidos por el tipo de convocatoria):</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas o de alto impacto.</li>
      <li>Informes técnicos y metodológicos detallados.</li>
      <li>Bases de datos especializadas.</li>
      <li>Capítulos de libro o libros resultado de investigación.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales (hardware o software) validados en entornos relevantes.</li>
      <li>Desarrollo o mejora de procesos productivos.</li>
      <li>Variedades o razas mejoradas (especialmente para el Reto 2).</li>
      <li>Modelos de transferencia tecnológica o de conocimiento.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Diseño e implementación de programas de formación y talleres especializados.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Manuales, guías o material didáctico para la comunidad.</li>
      <li>Estrategias de comunicación y difusión de resultados.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones menores o mejoras en laboratorios y centros de investigación.</li>
      <li>Adquisición de equipos especializados (si son esenciales para el desarrollo del proyecto).</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <ul>
  <li><strong>Estándares:</strong> No se especifican estándares técnicos obligatorios de manera explícita. Sin embargo, se infiere la aplicación de buenas prácticas en investigación (ej. ética en investigación), gestión de datos (ej. principios FAIR), y potencialmente estándares específicos de la industria o sector al que apunte el proyecto (ej. normas para producción agrícola, sistemas de calidad ISO).</li>
  <li><strong>Hardware/Software:</strong> No se establecen especificaciones mínimas generales. Estas dependerán de los requisitos técnicos específicos de cada propuesta de proyecto.</li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li>Decreto 1821 de 2020 (para elegibilidad y conformación de alianzas).</li>
      <li>Plan Nacional de Desarrollo vigente y sus transformaciones.</li>
      <li>Plan Bienal 2025-2026 de CTeI.</li>
      <li>Políticas de Investigación e Innovación Orientadas por Misiones (PIIOM).</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria tiene un fuerte enfoque territorial, centrándose específicamente en el Departamento de Córdoba y en el desarrollo de proyectos de convergencia regional que atiendan las vocaciones y demandas territoriales definidas en los retos estratégicos.</li>
  <li><strong>Enfoque Diferencial:</strong> No se exige explícitamente un enfoque diferencial como requisito obligatorio. Sin embargo, la atención a retos como "Poner fin a todas las formas de violencia en Colombia" y el fomento de la "agricultura y producción animal, familiar, urbana, periurbana y rural" pueden implicar la consideración de poblaciones diversas y la aplicación de principios de equidad e inclusión en la formulación y ejecución de los proyectos.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>Detalle del equipo mínimo requerido (inferido y basado en requisitos de la alianza):</p>
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con formación académica de posgrado (Maestría o Doctorado preferiblemente) y experiencia demostrable en la gestión y coordinación de proyectos de Ciencia, Tecnología e Innovación, especialmente aquellos financiados con recursos públicos.</li>
  <li><strong>Investigadores:</strong> Se requiere que al menos uno de los integrantes de la alianza cuente con un grupo de investigación de categorías A1, A o B (según clasificación de Minciencias). Esto implica la participación de investigadores con nivel educativo de Maestría o Doctorado, con trayectoria y publicaciones en áreas del conocimiento relevantes para las líneas temáticas de la convocatoria.</li>
  <li><strong>Técnicos:</strong> Perfiles de apoyo profesional y técnico específicos, cuya formación y experiencia se alineen con las necesidades operativas y técnicas de cada proyecto propuesto (ej. ingenieros, agrónomos, sociólogos, diseñadores, expertos en datos).</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Lista de documentos críticos para la participación:</p>
<ul>
  <li>Formato “Proyectos de ciencia, tecnología e innovación gestionados o ejecutados por el proponente e integrantes de la alianza” (Anexo 5).</li>
  <li>Soportes de experiencia del proponente y los aliados (ej. convenios/contratos, acuerdos, actos administrativos, actas de liquidación o finalización).</li>
  <li>Acreditación del adecuado desempeño en la medición del DNP (si aplica).</li>
  <li>Registro del grupo(s) de investigación en la plataforma SIGP con categoría A1, A o B.</li>
  <li>Documentos legales de constitución y representación de todas las entidades que conforman la alianza.</li>
  <li>Cartas de intención o acuerdos de la alianza que formalicen la participación y responsabilidades de cada integrante.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> $17.154.450.476 COP (Diecisiete mil ciento cincuenta y cuatro millones cuatrocientos cincuenta mil cuatrocientos setenta y seis pesos colombianos).</li>
  <li><strong>Tope por Proyecto:</strong> No especificado por proyecto en la información pública disponible.</li>
  <li><strong>Contrapartida:</strong> No especificado en la información pública disponible.</li>
  <li><strong>Rubros Financiables:</strong> (Inferido por el tipo de proyecto CTeI)
    <ul>
      <li>Talento Humano (personal de investigación, técnico y de apoyo).</li>
      <li>Adquisición de Equipos y Software especializados.</li>
      <li>Materiales e Insumos para investigación y desarrollo.</li>
      <li>Servicios Técnicos y Profesionales (consultorías, análisis de laboratorio).</li>
      <li>Gastos de Viaje y Salidas de Campo.</li>
      <li>Divulgación y Apropiación del Conocimiento.</li>
      <li>Adecuaciones y Mantenimiento menor de infraestructura (si es pertinente).</li>
      <li>Costos indirectos o de administración del proyecto (según topes permitidos).</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- _class: compact -->
<!-- header: '13. MAPA DE RIESGOS' -->
<h2>🛡️ Matriz de Riesgos</h2>
<!-- Si la tabla es muy larga, reduce fuente -->
<div style="font-size: 0.8em;">
  <p>Riesgos inferidos basados en la naturaleza de proyectos de fortalecimiento de CTeI:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li>Dificultad en la adopción o escalamiento de las tecnologías y soluciones desarrolladas por parte de los beneficiarios finales en Córdoba.</li>
      <li>Fallos en la integración de diferentes componentes tecnológicos o metodológicos dentro de los proyectos.</li>
      <li>Obsolescencia tecnológica de equipos o software adquiridos debido a la rápida evolución en el campo de la CTeI.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li>Retrasos en la ejecución de actividades debido a factores externos (climáticos, sociales, permisos locales) o internos (problemas de coordinación entre aliados).</li>
      <li>Alta rotación del personal clave del proyecto, afectando la continuidad y calidad de los resultados.</li>
      <li>Dificultades en la articulación y coordinación efectiva entre las múltiples entidades que conforman la alianza estratégica.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li>Insuficiencia de recursos para cubrir sobrecostos inesperados o cambios en las condiciones económicas (ej. inflación, fluctuación del dólar para importaciones).</li>
      <li>Dificultades en la justificación y legalización de gastos ante la entidad financiadora, lo que podría generar glosas o desembolsos tardíos.</li>
      <li>Posibles recortes presupuestales o cambios en las políticas de financiación a nivel nacional o regional que afecten la continuidad del proyecto.</li>
    </ul>
  </li>
</ul>
</div>

