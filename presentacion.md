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

  /* --- AJUSTES DE ESPACIO --- */
  section {
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
  }

  /* --- HEADER (LOGO COTECMAR A LA DERECHA) --- */
  header {
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
  }

  /* --- PORTADA (IMAGEN NAVAL/INDUSTRIAL) --- */
  section.title-slide {
    padding: 0;
    /* Fondo alusivo a astilleros/mar con filtro azul corporativo */
    **background-image: linear-gradient(rgba(0,51,102,0.85), rgba(0,51,102,0.95)), url('https://upload.wikimedia.org/wikipedia/commons/9/90/Buque_de_Desembarco_Anfibio_ARC_%22Golfo_de_Tribug%C3%A1%22_%28ARC-241%29_de_la_Armada_Nacional_de_Colombia.jpg');**
    background-size: cover; 
    background-position: center;
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    align-items: center; 
    text-align: center;
    
    /* CORRECCIÓN DE TEXTO INVISIBLE */
    color: white; 
  }

  section.title-slide h1 { 
    color: white; 
    font-size: 2.8em; 
    margin-bottom: 20px; 
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  }
  
  /* Estilo para el subtítulo (###) en la portada */
  section.title-slide h3 { 
    color: var(--secondary); /* Amarillo Cotecmar */
    font-size: 1.5em;
    font-weight: normal;
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
# CONVOCATORIA COLOMBIA INTELIGENTE: CIENCIA Y TECNOLOGÍAS CUÁNTICAS E INTELIGENCIA ARTIFICIAL PARA LOS TERRITORIOS | Convocatoria 966

### Informe de Inteligencia de Convocatoria

---

<div class="card warning">
  <h3>📅 Información Clave</h3>
  <ul>
  <li><strong>Entidad:</strong> Ministerio de Ciencia, Tecnología e Innovación (Minciencias)</li>
  <li><strong>Número:</strong> 966</li>
  <li><strong>Apertura:</strong> No especificado. Se requiere consultar los Términos de Referencia oficiales.</li>
  <li><strong>Cierre:</strong> No especificado. Se requiere consultar los Términos de Referencia oficiales.</li>
  <li><strong>Res:</strong> No especificado. Se requiere consultar los Términos de Referencia oficiales.</li>
  <li><strong>Cierre:</strong> No especificado. Se requiere consultar los Términos de Referencia oficiales.</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. Su objetivo principal es generar un impacto medible que contribuya al desarrollo ambiental, social y económico de las regiones, cerrando brechas tecnológicas en el país. Prioriza proyectos que fomenten la transferencia tecnológica, el desarrollo de talento especializado y la vinculación entre academia, industria y sector público, consolidando un ecosistema de innovación competitivo.</li>
</ul>
</div>


---
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones.</p>
</div>


---
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> Generalmente, este tipo de convocatorias de Minciencias está dirigido a Instituciones de Educación Superior (IES), centros de investigación y desarrollo tecnológico, empresas con capacidades de I+D+i, y otras entidades del Sistema Nacional de Ciencia, Tecnología e Innovación (SNCTI) de Colombia.</li>
  <li><strong>Alianzas Obligatorias:</strong> La convocatoria "promueve alianzas entre academia, empresa y sociedad civil" y busca "fortalecer la vinculación entre academia, industria y sector público". Aunque no se especifica explícitamente como "obligatorio" en la información inicial, es altamente recomendable y a menudo un criterio de evaluación la conformación de consorcios o alianzas estratégicas que incluyan al menos una entidad del sector productivo y una académica/investigativa para maximizar el impacto y la transferencia tecnológica.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>No cumplir con los requisitos legales y fiscales para contratar con el Estado colombiano.</li>
      <li>Personas o entidades que se encuentren incursas en causales de inhabilidad o incompatibilidad establecidas en la legislación colombiana para participar en convocatorias públicas.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene una focalización geográfica nacional, con un énfasis explícito en el impacto y cierre de brechas tecnológicas en los territorios del país. Busca contribuir al desarrollo ambiental, social y económico de las regiones.</p>
<ul>
  <li>No se especifican departamentos, ciudades o zonas PDET específicas, sin embargo, los proyectos deben demostrar un claro impacto territorial y de inclusión social en las regiones de Colombia.</li>
</ul>
</div>


---
<h2>📚 Áreas de Investigación</h2>
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales con diversas líneas de trabajo:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial (IA):</strong> Responde a lo establecido en el CONPES 4144, promoviendo el desarrollo, implementación y adopción ética y sostenible de soluciones basadas en IA en sectores estratégicos.
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de Tecnologías de IA para clasificar especies, monitorear ecosistemas y reforzar estrategias de conservación, fomentando la innovación colaborativa con conocimientos locales para transformar recursos biológicos en bienes o servicios de alto valor agregado.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Desarrollo y aplicaciones de Tecnologías de IA en agricultura de precisión, agroindustria, gestión de recursos hídricos y trazabilidad de productos, orientado a la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de Tecnologías de IA para el pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), complementada con modelos predictivos para la toma de decisiones en redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de tecnologías basadas en IA para apoyar el aprendizaje en áreas como matemáticas y programación, personalización de contenidos, reducción de brechas tecnológicas y promoción de competencias.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Desarrollo y aplicación de Tecnologías que integren modelos de IA para la detección temprana de desastres (inundaciones, incendios, deslizamientos) y la protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo y aplicaciones de Tecnologías para el análisis de imágenes médicas para mejorar la precisión en el diagnóstico temprano de enfermedades, personalizar tratamientos según datos genómicos y clínicos, u optimizar la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos que utilicen principios cuánticos para el procesamiento de información y comunicación. Incluye sublíneas como Algoritmos Cuánticos, Simulación Cuántica, Circuitos Integrados Cuánticos y Fotónicos, Comunicaciones Ultra Seguras e Internet Cuántico y Nodos de Red.</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías basadas en principios cuánticos para la detección, medición, trazabilidad y caracterización ultra precisa de fenómenos físicos, químicos o biológicos. Incluye sublíneas como Sensores Cuánticos para Agricultura, Salud, Medioambiente, Tecnologías para el Desminado y Metrología Cuántica.</li>
    </ul>
  </li>
</ul>
</div>


---
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> Dada la naturaleza de "Investigación Aplicada, Desarrollo Tecnológico e Innovación", se infiere que los proyectos deben iniciar en niveles de madurez tecnológica bajos o intermedios (TRL 2-4) y aspirar a alcanzar niveles más altos (TRL 5-7) que permitan la demostración de prototipos en entornos relevantes o la validación en un entorno operativo, facilitando la transferencia tecnológica.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Investigación Aplicada y Desarrollo de soluciones disruptivas.</li>
      <li>Transferencia tecnológica efectiva.</li>
      <li>Desarrollo de talento especializado en tecnologías cuánticas e IA.</li>
      <li>Reducción de brechas tecnológicas en los territorios.</li>
      <li>Fortalecimiento de la vinculación entre academia, industria y sector público.</li>
      <li>Generación de impacto medible en el desarrollo ambiental, social y económico.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> No especificado. Se requiere consultar los Términos de Referencia oficiales para conocer el tiempo máximo de ejecución.</li>
</ul>
</div>


---
<h2>📦 Entregables Esperados</h2>
<div class="col-2">
  <p>Los entregables obligatorios se inferirán de los objetivos de la convocatoria, enfocados en la generación de conocimiento, desarrollo tecnológico, apropiación social y fortalecimiento de capacidades:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas.</li>
      <li>Ponencias en congresos nacionales e internacionales.</li>
      <li>Informes técnicos y metodológicos de investigación.</li>
      <li>Tesis de maestría y doctorado dirigidas o apoyadas por el proyecto.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software basados en IA o tecnologías cuánticas.</li>
      <li>Desarrollo de algoritmos, modelos o plataformas de IA.</li>
      <li>Registro de software o propiedad intelectual.</li>
      <li>Solicitudes de patente o modelos de utilidad.</li>
      <li>Demostradores de concepto o pruebas de viabilidad tecnológica.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y sensibilización dirigidos a comunidades o sectores productivos.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Publicaciones de divulgación (cartillas, manuales, guías).</li>
      <li>Material didáctico para la formación en IA y tecnologías cuánticas.</li>
      <li>Creación o fortalecimiento de comunidades de práctica o redes de conocimiento.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuación o mejora de laboratorios para investigación en IA o tecnologías cuánticas.</li>
      <li>Adquisición de equipos especializados (servidores de alto rendimiento, kits de desarrollo cuántico, sensores avanzados).</li>
      <li>Implementación de plataformas de computación en la nube para IA.</li>
    </ul>
  </li>
</ul>
</div>


---
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Aunque no se especifican directamente en la información inicial, se infieren estándares y normatividad relevantes para proyectos de esta naturaleza:</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>Para Inteligencia Artificial:</strong>
        <ul>
          <li><strong>ISO/IEC 42001:</strong> Gestión de la Inteligencia Artificial (recién publicada).</li>
          <li><strong>Principios Éticos de IA:</strong> Directrices de la OCDE sobre IA, Recomendación de la UNESCO sobre la Ética de la IA, o el Marco de Ética de la IA del CONPES 4144.</li>
          <li><strong>Estándares de Calidad de Software:</strong> ISO/IEC 25010 (SQuaRE) para calidad de producto software.</li>
          <li><strong>Estándares de Interoperabilidad de Datos:</strong> Para asegurar la compatibilidad y el intercambio de información entre sistemas.</li>
        </ul>
      </li>
      <li><strong>Para Tecnologías Cuánticas:</strong>
        <ul>
          <li><strong>Estándares de Criptografía Cuántica:</strong> Normas emergentes para la seguridad de las comunicaciones.</li>
          <li><strong>Estándares de Metrología Cuántica:</strong> Relacionados con la precisión y trazabilidad de las mediciones.</li>
          <li><strong>Estándares de Interoperabilidad de Hardware/Software Cuántico:</strong> Para la compatibilidad entre diferentes plataformas.</li>
        </ul>
      </li>
      <li><strong>Seguridad de la Información:</strong> ISO/IEC 27001 para la gestión de la seguridad de la información, especialmente relevante para el manejo de datos sensibles en aplicaciones de IA y comunicaciones cuánticas.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Hardware:</strong> Se requerirán especificaciones de equipos de cómputo de alto rendimiento (GPUs, TPUs) para proyectos de IA, o plataformas de hardware cuántico (simuladores, procesadores cuánticos si aplica) para proyectos de tecnologías cuánticas.</li>
      <li><strong>Software:</strong> Utilización de lenguajes de programación como Python, R, Julia; frameworks de IA como TensorFlow, PyTorch; librerías de computación cuántica como Qiskit, Cirq, PennyLane. Se espera el uso de metodologías de desarrollo ágil y DevOps.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>CONPES 4144 de 2023:</strong> Política Nacional de Inteligencia Artificial de Colombia, que establece el marco estratégico para el desarrollo y uso de la IA en el país.</li>
      <li><strong>Ley 1581 de 2012:</strong> Ley de Protección de Datos Personales en Colombia, fundamental para cualquier proyecto que involucre el manejo de información personal.</li>
      <li><strong>Normatividad de Propiedad Intelectual:</strong> Leyes y regulaciones colombianas sobre derechos de autor y patentes para la protección de los desarrollos tecnológicos.</li>
      <li><strong>Regulaciones Sectoriales:</strong> Dependiendo del sector de aplicación (ej. salud, agricultura, energía), pueden aplicar normativas específicas.</li>
    </ul>
  </li>
</ul>
</div>


---
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca específicamente que los proyectos "contribuyan al desarrollo ambiental, social y económico de las regiones" y ayuden a "cerrar brechas tecnológicas en los territorios del país". Se espera que las propuestas demuestren un impacto directo y medible en las necesidades y problemáticas de las comunidades o sectores productivos de regiones específicas, promoviendo la apropiación social del conocimiento y el fortalecimiento de capacidades locales.</li>
  <li><strong>Enfoque Diferencial:</strong> La convocatoria enfatiza la "inclusión social y cierre de brechas", así como la "promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos" en el marco de la transformación educativa con IA. Esto implica que las propuestas deben considerar la diversidad de la población colombiana, incluyendo grupos étnicos, personas con discapacidad, víctimas del conflicto, mujeres, y poblaciones vulnerables, asegurando que los beneficios de la ciencia y la tecnología lleguen a todos sin discriminación.</li>
</ul>


---
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>Basado en la naturaleza de proyectos de I+D+i en tecnologías avanzadas, se infieren los siguientes perfiles mínimos:</p>
<ul>
  <li><strong>Director/Gerente de Proyecto:</strong> Profesional con título de Doctorado (PhD) o Maestría en áreas relacionadas con Ciencias de la Computación, Ingeniería de Sistemas, Electrónica, Física, Matemáticas o áreas afines, con al menos 5 a 10 años de experiencia en gestión de proyectos de investigación, desarrollo tecnológico e innovación, preferiblemente en IA o tecnologías cuánticas. Certificaciones en gestión de proyectos (PMP) son un plus.</li>
  <li><strong>Investigadores Principales:</strong> Profesionales con título de Doctorado (PhD) o Maestría en campos específicos de Inteligencia Artificial (aprendizaje automático, procesamiento de lenguaje natural, visión por computador) o Tecnologías Cuánticas (computación cuántica, criptografía cuántica, sensórica cuántica), con experiencia demostrable en investigación y publicaciones científicas relevantes.</li>
  <li><strong>Investigadores Jóvenes/Asistentes:</strong> Profesionales con título de pregrado o Maestría en las áreas mencionadas, con interés y experiencia inicial en investigación en IA o tecnologías cuánticas.</li>
  <li><strong>Técnicos Especializados:</strong>
    <ul>
      <li><strong>Desarrolladores de Software:</strong> Con experiencia en Python, R, frameworks de IA, desarrollo de APIs, bases de datos.</li>
      <li><strong>Ingenieros de Datos:</strong> Con conocimientos en manejo, procesamiento y análisis de grandes volúmenes de datos.</li>
      <li><strong>Ingenieros Electrónicos/Físicos:</strong> Para el diseño y desarrollo de hardware en proyectos cuánticos o de sensórica.</li>
      <li><strong>Expertos en Dominio:</strong> Profesionales de los sectores de aplicación (bioeconomía, agro, salud, educación, etc.) con experiencia relevante para la implementación de las soluciones.</li>
    </ul>
  </li>
</ul>
</div>


---
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Los documentos más críticos para la postulación, a inferir de convocatorias similares de Minciencias, suelen incluir:</p>
<ul>
  <li><strong>Documentos Jurídicos:</strong>
    <ul>
      <li>Certificado de Existencia y Representación Legal (para personas jurídicas).</li>
      <li>Copia de la Cédula de Ciudadanía del Representante Legal.</li>
      <li>Certificado de Antecedentes Disciplinarios y Fiscales del Representante Legal.</li>
      <li>Declaración de No Inhabilidad e Incompatibilidad.</li>
    </ul>
  </li>
  <li><strong>Documentos Financieros:</strong>
    <ul>
      <li>Estados Financieros del último año (Balance General, Estado de Resultados).</li>
      <li>Certificación de experiencia financiera o capacidad para cofinanciar el proyecto (si aplica contrapartida).</li>
      <li>Declaración de Renta.</li>
    </ul>
  </li>
  <li><strong>Certificaciones específicas:</strong>
    <ul>
      <li>Certificación de existencia y registro en el SNCTI (Sistema Nacional de Ciencia, Tecnología e Innovación) como actor reconocido por Minciencias.</li>
      <li>Certificaciones de experiencia del equipo de trabajo en proyectos similares.</li>
    </ul>
  </li>
  <li><strong>Avales institucionales:</strong>
    <ul>
      <li>Carta de aval institucional del representante legal de la entidad proponente.</li>
      <li>Cartas de compromiso o intención de las entidades aliadas (si aplica consorcio o alianza).</li>
    </ul>
  </li>
  <li><strong>Propuesta Técnica y Económica:</strong>
    <ul>
      <li>Formulario de presentación de proyectos diligenciado en la plataforma.</li>
      <li>Descripción detallada del proyecto (problema, objetivos, metodología, resultados esperados, cronograma, presupuesto).</li>
      <li>Plan de trabajo y cronograma detallado.</li>
      <li>Currículos del equipo de trabajo (CvLAC o similar).</li>
      <li>Plan de apropiación social del conocimiento.</li>
      <li>Plan de gestión tecnológica y transferencia.</li>
    </ul>
  </li>
</ul>
</div>


---
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> No especificado. Se requiere consultar los Términos de Referencia oficiales.</li>
  <li><strong>Tope por Proyecto:</strong> No especificado. Se requiere consultar los Términos de Referencia oficiales.</li>
  <li><strong>Contrapartida:</strong> No especificado. En convocatorias de Minciencias, es común que se exija un porcentaje de contrapartida (en efectivo y/o en especie) por parte de las entidades proponentes. Se requiere consultar los Términos de Referencia oficiales.</li>
  <li><strong>Rubros Financiables:</strong> (Inferencia basada en convocatorias similares de I+D+i)
    <ul>
      <li><strong>Personal:</strong> Salarios y honorarios del equipo de investigación y apoyo (investigadores, técnicos, gestores).</li>
      <li><strong>Equipos y Software:</strong> Adquisición, alquiler o mantenimiento de equipos especializados, licencias de software, herramientas de computación de alto rendimiento.</li>
      <li><strong>Materiales e Insumos:</strong> Consumibles, reactivos, componentes electrónicos, materiales para prototipado.</li>
      <li><strong>Servicios Técnicos:</strong> Contratación de servicios especializados (análisis de laboratorio, consultorías técnicas, certificación).</li>
      <li><strong>Viajes y Salidas de Campo:</strong> Gastos de transporte, alojamiento y manutención para actividades de investigación, apropiación social o transferencia en los territorios.</li>
      <li><strong>Publicaciones y Divulgación:</strong> Costos asociados a la publicación de artículos científicos, asistencia a congresos, elaboración de material de divulgación.</li>
      <li><strong>Administración y Gestión:</strong> Gastos indirectos asociados a la administración del proyecto (generalmente un porcentaje del valor total del proyecto).</li>
      <li><strong>Propiedad Intelectual:</strong> Gastos de registro de patentes, derechos de autor.</li>
      <li><strong>Formación:</strong> Apoyo a la formación de talento humano (becas, cursos especializados).</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<h2>🛡️ Matriz de Riesgos</h2>
<div style="font-size: 0.8em;">
  <p>Basado en la naturaleza de proyectos de ciencia y tecnologías cuánticas e Inteligencia Artificial, se infieren los siguientes riesgos:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia tecnológica rápida:</strong> Dada la velocidad de avance en IA y tecnologías cuánticas, existe el riesgo de que las herramientas o plataformas seleccionadas queden desactualizadas durante la ejecución del proyecto.</li>
      <li><strong>Fallos en la integración de tecnologías:</strong> Dificultades en la interoperabilidad entre diferentes componentes de software, hardware o plataformas cuánticas.</li>
      <li><strong>Limitaciones de rendimiento:</strong> Los modelos de IA o algoritmos cuánticos pueden no alcanzar el rendimiento o la precisión esperada en entornos reales.</li>
      <li><strong>Disponibilidad y calidad de datos:</strong> Retos en la obtención de conjuntos de datos suficientes, relevantes y de alta calidad para el entrenamiento de modelos de IA.</li>
      <li><strong>Complejidad algorítmica:</strong> Dificultades en el desarrollo y optimización de algoritmos cuánticos o de IA que sean computacionalmente eficientes y escalables.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en la adquisición o importación de equipos especializados:</strong> Especialmente para hardware cuántico o componentes de alto rendimiento, que pueden tener tiempos de entrega prolongados o restricciones aduaneras.</li>
      <li><strong>Rotación de personal especializado:</strong> La alta demanda de talento en IA y tecnologías cuánticas puede llevar a la pérdida de miembros clave del equipo, afectando la continuidad y el cronograma del proyecto.</li>
      <li><strong>Falta de acceso a infraestructura de cómputo:</strong> Insuficiencia de recursos computacionales (GPUs, clusters) o acceso limitado a plataformas cuánticas.</li>
      <li><strong>Dificultades en la coordinación de alianzas:</strong> Desafíos en la gestión de equipos multidisciplinarios y la colaboración entre diferentes entidades (academia, industria, sector público).</li>
      <li><strong>Cumplimiento de normatividad ética:</strong> Riesgos asociados a la implementación ética de soluciones de IA, incluyendo sesgos algorítmicos o problemas de privacidad de datos.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Sobrecostos tecnológicos:</strong> Gastos imprevistos en la adquisición de software, licencias o hardware debido a fluctuaciones del mercado o necesidades técnicas no anticipadas.</li>
      <li><strong>Fluctuación de tasas de cambio:</strong> Impacto en la adquisición de equipos o servicios importados si la financiación no considera variaciones monetarias.</li>
      <li><strong>Recortes presupuestales:</strong> Posibles reducciones en la financiación por parte de la entidad, afectando la ejecución del proyecto.</li>
      <li><strong>Dificultades en la consecución de la contrapartida:</strong> Si se exige, el riesgo de no poder aportar los recursos comprometidos en efectivo o en especie.</li>
      <li><strong>Dependencia de financiación externa:</strong> Si el proyecto requiere etapas posteriores de financiación, existe el riesgo de no obtenerla, afectando la escalabilidad y sostenibilidad.</li>
    </ul>
  </li>
</ul>
</div>