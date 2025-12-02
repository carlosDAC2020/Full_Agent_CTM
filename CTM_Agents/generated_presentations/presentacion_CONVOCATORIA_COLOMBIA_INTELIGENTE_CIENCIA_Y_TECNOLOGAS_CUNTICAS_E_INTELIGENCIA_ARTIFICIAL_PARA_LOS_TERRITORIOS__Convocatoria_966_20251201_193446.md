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
  <li><strong>Cierre:</strong> 18 de junio de 2025</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca:</strong> 25 de abril de 2025</li>
  <li><strong>Cierre:</strong> 18 de junio de 2025</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial. Su objetivo principal es contribuir al desarrollo ambiental, social y económico de las regiones, en el marco de la Política de Investigación e Innovación Orientada por Misiones, promoviendo soluciones disruptivas con impacto medible en los territorios.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones. La convocatoria busca consolidar a Colombia como un referente en innovación tecnológica, abordando desafíos productivos y sociales con soluciones disruptivas y medibles.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> La entidad ejecutora principal de la propuesta debe ser una Institución de Educación Superior (IES) colombiana.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se exige la conformación de una alianza estratégica. Esta debe estar integrada por una Institución de Educación Superior (IES), una Empresa Nacional y, como mínimo, una Organización Local – Regional.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>Proyectos que no demuestren un impacto medible y directo en el cierre de brechas tecnológicas o el desarrollo territorial.</li>
      <li>Propuestas que no cumplan con la articulación obligatoria entre academia, empresa y el sector local/regional, debilitando el ecosistema de innovación propuesto.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene una focalización geográfica amplia, buscando impactar los territorios del país. No se especifican departamentos, ciudades o zonas PDET específicas de forma exclusiva, sino que se orienta a contribuir al desarrollo ambiental, social y económico de las regiones en general, haciendo énfasis en el cierre de brechas tecnológicas a nivel territorial.</p>
<ul>
  <li>Todos los territorios de Colombia, con énfasis en aquellos con mayores brechas tecnológicas y necesidades de desarrollo en las áreas temáticas de la convocatoria.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales, con diversas líneas de trabajo:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial (IA):</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de Tecnologías de IA para clasificar especies, monitorear ecosistemas y reforzar estrategias de conservación, fomentando la innovación colaborativa con conocimientos locales para transformar recursos biológicos en bienes o servicios de alto valor agregado.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Desarrollo y aplicaciones de Tecnologías de IA en agricultura de precisión, agroindustria, gestión de recursos hídricos y trazabilidad de productos, orientado a la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de Tecnologías de IA para el pronóstico, control y uso sostenible de fuentes limpias, complementada con modelos predictivos para la toma de decisiones en redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de tecnologías basadas en IA para apoyar el aprendizaje en áreas como matemáticas y programación, personalización de contenidos y reducción de brechas tecnológicas.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo y aplicaciones de Tecnologías de IA para el análisis de imágenes médicas, mejora de la precisión en el diagnóstico temprano de enfermedades y personalización de tratamientos.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos que utilicen principios cuánticos para el procesamiento de información y comunicación, incluyendo criptografía cuántica e Internet cuántico.</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías basadas en principios cuánticos para la detección, medición, trazabilidad y caracterización ultra precisa de fenómenos físicos, químicos o biológicos, con impacto en sectores como agricultura, salud y medioambiente.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> La convocatoria se enfoca en Investigación Aplicada, Desarrollo Tecnológico e Innovación. Esto sugiere que los proyectos deben iniciar en niveles de madurez tecnológica bajos o intermedios (TRL 3-5) y aspirar a alcanzar niveles más altos (TRL 6-8), demostrando prototipos funcionales o sistemas validados en entornos relevantes.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Fomento de la transferencia tecnológica y el desarrollo de talento especializado.</li>
      <li>Reducción de brechas tecnológicas en el país.</li>
      <li>Fortalecimiento de la vinculación entre academia, industria y sector público.</li>
      <li>Integración de elementos complementarios del eje temático secundario, si se justifica adecuadamente en términos de impacto, viabilidad y madurez tecnológica.</li>
      <li>Desarrollo, implementación y adopción ética y sostenible de soluciones basadas en IA (para el eje de IA).</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> No se especifica una duración máxima de ejecución en la información proporcionada. Sin embargo, para proyectos de Investigación Aplicada y Desarrollo Tecnológico de esta envergadura, se infiere una duración típica que oscila entre 18 y 36 meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Los entregables esperados se clasifican en:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas.</li>
      <li>Capítulos de libro o libros resultados de investigación.</li>
      <li>Tesis de maestría y doctorado desarrolladas en el marco del proyecto.</li>
      <li>Informes técnicos y científicos detallados sobre los avances y resultados de la investigación.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software basados en IA o tecnologías cuánticas.</li>
      <li>Desarrollo de algoritmos, modelos y herramientas computacionales innovadoras.</li>
      <li>Solicitudes de patente, registros de software o derechos de autor.</li>
      <li>Productos o servicios tecnológicos validados en entornos relevantes.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y transferencia de conocimiento dirigidos a comunidades y actores territoriales.</li>
      <li>Eventos de divulgación científica y tecnológica (seminarios, conferencias, ferias).</li>
      <li>Manuales de usuario o guías de implementación de las soluciones desarrolladas.</li>
      <li>Publicaciones de divulgación (infografías, videos, cartillas) para público no especializado.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones de laboratorios o espacios para investigación y desarrollo.</li>
      <li>Adquisición de equipos especializados (hardware cuántico, servidores de alto rendimiento, sensores, etc.).</li>
      <li>Implementación de plataformas o entornos de desarrollo para IA o computación cuántica.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Si bien los términos de referencia no detallan estándares específicos, se infieren los siguientes:</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>Gestión de la Información y Seguridad:</strong> Normas ISO 27001 (Sistemas de Gestión de Seguridad de la Información) para el manejo de datos en proyectos de IA.</li>
      <li><strong>Calidad de Software:</strong> Normas ISO/IEC 25000 (SQuaRE) para el desarrollo de soluciones de software de IA.</li>
      <li><strong>Ética en IA:</strong> Adherencia a los principios éticos para la IA establecidos por organismos internacionales y nacionales, como los propuestos por la OCDE o el CONPES 4144.</li>
      <li><strong>Interoperabilidad:</strong> Estándares para asegurar la compatibilidad y el intercambio de datos entre diferentes sistemas, especialmente en soluciones para sistemas agroalimentarios o salud.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Infraestructura de Cómputo:</strong> Para proyectos de IA, se requerirán plataformas con capacidad de procesamiento de alto rendimiento (GPUs, TPUs) y almacenamiento escalable.</li>
      <li><strong>Lenguajes de Programación:</strong> Python, R, Julia para IA; lenguajes específicos para computación cuántica (Qiskit, Cirq, etc.).</li>
      <li><strong>Frameworks de IA:</strong> TensorFlow, PyTorch, Scikit-learn, entre otros, para el desarrollo de modelos.</li>
      <li><strong>Plataformas Cuánticas:</strong> Acceso a simuladores cuánticos o hardware real (IBM Quantum Experience, Azure Quantum, etc.) según el alcance del proyecto.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>Protección de Datos:</strong> Ley 1581 de 2012 (Protección de Datos Personales en Colombia) y sus decretos reglamentarios, crucial para proyectos de IA en salud o educación.</li>
      <li><strong>Propiedad Intelectual:</strong> Normativa nacional e internacional aplicable a patentes, derechos de autor y secretos industriales para proteger los resultados de investigación.</li>
      <li><strong>Políticas de CTeI:</strong> Cumplimiento de las directrices y políticas del Ministerio de Ciencia, Tecnología e Innovación y el CONPES 4144 de Inteligencia Artificial.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca explícitamente impulsar el desarrollo ambiental, social y económico de las regiones, contribuyendo al cierre de brechas tecnológicas en los territorios del país. Se priorizan propuestas que demuestren un impacto medible y pertinente en las necesidades y problemáticas locales.</li>
  <li><strong>Enfoque Diferencial:</strong> Se promueve la inclusión social y el cierre de brechas, con énfasis en la promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos, impulsando la inclusión y el acceso a oportunidades formativas en los territorios. Esto implica considerar las particularidades de diferentes grupos poblacionales y regiones en el diseño y ejecución de los proyectos.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>La convocatoria enfatiza la vinculación de talento especializado y el fortalecimiento de capacidades, aunque los perfiles específicos pueden variar según el tipo de proyecto. Se infieren los siguientes roles mínimos:</p>
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con título de Maestría o Doctorado en áreas afines a las Ciencias de la Computación, Inteligencia Artificial, Física Cuántica o Ingenierías relacionadas. Mínimo 5 años de experiencia en dirección o coordinación de proyectos de I+D+i, preferiblemente con experiencia en gestión de equipos multidisciplinarios y relacionamiento con el sector productivo.</li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Investigador Principal:</strong> Título de Doctorado en campos relevantes (IA, Computación Cuántica, Matemáticas, Física). Mínimo 3 años de experiencia en investigación activa y publicaciones científicas en el área del proyecto.</li>
      <li><strong>Coinvestigadores:</strong> Título de Maestría o Doctorado en áreas afines. Mínimo 2 años de experiencia en investigación.</li>
      <li>Se debe vincular a <strong>jóvenes investigadores e innovadores</strong>, así como <strong>estudiantes de maestría y estancias posdoctorales</strong>, fomentando la formación de capital humano de alto nivel.</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong>
    <ul>
      <li><strong>Ingenieros de Desarrollo/Programadores:</strong> Profesionales con experiencia en desarrollo de software, manejo de plataformas de IA o herramientas de computación cuántica.</li>
      <li><strong>Especialistas de Datos:</strong> Profesionales con experiencia en análisis, procesamiento y gestión de grandes volúmenes de datos.</li>
      <li><strong>Personal de Apoyo:</strong> Técnicos o tecnólogos con experiencia relevante para la implementación de prototipos, montaje de equipos o trabajo de campo.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Basado en las convocatorias de Minciencias y el tipo de alianza requerida, los documentos críticos para la participación incluyen:</p>
<ul>
  <li><strong>Documentos Jurídicos:</strong>
    <ul>
      <li>Certificado de Existencia y Representación Legal de la IES ejecutora y de la Empresa Nacional aliada.</li>
      <li>Acuerdo de Consorcio, Unión Temporal o Alianza Estratégica, debidamente formalizado, que especifique roles, responsabilidades y aportes de cada miembro.</li>
      <li>RUT de todas las entidades participantes.</li>
    </ul>
  </li>
  <li><strong>Documentos Financieros:</strong>
    <ul>
      <li>Estados financieros auditados de la IES y la Empresa Nacional de las últimas dos vigencias.</li>
      <li>Certificación bancaria que acredite la capacidad financiera y la existencia de la cuenta principal del proyecto.</li>
      <li>Certificación de aportes de contrapartida (en efectivo y/o especie).</li>
    </ul>
  </li>
  <li><strong>Certificaciones específicas:</strong>
    <ul>
      <li>Certificaciones de experiencia de la IES y la Empresa en proyectos de I+D+i relevantes.</li>
      <li>Certificaciones de los perfiles del equipo de trabajo (títulos académicos, experiencia laboral).</li>
    </ul>
  </li>
  <li><strong>Avales institucionales:</strong>
    <ul>
      <li>Carta de aval institucional de la IES ejecutora, comprometiendo los recursos y el personal necesario.</li>
      <li>Cartas de intención o compromiso de la Organización Local – Regional, detallando su participación y el impacto esperado en su territorio.</li>
    </ul>
  </li>
  <li><strong>Propuesta Técnica y Económica:</strong>
    <ul>
      <li>Documento técnico detallado que describa el proyecto, metodología, cronograma, resultados esperados y plan de transferencia.</li>
      <li>Presupuesto detallado y justificado por rubros, incluyendo la cofinanciación solicitada y la contrapartida.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> Se ha identificado un valor de recursos de 20.000.000.000,00 COP para la convocatoria.</li>
  <li><strong>Tope por Proyecto:</strong> No se especifica un tope exacto por proyecto en la información disponible. Este valor suele depender de la complejidad y alcance de la propuesta.</li>
  <li><strong>Contrapartida:</strong> La convocatoria no especifica un porcentaje exacto de contrapartida. Sin embargo, en convocatorias de Minciencias de esta índole, es habitual que se exija una contrapartida significativa (en efectivo y/o especie) que puede oscilar entre el 30% y el 50% del valor total del proyecto, demostrando el compromiso de los aliados.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li><strong>Personal:</strong> Salarios y honorarios del equipo de investigación y desarrollo (investigadores, técnicos, jóvenes investigadores).</li>
      <li><strong>Equipos y Software:</strong> Adquisición o alquiler de hardware especializado (computadores de alto rendimiento, equipos cuánticos, sensores), licencias de software y herramientas de desarrollo.</li>
      <li><strong>Materiales e Insumos:</strong> Materias primas, componentes electrónicos, reactivos necesarios para la ejecución del proyecto.</li>
      <li><strong>Servicios Técnicos:</strong> Contratación de servicios especializados (análisis de laboratorio, consultorías específicas, acceso a plataformas cuánticas).</li>
      <li><strong>Salidas de Campo:</strong> Gastos de transporte, alojamiento y alimentación asociados a actividades de recopilación de datos o implementación en campo.</li>
      <li><strong>Publicaciones y Divulgación:</strong> Costos asociados a la publicación de artículos científicos, organización de eventos de divulgación y materiales de comunicación.</li>
      <li><strong>Administración y Gestión:</strong> Gastos indirectos asociados a la gestión del proyecto (hasta un porcentaje definido por la entidad).</li>
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
  <p>Basado en la naturaleza de proyectos de alta tecnología (IA y cuántica) y su impacto territorial, se infieren los siguientes riesgos:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica:</strong> Rápida evolución de las tecnologías cuánticas y de IA, lo que podría hacer que las soluciones desarrolladas queden desactualizadas antes o durante la finalización del proyecto.</li>
      <li><strong>Fallos en Integración:</strong> Dificultades en la integración de diferentes componentes de software o hardware, especialmente si se trabaja con tecnologías emergentes o de diversos proveedores.</li>
      <li><strong>Brechas de Desempeño:</strong> Los prototipos o soluciones desarrolladas no alcanzan los niveles de rendimiento, precisión o escalabilidad esperados, limitando su impacto real.</li>
      <li><strong>Disponibilidad de Datos:</strong> Dificultades para acceder a datos de calidad, etiquetados o en volúmenes suficientes para el entrenamiento de modelos de IA, especialmente en contextos territoriales específicos.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en Importaciones:</strong> Demoras en la adquisición e importación de equipos o componentes tecnológicos especializados necesarios para el desarrollo del proyecto.</li>
      <li><strong>Rotación de Personal Especializado:</strong> Pérdida de talento clave (investigadores, ingenieros) con experticia en IA o tecnologías cuánticas, debido a la alta demanda y competencia en el mercado laboral.</li>
      <li><strong>Coordinación de Alianzas:</strong> Dificultades en la coordinación y comunicación efectiva entre la IES, la Empresa Nacional y la Organización Local – Regional, afectando la ejecución del proyecto.</li>
      <li><strong>Apropiación Territorial:</strong> Baja adopción o resistencia por parte de las comunidades o usuarios finales en los territorios, debido a barreras culturales, de acceso o falta de capacitación.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Fluctuación del Dólar:</strong> Aumento en los costos de adquisición de equipos o licencias de software importados debido a la devaluación de la moneda local.</li>
      <li><strong>Recortes Presupuestales:</strong> Posibles ajustes o recortes en la financiación asignada al proyecto por parte de la entidad, afectando el alcance o cronograma.</li>
      <li><strong>Sobre-costos Tecnológicos:</strong> Costos imprevistos asociados a la investigación y desarrollo en tecnologías emergentes, que pueden exceder el presupuesto inicial.</li>
      <li><strong>Inadecuada Contrapartida:</strong> Incumplimiento de los aportes de contrapartida comprometidos por los aliados, poniendo en riesgo la continuidad financiera del proyecto.</li>
    </ul>
  </li>
</ul>
</div>

