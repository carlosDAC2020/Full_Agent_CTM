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
  <li><strong>Apertura:</strong> No especificado. Se requiere consultar los Términos de Referencia completos.</li>
  <li><strong>Cierre:</strong> No especificado. Se requiere consultar los Términos de Referencia completos.</li>
  <li><strong>Res:</strong> No especificado. Se requiere consultar los Términos de Referencia completos.</li>
  <li><strong>Cierre:</strong> No especificado. Se requiere consultar los Términos de Referencia completos.</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente 966 busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. Su objetivo principal es generar un impacto medible y contribuir al desarrollo ambiental, social y económico de las regiones, cerrando brechas tecnológicas y promoviendo un ecosistema de innovación competitivo a través de la vinculación entre academia, industria y sector público.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones. La convocatoria busca consolidar a Colombia como un referente en innovación tecnológica, abordando desafíos productivos y sociales con soluciones disruptivas y un impacto medible.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> Generalmente, este tipo de convocatorias de Minciencias está dirigido a grupos de investigación de Instituciones de Educación Superior (IES), centros de investigación, centros de desarrollo tecnológico y empresas legalmente constituidas en Colombia con capacidades en CTeI. Sin embargo, los términos de referencia específicos deben detallar los requisitos exactos de la entidad proponente.</li>
  <li><strong>Alianzas Obligatorias:</strong> La convocatoria "fomenta alianzas entre academia, empresa y sociedad civil" y busca "fortalecer la vinculación entre academia, industria y sector público". Aunque no se especifica como *obligatorio* en la información inicial, es altamente probable que se valore y/o exija la conformación de consorcios o alianzas estratégicas entre al menos dos tipos de actores (ej. academia-empresa) para la presentación de propuestas, buscando la transferencia tecnológica y el impacto territorial.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>Inhabilidad por conflicto de intereses, donde el proponente o sus representantes tengan vínculos directos con la evaluación o administración de la convocatoria.</li>
      <li>Incumplimiento de requisitos legales o financieros previos con el Ministerio o el Estado Colombiano.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene una clara focalización en los "territorios del país" y el "desarrollo ambiental, social y económico de las regiones". Se menciona un "enfoque territorial, inclusión social y cierre de brechas". Aunque no se listan departamentos, ciudades o zonas PDET específicas en la información proporcionada, se espera que los proyectos demuestren un impacto directo y medible en contextos regionales específicos, priorizando aquellos con mayores necesidades o brechas tecnológicas.</p>
<ul>
  <li>La convocatoria busca impactar en las <strong>regiones</strong>, con un énfasis en el cierre de <strong>brechas tecnológicas territoriales</strong>.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>Las líneas temáticas se dividen en dos ejes estratégicos principales:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial:</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo de IA para clasificar especies, monitorear ecosistemas, conservación y transformación de recursos biológicos en bienes/servicios de alto valor.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Aplicaciones de IA en agricultura de precisión, agroindustria, gestión hídrica y trazabilidad para la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Uso de IA para pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa) y modelos predictivos para redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de IA para apoyar el aprendizaje en matemáticas y programación, personalización de contenidos y reducción de brechas tecnológicas en todos los grupos de edad.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Aplicación de IA para la detección temprana de desastres naturales (inundaciones, incendios, deslizamientos) y protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo de IA para análisis de imágenes médicas, diagnóstico temprano de enfermedades, tratamientos personalizados y optimización de la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos, simulación cuántica, circuitos integrados (cuánticos y fotónicos), criptografía cuántica y redes cuánticas (Internet cuántico y nodos de red).</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías cuánticas para detección, medición y caracterización ultra precisa en sectores estratégicos, incluyendo sensores para agricultura, salud, medioambiente, tecnologías para el desminado y metrología cuántica.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> Dado que la convocatoria busca fortalecer la "Investigación Aplicada, el Desarrollo Tecnológico y la Innovación" y la creación de "soluciones disruptivas con impacto medible", se infiere que los proyectos deben iniciar en niveles de madurez tecnológica intermedios (TRL 3-5, prueba de concepto o validación en entorno relevante) y aspirar a alcanzar niveles más altos (TRL 6-8, prototipo validado en entorno real o sistema completo y calificado). Los términos de referencia específicos son cruciales para confirmar los rangos de TRL.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Fomento de la <strong>transferencia tecnológica</strong>.</li>
      <li>Desarrollo de <strong>talento especializado</strong> en tecnologías cuánticas e IA.</li>
      <li>Reducción de <strong>brechas tecnológicas</strong> en el país.</li>
      <li>Fortalecimiento de la <strong>vinculación entre academia, industria y sector público</strong>.</li>
      <li>Generación de <strong>soluciones disruptivas</strong> con impacto medible.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> No especificado en la información inicial. Típicamente, proyectos de Investigación Aplicada y Desarrollo Tecnológico de esta envergadura suelen tener duraciones entre 18 y 36 meses. Se requiere consultar los Términos de Referencia para la duración máxima permitida.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Basado en el objetivo de fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación, se infieren los siguientes tipos de entregables obligatorios, los cuales deben ser detallados en los anexos técnicos de la convocatoria:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas (Q1, Q2).</li>
      <li>Capítulos de libro o libros resultado de investigación.</li>
      <li>Tesis de maestría o doctorado dirigidas en el marco del proyecto.</li>
      <li>Informes técnicos y científicos detallados de los resultados de investigación.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales (hardware o software) de soluciones basadas en IA o tecnologías cuánticas.</li>
      <li>Desarrollo de software especializado, algoritmos o plataformas (con código fuente y documentación).</li>
      <li>Solicitudes de patente, modelos de utilidad o diseños industriales.</li>
      <li>Registros de software o derechos de autor.</li>
      <li>Pruebas de concepto validadas en entornos relevantes.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Diseño e implementación de talleres, cursos o seminarios de capacitación dirigidos a comunidades o sectores productivos.</li>
      <li>Organización de eventos de divulgación científica y tecnológica.</li>
      <li>Elaboración de manuales, guías o material didáctico para la apropiación del conocimiento.</li>
      <li>Generación de espacios de interacción y cocreación con actores territoriales.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras de laboratorios para investigación en IA o tecnologías cuánticas.</li>
      <li>Adquisición o desarrollo de equipos especializados (ej. hardware cuántico, servidores de alto rendimiento para IA).</li>
      <li>Implementación de plataformas o entornos de desarrollo específicos.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Aunque no se especifican estándares técnicos explícitos en la información inicial, dado el campo de acción (IA y Tecnologías Cuánticas), se infieren los siguientes, que deberán ser confirmados en los términos de referencia o anexos técnicos:</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>ISO/IEC 27001:</strong> Para la gestión de la seguridad de la información, crucial en proyectos de IA y cuántica que manejan datos sensibles.</li>
      <li><strong>ISO/IEC 42001:</strong> Norma para sistemas de gestión de IA, enfocada en el desarrollo y uso responsable de la inteligencia artificial.</li>
      <li><strong>Estándares de interoperabilidad:</strong> Para asegurar la integración de soluciones con sistemas existentes, posiblemente estándares abiertos o APIs documentadas.</li>
      <li><strong>Principios Éticos para la IA:</strong> Cumplimiento de directrices éticas para el desarrollo de IA, como las promovidas por la UNESCO o la OCDE.</li>
      <li><strong>Normas de Metrología:</strong> Para proyectos de sensórica cuántica, se esperaría el cumplimiento de normas internacionales de medición y trazabilidad.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Infraestructura de computación:</strong> Posiblemente se requieran especificaciones mínimas para clústeres de GPU, CPUs de alto rendimiento o acceso a plataformas de computación cuántica (ej. IBM Quantum Experience, Amazon Braket).</li>
      <li><strong>Lenguajes de programación:</strong> Python, R, Julia para IA; Qiskit, Cirq, OpenQASM para computación cuántica.</li>
      <li><strong>Frameworks de IA:</strong> TensorFlow, PyTorch, Scikit-learn, Keras.</li>
      <li><strong>Bases de datos:</strong> SQL/NoSQL escalables para grandes volúmenes de datos.</li>
      <li><strong>Entornos de desarrollo:</strong> Docker, Kubernetes para despliegue y gestión de contenedores.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>CONPES 4144 de 2023:</strong> Política Nacional de Desarrollo de la Inteligencia Artificial en Colombia, que orienta las líneas de trabajo en IA de esta convocatoria.</li>
      <li><strong>Ley 1581 de 2012:</strong> Ley de Protección de Datos Personales, fundamental para cualquier proyecto que involucre recopilación, procesamiento o análisis de datos.</li>
      <li><strong>Leyes de propiedad intelectual:</strong> Para la protección de los resultados de investigación y desarrollo (patentes, derechos de autor).</li>
      <li><strong>Regulaciones sectoriales:</strong> Dependiendo del sector de aplicación (ej. salud, agricultura, energía), se deben cumplir las normativas específicas de cada uno.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria enfatiza el "desarrollo ambiental, social y económico de las regiones" y el "cierre de brechas tecnológicas en los territorios del país". Los proyectos deben demostrar cómo sus soluciones basadas en IA o tecnologías cuánticas generarán un impacto directo y medible en las necesidades y desafíos específicos de una o varias regiones de Colombia, promoviendo la apropiación social del conocimiento en esos contextos.</li>
  <li><strong>Enfoque Diferencial:</strong> Se busca la "inclusión social y cierre de brechas", así como la "promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos". Esto implica que los proyectos deben considerar la participación equitativa de diversos grupos poblacionales, incluyendo mujeres, comunidades étnicas, víctimas del conflicto, personas con discapacidad, y otros grupos minoritarios, asegurando que las soluciones desarrolladas sean accesibles y beneficien a una amplia gama de usuarios, y que los equipos de trabajo reflejen esta diversidad.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>Aunque los perfiles específicos no se detallan en la información inicial, para proyectos de esta complejidad y en el marco de Minciencias, se infieren los siguientes requisitos mínimos para el equipo técnico y de investigación:</p>
<ul>
  <li><strong>Director/Gerente:</strong>
    <ul>
      <li><strong>Perfil:</strong> Profesional en áreas de ingeniería, ciencias básicas, ciencias de la computación o afines, con experiencia demostrable en gestión y dirección de proyectos de I+D+i, preferiblemente en tecnologías avanzadas.</li>
      <li><strong>Formación:</strong> Título de Doctorado (PhD) o Maestría con amplia experiencia relevante.</li>
      <li><strong>Años de experiencia:</strong> Mínimo 5 años de experiencia en dirección de proyectos de investigación y/o desarrollo tecnológico.</li>
    </ul>
  </li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Nivel educativo requerido:</strong> Preferentemente con título de Doctorado (PhD) o Maestría en áreas relacionadas con Inteligencia Artificial, computación cuántica, física, matemáticas, ingeniería electrónica, sistemas o afines.</li>
      <li><strong>Experiencia:</strong> Experiencia en investigación aplicada, publicaciones científicas y participación en proyectos relevantes.</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong>
    <ul>
      <li><strong>Perfiles de apoyo:</strong> Ingenieros de software, desarrolladores, científicos de datos, expertos en hardware, especialistas en infraestructura tecnológica.</li>
      <li><strong>Formación:</strong> Nivel profesional o tecnólogo con experiencia específica en las tecnologías a aplicar.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Basado en la experiencia en convocatorias de Minciencias y la naturaleza de la entidad, se infieren los siguientes documentos críticos para la participación, que deberán ser confirmados en los Términos de Referencia:</p>
<ul>
  <li><strong>Documento Jurídico 1:</strong> Certificado de Existencia y Representación Legal (expedido por la Cámara de Comercio) con una antigüedad no mayor a 30 días.</li>
  <li><strong>Documento Financiero 1:</strong> Estados Financieros del último año fiscal (Balance General, Estado de Resultados) auditados o certificados, demostrando solidez financiera.</li>
  <li><strong>Certificaciones específicas:</strong>
    <ul>
      <li>Certificación de experiencia del proponente en proyectos de I+D+i similares.</li>
      <li>Certificaciones de capacidad técnica y tecnológica (ej. infraestructura, laboratorios).</li>
      <li>Certificados de registro en el Sistema de Gestión de Información de Minciencias (SIGP, CvLAC, GrupLAC, InstituLAC) de los investigadores y la institución.</li>
    </ul>
  </li>
  <li><strong>Avales institucionales:</strong>
    <ul>
      <li>Carta de aval institucional firmada por el representante legal del proponente.</li>
      <li>Cartas de compromiso de las entidades aliadas (si aplica).</li>
    </ul>
  </li>
  <li><strong>Cartas de intención:</strong> Cartas de intención o de apoyo de comunidades, empresas o entidades territoriales que demuestren la pertinencia y el impacto del proyecto.</li>
  <li><strong>Propuesta Técnica y Económica:</strong> Documento detallado del proyecto, incluyendo metodología, plan de trabajo, cronograma, presupuesto y resultados esperados, siguiendo los formatos establecidos por la convocatoria.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> No especificado en la información inicial. Se requiere consultar los Términos de Referencia o el anexo de presupuesto para conocer la asignación total para la convocatoria.</li>
  <li><strong>Tope por Proyecto:</strong> No especificado en la información inicial. Generalmente, Minciencias establece un monto máximo financiable por proyecto, que puede variar ampliamente según la complejidad y el alcance.</li>
  <li><strong>Contrapartida:</strong> No especificado en la información inicial. Es común que Minciencias exija un porcentaje de contrapartida, que puede ser en efectivo (recursos propios) y/o en especie (infraestructura, equipos, personal dedicado, software, etc.). Este porcentaje puede oscilar entre el 10% y el 50% del valor total del proyecto.</li>
  <li><strong>Rubros Financiables:</strong> Se infieren los siguientes rubros comunes en proyectos de I+D+i de Minciencias, que deben ser detallados en los anexos financieros:
    <ul>
      <li><strong>Personal:</strong> Salarios y honorarios del equipo de investigación y técnico (investigadores, coinvestigadores, jóvenes investigadores, personal de apoyo).</li>
      <li><strong>Equipos:</strong> Adquisición de equipos especializados, software y licencias necesarias para la ejecución del proyecto.</li>
      <li><strong>Materiales e insumos:</strong> Materias primas, reactivos, componentes electrónicos, licencias de software específicas.</li>
      <li><strong>Servicios técnicos:</strong> Contratación de servicios de laboratorio, análisis especializados, consultorías externas.</li>
      <li><strong>Salidas de campo:</strong> Gastos de transporte, alojamiento y alimentación para actividades de campo o trabajo en los territorios.</li>
      <li><strong>Publicaciones y divulgación:</strong> Costos asociados a la publicación de artículos científicos, participación en eventos académicos y actividades de apropiación social.</li>
      <li><strong>Administración y gerencia:</strong> Gastos indirectos asociados a la gestión del proyecto (hasta un porcentaje límite).</li>
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
  <p>Dado que no se proporciona una matriz de riesgos explícita, se infieren los siguientes riesgos inherentes a proyectos de alta tecnología como IA y tecnologías cuánticas:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia tecnológica:</strong> Rápida evolución de las tecnologías cuánticas y de IA que puede dejar obsoleto el enfoque o la tecnología seleccionada durante la ejecución del proyecto.</li>
      <li><strong>Fallos en integración:</strong> Dificultades o incompatibilidades en la integración de diferentes componentes de hardware o software, especialmente en sistemas complejos.</li>
      <li><strong>Limitaciones de rendimiento:</strong> Los prototipos o soluciones desarrolladas pueden no alcanzar el rendimiento esperado o requerido debido a desafíos inherentes a las tecnologías emergentes.</li>
      <li><strong>Disponibilidad de datos:</strong> Dificultades para acceder a conjuntos de datos de alta calidad, representativos y suficientes para el entrenamiento y validación de modelos de IA.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en importaciones:</strong> Demoras en la adquisición e importación de equipos o componentes especializados (ej. hardware cuántico) debido a trámites aduaneros o restricciones de cadena de suministro.</li>
      <li><strong>Rotación de personal especializado:</strong> Dificultad para retener talento altamente calificado en IA y tecnologías cuánticas, lo que puede afectar la continuidad y el cronograma del proyecto.</li>
      <li><strong>Acceso a infraestructura:</strong> Limitaciones en el acceso a infraestructura de computación de alto rendimiento o plataformas cuánticas necesarias para la investigación y el desarrollo.</li>
      <li><strong>Cambios regulatorios:</strong> Modificaciones en la legislación sobre el uso de IA o protección de datos que puedan impactar el alcance o la viabilidad del proyecto.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Fluctuación del dólar:</strong> Impacto de la devaluación o revaluación del peso colombiano en la compra de equipos o licencias importadas.</li>
      <li><strong>Recortes presupuestales:</strong> Posibilidad de reducciones en la financiación por parte del ente financiador o de la contrapartida.</li>
      <li><strong>Sobrecostos tecnológicos:</strong> Gastos imprevistos asociados a la investigación y desarrollo de tecnologías emergentes, que pueden exceder el presupuesto inicial.</li>
    </ul>
  </li>
</ul>
</div>

