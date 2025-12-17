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
  <li><strong>Cierre:</strong> miércoles 18 junio 2025 04:00 pm</li>
  <li><strong>Resumen:</strong> La Convocatoria 966 "Colombia Inteligente" de Minciencias busca fortalecer la investigación aplicada, el desarrollo tecnológico y la innovación en el campo de las ciencias y tecnologías cuánticas e Inteligencia Artificial. Su objetivo es generar soluciones disruptivas con impacto medible que contribuyan al desarrollo ambiental, social y económico, y ayuden a cerrar brechas tecnológicas en los territorios colombianos, fomentando un ecosistema de innovación competitivo.</li>
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
  <li><strong>Ejecutor:</strong> Instituciones de Educación Superior (IES), centros de investigación y desarrollo tecnológico, empresas legalmente constituidas con capacidades demostradas en investigación, desarrollo tecnológico e innovación.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se promueve la vinculación entre academia, industria y sector público. Aunque no se especifica una alianza obligatoria de tipo legal, la naturaleza de la convocatoria y los objetivos de transferencia tecnológica y cierre de brechas sugieren fuertemente la participación en consorcios o alianzas estratégicas entre estos actores.</li>
  <li><strong>Inhabilidades:</strong> No cumplir con los requisitos legales y financieros establecidos en los términos de referencia. Presentar proyectos que no se ajusten a las líneas temáticas o ejes estratégicos definidos. No tener la capacidad técnica o administrativa para ejecutar el proyecto.</li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene un enfoque nacional, buscando impactar en los territorios del país y las regiones, contribuyendo a su desarrollo ambiental, social y económico, así como al cierre de brechas tecnológicas. No se especifican departamentos, ciudades o zonas PDET específicas, lo que implica una elegibilidad general para proyectos con impacto regional demonstrable.</p>
<ul>
  <li>Impacto en los territorios y regiones de Colombia en general.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales, con líneas de trabajo detalladas dentro de cada uno:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial (IA):</strong>
    <ul>
      <li><strong>Línea 1 - Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificar especies, monitorear ecosistemas y reforzar estrategias de conservación, fomentando la innovación colaborativa con conocimientos locales.</li>
      <li><strong>Línea 2 - Sistemas Agroalimentarios Inteligentes:</strong> Desarrollo y aplicaciones de IA en agricultura de precisión, agroindustria, gestión de recursos hídricos y trazabilidad de productos para la soberanía alimentaria.</li>
      <li><strong>Línea 3 - Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de IA para el pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), con modelos predictivos para redes energéticas.</li>
      <li><strong>Línea 4 - Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de IA para apoyar el aprendizaje en matemáticas y programación, personalización de contenidos y reducción de brechas.</li>
      <li><strong>Línea 5 - Gestión de Riesgos y Conservación de Fauna con IA:</strong> Desarrollo y aplicación de IA para detección temprana de desastres (inundaciones, incendios, deslizamientos) y protección de especies silvestres.</li>
      <li><strong>Línea 6 - IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo y aplicaciones de IA para análisis de imágenes médicas, diagnóstico temprano de enfermedades, tratamientos personalizados y optimización de atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong>
    <ul>
      <li><strong>Línea 1 - Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos que utilicen principios cuánticos.
        <ul>
          <li>Sublíneas: Algoritmos cuánticos, Simulación cuántica, Circuitos integrados cuánticos y fotónicos, Comunicaciones ultra seguras, Internet cuántico y nodos de red.</li>
        </ul>
      </li>
      <li><strong>Línea 2 - Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías basadas en principios cuánticos para detección, medición, trazabilidad y caracterización ultra precisa.
        <ul>
          <li>Sublíneas: Sensores cuánticos para agricultura, Sensores cuánticos para salud, Sensores cuánticos para medioambiente, Tecnologías para el desminado, Metrología cuántica.</li>
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
  <li><strong>TRL Esperado:</strong> Se espera que los proyectos abarquen un rango de madurez tecnológica, iniciando en niveles de <strong>TRL 3 (Prueba de concepto experimental)</strong> y avanzando hacia <strong>TRL 7 (Demostración de prototipo de sistema en un entorno operativo)</strong>. El enfoque en Investigación Aplicada, Desarrollo Tecnológico e Innovación implica la evolución de soluciones desde la fase de laboratorio hasta prototipos funcionales y validados.</li>
  <li><strong>Componentes Obligatorios:</strong> La convocatoria prioriza la <strong>transferencia tecnológica</strong>, el <strong>desarrollo de talento especializado</strong> y la <strong>reducción de brechas tecnológicas</strong>. Asimismo, se busca fortalecer la vinculación entre academia, industria y sector público, lo que sugiere actividades obligatorias relacionadas con estas áreas, además del componente técnico central del proyecto.</li>
  <li><strong>Duración:</strong> Los proyectos tendrán una duración máxima de <strong>18 meses</strong>.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Los entregables obligatorios deben reflejar el fortalecimiento de capacidades de CTeI y la generación de soluciones aplicadas:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Publicaciones científicas (artículos en revistas indexadas).</li>
      <li>Ponencias y presentaciones en eventos académicos nacionales e internacionales.</li>
      <li>Tesis de maestría y/o doctorado asociadas al proyecto.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software basados en IA o tecnologías cuánticas.</li>
      <li>Desarrollos de software, algoritmos o modelos innovadores.</li>
      <li>Solicitudes de patente, registros de software o derechos de autor.</li>
      <li>Implementación de soluciones tecnológicas validadas en entornos reales.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y transferencia de conocimiento a comunidades o sectores productivos.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Manuales, guías o material didáctico para usuarios finales.</li>
      <li>Creación o fortalecimiento de semilleros de investigación.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras en laboratorios y espacios de investigación.</li>
      <li>Adquisición de equipos especializados (hardware cuántico, servidores de alto rendimiento, etc.).</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Dada la naturaleza de la convocatoria en IA y tecnologías cuánticas, se infieren los siguientes estándares y normativas:</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>ISO 27001:</strong> Para la gestión de la seguridad de la información, especialmente relevante en proyectos de IA que manejen datos sensibles.</li>
      <li><strong>ISO 9001:</strong> Para sistemas de gestión de calidad en el desarrollo de productos o servicios tecnológicos.</li>
      <li><strong>Estándares de interoperabilidad:</strong> Para sistemas de IA que requieran integración con otras plataformas o bases de datos.</li>
      <li><strong>Guías éticas para IA:</strong> Adopción de principios de ética en IA, como transparencia, explicabilidad, equidad y privacidad, en línea con marcos internacionales y nacionales.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Especificaciones de servidores:</strong> Para el procesamiento intensivo de datos en IA (GPUs, TPUs, etc.).</li>
      <li><strong>Lenguajes de programación:</strong> Python, R, Julia, C++ para desarrollo de algoritmos de IA y simulaciones cuánticas.</li>
      <li><strong>Plataformas de computación cuántica:</strong> Familiaridad con entornos como IBM Qiskit, Google Cirq, o kits de desarrollo de software para hardware cuántico.</li>
      <li><strong>Bases de datos:</strong> Sistemas de gestión de bases de datos relacionales o no relacionales, adecuados para grandes volúmenes de datos.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li><strong>Ley 1581 de 2012 (Protección de Datos Personales):</strong> Obligatorio para proyectos que involucren recolección, almacenamiento y procesamiento de datos personales.</li>
      <li><strong>Legislación sobre Propiedad Intelectual:</strong> Para la protección de los desarrollos de software, patentes y demás resultados de investigación.</li>
      <li><strong>Regulaciones específicas del sector:</strong> Si el proyecto se enfoca en salud (ej. normativas INVIMA) o energía (ej. normativas CREG), deberán cumplirse las regulaciones pertinentes.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> Los proyectos deben demostrar un impacto directo y medible en el desarrollo ambiental, social y económico de las regiones y territorios del país. Se espera que las soluciones propuestas contribuyan al cierre de brechas tecnológicas y al fortalecimiento de las capacidades locales, generando valor para las comunidades.</li>
  <li><strong>Enfoque Diferencial:</strong> La convocatoria busca promover la inclusión social y la reducción de brechas. Esto implica que las propuestas deben considerar la participación y el beneficio de poblaciones vulnerables, comunidades étnicas, mujeres, víctimas del conflicto, o cualquier otro grupo minoritario que pueda ser impactado positiva y específicamente por los resultados del proyecto.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>El equipo de trabajo debe contar con perfiles idóneos y experiencia relevante en las áreas de IA o tecnologías cuánticas:</p>
<ul>
  <li><strong>Director/Gerente:</strong> Profesional con título de Doctorado (PhD) o Maestría en áreas relacionadas con Ciencias de la Computación, Ingeniería de Sistemas, Física, Matemáticas o afines, con al menos 5 años de experiencia demostrable en dirección o coordinación de proyectos de I+D+i en tecnologías avanzadas.</li>
  <li><strong>Investigadores:</strong> Se requiere la participación de investigadores con al menos título de <strong>Maestría</strong> en áreas temáticas específicas de IA o tecnologías cuánticas. Se valora experiencia en investigación aplicada, publicaciones científicas y desarrollo de proyectos relevantes. Se contempla la vinculación de un investigador por cada foco de conocimiento propuesto por la Misión de Sabios y otro con relacionamiento en procesos de CTI.</li>
  <li><strong>Técnicos:</strong> Profesionales o tecnólogos con experiencia comprobada en desarrollo de software, implementación de hardware, gestión de datos, o soporte técnico especializado en tecnologías de la información, IA o sistemas cuánticos.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Para evitar ser descartado, la presentación de los siguientes documentos es crítica:</p>
<ul>
  <li>Propuesta técnica completa y coherente con los términos de referencia.</li>
  <li>Documentos jurídicos que acrediten la existencia y representación legal de la entidad ejecutora y de los aliados (Certificado de Existencia y Representación Legal).</li>
  <li>Documentos financieros que demuestren la capacidad económica de la entidad ejecutora y la contrapartida (Estados financieros, certificaciones bancarias).</li>
  <li>Carta de aval institucional de la entidad ejecutora y de las entidades aliadas.</li>
  <li>Cartas de intención o acuerdos de colaboración que formalicen las alianzas.</li>
  <li>Certificaciones de experiencia relevante de la entidad ejecutora y del equipo de trabajo.</li>
  <li>Hoja de vida del equipo de trabajo, con soportes académicos y de experiencia.</li>
  <li>Evidencia de registro en el Sistema Integrado de Gestión de Proyectos (SIGP) de Minciencias.</li>
  <li>Anexos específicos de la convocatoria, como la carta de experiencia de la empresa nacional (Anexo 2).</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> 20,000 millones de pesos colombianos.</li>
  <li><strong>Tope por Proyecto:</strong> Hasta 1,500 millones de pesos colombianos.</li>
  <li><strong>Contrapartida:</strong> Un valor mínimo equivalente al <strong>20%</strong> del monto total solicitado para la financiación del proyecto, el cual podrá ser aportado en dinero y/o en especie.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li>Gastos de personal (investigadores, coinvestigadores, jóvenes investigadores, personal técnico y de apoyo).</li>
      <li>Adquisición y/o adecuación de equipos, software especializado y licencias.</li>
      <li>Materiales e insumos para el desarrollo de actividades experimentales o prototipado.</li>
      <li>Servicios tecnológicos y de consultoría especializada.</li>
      <li>Capacitación y formación relacionada con el proyecto.</li>
      <li>Viajes y salidas de campo nacionales e internacionales necesarias para la ejecución.</li>
      <li>Gastos de publicación y divulgación de resultados.</li>
      <li>Gastos asociados a la protección de la propiedad intelectual.</li>
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
  <p>Considerando la complejidad y la naturaleza avanzada de las tecnologías cuánticas y la Inteligencia Artificial, se infieren los siguientes riesgos:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li>Obsolescencia tecnológica rápida de hardware o software debido a la evolución acelerada de estas áreas.</li>
      <li>Dificultades en la integración de diferentes componentes tecnológicos (ej. hardware cuántico con software clásico).</li>
      <li>Fallos en la validación o rendimiento esperado de los algoritmos de IA o los sistemas cuánticos.</li>
      <li>Disponibilidad limitada de datos de alta calidad o sesgos inherentes en los conjuntos de datos para entrenamiento de IA.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li>Retrasos en la adquisición o importación de equipos especializados y de alto costo.</li>
      <li>Rotación de personal altamente calificado o dificultad para encontrar talento con habilidades específicas en IA y computación cuántica.</li>
      <li>Problemas de infraestructura física o tecnológica (conectividad, energía) en los territorios donde se implementen los proyectos.</li>
      <li>Dificultades en la coordinación entre los miembros del consorcio (academia, industria, sector público).</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li>Sobre costos inesperados en el desarrollo de prototipos o la adquisición de licencias.</li>
      <li>Fluctuación de tasas de cambio que afecte la compra de equipos o servicios internacionales.</li>
      <li>Dependencia exclusiva de la financiación de la convocatoria sin fuentes de financiación complementarias.</li>
      <li>Dificultades en la justificación de rubros o desembolsos de la contrapartida.</li>
    </ul>
  </li>
</ul>
</div>

