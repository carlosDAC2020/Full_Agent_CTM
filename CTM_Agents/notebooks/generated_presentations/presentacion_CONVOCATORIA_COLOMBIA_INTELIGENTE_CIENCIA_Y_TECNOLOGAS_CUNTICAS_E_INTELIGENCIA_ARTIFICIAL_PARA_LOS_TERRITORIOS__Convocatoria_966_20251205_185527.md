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
  <li><strong>Cierre:</strong> 18 de junio de 2025 04:00 pm</li>
  <li><strong>Resumen:</strong> Esta convocatoria busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. El objetivo es generar un impacto medible que contribuya al desarrollo ambiental, social y económico de las regiones colombianas, alineándose con la Política de Investigación e Innovación Orientada por Misiones para cerrar brechas tecnológicas.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> La convocatoria está dirigida a la comunidad científica, académica, empresarial (micro, pequeñas y medianas empresas constituidas legalmente en Colombia), sociedad civil y demás actores interesados en CTeI.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se priorizan propuestas que fortalezcan la vinculación entre academia, industria y sector público. Se exige una alianza estratégica mínima que involucre entidades ejecutoras y otras entidades que integren la alianza.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>No cumplir con los requisitos legales y financieros establecidos en los términos de referencia de la convocatoria.</li>
      <li>No presentar la totalidad de la documentación obligatoria dentro de los plazos y formatos estipulados.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene una focalización nacional con un claro enfoque territorial, buscando el impacto en el desarrollo ambiental, social y económico de las diversas regiones del país. No se especifican departamentos o ciudades puntuales, sino que se orienta a proyectos que contribuyan al cierre de brechas tecnológicas en los territorios.</p>
<ul>
  <li>Impacto en el desarrollo territorial a nivel nacional.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales, permitiendo la integración complementaria de elementos del otro eje si se justifica adecuadamente:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial:</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificación de especies, monitoreo de ecosistemas y conservación, fomentando la innovación colaborativa con conocimientos locales.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Aplicaciones de IA en agricultura de precisión, agroindustria, gestión hídrica y trazabilidad para la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de IA para pronóstico, control y uso sostenible de fuentes limpias, impulsando sistemas energéticos más eficientes.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de IA para apoyar el aprendizaje, personalizar contenidos y reducir brechas tecnológicas en diferentes grupos etarios.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Aplicación de IA para la detección temprana de desastres naturales y la protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo de IA para análisis de imágenes médicas, diagnóstico temprano de enfermedades, personalización de tratamientos y optimización de la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos cuánticos para procesamiento de información y comunicación ultra segura, incluyendo simulación cuántica, circuitos integrados y redes cuánticas.</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías cuánticas para detección, medición y caracterización ultra precisa de fenómenos físicos, químicos o biológicos con impacto en sectores estratégicos como agricultura, salud, medioambiente y desminado.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> Los proyectos deben fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación, lo que implica un rango de madurez tecnológica que puede iniciar en TRL 3-4 (prueba de concepto, validación en laboratorio) y aspirar a TRL 6-7 (prototipo a escala, demostración en entorno relevante).</li>
  <li><strong>Componentes Obligatorios:</strong> Los proyectos deben incluir la transferencia tecnológica, el desarrollo de talento especializado (vinculación de jóvenes investigadores, estudiantes de maestría y estancias posdoctorales), y la reducción de brechas tecnológicas. Se exige la vinculación entre academia, industria y sector público.</li>
  <li><strong>Duración:</strong> Aunque no está explícitamente detallada, proyectos de esta naturaleza suelen tener una duración estimada entre 12 y 24 meses, dependiendo de la complejidad y alcance tecnológico propuesto.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  Clasifica los entregables obligatorios (busca en anexos técnicos):
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Publicaciones científicas (artículos en revistas indexadas).</li>
      <li>Capítulos de libro o libros resultado de investigación.</li>
      <li>Tesis de maestría o doctorado desarrolladas en el marco del proyecto.</li>
      <li>Informes técnicos de investigación aplicada.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales (hardware o software) de soluciones basadas en IA o tecnologías cuánticas.</li>
      <li>Software especializado o plataformas tecnológicas.</li>
      <li>Patentes, diseños industriales o registros de propiedad intelectual.</li>
      <li>Modelos predictivos o algoritmos avanzados.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y divulgación tecnológica.</li>
      <li>Eventos de socialización de resultados a la comunidad.</li>
      <li>Manuales de usuario o guías de implementación de tecnologías.</li>
      <li>Semilleros de investigación y formación de jóvenes talentos.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuación o mejora de laboratorios para investigación cuántica o IA.</li>
      <li>Adquisición de equipos especializados para el desarrollo tecnológico.</li>
      <li>Desarrollo de entornos de simulación cuántica o plataformas de datos para IA.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  Investiga estándares técnicos específicos. NO digas "No especificado" sin buscar "Anexo Técnico".
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li>Para proyectos de IA: Se infiere el cumplimiento de estándares éticos para el desarrollo y uso de IA, como las directrices de la OCDE sobre IA, y buenas prácticas en ciencia de datos y aprendizaje automático. Podrían aplicarse estándares ISO para gestión de calidad (ISO 9001) y seguridad de la información (ISO 27001) para el desarrollo de software.</li>
      <li>Para tecnologías cuánticas: Se espera la aplicación de estándares emergentes en metrología cuántica y protocolos de comunicación segura, así como buenas prácticas en diseño de circuitos cuánticos y fotónicos.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li>No se especifican marcas o modelos mínimos, pero se espera que las soluciones de software y hardware sean robustas, escalables y compatibles con las tecnologías cuánticas y de IA más recientes. Para IA, se infiere la necesidad de infraestructura computacional adecuada (GPUs, CPUs de alto rendimiento) y entornos de desarrollo (Python, R, frameworks como TensorFlow, PyTorch). Para cuántica, se espera el uso de plataformas de programación cuántica (Qiskit, Cirq) o simuladores.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>CONPES 4144:</strong> Que establece la Política Nacional de Inteligencia Artificial en Colombia, siendo un marco fundamental para el desarrollo de proyectos en este eje.</li>
      <li>Ley 1951 de 2019: Por la cual se crea el Ministerio de Ciencia, Tecnología e Innovación, que rige las acciones de la entidad.</li>
      <li>Normativa de protección de datos personales (Ley 1581 de 2012) para proyectos que involucren manejo de información sensible.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca específicamente contribuir al desarrollo ambiental, social y económico de las regiones del país, promoviendo el cierre de brechas tecnológicas en los territorios. Los proyectos deben tener un impacto medible a nivel regional.</li>
  <li><strong>Enfoque Diferencial:</strong> Se promueve la inclusión social y la reducción de brechas. Aunque no se detallan grupos específicos, se espera que los proyectos fomenten la participación de poblaciones diversas y consideren el impacto en comunidades vulnerables o minorías, así como la promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  Detalla el equipo mínimo requerido (Busca en "Condiciones Habilitantes"):
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con formación de posgrado (Maestría o Doctorado) y experiencia demostrable en gestión de proyectos de investigación aplicada, desarrollo tecnológico o innovación en áreas afines a las tecnologías cuánticas o Inteligencia Artificial.</li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Investigadores Principales:</strong> Se requiere personal con nivel educativo de Doctorado (PhD) o Maestría, con trayectoria reconocida en investigación en las líneas temáticas de la convocatoria.</li>
      <li><strong>Jóvenes Investigadores e Innovadores:</strong> Vinculación obligatoria de jóvenes talentos, lo que implica perfiles en formación o recién egresados con interés en CTeI.</li>
      <li><strong>Estudiantes de Maestría:</strong> Participación activa de estudiantes de posgrado en el desarrollo de los proyectos.</li>
      <li><strong>Estancias Posdoctorales:</strong> Vinculación de investigadores con formación posdoctoral.</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong> Perfiles de apoyo técnico especializados en áreas como desarrollo de software, ingeniería de datos, electrónica, física cuántica, con experiencia práctica en la implementación de soluciones tecnológicas.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  Lista tipo checklist de los documentos más críticos para no ser descartado:
<ul>
  <li>Formulario electrónico de inscripción del proyecto en el Sistema Integrado de Gestión de Proyectos (SIGP) de Minciencias.</li>
  <li>Carta de Aval institucional de la entidad proponente.</li>
  <li>Anexo 2 —CARTA DE EXPERIENCIA DE LA EMPRESA NACIONAL— (cuando aplique, demostrando experiencia en al menos tres proyectos ejecutados en los últimos cinco años).</li>
  <li>Documentos jurídicos que acrediten la existencia y representación legal de la entidad ejecutora y los aliados.</li>
  <li>Certificaciones de experiencia del equipo de trabajo.</li>
  <li>Cuando aplique, aprobación de Comité de Ética o Bioética.</li>
  <li>Propuesta técnica y financiera detallada, conforme a los anexos de la convocatoria.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> No se especifica un monto total de la bolsa para la convocatoria general. Sin embargo, se ha mencionado una inversión total de $1.771 millones para alianzas específicas.</li>
  <li><strong>Tope por Proyecto:</strong> No se especifica un tope máximo por proyecto en la información disponible.</li>
  <li><strong>Contrapartida:</strong> Se exige una contrapartida mínima equivalente al 20% del monto total solicitado para la financiación del proyecto, la cual debe ser en dinero y/o especie.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li>Personal científico y técnico (incluyendo estancias posdoctorales, jóvenes investigadores, estudiantes de maestría).</li>
      <li>Adquisición o adecuación de equipos e infraestructura.</li>
      <li>Materiales e insumos para investigación y desarrollo.</li>
      <li>Servicios técnicos especializados.</li>
      <li>Actividades de divulgación y apropiación social del conocimiento.</li>
      <li>Gastos de viaje y manutención asociados a actividades del proyecto.</li>
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
  Si no hay matriz de riesgos explícita, INFIERELOS basados en proyectos similares de tecnología/ciencia:
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li>Obsolescencia tecnológica rápida en campos como IA y cuántica, afectando la pertinencia de las soluciones a largo plazo.</li>
      <li>Dificultades en la integración de tecnologías emergentes o en el desarrollo de algoritmos complejos.</li>
      <li>Fallos en la validación de prototipos o en la escalabilidad de las soluciones a entornos reales.</li>
      <li>Ciberseguridad y protección de datos, especialmente en aplicaciones de IA y comunicaciones cuánticas.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li>Retrasos en la importación de equipos o componentes especializados necesarios para la investigación.</li>
      <li>Alta rotación de personal altamente calificado en áreas de IA y cuántica, dificultando la continuidad del proyecto.</li>
      <li>Falta de acceso a infraestructura computacional o de laboratorio adecuada en los territorios.</li>
      <li>Dificultades en la gestión de alianzas entre academia, industria y sector público, afectando la ejecución coordinada.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li>Fluctuaciones en las tasas de cambio si se requieren insumos o servicios internacionales.</li>
      <li>Posibles sobrecostos no previstos debido a la naturaleza experimental de las tecnologías.</li>
      <li>Insuficiencia de la contrapartida prometida, ya sea en efectivo o en especie.</li>
      <li>Cambios en la política de financiación o prioridades del Ministerio durante la ejecución del proyecto.</li>
    </ul>
  </li>
</ul>
</div>

