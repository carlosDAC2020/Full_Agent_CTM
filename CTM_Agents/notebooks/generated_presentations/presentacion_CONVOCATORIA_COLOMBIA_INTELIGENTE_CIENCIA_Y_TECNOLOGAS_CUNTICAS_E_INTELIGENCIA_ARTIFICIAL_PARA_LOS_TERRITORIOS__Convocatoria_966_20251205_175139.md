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
  <li><strong>Apertura:</strong> No especificado en la información proporcionada.</li>
  <li><strong>Cierre:</strong> No especificado en la información proporcionada.</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca impulsar la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. El objetivo principal es generar un impacto medible en el desarrollo ambiental, social y económico de las regiones colombianas, contribuyendo al cierre de brechas tecnológicas y alineándose con la Política de Investigación e Innovación Orientada por Misiones.</li>
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
  <li><strong>Ejecutor:</strong> La convocatoria busca fortalecer la vinculación entre academia, industria y sector público, lo que sugiere que las propuestas pueden ser presentadas por Instituciones de Educación Superior (IES), centros de investigación, empresas y/o entidades públicas, preferiblemente en esquemas de colaboración.</li>
  <li><strong>Alianzas Obligatorias:</strong> La convocatoria promueve activamente la formación de alianzas entre academia, empresa y sociedad civil, buscando fortalecer un ecosistema de innovación competitivo. Aunque no se declara explícitamente como "obligatorio", la integración de múltiples actores es un factor clave para el fortalecimiento de las propuestas y la consecución de los objetivos.</li>
  <li><strong>Inhabilidades:</strong> No se especifican inhabilidades directas en la información proporcionada. Sin embargo, por inferencia en convocatorias de esta naturaleza, se suelen excluir entidades o personas que: <ul><li>No cumplan con los requisitos legales o fiscales para contratar con el Estado colombiano.</li><li>Presenten conflictos de interés con la entidad convocante o los evaluadores del proceso.</li></ul></li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene una focalización geográfica en los "territorios" y "regiones" del país, buscando contribuir al desarrollo ambiental, social y económico de estas áreas y cerrar brechas tecnológicas. No obstante, no se especifican departamentos, ciudades o zonas PDET específicas en la información detallada.</p>
<ul>
  <li>Impacto en los <strong>territorios</strong> y <strong>regiones</strong> de Colombia de manera general.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales, con múltiples líneas y sublíneas temáticas:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial:</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificación de especies, monitoreo de ecosistemas, conservación y fomento de innovación colaborativa para transformar recursos biológicos en bienes y servicios de alto valor.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Aplicaciones de IA en agricultura de precisión, agroindustria, gestión de recursos hídricos y trazabilidad de productos, orientadas a la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Aplicaciones de IA para pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), incluyendo modelos predictivos para redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de IA para apoyar el aprendizaje en áreas como matemáticas y programación, personalización de contenidos, reducción de brechas y promoción de competencias en diversos grupos etarios.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Desarrollo y aplicación de IA para detección temprana de desastres (inundaciones, incendios, deslizamientos) y protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Aplicaciones de IA para análisis de imágenes médicas, diagnóstico temprano de enfermedades, personalización de tratamientos y optimización de la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos cuánticos para procesamiento de información y comunicación. Incluye sublíneas como algoritmos cuánticos, simulación cuántica, circuitos integrados cuánticos y fotónicos, comunicaciones ultra seguras e internet cuántico.</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías cuánticas para detección, medición, trazabilidad y caracterización ultra precisa de fenómenos físicos, químicos o biológicos. Incluye sublíneas como sensores cuánticos para agricultura, salud, medioambiente, tecnologías para el desminado y metrología cuántica.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> La convocatoria se centra en "Investigación Aplicada, Desarrollo Tecnológico y la Innovación". Esto implica que los proyectos deben abarcar un rango de madurez tecnológica que va desde la investigación básica con potencial de aplicación (aproximadamente TRL 3-4) hasta el desarrollo de prototipos y soluciones demostradas en entornos relevantes o reales (aproximadamente TRL 6-7).</li>
  <li><strong>Componentes Obligatorios:</strong> Los proyectos deben incluir actividades que promuevan la transferencia tecnológica, el desarrollo de talento especializado y la reducción de brechas tecnológicas en el país. Asimismo, es fundamental que fortalezcan la vinculación entre la academia, la industria y el sector público.</li>
  <li><strong>Duración:</strong> La duración máxima de los proyectos no se especifica en la información proporcionada.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Basado en el objetivo de fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación, se infieren los siguientes entregables:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas.</li>
      <li>Ponencias en congresos nacionales e internacionales.</li>
      <li>Informes técnicos de investigación.</li>
      <li>Tesis de maestría y doctorado resultantes de las investigaciones.</li>
      <li>Modelos teóricos y marcos conceptuales.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de soluciones basadas en IA o tecnologías cuánticas.</li>
      <li>Software especializado o módulos de software (código fuente, documentación).</li>
      <li>Patentes, registros de propiedad intelectual o secretos industriales.</li>
      <li>Nuevos dispositivos, componentes o sistemas cuánticos.</li>
      <li>Metodologías o herramientas innovadoras.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y sensibilización dirigidos a comunidades.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Manuales de usuario o guías de implementación.</li>
      <li>Programas de formación de talento humano especializado.</li>
      <li>Resultados de investigación adaptados para el público general.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras en laboratorios para investigación cuántica o IA.</li>
      <li>Adquisición o desarrollo de equipos especializados (hardware cuántico, servidores de alto rendimiento).</li>
      <li>Plataformas o entornos computacionales para simulación y desarrollo.</li>
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
  <li><strong>Estándares:</strong> Para el eje de Inteligencia Artificial, se hace referencia a lo establecido en el <strong>CONPES 4144</strong>. Para las Tecnologías Cuánticas, se menciona la participación de un grupo de expertos para definir áreas clave, lo que implica una alineación con las tendencias y capacidades nacionales e internacionales en el campo. Aunque no se especifican normas ISO o sectoriales directas, los proyectos de desarrollo de software y sistemas de IA suelen adherirse a estándares de calidad de software (ej., <strong>ISO/IEC 25010</strong>) y seguridad de la información (ej., <strong>ISO/IEC 27001</strong>).</li>
  <li><strong>Hardware/Software:</strong> No se detallan especificaciones mínimas de hardware o software en la convocatoria. Sin embargo, para proyectos de IA, se inferiría la necesidad de infraestructura de cómputo de alto rendimiento (GPUs, TPUs), acceso a grandes volúmenes de datos y plataformas de desarrollo (Python, TensorFlow, PyTorch). Para tecnologías cuánticas, se requeriría acceso a hardware cuántico (simuladores, procesadores cuánticos) o herramientas de desarrollo y simulación cuántica.</li>
  <li><strong>Normatividad:</strong> La principal normatividad mencionada es el <strong>CONPES 4144</strong>, que guía el desarrollo, implementación y adopción ética y sostenible de soluciones basadas en IA en Colombia. Adicionalmente, cualquier proyecto deberá cumplir con la legislación colombiana vigente en materia de investigación, protección de datos (ej., Ley 1581 de 2012), ética en IA y propiedad intelectual.</li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca explícitamente contribuir al desarrollo ambiental, social y económico de las regiones y territorios del país, así como cerrar brechas tecnológicas. Se priorizan propuestas con un "enfoque territorial" que respondan a las necesidades específicas de las comunidades y regiones.</li>
  <li><strong>Enfoque Diferencial:</strong> La convocatoria promueve la "inclusión social" y la "reducción de brechas", enfatizando la "promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos" en el contexto de la transformación educativa con IA. Esto implica la necesidad de diseñar e implementar soluciones que consideren las particularidades y necesidades de diversos grupos poblacionales, incluyendo minorías, género y poblaciones vulnerables.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>Aunque no se detallan perfiles específicos, la naturaleza de la convocatoria en investigación aplicada, desarrollo tecnológico e innovación en áreas de alta complejidad (IA y tecnologías cuánticas) permite inferir los siguientes requisitos mínimos para el equipo:</p>
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con título de Doctorado (PhD) o Maestría en áreas relacionadas con Ciencias de la Computación, Ingeniería de Sistemas, Física Cuántica, Matemáticas Aplicadas o campos afines. Se espera una experiencia mínima de 5 a 10 años en gestión de proyectos de I+D+i y liderazgo de equipos de investigación.</li>
  <li><strong>Investigadores:</strong> Se requerirá la participación de investigadores con formación de Doctorado (PhD) o Maestría en las líneas temáticas específicas de la propuesta (ej., Machine Learning, Procesamiento del Lenguaje Natural, Física Cuántica, Criptografía Cuántica, etc.). Se valorará la experiencia en publicaciones científicas y desarrollo tecnológico previo.</li>
  <li><strong>Técnicos:</strong> Profesionales o tecnólogos con experiencia en desarrollo de software, implementación de prototipos, ingeniería de datos, administración de infraestructura tecnológica o soporte técnico especializado en las tecnologías relevantes para el proyecto.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Basado en las prácticas comunes para convocatorias de Minciencias y la naturaleza del proyecto, se infieren los siguientes documentos críticos:</p>
<ul>
  <li><strong>Documento Jurídico 1:</strong> Certificado de Existencia y Representación Legal de todas las entidades participantes (ejecutor y aliados), con una antigüedad no mayor a 30 días.</li>
  <li><strong>Documento Financiero 1:</strong> Estados Financieros auditados del último año fiscal de la entidad ejecutora, demostrando capacidad financiera para la ejecución del proyecto.</li>
  <li><strong>Certificaciones específicas:</strong> Certificaciones de grupos de investigación reconocidos por Minciencias, si aplica.</li>
  <li><strong>Avales institucionales:</strong> Carta de aval institucional por parte del representante legal de cada entidad participante, manifestando el compromiso con el proyecto y la disponibilidad de recursos (humanos, técnicos, financieros).</li>
  <li><strong>Cartas de intención:</strong> Cartas de intención o acuerdos de colaboración firmados entre el ejecutor y sus aliados estratégicos (academia, industria, sociedad civil), detallando roles y responsabilidades.</li>
  <li><strong>Hoja de Vida:</strong> Hojas de vida del equipo de trabajo principal, incluyendo soportes de títulos académicos y experiencia relevante.</li>
  <li><strong>Propuesta Técnica:</strong> Documento detallado que contenga la descripción del proyecto, justificación, objetivos, metodología, resultados esperados, cronograma y presupuesto.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> No especificado en la información proporcionada.</li>
  <li><strong>Tope por Proyecto:</strong> No especificado en la información proporcionada.</li>
  <li><strong>Contrapartida:</strong> No se especifica un porcentaje de contrapartida obligatorio. Sin embargo, en convocatorias de I+D+i, es común que se valore y/o se exija una contrapartida en efectivo y/o en especie por parte de las entidades participantes, demostrando su compromiso y cofinanciación.</li>
  <li><strong>Rubros Financiables:</strong> Aunque no se detallan explícitamente, los rubros financiables en este tipo de proyectos suelen incluir:
    <ul>
      <li>Personal científico y técnico (salarios, honorarios).</li>
      <li>Adquisición o alquiler de equipos y software especializado.</li>
      <li>Materiales e insumos para investigación y desarrollo.</li>
      <li>Servicios técnicos y profesionales (asesorías, consultorías).</li>
      <li>Viajes y salidas de campo (para recolección de datos, socialización).</li>
      <li>Publicaciones y divulgación de resultados.</li>
      <li>Adecuación de infraestructura menor.</li>
      <li>Gastos de administración y gerencia del proyecto.</li>
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
  <p>Dado que no se proporciona una matriz de riesgos explícita, se infieren los siguientes riesgos comunes para proyectos de ciencia y tecnología cuánticas e inteligencia artificial:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica:</strong> Rápida evolución de las tecnologías cuánticas e IA que podría dejar obsoleto el enfoque o las herramientas propuestas antes de la finalización del proyecto.</li>
      <li><strong>Fallos en la Integración:</strong> Dificultades o incompatibilidades técnicas en la integración de diferentes componentes de software, hardware o algoritmos.</li>
      <li><strong>Rendimiento Inesperado:</strong> Los modelos de IA o los prototipos cuánticos no alcanzan el rendimiento, la precisión o la escalabilidad esperados.</li>
      <li><strong>Disponibilidad de Datos:</strong> Dificultades para acceder a datos de calidad, suficientes o representativos para el entrenamiento y validación de modelos de IA.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en la Ejecución:</strong> Dificultades en la coordinación entre los equipos multidisciplinarios e interinstitucionales, o en la adquisición de equipos especializados (especialmente para tecnologías cuánticas que pueden requerir importación).</li>
      <li><strong>Rotación de Personal Clave:</strong> Pérdida de investigadores o técnicos altamente especializados durante la ejecución del proyecto, afectando el cronograma y los resultados.</li>
      <li><strong>Falta de Apropiación:</strong> Dificultad para lograr una apropiación efectiva de las soluciones por parte de los territorios o comunidades beneficiarias.</li>
      <li><strong>Cumplimiento Normativo:</strong> Desafíos en el cumplimiento de la normatividad ética y de privacidad de datos, especialmente en aplicaciones sensibles de IA (salud, seguridad).</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Sobrecostos Inesperados:</strong> Aumento de los costos de equipos, licencias de software o servicios especializados debido a la inflación o fluctuaciones del mercado.</li>
      <li><strong>Subestimación Presupuestal:</strong> El presupuesto inicial no es suficiente para cubrir todas las actividades y recursos necesarios para el éxito del proyecto.</li>
      <li><strong>Dependencia de Financiación Externa:</strong> Riesgo de recortes presupuestales o retrasos en los desembolsos por parte de las entidades financiadoras.</li>
    </ul>
  </li>
</ul>
</div>

