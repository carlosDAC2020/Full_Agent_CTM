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
  <li><strong>Número:</strong> 966</li>
  <li><strong>Apertura:</strong> 25 de abril de 2025</li>
  <li><strong>Cierre:</strong> 26 de mayo de 2025, 4:00 p.m. (hora colombiana):</strong> 25 de abril de 2025</li>
  <li><strong>Cierre:</strong> 26 de mayo de 2025, 4:00 p.m. (hora colombiana)</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. Su propósito es generar un impacto medible en el desarrollo ambiental, social y económico de las regiones del país, contribuyendo al cierre de brechas tecnológicas y consolidando a Colombia como un referente en innovación a través de la Política de Investigación e Innovación Orientada por Misiones.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones. La convocatoria busca consolidar a Colombia como un referente en innovación tecnológica, abordando desafíos tecnológicos, productivos y sociales mediante soluciones disruptivas con impacto medible y promoviendo la transferencia tecnológica, el desarrollo de talento especializado y la reducción de brechas tecnológicas.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> La propuesta debe ser presentada por una Institución de Educación Superior (IES) que actuará como entidad ejecutora principal.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se exige una alianza estratégica conformada por una Institución de Educación Superior (IES), una Empresa Nacional y un mínimo de una (1) Organización Local – Regional.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>Una empresa nacional no puede estar relacionada en más de una propuesta de esta convocatoria.</li>
      <li>Las entidades que presenten información inconsistente o falsa en su propuesta serán excluidas.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene un enfoque nacional, priorizando el impacto en el desarrollo ambiental, social y económico de las regiones del país, con el objetivo de cerrar brechas tecnológicas. No se especifican departamentos, ciudades o zonas PDET específicas, sino que se busca un impacto generalizado en los territorios.</p>
<ul>
  <li>Territorios del país en general, con énfasis en el cierre de brechas tecnológicas regionales.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria se estructura en dos ejes estratégicos principales, permitiendo la integración de elementos complementarios del otro eje si se justifica su impacto, viabilidad y madurez tecnológica.</p>
<ul>
  <li><strong>EJE TEMÁTICO INTELIGENCIA ARTIFICIAL:</strong> Responde al CONPES 4144, promoviendo el desarrollo y la adopción ética y sostenible de soluciones basadas en IA en sectores estratégicos.
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo de IA para clasificación de especies, monitoreo de ecosistemas, estrategias de conservación e innovación colaborativa.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Aplicaciones de IA en agricultura de precisión, agroindustria, gestión hídrica y trazabilidad para la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> IA para pronóstico, control y uso sostenible de fuentes limpias, y modelos predictivos para redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de IA para apoyar el aprendizaje, personalizar contenidos y reducir brechas tecnológicas.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Aplicación de IA para la detección temprana de desastres y la protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo de IA para análisis de imágenes médicas, diagnóstico temprano, personalización de tratamientos y optimización de la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>EJE TEMÁTICO CIENCIA Y TECNOLOGÍAS CUÁNTICAS:</strong> Definido por un grupo de expertos, enfocado en pertinencia científica, tecnológica y alineación con capacidades nacionales.
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos cuánticos.
        <ul>
          <li>Algoritmos cuánticos para física, química, biología, energía, salud y fármacos.</li>
          <li>Simulación cuántica (software y hardware).</li>
          <li>Circuitos integrados cuánticos y fotónicos (diseño y perspectiva de producción nacional).</li>
          <li>Comunicaciones ultra seguras (criptografía cuántica).</li>
          <li>Internet cuántico y nodos de red.</li>
        </ul>
      </li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías cuánticas para detección, medición y caracterización ultra precisa.
        <ul>
          <li>Sensores cuánticos para agricultura (control de plagas, calidad de suelos).</li>
          <li>Sensores cuánticos para salud (medicina de precisión, diagnóstico temprano, biotecnología).</li>
          <li>Sensores cuánticos para medioambiente (gestión ambiental).</li>
          <li>Tecnologías para el desminado (capacidades sensóricas cuánticas).</li>
          <li>Metrología cuántica (patrones y unidades de medida aplicados a insumos médicos, alimentos y materiales).</li>
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
  <li><strong>TRL Esperado:</strong> La convocatoria busca fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación. Esto implica proyectos que pueden iniciar en niveles de madurez tecnológica intermedios (TRL 3-4) y aspirar a alcanzar niveles más avanzados (TRL 6-7) que permitan la validación en entornos relevantes o demostración de prototipos en sistemas operativos.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Investigación aplicada y desarrollo de soluciones disruptivas en IA o Tecnologías Cuánticas.</li>
      <li>Transferencia tecnológica efectiva de los resultados de investigación.</li>
      <li>Desarrollo y formación de talento humano especializado en las áreas de la convocatoria.</li>
      <li>Reducción de brechas tecnológicas en los territorios del país.</li>
      <li>Vinculación y fortalecimiento del ecosistema entre academia, industria y sector público.</li>
      <li>Impacto medible en el desarrollo ambiental, social y económico de las regiones.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> No se especifica un tiempo máximo de ejecución en la información disponible. Se infiere que la duración debe ser coherente con el alcance y la complejidad de los proyectos de investigación aplicada y desarrollo tecnológico propuestos.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Basado en la naturaleza de la convocatoria en Ciencia, Tecnología e Innovación, se esperan los siguientes entregables:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Publicaciones científicas (artículos en revistas indexadas, capítulos de libro).</li>
      <li>Ponencias y presentaciones en eventos académicos nacionales e internacionales.</li>
      <li>Trabajos de grado (tesis de maestría y doctorado) asociados a los proyectos.</li>
      <li>Bases de datos o repositorios de información generada.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software basados en IA o tecnologías cuánticas.</li>
      <li>Desarrollos de software (algoritmos, plataformas, aplicaciones) con código fuente documentado.</li>
      <li>Patentes o solicitudes de propiedad intelectual (modelos de utilidad, diseños industriales).</li>
      <li>Desarrollo de nuevas metodologías o procesos tecnológicos.</li>
      <li>Reportes técnicos de validación y pruebas de los desarrollos.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Realización de talleres, seminarios y eventos de divulgación científica y tecnológica.</li>
      <li>Elaboración de manuales, guías o material didáctico para la apropiación del conocimiento.</li>
      <li>Programas de formación o capacitación para comunidades o sectores específicos.</li>
      <li>Publicaciones de divulgación (infografías, videos, artículos de prensa).</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuación o mejora de laboratorios y espacios para la investigación.</li>
      <li>Adquisición o desarrollo de equipos especializados para IA o tecnologías cuánticas.</li>
      <li>Implementación de infraestructura computacional o de red avanzada.</li>
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
  <li><strong>Estándares:</strong>
    <ul>
      <li>Para proyectos de Inteligencia Artificial, se esperan consideraciones éticas y de seguridad en el desarrollo y despliegue, alineadas con principios de IA responsable (ej. CONPES 4144).</li>
      <li>En el desarrollo de software, se pueden inferir estándares de calidad de software (ej. ISO/IEC 25000 series, metodologías ágiles).</li>
      <li>Para la gestión de datos, se podrían aplicar normativas de privacidad y seguridad de la información (ej. ISO 27001, leyes de protección de datos personales).</li>
      <li>En tecnologías cuánticas, se considerarían estándares emergentes para la interoperabilidad y seguridad de sistemas cuánticos.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li>Se requeriría infraestructura computacional robusta para el entrenamiento de modelos de IA (ej. GPUs de alto rendimiento, clusters de cómputo).</li>
      <li>Para tecnologías cuánticas, se podría requerir acceso a plataformas de cómputo cuántico (nubes cuánticas) o hardware cuántico especializado.</li>
      <li>Lenguajes de programación y frameworks comunes en IA (Python, TensorFlow, PyTorch) y en computación cuántica (Qiskit, Cirq) son esperables.</li>
      <li>Herramientas de simulación y desarrollo para entornos cuánticos.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>CONPES 4144:</strong> “Política Nacional de Inteligencia Artificial” como marco de referencia para el eje de IA.</li>
      <li>Ley 1951 de 2019, por la cual se crea el Ministerio de Ciencia, Tecnología e Innovación.</li>
      <li>Leyes y decretos relacionados con la gestión de recursos públicos y la contratación estatal en Colombia.</li>
      <li>Normativa de protección de datos personales (Ley 1581 de 2012 y sus decretos reglamentarios) cuando los proyectos involucren información sensible.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca explícitamente impulsar proyectos que generen un impacto medible y ayuden a cerrar brechas tecnológicas en los territorios del país. Esto implica que las propuestas deben demostrar cómo sus soluciones se adaptarán y beneficiarán a las necesidades y contextos específicos de las regiones, contribuyendo al desarrollo ambiental, social y económico local.</li>
  <li><strong>Enfoque Diferencial:</strong> Se promueve la inclusión social y el cierre de brechas, especialmente en el eje de Inteligencia Artificial para la Transformación Educativa, donde se busca la promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos. Esto sugiere la necesidad de considerar la diversidad de la población y garantizar que los beneficios de los proyectos lleguen a grupos históricamente marginados o con menos acceso a la tecnología.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>La convocatoria enfatiza la formación de talento especializado y la vinculación de jóvenes investigadores. Se infieren los siguientes perfiles:</p>
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con formación de posgrado (Maestría o Doctorado) en áreas de ciencia, tecnología, ingeniería o campos relacionados. Experiencia demostrable en la dirección y gestión de proyectos de investigación, desarrollo tecnológico e innovación, preferiblemente en IA o tecnologías cuánticas, con al menos 5 años de experiencia relevante.</li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Investigadores Principales:</strong> Profesionales con grado de Doctorado (PhD) en áreas afines a la línea temática del proyecto (ej. Ciencias de la Computación, Física Cuántica, Ingeniería Electrónica, Bioinformática), con trayectoria reconocida en investigación y publicaciones.</li>
      <li><strong>Coinvestigadores:</strong> Profesionales con grado de Maestría o Doctorado, con experiencia en las áreas específicas del proyecto y capacidad para liderar actividades de investigación.</li>
      <li><strong>Jóvenes Investigadores e Innovadores:</strong> Profesionales recién egresados o estudiantes de posgrado (Maestría) vinculados al proyecto para fortalecer sus capacidades.</li>
      <li><strong>Estancias Posdoctorales:</strong> Investigadores con Doctorado que realizan una estancia de investigación en el marco del proyecto.</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong>
    <ul>
      <li><strong>Ingenieros de Desarrollo:</strong> Profesionales con experiencia en desarrollo de software, implementación de algoritmos de IA, o diseño de sistemas electrónicos/cuánticos.</li>
      <li><strong>Técnicos de Laboratorio:</strong> Personal de apoyo con conocimientos específicos en la operación de equipos, mantenimiento de infraestructura tecnológica y recolección de datos.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Basado en las características de las convocatorias de Minciencias y la información disponible, los documentos críticos para la participación incluirían:</p>
<ul>
  <li><strong>Documento Jurídico 1:</strong> Certificado de Existencia y Representación Legal de la Institución de Educación Superior (IES) ejecutora y de la Empresa Nacional aliada, con fecha de expedición reciente.</li>
  <li><strong>Documento Financiero 1:</strong> Estados Financieros auditados de la IES ejecutora y de la Empresa Nacional, que demuestren solidez financiera.</li>
  <li><strong>Certificaciones específicas:</strong> Certificaciones de experiencia de la IES y la Empresa Nacional en proyectos de CTeI relacionados con la temática de la convocatoria.</li>
  <li><strong>Avales institucionales:</strong> Carta de aval institucional de la IES ejecutora, comprometiéndose con la ejecución del proyecto y la asignación de recursos humanos y de infraestructura.</li>
  <li><strong>Cartas de intención:</strong> Cartas de compromiso o intención de las Organizaciones Locales – Regionales participantes en la alianza, detallando su rol y aportes.</li>
  <li><strong>Hoja de Vida:</strong> Perfiles de los investigadores principales y del equipo de trabajo, con soportes de formación académica y experiencia relevante.</li>
  <li><strong>Propuesta Técnica y Económica:</strong> Documento detallado que contenga la descripción del proyecto, metodología, cronograma, presupuesto y resultados esperados.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> $20.000.000.000 (Veinte mil millones de pesos colombianos).</li>
  <li><strong>Tope por Proyecto:</strong> No se especifica un tope máximo por proyecto en la información disponible. El monto a solicitar debe ser coherente con el alcance, la complejidad y los resultados esperados del proyecto.</li>
  <li><strong>Contrapartida:</strong> No se especifica un porcentaje de contrapartida exigido en efectivo o especie en la información disponible. Sin embargo, es usual en este tipo de convocatorias la exigencia de contrapartida institucional.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li>Personal científico, técnico y de apoyo vinculado directamente al proyecto.</li>
      <li>Adquisición o arrendamiento de equipos de laboratorio, hardware y software especializados.</li>
      <li>Materiales e insumos necesarios para la investigación y desarrollo.</li>
      <li>Servicios técnicos y profesionales externos.</li>
      <li>Gastos de viaje y manutención para salidas de campo, asistencia a eventos o capacitación.</li>
      <li>Publicaciones y difusión de resultados.</li>
      <li>Adecuaciones menores de infraestructura para la ejecución del proyecto.</li>
      <li>Costos indirectos de administración y gestión del proyecto.</li>
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
  <p>Basado en la naturaleza de proyectos de alta tecnología, investigación y desarrollo con enfoque territorial, se pueden inferir los siguientes riesgos:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica:</strong> Dada la rápida evolución de la IA y las tecnologías cuánticas, existe el riesgo de que las tecnologías seleccionadas queden obsoletas antes de la finalización del proyecto.</li>
      <li><strong>Fallos en la Integración:</strong> Dificultades en la integración de diferentes componentes tecnológicos (hardware, software, algoritmos) o en la interoperabilidad con sistemas existentes.</li>
      <li><strong>Limitaciones de Rendimiento:</strong> Los prototipos o soluciones desarrolladas pueden no alcanzar los niveles de rendimiento o precisión esperados en entornos reales.</li>
      <li><strong>Disponibilidad de Datos:</strong> Dificultades para acceder a datos de calidad, suficientes o relevantes para el entrenamiento de modelos de IA, especialmente con enfoque territorial.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en Adquisiciones/Importaciones:</strong> Demoras en la adquisición o importación de equipos especializados o componentes tecnológicos necesarios.</li>
      <li><strong>Rotación de Personal Especializado:</strong> Pérdida de talento humano clave con experticia en IA o tecnologías cuánticas, lo que puede afectar la continuidad y calidad del proyecto.</li>
      <li><strong>Dificultades en la Coordinación de Alianzas:</strong> Desafíos en la gestión y coordinación efectiva entre la IES, la Empresa Nacional y las Organizaciones Locales – Regionales.</li>
      <li><strong>Acceso a Infraestructura:</strong> Limitaciones en el acceso o disponibilidad de infraestructura computacional o de laboratorio necesaria para las fases de desarrollo y prueba.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Fluctuación del Tipo de Cambio:</strong> Impacto negativo de la variación del dólar u otras divisas en la adquisición de equipos importados o licencias de software.</li>
      <li><strong>Sobrecostos Inesperados:</strong> Surgimiento de gastos no previstos debido a la complejidad de la investigación, cambios tecnológicos o problemas técnicos.</li>
      <li><strong>Recortes Presupuestales:</strong> Posibles ajustes o recortes en la financiación asignada al proyecto por parte de la entidad financiadora.</li>
    </ul>
  </li>
</ul>
</div>

