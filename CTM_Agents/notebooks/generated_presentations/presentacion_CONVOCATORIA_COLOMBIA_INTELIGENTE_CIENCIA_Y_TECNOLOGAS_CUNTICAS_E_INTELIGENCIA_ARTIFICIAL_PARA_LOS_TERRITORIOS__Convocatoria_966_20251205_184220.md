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

# CONVOCATORIA COLOMBIA INTELIGENTE: CIENCIA Y TECNOLOGÍAS CUÁNTICAS E INTELIGENCIA ARTIFICIAL PARA LOS TERRITORIOS | Convocatoria 966

### Informe de Inteligencia de Convocatoria

---

<!-- header: '1. DATOS GENERALES' -->
<div class="card warning">
  <h3>📅 Información Clave</h3>
  <ul>
  <li><strong>Entidad:</strong> Ministerio de Ciencia, Tecnología e Innovación (Minciencias)</li>
  <li><strong>Número:</strong> Convocatoria 966</li>
  <li><strong>Apertura:</strong> 25 de abril de 2025</li>
  <li><strong>Cierre:</strong> 18 de junio de 2025</li>
  <li><strong>Resumen:</strong> La convocatoria "Colombia Inteligente" busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. Su propósito es generar un impacto socioeconómico y ambiental significativo en las regiones del país, cerrando brechas tecnológicas y promoviendo la colaboración entre la academia, la industria y el sector público, en línea con la Política de Investigación e Innovación Orientada por Misiones.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones. Busca consolidar a Colombia como un referente en innovación tecnológica, abordando desafíos tecnológicos, productivos y sociales mediante soluciones disruptivas con impacto medible.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> Instituciones de Educación Superior (IES), centros de investigación, empresas nacionales con capacidades en CTeI, y otras entidades que conformen la comunidad científica y tecnológica.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se fomenta la vinculación de jóvenes investigadores e innovadores, estudiantes de maestría, estancias posdoctorales y la participación de semilleros de investigación (mínimo uno por proyecto, conformado por al menos diez estudiantes de pregrado a partir del tercer semestre). Se priorizan las alianzas entre academia, industria y sociedad civil.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>Una empresa nacional no puede estar relacionada en más de una propuesta dentro de esta convocatoria en el rol de empresa.</li>
      <li>Incumplimiento de requisitos legales o técnicos establecidos en los términos de referencia.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene un enfoque territorial explícito, buscando un impacto medible y ayudando a cerrar brechas tecnológicas en los territorios del país. Se orienta al desarrollo ambiental, social y económico de las regiones, sin especificar departamentos, ciudades o zonas PDET específicas, pero priorizando la relevancia y el impacto local de las propuestas.</p>
<ul>
  <li>No se especifican lugares geográficos concretos; la focalización es a nivel de "territorios" y "regiones" del país.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria se estructura en dos ejes temáticos principales, con líneas de trabajo detalladas:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial (IA):</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificación de especies, monitoreo de ecosistemas y conservación, fomentando la innovación colaborativa con conocimientos locales.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Aplicaciones de IA en agricultura de precisión, agroindustria, gestión hídrica y trazabilidad para la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Uso de IA para pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), y modelos predictivos para redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de IA para apoyar el aprendizaje en matemáticas y programación, personalización de contenidos y reducción de brechas tecnológicas.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Aplicación de IA para la detección temprana de desastres naturales y la protección de especies silvestres.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo de IA para análisis de imágenes médicas, diagnóstico temprano de enfermedades, personalización de tratamientos y optimización de atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong>
        <ul>
          <li><strong>Algoritmos cuánticos:</strong> Investigación e implementación para resolver problemas en física, química, biología, energía, salud y fármacos.</li>
          <li><strong>Simulación cuántica:</strong> Investigación y aplicación de herramientas y entornos de desarrollo (software y hardware).</li>
          <li><strong>Circuitos integrados cuánticos y fotónicos:</strong> Investigación en arquitectura y diseño, con perspectiva hacia la producción nacional.</li>
          <li><strong>Comunicaciones ultra seguras:</strong> Investigación e implementación de protocolos de criptografía cuántica.</li>
          <li><strong>Internet cuántico y nodos de red:</strong> Investigación e implementación de redes cuánticas de comunicación distribuidas y seguras.</li>
        </ul>
      </li>
      <li><strong>Sensórica Cuántica y Metrología:</strong>
        <ul>
          <li><strong>Sensores cuánticos para agricultura:</strong> Desarrollo de dispositivos de alta sensibilidad para variables críticas en agroindustria.</li>
          <li><strong>Sensores cuánticos para salud:</strong> Desarrollo de dispositivos de alta sensibilidad para medicina de precisión y diagnóstico temprano.</li>
          <li><strong>Sensores cuánticos para medioambiente:</strong> Desarrollo de dispositivos de alta sensibilidad para gestión ambiental.</li>
          <li><strong>Tecnologías para el desminado:</strong> Investigación y desarrollo de tecnologías de desminado seguro con capacidades sensóricas cuánticas.</li>
          <li><strong>Metrología cuántica:</strong> Implementación de patrones y unidades de medida aplicados a insumos médicos, alimentos y materiales estratégicos.</li>
        </ul>
      </li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> Se espera que los proyectos aborden la investigación aplicada y el desarrollo tecnológico, lo que implica un rango de madurez tecnológica. Si bien no se especifica un TRL inicial o final, la orientación a "soluciones disruptivas con impacto medible" y "transferencia tecnológica" sugiere que los proyectos deben avanzar desde etapas de investigación fundamental hacia prototipos o pruebas de concepto (aproximadamente TRL 3-6), con potencial de escalabilidad.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Vinculación de jóvenes investigadores e innovadores.</li>
      <li>Inclusión de estudiantes de maestría y estancias posdoctorales.</li>
      <li>Vinculación de al menos un semillero de investigación, compuesto por un mínimo de diez estudiantes de pregrado a partir del tercer semestre.</li>
      <li>Justificación de la integración estratégica de elementos complementarios entre los ejes temáticos (IA y Tecnologías Cuánticas) si aplica.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> No se especifica un tiempo máximo de ejecución en la información disponible. Sin embargo, para proyectos de investigación aplicada y desarrollo tecnológico de esta envergadura, la duración típica suele oscilar entre 12 y 36 meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Los entregables obligatorios se orientan a fortalecer las capacidades de CTeI y generar soluciones concretas:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas.</li>
      <li>Capítulos de libro o libros especializados.</li>
      <li>Tesis de maestría y doctorado desarrolladas en el marco del proyecto.</li>
      <li>Informes técnicos y metodológicos de investigación.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software (ej. algoritmos de IA, dispositivos cuánticos).</li>
      <li>Software desarrollado (código fuente, documentación, manuales de usuario).</li>
      <li>Patentes, modelos de utilidad o diseños industriales solicitados/concedidos.</li>
      <li>Demostradores de concepto o pruebas de concepto.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y transferencia de conocimiento a comunidades o sectores específicos.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Manuales o guías de uso para las tecnologías desarrolladas.</li>
      <li>Programas de formación para talento humano especializado (ej. en IA o tecnologías cuánticas).</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras en laboratorios para la implementación de las tecnologías.</li>
      <li>Adquisición o desarrollo de equipos especializados para investigación y desarrollo.</li>
      <li>Consolidación de capacidades computacionales o de laboratorio específicas para IA o tecnologías cuánticas.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Aunque no se especifican estándares técnicos explícitos en la información proporcionada o en los resultados de búsqueda, se infiere la aplicación de normas y directrices relevantes para el desarrollo de tecnologías avanzadas:</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>ISO/IEC 27001:</strong> Para la gestión de la seguridad de la información, especialmente relevante en el manejo de datos sensibles en proyectos de IA y comunicaciones seguras cuánticas.</li>
      <li><strong>ISO/IEC 42001:</strong> Para la gestión de la inteligencia artificial, abordando la gobernanza, ética y riesgos asociados a sistemas de IA.</li>
      <li><strong>IEEE P7000 Series:</strong> Estándares para el diseño ético de sistemas autónomos y de inteligencia artificial.</li>
      <li><strong>NIST Cybersecurity Framework:</strong> Para la gestión de riesgos de ciberseguridad en infraestructura y sistemas críticos.</li>
      <li><strong>Normatividad de Protección de Datos:</strong> Cumplimiento de la Ley 1581 de 2012 y el Decreto 1377 de 2013 en Colombia para el tratamiento de datos personales.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Especificaciones de Servidores y Plataformas:</strong> Requisitos de capacidad de procesamiento (GPUs, CPUs de alto rendimiento), almacenamiento y memoria para el entrenamiento de modelos de IA complejos y simulaciones cuánticas.</li>
      <li><strong>Lenguajes de Programación:</strong> Dominio de Python, R, Julia para IA; C++, Qiskit, Cirq para tecnologías cuánticas.</li>
      <li><strong>Frameworks y Librerías:</strong> Uso de TensorFlow, PyTorch, scikit-learn para IA; frameworks específicos de computación cuántica.</li>
      <li><strong>Arquitecturas de Hardware Cuántico:</strong> Familiaridad con diferentes plataformas (superconductores, iones atrapados, fotónica) si el proyecto implica desarrollo a nivel de hardware.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>CONPES 4144:</strong> Directrices para la Política Nacional de Desarrollo de la Inteligencia Artificial en Colombia.</li>
      <li><strong>Ley 1951 de 2019:</strong> Creación del Ministerio de Ciencia, Tecnología e Innovación.</li>
      <li><strong>Marco Ético para la IA:</strong> Cumplimiento de las directrices éticas para el desarrollo y uso de la IA en Colombia y a nivel internacional.</li>
      <li><strong>Regulaciones Sectoriales:</strong> Normas específicas para sectores como salud (ej. manejo de datos clínicos), agricultura o energía, donde se apliquen las tecnologías.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca explícitamente impulsar el desarrollo ambiental, social y económico de las regiones, contribuyendo al cierre de brechas tecnológicas en los territorios del país. Se priorizan propuestas con impacto medible a nivel local y regional.</li>
  <li><strong>Enfoque Diferencial:</strong> Se promueve la inclusión social y el cierre de brechas, con énfasis en la promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos. Esto implica considerar la diversidad de la población y las necesidades específicas de grupos vulnerables o minorías en el diseño y ejecución de los proyectos.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>El equipo mínimo requerido debe asegurar la capacidad técnica y de gestión del proyecto:</p>
<ul>
  <li><strong>Director/Gerente:</strong>
    <ul>
      <li><strong>Perfil:</strong> Profesional con título de Doctorado (PhD) o Maestría en áreas relacionadas con Ciencias de la Computación, Ingeniería de Sistemas, Física, Matemáticas, o campos afines a la Inteligencia Artificial o Tecnologías Cuánticas.</li>
      <li><strong>Experiencia:</strong> Mínimo 5 años de experiencia en dirección o coordinación de proyectos de investigación, desarrollo e innovación (I+D+i) en las temáticas de la convocatoria, con publicaciones científicas y experiencia en gestión de equipos multidisciplinarios.</li>
    </ul>
  </li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Nivel educativo requerido:</strong> Se espera la vinculación de investigadores con título de Doctorado (PhD) y Maestría en áreas pertinentes a los ejes temáticos de la convocatoria (IA o Tecnologías Cuánticas).</li>
      <li><strong>Jóvenes Investigadores e Innovadores:</strong> Vinculación obligatoria de profesionales recién egresados o estudiantes de posgrado con potencial en investigación.</li>
      <li><strong>Estudiantes de Maestría y Estancias Posdoctorales:</strong> Inclusión de estudiantes de posgrado para fortalecer la capacidad investigativa y la formación de alto nivel.</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong>
    <ul>
      <li><strong>Perfiles de apoyo:</strong> Profesionales o tecnólogos con experiencia en desarrollo de software, manejo de hardware especializado, análisis de datos, o soporte técnico relevante para la ejecución de los proyectos.</li>
      <li><strong>Semilleros de Investigación:</strong> Vinculación de un semillero de investigación conformado por un mínimo de diez (10) estudiantes de pregrado a partir del tercer semestre.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Lista de documentos críticos para la postulación:</p>
<ul>
  <li>Propuesta técnica y financiera del proyecto, alineada con los ejes y líneas temáticas de la convocatoria.</li>
  <li>Documentos que acrediten la personería jurídica y representación legal de la entidad ejecutora y de los aliados.</li>
  <li>Certificados de experiencia de la entidad ejecutora y del equipo de trabajo en proyectos de I+D+i.</li>
  <li>Documento que acredite la fecha de constitución y el listado de integrantes del semillero de investigación vinculado.</li>
  <li>Cartas de compromiso de los investigadores, jóvenes investigadores, estudiantes de maestría y posdoctorales.</li>
  <li>Avales institucionales de la entidad ejecutora y de las entidades aliadas.</li>
  <li>Certificaciones financieras que demuestren la solidez económica de la entidad ejecutora.</li>
  <li>Declaración de no inhabilidades e incompatibilidades.</li>
  <li>Plan de trabajo detallado y cronograma de actividades.</li>
  <li>Presupuesto detallado del proyecto con la distribución de rubros y fuentes de financiación.</li>
  <li>Documentos que soporten la contrapartida (si aplica).</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> No se especifica un monto total de la bolsa en la información pública disponible. Los términos de referencia y sus anexos suelen contener esta información detallada.</li>
  <li><strong>Tope por Proyecto:</strong> No se especifica un tope máximo de financiación por proyecto en la información pública disponible. Esta información se encuentra detallada en los términos de referencia o anexos financieros.</li>
  <li><strong>Contrapartida:</strong> No se especifica un porcentaje de contrapartida exigido en efectivo y/o especie en la información pública disponible. Es común en este tipo de convocatorias que se solicite un porcentaje de cofinanciación por parte de la entidad ejecutora o sus aliados.</li>
  <li><strong>Rubros Financiables:</strong> Aunque no se detallan explícitamente, se infieren rubros comunes para proyectos de I+D+i en tecnologías avanzadas:
    <ul>
      <li>Personal científico y técnico (salarios, honorarios).</li>
      <li>Adquisición y mantenimiento de equipos especializados (hardware, software, licencias).</li>
      <li>Materiales e insumos para investigación.</li>
      <li>Servicios técnicos y profesionales externos.</li>
      <li>Movilidad y salidas de campo (para recolección de datos, visitas técnicas).</li>
      <li>Publicaciones científicas y divulgación.</li>
      <li>Formación de talento humano (becas, pasantías).</li>
      <li>Adecuación y mantenimiento de infraestructura de laboratorios.</li>
      <li>Gastos de administración y gerencia del proyecto (indirectos).</li>
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
  <p>Basado en la naturaleza de proyectos de alta tecnología como IA y Tecnologías Cuánticas, se infieren los siguientes riesgos:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica Rápida:</strong> Las tecnologías cuánticas y de IA evolucionan a gran velocidad, lo que puede hacer que las soluciones propuestas queden desactualizadas antes o durante la ejecución del proyecto.</li>
      <li><strong>Fallos en la Integración de Componentes:</strong> Dificultades en la integración de diferentes módulos de software, hardware o plataformas cuánticas, afectando la funcionalidad esperada.</li>
      <li><strong>Rendimiento Inferior al Esperado:</strong> Los algoritmos de IA o los prototipos cuánticos pueden no alcanzar los niveles de precisión o eficiencia previstos en entornos reales.</li>
      <li><strong>Limitaciones de Datos:</strong> Insuficiencia o baja calidad de los conjuntos de datos disponibles para el entrenamiento de modelos de IA, impactando la robustez de las soluciones.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en la Importación de Equipos:</strong> Demoras en la adquisición o importación de hardware especializado (ej. computadoras cuánticas, sensores avanzados) debido a trámites aduaneros o restricciones internacionales.</li>
      <li><strong>Rotación de Personal Clave:</strong> Pérdida de investigadores o técnicos con experiencia crítica en IA o tecnologías cuánticas durante la ejecución del proyecto, afectando el cronograma y los resultados.</li>
      <li><strong>Dificultades en la Colaboración Interinstitucional:</strong> Problemas de comunicación, coordinación o alineación de objetivos entre los diferentes actores (academia, industria, sociedad civil) de las alianzas.</li>
      <li><strong>Acceso Restringido a Infraestructura:</strong> Limitaciones en el acceso a laboratorios especializados o recursos computacionales de alto rendimiento necesarios para el desarrollo y prueba de las soluciones.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Sobrecostos Tecnológicos Inesperados:</strong> Aumento en el precio de componentes de hardware, software o licencias debido a fluctuaciones del mercado o cambios en las especificaciones.</li>
      <li><strong>Fluctuación del Tipo de Cambio:</strong> Impacto negativo en el presupuesto de proyectos que requieren la adquisición de bienes o servicios importados, afectando la capacidad de compra.</li>
      <li><strong>Recortes Presupuestales o Retrasos en Desembolsos:</strong> Modificaciones en la disponibilidad de fondos por parte de la entidad financiadora o demoras en los giros, afectando la liquidez del proyecto.</li>
      <li><strong>Insuficiencia de Contrapartida:</strong> Dificultades para asegurar la cofinanciación comprometida por la entidad ejecutora o sus aliados, poniendo en riesgo la viabilidad financiera del proyecto.</li>
    </ul>
  </li>
</ul>
</div>

