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
  <li><strong>Número:</strong> Convocatoria 966 de 2025</li>
  <li><strong>Apertura:</strong> 25 de abril de 2025</li>
  <li><strong>Cierre:</strong> 18 de junio de 2025 04:00 pm (Hora colombiana)</li>
  <li><strong>Resumen:</strong> La convocatoria "ColombIA Inteligente" busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial. El objetivo es impulsar proyectos que generen un impacto medible y contribuyan al cierre de brechas tecnológicas en los territorios colombianos, fomentando la colaboración entre la academia, el sector empresarial y las comunidades.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones. La convocatoria prioriza propuestas que fomenten la transferencia tecnológica, el desarrollo de talento especializado y la reducción de brechas tecnológicas.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> Instituciones de Educación Superior (IES) colombianas, que actuarán como la entidad principal de la propuesta.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se exige la conformación de alianzas estratégicas integradas por al menos una Institución de Educación Superior (IES), una empresa nacional y al menos tres organizaciones locales o regionales (pueden ser comunitarias, de base tecnológica, entre otras).</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>No cumplir con los requisitos legales de constitución y existencia de la persona jurídica (ejecutor o aliados).</li>
      <li>Tener inhabilidades o incompatibilidades según la normatividad colombiana para contratar con el Estado o recibir recursos públicos de CTeI.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene un alcance nacional, con un fuerte enfoque territorial. No se especifican departamentos, ciudades o zonas PDET (Programas de Desarrollo con Enfoque Territorial) obligatorios. Sin embargo, las propuestas deben demostrar un impacto medible y contribuir al cierre de brechas tecnológicas en los territorios del país, lo que implica abordar necesidades y desafíos específicos de diversas regiones de Colombia.</p>
<ul>
  <li>Se priorizan propuestas que aborden desafíos tecnológicos, productivos y sociales con enfoque territorial, inclusión social y cierre de brechas a nivel nacional.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria se estructura en dos ejes estratégicos principales, con diversas líneas y sublíneas:</p>
<ul>
  <li><strong>Línea Principal 1: Inteligencia Artificial (IA)</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Aplicaciones de IA para clasificación de especies, monitoreo de ecosistemas y conservación, con colaboración en conocimientos locales.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> IA en agricultura de precisión, agroindustria, gestión hídrica y trazabilidad de productos para soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> IA para pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa).</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> IA para apoyar el aprendizaje en matemáticas y programación, personalización de contenidos y reducción de brechas.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Modelos de IA para detección temprana de desastres y protección de especies silvestres.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Aplicaciones de IA para análisis de imágenes médicas, diagnóstico temprano, tratamientos personalizados y optimización sanitaria.</li>
    </ul>
  </li>
  <li><strong>Línea Principal 2: Ciencia y Tecnologías Cuánticas</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Desarrollo de algoritmos cuánticos para física, química, biología, energía, salud, fármacos; simulación cuántica; circuitos integrados cuánticos y fotónicos; criptografía cuántica; Internet cuántico y nodos de red.</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías cuánticas para detección y medición ultra precisa. Incluye sensores para agricultura, salud, medioambiente; tecnologías para desminado; metrología cuántica.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> Los proyectos deben iniciar en un nivel de madurez tecnológica (TRL) entre <strong>TRL 4 (Validación de tecnología en entorno de laboratorio) y TRL 6 (Demostración de prototipo en entorno relevante)</strong>. Al finalizar la ejecución, deben demostrar un TRL superior al inicial, siendo coherentes con los productos planteados.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Investigación Aplicada y/o Desarrollo Tecnológico.</li>
      <li>Generación de soluciones innovadoras y disruptivas.</li>
      <li>Fortalecimiento o formación de talento humano especializado.</li>
      <li>Estrategias de Apropiación Social del Conocimiento y Divulgación Científica.</li>
      <li>Transferencia tecnológica y/o innovación que contribuya al desarrollo regional.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> Aunque no se especifica una duración exacta, proyectos de esta naturaleza y complejidad suelen tener una duración máxima de <strong>hasta 36 meses</strong>.</li>
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
      <li>Publicaciones científicas (artículos en revistas indexadas, capítulos de libro).</li>
      <li>Tesis de posgrado (Maestría, Doctorado) asociadas al proyecto.</li>
      <li>Informes técnicos de investigación y desarrollo.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales validados en entornos relevantes.</li>
      <li>Desarrollo de software, algoritmos o modelos de IA/Cuánticos.</li>
      <li>Patentes, registros de propiedad intelectual o nuevas variedades vegetales/animales.</li>
      <li>Diseños y/o circuitos integrados especializados.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Eventos de divulgación y comunicación pública de la ciencia y tecnología.</li>
      <li>Talleres de capacitación y formación dirigidos a comunidades o sectores específicos.</li>
      <li>Manuales, guías o material didáctico para la apropiación del conocimiento.</li>
      <li>Participación de jóvenes investigadores y semilleros de investigación.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adquisición, instalación o adecuación de equipos especializados y laboratorios para CTeI.</li>
      <li>Fortalecimiento de capacidades de infraestructura computacional (HPC, clusters).</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Aunque los términos de referencia no especifican estándares o especificaciones técnicas rígidas, dada la naturaleza de las tecnologías cuánticas y la inteligencia artificial, se infieren los siguientes requisitos y consideraciones:</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>Seguridad de la Información:</strong> Adherencia a normas como ISO 27001 para la gestión de la seguridad de datos.</li>
      <li><strong>Gestión de Calidad:</strong> Aplicación de principios de ISO 9001 en los procesos de investigación y desarrollo.</li>
      <li><strong>Ética en IA:</strong> Alineación con principios éticos para el desarrollo y uso de la Inteligencia Artificial (ej. guías de la OCDE, UNESCO).</li>
      <li><strong>Interoperabilidad:</strong> Consideración de estándares para la integración de sistemas y datos.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Infraestructura Computacional:</strong> Se espera el uso o desarrollo de capacidad de cómputo avanzada (GPUs, HPC, plataformas de cloud computing) para proyectos de IA.</li>
      <li><strong>Entornos de Desarrollo Cuántico:</strong> Familiaridad y uso de herramientas y lenguajes específicos para computación cuántica (ej. Qiskit, Cirq, TensorFlow Quantum).</li>
      <li><strong>Lenguajes de Programación:</strong> Dominio de lenguajes como Python, R, C++ para desarrollo de algoritmos de IA y simulaciones.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>Protección de Datos:</strong> Cumplimiento de la Ley 1581 de 2012 y sus decretos reglamentarios sobre protección de datos personales.</li>
      <li><strong>Propiedad Intelectual:</strong> Manejo de la propiedad intelectual generada según la legislación colombiana y políticas de Minciencias.</li>
      <li><strong>Regulaciones Específicas:</strong> Observancia de cualquier regulación sectorial aplicable (ej. salud, agricultura) donde se aplique la tecnología.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> Los proyectos deben generar un impacto medible en los territorios del país, contribuyendo al cierre de brechas tecnológicas y al desarrollo ambiental, social y económico de las regiones. Se busca la pertinencia y relevancia de las soluciones propuestas para las necesidades específicas de las comunidades y ecosistemas locales.</li>
  <li><strong>Enfoque Diferencial:</strong> Se espera la inclusión y el beneficio de poblaciones vulnerables, grupos étnicos, mujeres, víctimas del conflicto armado y personas con discapacidad, en línea con el objetivo de promover la inclusión social y la reducción de inequidades en el acceso a la ciencia y tecnología.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>El equipo mínimo requerido para las propuestas, inferido de proyectos de CTeI similares, incluye:</p>
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con título de posgrado (Maestría o Doctorado) en áreas afines a la convocatoria (Ciencias de la Computación, Ingeniería, Física, Matemáticas) y experiencia mínima de 5 años en dirección o coordinación de proyectos de investigación, desarrollo tecnológico o innovación, preferiblemente en IA o tecnologías cuánticas.</li>
  <li><strong>Investigadores:</strong> Se requiere la participación de investigadores con nivel educativo mínimo de Maestría, y se valorará positivamente la inclusión de investigadores con Doctorado, en las líneas temáticas de la convocatoria.</li>
  <li><strong>Técnicos:</strong> Profesionales o tecnólogos con experiencia específica en desarrollo de software, manejo de plataformas computacionales, operación de equipos de laboratorio o soporte técnico especializado en las áreas de IA y/o tecnologías cuánticas.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Lista de documentos críticos para la participación (tipo checklist):</p>
<ul>
  <li>Propuesta Técnica y Financiera detallada, presentada a través del sistema SIGP de Minciencias.</li>
  <li>Certificado de Existencia y Representación Legal de la entidad ejecutora y de cada una de las entidades aliadas, con una antigüedad no inferior a tres (3) años al cierre de la convocatoria.</li>
  <li>Estados Financieros auditados del último año de la entidad ejecutora y de las empresas aliadas.</li>
  <li>Hojas de Vida actualizadas de todo el equipo de trabajo (Director, Investigadores, Técnicos) en el sistema CvLAC de Minciencias.</li>
  <li>Cartas de Aval y Compromiso Institucional de la entidad ejecutora y de cada uno de los aliados, formalizando la alianza y la contrapartida.</li>
  <li>Certificaciones que acrediten la experiencia relevante de la entidad ejecutora y de la empresa aliada en proyectos de CTeI.</li>
  <li>Plan de Trabajo detallado y Cronograma de actividades.</li>
  <li>Presupuesto desglosado por rubros financiables y fuentes de financiación (Minciencias y contrapartida).</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> No se especifica un monto global único en los documentos públicos fácilmente accesibles, pero se infiere un presupuesto considerable por la naturaleza de la convocatoria y menciones de distribución de recursos en presentaciones, estimado en al menos <strong>$6.003.000.000 COP</strong> (suma de valores mencionados para investigación y apoyo).</li>
  <li><strong>Tope por Proyecto:</strong> El monto máximo de financiación por proyecto será de hasta <strong>MIL QUINIENTOS MILLONES DE PESOS MCTE ($ 1.500.000.000 COP)</strong>.</li>
  <li><strong>Contrapartida:</strong> La contrapartida es <strong>requerida</strong>. Aunque no se especifica un porcentaje exacto para esta convocatoria, Minciencias generalmente exige una contrapartida que oscila entre el <strong>10% y el 30%</strong> del valor total del proyecto, la cual puede ser aportada en efectivo y/o en especie.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li>Personal científico y de apoyo técnico vinculado al proyecto.</li>
      <li>Adquisición y/o adecuación de equipos, software y materiales especializados.</li>
      <li>Gastos de viaje y salidas de campo relacionadas con la investigación.</li>
      <li>Materiales e insumos fungibles.</li>
      <li>Servicios técnicos especializados.</li>
      <li>Publicaciones y divulgación.</li>
      <li>Gastos de administración y gerencia de proyecto (con topes).</li>
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
  <p>Basado en la naturaleza de proyectos de tecnologías cuánticas e Inteligencia Artificial, se infieren los siguientes riesgos:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica:</strong> Rápida evolución de tecnologías de IA y cuánticas que pueden hacer que las soluciones propuestas queden desactualizadas antes o durante la ejecución.</li>
      <li><strong>Complejidad Inherente:</strong> Dificultades no previstas en la implementación de algoritmos complejos o en la integración de componentes cuánticos/IA con sistemas existentes.</li>
      <li><strong>Fallas en Integración:</strong> Desafíos en la interoperabilidad entre diferentes plataformas, hardware o software.</li>
      <li><strong>Escalabilidad:</strong> Limitaciones inesperadas en la escalabilidad de las soluciones desarrolladas a entornos reales o a mayor escala.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en Adquisiciones/Importaciones:</strong> Demoras en la adquisición o importación de equipos y licencias de software especializado, debido a la cadena de suministro global o regulaciones aduaneras.</li>
      <li><strong>Rotación de Talento Humano:</strong> Dificultad para retener personal altamente calificado en IA y tecnologías cuánticas, dada la alta demanda en el mercado.</li>
      <li><strong>Acceso a Datos:</strong> Limitaciones en la disponibilidad o calidad de los conjuntos de datos necesarios para entrenar modelos de IA o validar hipótesis.</li>
      <li><strong>Gestión de Alianzas:</strong> Dificultades en la coordinación y gestión efectiva entre los múltiples actores de la alianza (IES, empresa, organizaciones locales).</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Sobrecostos No Previstos:</strong> Incremento en los costos de licencias, hardware o servicios por fluctuaciones del mercado o tasas de cambio.</li>
      <li><strong>No Consecución de Contrapartida:</strong> Dificultad para que los aliados cumplan con los aportes de contrapartida prometidos en efectivo o especie.</li>
      <li><strong>Recortes Presupuestales:</strong> Posibles ajustes o recortes en el presupuesto asignado por Minciencias durante la ejecución del proyecto.</li>
    </ul>
  </li>
</ul>
</div>

