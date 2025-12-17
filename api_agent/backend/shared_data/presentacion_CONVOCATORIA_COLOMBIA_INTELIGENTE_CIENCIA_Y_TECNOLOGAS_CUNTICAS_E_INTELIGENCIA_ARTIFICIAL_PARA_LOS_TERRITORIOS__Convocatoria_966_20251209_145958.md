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
  <li><strong>Cierre:</strong> 16 de junio de 2025 hasta las 4:00 p.m. hora colombiana (según Adenda No. 1)</li>
  <li><strong>Resumen:</strong> La Convocatoria "Colombia Inteligente" busca fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en tecnologías cuánticas e Inteligencia Artificial. Su objetivo es generar un impacto medible que contribuya al desarrollo ambiental, social y económico, y ayude a cerrar brechas tecnológicas en los territorios colombianos. Prioriza la transferencia tecnológica, el desarrollo de talento especializado y el fortalecimiento de alianzas entre academia, industria y sector público.</li>
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
  <li><strong>Ejecutor:</strong> La entidad ejecutora principal deberá ser una Institución de Educación Superior (IES).</li>
  <li><strong>Alianzas Obligatorias:</strong> Las propuestas deben ser presentadas a través de una alianza estratégica conformada por una Institución de Educación Superior (IES), una Empresa Nacional y, como mínimo, una (1) Organización Local – Regional. Las entidades de la alianza deben tener domicilio en la misma región.</li>
  <li><strong>Inhabilidades:</strong> Una empresa nacional no podrá estar relacionada en más de una propuesta presentada a esta convocatoria. Se requiere que el Investigador Principal sea profesor regular, ocasional o visitante (tiempo completo o medio tiempo), y si es ocasional o visitante, debe contar con el respaldo de un profesor de planta.</li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene un marcado enfoque territorial, buscando impactar el desarrollo ambiental, social y económico de las regiones del país. Sin embargo, no especifica departamentos, ciudades o zonas PDET específicas, sino que se orienta a proyectos con impacto regional generalizado, exigiendo que las entidades de la alianza (IES, Empresa Nacional, Organización Local-Regional) cuenten con domicilio en la misma región.</p>
<ul>
  <li>No se especifican lugares geográficos concretos más allá del impacto general en las <strong>regiones</strong> de Colombia.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>Desglosa las líneas temáticas o ejes de investigación:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial:</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificar especies, monitorear ecosistemas y reforzar estrategias de conservación, fomentando la innovación colaborativa con conocimientos locales para transformar recursos biológicos.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Desarrollo y aplicaciones de IA en agricultura de precisión, agroindustria, gestión de recursos hídricos y trazabilidad de productos para la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de IA para el pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), y modelos predictivos para la toma de decisiones en redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de tecnologías basadas en IA para apoyar el aprendizaje en áreas como matemáticas y programación, con personalización de contenidos y reducción de brechas tecnológicas.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Desarrollo y aplicación de tecnologías de IA para la detección temprana de desastres (inundaciones, incendios, deslizamientos) y la protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo y aplicaciones de IA para el análisis de imágenes médicas, mejora de precisión en diagnóstico temprano de enfermedades, personalización de tratamientos y optimización de atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos que utilicen principios cuánticos para el procesamiento de información y comunicación. Incluye algoritmos cuánticos, simulación cuántica, circuitos integrados cuánticos y fotónicos, comunicaciones ultra seguras e internet cuántico.</li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías basadas en principios cuánticos para la detección, medición, trazabilidad y caracterización ultra precisa de fenómenos físicos, químicos o biológicos. Incluye sensores cuánticos para agricultura, salud, medioambiente, tecnologías para el desminado y metrología cuántica.</li>
      <li><strong>Energía Sostenible y Minerales Estratégicos:</strong> Línea enfocada en la aplicación de tecnologías cuánticas para estos sectores.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> La convocatoria busca fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación, lo que implica proyectos que probablemente inicien en niveles de madurez tecnológica bajos o intermedios (ej. TRL 3 - Prueba de concepto experimental) y avancen hacia niveles más altos (ej. TRL 6-7 - Demostración de prototipo a escala en entorno relevante/operacional). Se enfatiza la identificación del TRL y la transferencia tecnológica.</li>
  <li><strong>Componentes Obligatorios:</strong> El proyecto debe incluir componentes de Investigación, Desarrollo e Innovación (I+D+i) y un fuerte componente de Formación de Talento Humano. También se debe considerar la protección de los activos de conocimiento (Propiedad Intelectual).</li>
  <li><strong>Duración:</strong> El término de duración de los proyectos postulados deberá ser de hasta dieciocho (18) meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Clasifica los entregables obligatorios (inferidos por la naturaleza de la convocatoria):</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas o de alto impacto.</li>
      <li>Ponencias y presentaciones en eventos académicos y científicos.</li>
      <li>Tesis de maestría y doctorado resultantes de la investigación.</li>
      <li>Informes técnicos y científicos detallados del progreso y resultados del proyecto.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos de hardware o software funcional demostrando las tecnologías de IA o cuánticas.</li>
      <li>Algoritmos y modelos computacionales desarrollados.</li>
      <li>Software especializado o módulos tecnológicos.</li>
      <li>Solicitudes de patente, registros de software o derechos de autor sobre las innovaciones generadas.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Realización de talleres, seminarios o eventos de divulgación científica y tecnológica.</li>
      <li>Creación de material didáctico o guías para la apropiación del conocimiento.</li>
      <li>Programas de formación para jóvenes investigadores, semilleros de investigación, estudiantes de maestría y postdoctorales.</li>
      <li>Eventos de transferencia tecnológica o demostraciones a comunidades y sectores productivos.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones menores en laboratorios o espacios de investigación.</li>
      <li>Adquisición de equipos especializados o componentes de hardware necesarios para el desarrollo del proyecto.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Investiga estándares técnicos específicos (inferidos o menciones de políticas):</p>
<ul>
  <li><strong>Estándares:</strong> Aunque no se detallan estándares específicos de forma explícita, se infiere la necesidad de adherencia a buenas prácticas de ingeniería de software (para IA), principios de seguridad de la información (ej. ISO 27001 para la gestión de datos y comunicaciones seguras en IA y cuántica), y estándares de precisión en metrología. Para tecnologías cuánticas, se esperaría cumplimiento con principios fundamentales de la física cuántica y protocolos de seguridad criptográfica.</li>
  <li><strong>Hardware/Software:</strong> No se especifican marcas o arquitecturas mínimas. Sin embargo, los proyectos de IA y cuánticos generalmente requieren infraestructura de computación de alto rendimiento (GPUs, TPUs, clústeres), lenguajes de programación especializados (Python con librerías como TensorFlow, PyTorch para IA; Qiskit, Cirq para cuántica), y entornos de desarrollo robustos.</li>
  <li><strong>Normatividad:</strong> La convocatoria se enmarca en la Política de Investigación e Innovación Orientada por Misiones. Específicamente, el eje de Inteligencia Artificial se alinea con lo establecido en el <strong>CONPES 4144</strong>, que promueve el desarrollo, la implementación y la adopción ética y sostenible de soluciones basadas en IA.</li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> Los proyectos deben contribuir al desarrollo ambiental, social y económico de las regiones del país. Se busca cerrar brechas tecnológicas y fortalecer el ecosistema de innovación local, exigiendo que las entidades de la alianza tengan domicilio en la misma región.</li>
  <li><strong>Enfoque Diferencial:</strong> Se busca la inclusión social y el cierre de brechas, con una especial promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos, impulsando la inclusión y el acceso a oportunidades formativas en los territorios.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>Detalla el equipo mínimo requerido (inferido de rubros financiables y menciones en TDR):</p>
<ul>
  <li><strong>Director/Gerente:</strong> El Investigador Principal deberá ser profesor regular, ocasional o visitante (de tiempo completo o medio tiempo) de una IES. Si es ocasional o visitante, se requiere el respaldo de un profesor de planta. No se especifican años de experiencia mínimos, pero se infiere una trayectoria relevante en investigación.</li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Doctor/Postdoctoral:</strong> Apoyo económico para la realización de una estancia posdoctoral (doctor).</li>
      <li><strong>Estudiantes de Maestría:</strong> Apoyo para el pago de matrícula de hasta dos estudiantes de maestría, implicando su vinculación a los proyectos.</li>
      <li><strong>Jóvenes Investigadores:</strong> Apoyo económico para la vinculación de jóvenes investigadores e innovadores profesionales.</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong> Se contempla apoyo para el desarrollo de semilleros de investigación, lo que implica la vinculación de talento joven en etapas iniciales de formación.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Lista tipo checklist de los documentos más críticos (inferidos de prácticas estándar en convocatorias de I+D+i):</p>
<ul>
  <li>Propuesta Técnica detallada del proyecto (incluyendo metodología, cronograma, plan de trabajo).</li>
  <li>Propuesta Económica/Presupuesto detallado y justificado.</li>
  <li>Acta o Acuerdo de Conformación de Alianza Estratégica.</li>
  <li>Cartas de Intención o Avales institucionales de cada miembro de la alianza (IES, Empresa Nacional, Organización Local-Regional).</li>
  <li>Certificados de Existencia y Representación Legal de las entidades de la alianza.</li>
  <li>Certificados de Experiencia o Capacidad Técnica de las entidades.</li>
  <li>Hoja de Vida y Soportes académicos/profesionales del Investigador Principal y equipo de trabajo.</li>
  <li>Declaraciones de No Inhabilidad e Incompatibilidad.</li>
  <li>Certificación de Domicilio en la misma región para los miembros de la alianza.</li>
  <li>Documentos relacionados con la protección de Propiedad Intelectual o plan de gestión de IP.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> 20.000 millones de pesos.</li>
  <li><strong>Tope por Proyecto:</strong> Hasta MIL QUINIENTOS MILLONES DE PESOS M/CTE ($1.500.000.000).</li>
  <li><strong>Contrapartida:</strong> Mínimo equivalente al 20% del monto total solicitado para la financiación del proyecto, en dinero y/o especie.</li>
  <li><strong>Rubros Financiables:</strong> Incluyen costos de Investigación, Desarrollo e Innovación (hasta $1.004.000.000), Formación de Talento Humano (hasta $496.000.000 para estancias posdoctorales, estudiantes de maestría, jóvenes investigadores y semilleros), y costos asociados a la protección de activos de conocimiento (ej. trámites de patentes, diseños industriales, marcas). No son financiables la compra de terrenos o inmuebles.</li>
</ul>
  </div>
</div>


---
<!-- _class: compact -->
<!-- header: '13. MAPA DE RIESGOS' -->
<h2>🛡️ Matriz de Riesgos</h2>
<!-- Si la tabla es muy larga, reduce fuente -->
<div style="font-size: 0.8em;">
  <p>Si no hay matriz de riesgos explícita, INFIERELOS basados en proyectos similares de tecnología/ciencia:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica:</strong> Rápido avance en tecnologías cuánticas e IA que podría dejar obsoleto el enfoque o las herramientas del proyecto antes de su finalización.</li>
      <li><strong>Fallas en la Integración:</strong> Dificultades para integrar diferentes componentes tecnológicos o resultados de investigación de las diferentes entidades de la alianza.</li>
      <li><strong>Escalabilidad Limitada:</strong> Los prototipos o soluciones desarrolladas podrían no ser fácilmente escalables a entornos reales o a mayor volumen.</li>
      <li><strong>Disponibilidad de Datos y Algoritmos:</strong> Retos en la adquisición, calidad o curación de los datos necesarios para el entrenamiento y validación de modelos de IA, o la disponibilidad de recursos de computación cuántica.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en la Ejecución:</strong> Dificultades administrativas, logísticas o de coordinación entre las entidades de la alianza que afectan el cronograma.</li>
      <li><strong>Rotación de Personal Clave:</strong> Pérdida de investigadores o personal técnico especializado durante la ejecución del proyecto.</li>
      <li><strong>Dependencia Tecnológica Externa:</strong> Retrasos o altos costos asociados a la importación de equipos especializados o licencias de software/hardware.</li>
      <li><strong>Gestión de la Alianza:</strong> Desacuerdos o dificultades en la gestión de las expectativas y contribuciones de cada miembro de la alianza.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Sobrecostos No Previstos:</strong> Aparición de gastos adicionales no contemplados en el presupuesto original, especialmente en investigación y desarrollo de tecnologías emergentes.</li>
      <li><strong>Fluctuación Monetaria:</strong> Impacto de la devaluación o revaluación de la moneda en la adquisición de insumos importados o servicios tecnológicos.</li>
      <li><strong>Subutilización de Recursos:</strong> No lograr la ejecución completa de los rubros asignados dentro del plazo, generando posibles reintegros.</li>
      <li><strong>Disponibilidad de Contrapartida:</strong> Dificultades de las entidades aliadas para garantizar la contrapartida prometida en tiempo y forma.</li>
    </ul>
  </li>
</ul>
</div>

