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
  <li><strong>Cierre:</strong> 18 de junio de 2025 (Según Adenda No. 2)</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. Su objetivo principal es generar un impacto medible en el desarrollo ambiental, social y económico de las regiones colombianas, contribuyendo a cerrar brechas tecnológicas y a consolidar un ecosistema de innovación competitivo en el país.</li>
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
  <li><strong>Ejecutor:</strong> Comunidad científica, académica, empresarial, sociedad civil y demás actores interesados en CTeI. Esto incluye instituciones de educación superior, centros de investigación, empresas y organizaciones de la sociedad civil con capacidad para ejecutar proyectos de I+D+i.</li>
  <li><strong>Alianzas Obligatorias:</strong> La convocatoria prioriza propuestas que fomenten la vinculación entre academia, industria y sector público, impulsando el crecimiento de un ecosistema de innovación competitivo. Aunque no se especifica como "obligatoria", la colaboración intersectorial es fuertemente incentivada y puede ser un criterio de evaluación.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>Una empresa nacional no puede estar relacionada en más de una propuesta presentada a esta convocatoria.</li>
      <li>No se permite la participación de entidades o personas que se encuentren incursas en causales de inhabilidad o incompatibilidad de acuerdo con la legislación colombiana vigente.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene una focalización geográfica en los territorios del país, buscando contribuir al desarrollo ambiental, social y económico de las regiones y cerrar brechas tecnológicas a nivel nacional. No se especifican departamentos, ciudades o zonas PDET específicas, sino un impacto generalizado en las diversas regiones de Colombia.</p>
<ul>
  <li>Impacto en los territorios del país en general.</li>
  <li>Desarrollo regional en áreas ambientales, sociales y económicas.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales: Inteligencia Artificial y Ciencia y Tecnologías Cuánticas, permitiendo la integración de elementos complementarios entre ambos ejes si se justifica adecuadamente.</p>
<ul>
  <li><strong>Línea 1: Eje Temático Inteligencia Artificial (IA)</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de Tecnologías de IA para clasificar especies, monitorear ecosistemas y reforzar estrategias de conservación, fomentando la innovación colaborativa con conocimientos locales para transformar recursos biológicos en bienes o servicios de alto valor agregado.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Desarrollo y aplicaciones de Tecnologías de IA en agricultura de precisión, agroindustria, gestión de recursos hídricos y trazabilidad de productos, orientado a la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de Tecnologías de IA para el pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), complementada con modelos predictivos para la toma de decisiones en redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de tecnologías basadas en IA para apoyar el aprendizaje en áreas como matemáticas y programación, personalización de contenidos y reducción de brechas tecnológicas.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo y aplicaciones de Tecnologías para el análisis de imágenes médicas para mejorar la precisión en el diagnóstico temprano de enfermedades, personalizar tratamientos y optimizar la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Línea 2: Eje Temático Ciencia y Tecnologías Cuánticas</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos que utilicen principios cuánticos para el procesamiento de información y comunicación. Incluye algoritmos cuánticos, simulación cuántica, circuitos integrados cuánticos y fotónicos, comunicaciones ultra seguras e internet cuántico.</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías basadas en principios cuánticos para la detección, medición, trazabilidad y caracterización ultra precisa de fenómenos físicos, químicos o biológicos. Incluye sensores cuánticos para agricultura, salud, medioambiente, tecnologías para el desminado y metrología cuántica.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> La convocatoria busca fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación. Esto implica que los proyectos deben avanzar en los niveles de madurez tecnológica (TRL), probablemente iniciando en TRL 3-4 (prueba de concepto, validación en laboratorio) y buscando alcanzar TRL 6-7 (prototipo a escala, demostración en entorno relevante) al finalizar, con un claro potencial de escalabilidad y transferencia tecnológica.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Desarrollo de soluciones disruptivas en IA o Tecnologías Cuánticas con impacto medible.</li>
      <li>Promoción de la transferencia tecnológica.</li>
      <li>Desarrollo de talento especializado en las áreas de la convocatoria.</li>
      <li>Reducción de brechas tecnológicas en el país.</li>
      <li>Fomento de alianzas entre academia, industria y sector público.</li>
      <li>Enfoque territorial, inclusión social y cierre de brechas.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> La información disponible no especifica la duración máxima de ejecución de los proyectos. Se infiere que la duración debe ser coherente con el alcance de los objetivos de investigación aplicada, desarrollo tecnológico e innovación, probablemente entre 12 y 36 meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  Clasifica los entregables obligatorios, inferidos de la naturaleza de la convocatoria y sus objetivos:
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas (Q1, Q2).</li>
      <li>Capítulos de libro o libros resultado de investigación.</li>
      <li>Tesis de maestría y/o doctorado dirigidas en el marco del proyecto.</li>
      <li>Informes técnicos y científicos detallados de los resultados de investigación.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software basados en IA o tecnologías cuánticas.</li>
      <li>Desarrollo de algoritmos, modelos o plataformas de IA.</li>
      <li>Patentes solicitadas o concedidas, secretos industriales o derechos de autor sobre software.</li>
      <li>Modelos de simulación cuántica o prototipos de circuitos integrados.</li>
      <li>Dispositivos de sensórica cuántica.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y sensibilización dirigidos a comunidades y sectores productivos.</li>
      <li>Eventos de divulgación científica y tecnológica (seminarios, conferencias, ferias).</li>
      <li>Manuales de usuario o guías técnicas para la implementación de las soluciones desarrolladas.</li>
      <li>Programas de formación para el desarrollo de talento especializado en IA y tecnologías cuánticas.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras en laboratorios para investigación en IA o cuántica.</li>
      <li>Adquisición o desarrollo de equipos especializados (ej. hardware cuántico, servidores de alto rendimiento para IA).</li>
      <li>Plataformas de datos o infraestructura computacional para el desarrollo y prueba de soluciones.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  Investiga estándares técnicos específicos.
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>Inteligencia Artificial:</strong> Normas ISO/IEC 27001 (Seguridad de la Información), ISO/IEC 42001 (Gestión de IA), principios éticos para la IA (ej. UNESCO, OCDE), estándares de interoperabilidad de datos.</li>
      <li><strong>Tecnologías Cuánticas:</strong> Estándares emergentes de la IEEE (ej. Quantum Computing, Quantum Communications), NIST para criptografía post-cuántica, estándares de metrología para sensores cuánticos.</li>
      <li><strong>Gestión de Proyectos:</strong> ISO 21500 (Dirección y gestión de proyectos), PMBOK (Project Management Body of Knowledge).</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Hardware:</strong> Especificaciones técnicas para plataformas de cómputo de alto rendimiento (GPUs, TPUs para IA), infraestructura de servidores con capacidad para procesamiento de grandes volúmenes de datos, equipos para laboratorios de cuántica (ej. criostatos, láseres, detectores).</li>
      <li><strong>Software:</strong> Lenguajes de programación (Python, R, Julia para IA; Qiskit, Cirq para cuántica), frameworks de IA (TensorFlow, PyTorch), herramientas de simulación cuántica, bases de datos (SQL, NoSQL), plataformas de desarrollo colaborativo (Git).</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>CONPES 4144:</strong> Política Nacional para el Desarrollo de la Inteligencia Artificial en Colombia.</li>
      <li><strong>Legislación sobre Protección de Datos:</strong> Ley 1581 de 2012 y sus decretos reglamentarios (Habeas Data).</li>
      <li><strong>Normatividad de Propiedad Intelectual:</strong> Ley 23 de 1982 (Derechos de Autor), Decisiones Andinas 486 y 351 (Patentes y Derechos de Autor).</li>
      <li><strong>Regulaciones Sectoriales:</strong> Específicas para los sectores de aplicación (salud, agro, energía, medioambiente).</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca contribuir al desarrollo ambiental, social y económico de las regiones del país, cerrando brechas tecnológicas en los territorios. Los proyectos deben demostrar cómo impactarán positivamente en las necesidades y problemáticas específicas de las comunidades y ecosistemas locales, fomentando la innovación colaborativa con conocimientos locales y promoviendo la inclusión y el acceso a oportunidades formativas en las regiones.</li>
  <li><strong>Enfoque Diferencial:</strong> La convocatoria promueve la inclusión social y el cierre de brechas, lo que implica considerar la participación y el beneficio de poblaciones diversas, incluyendo mujeres, comunidades étnicas, víctimas del conflicto armado y otras minorías, asegurando que las soluciones desarrolladas sean accesibles y relevantes para estos grupos. Se espera que las propuestas demuestren cómo sus actividades y resultados impactarán de manera equitativa y beneficiosa a estas poblaciones.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  Detalla el equipo mínimo requerido (inferido de proyectos de I+D+i de alta complejidad):
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con título de Doctorado (PhD) o Maestría en áreas relacionadas con Ciencias de la Computación, Ingeniería de Sistemas, Física, Matemáticas, o campos afines. Mínimo 5 a 8 años de experiencia en dirección o coordinación de proyectos de investigación, desarrollo tecnológico o innovación, preferiblemente en IA o tecnologías cuánticas.</li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Investigador Principal:</strong> Título de Doctorado (PhD) en áreas relevantes (IA, Física Cuántica, Ingeniería Electrónica, etc.) con experiencia demostrada en publicaciones científicas y proyectos de investigación.</li>
      <li><strong>Coinvestigadores:</strong> Título de Maestría o Doctorado con experiencia específica en las líneas temáticas del proyecto (ej. procesamiento de lenguaje natural, visión por computador, criptografía cuántica, sensórica).</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong>
    <ul>
      <li><strong>Ingenieros de Desarrollo (IA/Cuántica):</strong> Profesionales en Ingeniería de Sistemas, Electrónica, Telecomunicaciones o áreas afines, con experiencia en desarrollo de software, programación de algoritmos, implementación de modelos de IA o trabajo con plataformas cuánticas.</li>
      <li><strong>Analistas de Datos:</strong> Profesionales con experiencia en gestión, procesamiento y análisis de grandes volúmenes de datos.</li>
      <li><strong>Diseñadores UX/UI:</strong> Para proyectos que impliquen desarrollo de interfaces o aplicaciones.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  Lista tipo checklist de los documentos más críticos para no ser descartado (inferidos de convocatorias similares de Minciencias):
<ul>
  <li><strong>Propuesta Técnica y Financiera:</strong> Documento principal que detalla el proyecto, metodología, cronograma, presupuesto y resultados esperados.</li>
  <li><strong>Documentos Jurídicos de la Entidad Proponente:</strong> Certificado de Existencia y Representación Legal, RUT, copia de cédula del Representante Legal.</li>
  <li><strong>Documentos Financieros:</strong> Estados financieros auditados, declaración de renta, paz y salvos fiscales y parafiscales.</li>
  <li><strong>Cartas de Aval Institucional:</strong> De la(s) entidad(es) proponente(s) y de las entidades aliadas (si aplica), que respalden la participación y el compromiso con el proyecto.</li>
  <li><strong>Cartas de Intención/Compromiso de Aliados:</strong> Cuando existan alianzas obligatorias o estratégicas con otras instituciones, empresas o comunidades.</li>
  <li><strong>Hojas de Vida del Equipo de Trabajo:</strong> Con soportes de formación académica y experiencia relevante.</li>
  <li><strong>Plan de Trabajo Detallado:</strong> Con hitos, actividades y responsables.</li>
  <li><strong>Presupuesto Detallado y Justificado:</strong> Por rubros y fuentes de financiación.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> No especificado en la información disponible. Es necesario consultar los términos de referencia completos o adendas para obtener esta cifra.</li>
  <li><strong>Tope por Proyecto:</strong> No especificado en la información disponible. Este valor suele detallarse en los anexos financieros de la convocatoria.</li>
  <li><strong>Contrapartida:</strong> No especificado en la información disponible. Usualmente, Minciencias exige un porcentaje de contrapartida (en efectivo y/o en especie) por parte de la entidad proponente o sus aliados, que puede oscilar entre el 10% y el 50% del valor total del proyecto.</li>
  <li><strong>Rubros Financiables:</strong> (Inferidos de convocatorias de I+D+i)
    <ul>
      <li><strong>Personal:</strong> Salarios, honorarios y gastos asociados al equipo de investigación y desarrollo.</li>
      <li><strong>Equipos y Software:</strong> Adquisición, alquiler o mantenimiento de equipos especializados, licencias de software y herramientas tecnológicas.</li>
      <li><strong>Materiales e Insumos:</strong> Consumibles de laboratorio, componentes electrónicos, materiales de prototipado.</li>
      <li><strong>Servicios Técnicos:</strong> Contratación de servicios especializados (ej. análisis de datos, pruebas de laboratorio, consultorías).</li>
      <li><strong>Salidas de Campo y Viajes:</strong> Gastos de transporte, alojamiento y manutención para actividades de campo o participación en eventos relevantes.</li>
      <li><strong>Divulgación y Apropiación Social:</strong> Costos asociados a publicaciones, talleres, eventos y actividades de transferencia de conocimiento.</li>
      <li><strong>Administración y Auditoría:</strong> Gastos indirectos de gestión del proyecto (generalmente un porcentaje del valor total).</li>
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
      <li><strong>Obsolescencia Tecnológica:</strong> Rápido avance de las tecnologías cuánticas e IA que podría dejar obsoleto un enfoque o solución durante la ejecución del proyecto.</li>
      <li><strong>Fallos en la Integración:</strong> Dificultades para integrar diferentes componentes de hardware o software, especialmente en entornos de tecnologías cuánticas emergentes o sistemas complejos de IA.</li>
      <li><strong>Rendimiento Inesperado:</strong> Los resultados de los prototipos o algoritmos pueden no alcanzar el rendimiento esperado o la precisión necesaria para el impacto deseado.</li>
      <li><strong>Disponibilidad de Datos:</strong> Dificultades para acceder a conjuntos de datos de alta calidad, representativos y suficientes para el entrenamiento y validación de modelos de IA.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en Adquisiciones:</strong> Demoras en la importación o adquisición de equipos especializados (ej. hardware cuántico) debido a la cadena de suministro o trámites aduaneros.</li>
      <li><strong>Rotación de Personal Clave:</strong> Pérdida de investigadores o técnicos especializados en IA o tecnologías cuánticas, dada la alta demanda y escasez de talento en estas áreas.</li>
      <li><strong>Gestión de Alianzas:</strong> Dificultades en la coordinación y colaboración efectiva entre los diferentes actores (academia, industria, sector público) que conforman el consorcio o alianza.</li>
      <li><strong>Acceso a Infraestructura:</strong> Limitaciones en el acceso a infraestructura computacional de alto rendimiento o laboratorios especializados necesarios para el desarrollo del proyecto.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Fluctuación del Tipo de Cambio:</strong> Impacto negativo en el presupuesto debido a la devaluación de la moneda local, especialmente si se requiere importar equipos o servicios en moneda extranjera.</li>
      <li><strong>Sobrecostos No Previstos:</strong> Aparición de gastos adicionales no contemplados en la planificación inicial, comunes en proyectos de I+D+i de frontera.</li>
      <li><strong>Desembolsos Tardíos:</strong> Retrasos en los desembolsos de la financiación por parte de la entidad convocante o de los cofinanciadores, afectando el flujo de caja del proyecto.</li>
      <li><strong>Insuficiencia de Contrapartida:</strong> Dificultades para cumplir con el porcentaje de contrapartida comprometido, ya sea en efectivo o en especie.</li>
    </ul>
  </li>
</ul>
</div>

