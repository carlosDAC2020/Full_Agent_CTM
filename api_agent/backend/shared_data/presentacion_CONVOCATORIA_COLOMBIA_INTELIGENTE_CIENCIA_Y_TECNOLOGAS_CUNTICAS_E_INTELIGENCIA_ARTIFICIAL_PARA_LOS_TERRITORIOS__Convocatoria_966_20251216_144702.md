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
  <li><strong>Cierre:</strong> 18 de junio de 2025, 05:00 p.m.</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente 966 busca fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en los campos de las ciencias y tecnologías cuánticas e Inteligencia Artificial. Su objetivo principal es generar soluciones disruptivas que contribuyan al desarrollo ambiental, social y económico de las regiones, cerrando brechas tecnológicas y promoviendo un ecosistema de innovación competitivo en el país.</li>
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
  <li><strong>Ejecutor:</strong> La convocatoria está dirigida a la comunidad científica, académica, empresarial y sociedad civil. Las propuestas deben ser presentadas por alianzas estratégicas donde una Institución de Educación Superior (IES) actúa como entidad ejecutora. También pueden participar Centros e Institutos de Investigación, Centros de Desarrollo Tecnológico, Centros de Innovación y Productividad, y Parques Científicos, Tecnológicos o de Innovación, estén o no reconocidos por el Ministerio.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se exige la conformación de alianzas estratégicas integradas por al menos una Institución de Educación Superior (IES) como entidad ejecutora, una empresa nacional, y un mínimo de tres organizaciones adicionales comprometidas en la alianza base. Esto puede incluir entidades colombianas o extranjeras con trayectoria en CTeI.</li>
  <li><strong>Inhabilidades:</strong> No cumplir con los requisitos establecidos en los términos de referencia que son calificados como "NO subsanables". Esto generalmente incluye la falta de cumplimiento de requisitos legales de existencia y representación, o no presentar documentos esenciales que no admiten corrección posterior.</li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene un enfoque territorial amplio, buscando un impacto en las regiones y territorios del país para cerrar brechas tecnológicas. Aunque no especifica departamentos o ciudades particulares, se orienta a contribuir al desarrollo ambiental, social y económico de las diversas regiones colombianas.</p>
<ul>
  <li><strong>Territorios de Impacto:</strong> Todas las regiones y territorios del país que presenten brechas tecnológicas susceptibles de ser cerradas mediante la aplicación de tecnologías cuánticas e Inteligencia Artificial.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales con líneas temáticas específicas:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial:</strong>
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificación de especies, monitoreo de ecosistemas y estrategias de conservación, fomentando la innovación colaborativa con conocimientos locales.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Aplicaciones de IA en agricultura de precisión, agroindustria, gestión hídrica y trazabilidad de productos para la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo de IA para pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), incluyendo modelos predictivos para redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de IA para apoyar el aprendizaje (matemáticas, programación), personalizar contenidos y reducir brechas tecnológicas en poblaciones diversas.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Desarrollo de IA para detección temprana de desastres (inundaciones, incendios) y protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Aplicaciones de IA para análisis de imágenes médicas, diagnóstico temprano, personalización de tratamientos y optimización de la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong>
        <ul>
          <li>Algoritmos cuánticos para física, química, biología, energía, salud y fármacos.</li>
          <li>Simulación cuántica (software y hardware).</li>
          <li>Circuitos integrados cuánticos y fotónicos.</li>
          <li>Comunicaciones ultra seguras y criptografía cuántica.</li>
          <li>Internet cuántico y nodos de red distribuidos, seguros y estandarizados.</li>
        </ul>
      </li>
      <li><strong>Sensórica Cuántica y Metrología:</strong>
        <ul>
          <li>Sensores cuánticos para agricultura (control de plagas, calidad de suelos).</li>
          <li>Sensores cuánticos para salud (medicina de precisión, diagnóstico temprano).</li>
          <li>Sensores cuánticos para medioambiente (gestión ambiental).</li>
          <li>Tecnologías para el desminado seguro.</li>
          <li>Metrología cuántica para insumos médicos, alimentos y materiales estratégicos.</li>
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
  <li><strong>TRL Esperado:</strong> Los proyectos se esperan que inicien en niveles de madurez tecnológica de Investigación Aplicada (TRL 3-4, prueba de concepto validada) y finalicen con el Desarrollo Tecnológico e Innovación (TRL 6-7, prototipo a escala o sistema demostrado en un entorno relevante).</li>
  <li><strong>Componentes Obligatorios:</strong> Los proyectos deben enfocarse en la investigación aplicada y el desarrollo de soluciones disruptivas con impacto medible. Es mandatorio fomentar la transferencia tecnológica, el desarrollo de talento especializado, la reducción de brechas tecnológicas y fortalecer la vinculación efectiva entre academia, industria y sector público.</li>
  <li><strong>Duración:</strong> La duración máxima de los proyectos es de dieciocho (18) meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Los proyectos deberán generar entregables tangibles y medibles, clasificados de la siguiente manera:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos en revistas indexadas.</li>
      <li>Ponencias en eventos científicos y tecnológicos.</li>
      <li>Informes técnicos y metodológicos.</li>
      <li>Bases de datos y conjuntos de datos (datasets) resultantes de la investigación.</li>
      <li>Tesis de posgrado (Maestría, Doctorado) vinculadas al proyecto.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos o productos tecnológicos validados.</li>
      <li>Software especializado o plataformas tecnológicas desarrolladas.</li>
      <li>Patentes, diseños industriales o registros de propiedad intelectual.</li>
      <li>Modelos, algoritmos o soluciones basadas en IA y/o tecnologías cuánticas.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y transferencia de conocimiento.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Materiales pedagógicos o manuales de uso para las soluciones desarrolladas.</li>
      <li>Vinculación de jóvenes investigadores y estudiantes en el proyecto.</li>
      <li>Creación o fortalecimiento de comunidades de práctica.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones de laboratorios o espacios para la investigación y desarrollo.</li>
      <li>Adquisición y/o mejora de equipos especializados para tecnologías cuánticas o IA.</li>
      <li>Establecimiento o fortalecimiento de nodos de red para comunicaciones cuánticas.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>La convocatoria exige la adhesión a normativas y estándares técnicos relevantes para asegurar la calidad y ética de los desarrollos:</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>Para Inteligencia Artificial:</strong> Se prioriza la implementación ética y sostenible, en línea con las directrices del CONPES 4144 sobre la Política Nacional para el Desarrollo de la Inteligencia Artificial. Esto implica considerar aspectos de transparencia, explicabilidad, equidad y seguridad de los sistemas de IA.</li>
      <li><strong>Para Tecnologías Cuánticas:</strong> En el desarrollo de comunicaciones cuánticas se buscará la adherencia a estándares emergentes para redes cuánticas y protocolos de criptografía cuántica. Para la sensórica y metrología, se esperaría el cumplimiento de normas de precisión y trazabilidad aplicables.</li>
      <li><strong>Seguridad de la Información:</strong> Para el manejo de datos y sistemas, se infiere la aplicación de buenas prácticas y estándares de seguridad como ISO 27001, dada la criticidad de las tecnologías.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li>Se requieren plataformas computacionales robustas, potencialmente con capacidad de cómputo de alto rendimiento (HPC) para el entrenamiento de modelos de IA complejos y simulaciones cuánticas.</li>
      <li>Uso de herramientas y entornos de desarrollo específicos para tecnologías cuánticas (ej., kits de desarrollo de software cuántico, simuladores).</li>
      <li>Posible desarrollo o integración con circuitos integrados cuánticos y fotónicos.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>CONPES 4144:</strong> Política Nacional para el Desarrollo de la Inteligencia Artificial, que establece el marco estratégico y ético para la IA en Colombia.</li>
      <li>Leyes y regulaciones relacionadas con protección de datos personales y ciberseguridad, relevantes para la implementación de soluciones de IA y comunicaciones seguras.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> Los proyectos deben generar un impacto directo y medible en los territorios del país, contribuyendo al desarrollo ambiental, social y económico de las regiones. Se busca que las soluciones ayuden a cerrar brechas tecnológicas, impulsando la investigación aplicada y la innovación orientada a las necesidades específicas de las comunidades locales.</li>
  <li><strong>Enfoque Diferencial:</strong> La convocatoria promueve la inclusión social y el cierre de brechas, específicamente en la línea de IA para la Transformación Educativa, donde se busca la promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos. Se espera que los proyectos consideren la diversidad de poblaciones y sus necesidades para asegurar un acceso equitativo a las oportunidades formativas y tecnológicas en los territorios.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>El equipo de trabajo debe ser multidisciplinario y contar con la siguiente estructura mínima inferida:</p>
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con título de Doctorado (PhD) o Maestría, con experiencia demostrable en gestión de proyectos de investigación aplicada, desarrollo tecnológico e innovación en áreas afines a la convocatoria (IA o Tecnologías Cuánticas), y experiencia en liderazgo de equipos multidisciplinarios.</li>
  <li><strong>Investigadores:</strong> Se requiere la participación de investigadores con título de Doctorado (PhD) o Maestría, con trayectoria reconocida en los ejes temáticos de la convocatoria. Se valorará la vinculación de jóvenes investigadores y estudiantes de posgrado como parte de los semilleros de investigación.</li>
  <li><strong>Técnicos:</strong> Profesionales o tecnólogos con experiencia en el desarrollo, implementación y soporte de soluciones de software, hardware especializado, o infraestructura requerida para las tecnologías cuánticas e Inteligencia Artificial, incluyendo tutores de semilleros de investigación que pertenezcan al grupo de investigación.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Para la participación en la convocatoria, los proponentes deben presentar un conjunto de documentos críticos, los cuales, si no cumplen con lo establecido, pueden resultar en la no elegibilidad de la propuesta:</p>
<ul>
  <li>Documentos que acrediten la existencia y representación legal de la entidad ejecutora y de cada uno de los integrantes de la alianza.</li>
  <li>Documentos que soporten la capacidad financiera de la entidad ejecutora y sus co-financiadores, como estados financieros y certificaciones.</li>
  <li>Propuesta técnica y plan de trabajo detallado del proyecto.</li>
  <li>Curriculum Vitae (CvLAC) del equipo de investigación y técnico, demostrando la idoneidad y experiencia requerida.</li>
  <li>Cartas de intención y/o acuerdos de consorcio/alianza que formalicen la participación de todos los integrantes.</li>
  <li>Avales institucionales de las entidades participantes.</li>
  <li>Documentos relacionados con la gestión ética y de bioética del proyecto, si aplica (ej., concepto de comité de ética o bioética).</li>
  <li>Certificaciones de experiencia relevante de la empresa nacional asociada.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> Veinte mil millones de pesos colombianos ($20.000.000.000 COP).</li>
  <li><strong>Tope por Proyecto:</strong> Hasta mil quinientos millones de pesos colombianos ($1.500.000.000 COP) por proyecto.</li>
  <li><strong>Contrapartida:</strong> Se exige una contrapartida mínima equivalente al 20% del monto total solicitado para la financiación del proyecto, la cual puede ser aportada en dinero y/o en especie. Las Entidades Territoriales y las entidades extranjeras están exentas de este requisito de contrapartida.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li>Personal (investigadores, técnicos, jóvenes investigadores).</li>
      <li>Adquisición y/o adecuación de equipos, software y herramientas especializadas.</li>
      <li>Materiales e insumos para investigación y desarrollo.</li>
      <li>Viajes y salidas de campo (para recopilación de datos, apropiación social).</li>
      <li>Servicios técnicos y consultorías especializadas.</li>
      <li>Publicaciones y difusión de resultados.</li>
      <li>Gastos administrativos asociados directamente al proyecto (usualmente un porcentaje del monto total).</li>
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
  <p>Considerando la naturaleza de las tecnologías cuánticas y la Inteligencia Artificial, así como el alcance territorial de la convocatoria, se identifican los siguientes riesgos inherentes:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica:</strong> Rápida evolución de las tecnologías cuánticas y de IA, lo que podría desactualizar soluciones o equipos durante la ejecución del proyecto.</li>
      <li><strong>Integración y Escalabilidad:</strong> Dificultades en la integración de componentes de IA/Cuántica o en la escalabilidad de las soluciones a entornos reales y diversos territorios.</li>
      <li><strong>Sesgos Algorítmicos:</strong> Riesgo de introducir o amplificar sesgos en los modelos de IA, generando resultados inequitativos o discriminatorios, especialmente en aplicaciones con impacto social.</li>
      <li><strong>Seguridad Cuántica:</strong> Desafíos en garantizar la seguridad y privacidad de los datos en sistemas que implementan criptografía o comunicaciones cuánticas emergentes.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Acceso a Datos:</strong> Limitaciones en la disponibilidad o calidad de datos relevantes y representativos de los territorios para el entrenamiento y validación de modelos de IA.</li>
      <li><strong>Talento Especializado:</strong> Escasez de personal altamente calificado en tecnologías cuánticas y IA, lo que podría afectar la conformación del equipo o la continuidad del proyecto.</li>
      <li><strong>Coordinación de Alianzas:</strong> Retos en la gestión y coordinación efectiva de alianzas multidisciplinarias y multisectoriales (academia, empresa, sociedad civil).</li>
      <li><strong>Apropiación Social:</strong> Resistencia o baja adopción de las tecnologías desarrolladas por parte de las comunidades beneficiarias en los territorios.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Sobrecostos Tecnológicos:</strong> Gastos imprevistos asociados a la adquisición o licenciamiento de hardware/software especializado y de alto costo para IA o computación cuántica.</li>
      <li><strong>Fluctuación Monetaria:</strong> Impacto negativo de la devaluación o fluctuaciones del tipo de cambio en la adquisición de equipos o servicios importados.</li>
      <li><strong>Sub-ejecución:</strong> Dificultades en la ejecución presupuestal debido a la complejidad técnica, demoras en procesos de contratación o importación.</li>
    </ul>
  </li>
</ul>
</div>

