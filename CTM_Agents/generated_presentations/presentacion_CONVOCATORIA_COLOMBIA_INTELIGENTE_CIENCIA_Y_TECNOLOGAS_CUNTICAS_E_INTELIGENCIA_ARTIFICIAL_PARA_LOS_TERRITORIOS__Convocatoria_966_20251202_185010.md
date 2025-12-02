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
  <li><strong>Cierre:</strong> 16 de junio de 2025</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca catalizar proyectos de investigación aplicada y desarrollo tecnológico en los campos de la Inteligencia Artificial y las Tecnologías Cuánticas. Su finalidad es abordar desafíos territoriales específicos, fomentando la colaboración entre la academia, el sector empresarial y la sociedad civil, con el fin último de cerrar brechas tecnológicas y promover el desarrollo sostenible en Colombia.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones, en el marco de la Política de Investigación e Innovación Orientada por Misiones de Minciencias.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> La entidad ejecutora principal deberá ser una Institución de Educación Superior (IES) colombiana.</li>
  <li><strong>Alianzas Obligatorias:</strong> Las propuestas deben ser presentadas a través de una alianza estratégica conformada por una Institución de Educación Superior (IES), una Empresa Nacional y, como mínimo, una Organización Local o Regional.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>No cumplir con los requisitos legales y fiscales para contratar con el Estado colombiano.</li>
      <li>Existencia de conflictos de interés directos o indirectos con la entidad convocante o los evaluadores del proceso.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria está orientada a resolver problemáticas específicas en los territorios de Colombia, buscando un impacto medible y la reducción de brechas tecnológicas en diversas regiones del país. No se especifican departamentos o ciudades puntuales, sino que el enfoque es transversal a los territorios nacionales.</p>
<ul>
  <li>Territorios y regiones de Colombia que presenten problemáticas susceptibles de ser abordadas con tecnologías cuánticas e Inteligencia Artificial.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria se centra en dos ejes temáticos principales, con posibles sub-líneas de investigación y desarrollo:</p>
<ul>
  <li><strong>Línea 1: Tecnologías Cuánticas:</strong> Incluye investigación y desarrollo en computación cuántica, comunicación cuántica (criptografía cuántica), sensores cuánticos y metrología cuántica.</li>
  <li><strong>Línea 2: Inteligencia Artificial:</strong> Abarca áreas como aprendizaje automático (Machine Learning), aprendizaje profundo (Deep Learning), procesamiento del lenguaje natural (NLP), visión por computador y robótica inteligente.</li>
  <li><strong>Línea 3: Aplicaciones Transversales de IA y Cuánticas:</strong> Proyectos que integren ambas tecnologías o las apliquen en sectores estratégicos como salud, energía, agricultura, logística o medio ambiente.</li>
  <li><strong>Línea 4: Ética y Gobernanza en IA y Tecnologías Cuánticas:</strong> Investigación sobre el impacto social, ético y regulatorio de estas tecnologías, así como el desarrollo de marcos de gobernanza.</li>
  <li><strong>Línea 5: Formación de Talento Humano:</strong> Iniciativas para la capacitación y el desarrollo de capacidades en tecnologías cuánticas e Inteligencia Artificial en los territorios.</li>
</ul>
</div>


---
<!-- header: '6. ALCANCE DEL PROYECTO' -->
<h2>🔭 Componentes</h2>
<div class="card">
  <ul>
  <li><strong>TRL Esperado:</strong> Los proyectos deben enfocarse en investigación aplicada y desarrollo tecnológico, por lo que se espera que inicien en niveles de madurez tecnológica (TRL) de 3 (prueba de concepto) o 4 (validación en laboratorio) y finalicen en TRL 6 (demostración de prototipo en entorno relevante) o 7 (demostración de prototipo en entorno operacional).</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Establecimiento de alianzas estratégicas entre IES, empresas y organizaciones locales/regionales.</li>
      <li>Promoción y formación de talento humano especializado en las tecnologías objetivo.</li>
      <li>Generación de soluciones tecnológicas que aborden problemáticas territoriales específicas.</li>
      <li>Actividades de apropiación social del conocimiento y transferencia tecnológica.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> No especificada en la información inicial, pero para proyectos de esta naturaleza, se infiere una duración típica entre 12 y 24 meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  Clasifica los entregables obligatorios (inferidos por el tipo de convocatoria):
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas.</li>
      <li>Capítulos de libro o libros resultado de investigación.</li>
      <li>Tesis de maestría o doctorado dirigidas en el marco del proyecto.</li>
      <li>Informes técnicos de investigación y desarrollo.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software.</li>
      <li>Modelos de Inteligencia Artificial validados.</li>
      <li>Patentes o solicitudes de patente.</li>
      <li>Software registrado o licencias de uso de tecnología.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y sensibilización dirigidos a la comunidad.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Materiales didácticos o manuales de uso de las tecnologías desarrolladas.</li>
      <li>Creación o fortalecimiento de comunidades de práctica.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras en laboratorios para investigación.</li>
      <li>Adquisición de equipos especializados (computadores de alto rendimiento, kits cuánticos).</li>
      <li>Implementación de plataformas de desarrollo de IA o cuántico.</li>
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
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>Inteligencia Artificial:</strong> Principios éticos para el desarrollo y uso de la IA (ej. Recomendación de la UNESCO sobre la Ética de la Inteligencia Artificial). Estándares de seguridad de la información (ISO/IEC 27001) para la gestión de datos.</li>
      <li><strong>Tecnologías Cuánticas:</strong> Aunque no hay estándares comerciales masivos, se espera el uso de protocolos de interoperabilidad y buenas prácticas en el diseño experimental y la validación de resultados.</li>
      <li><strong>Desarrollo de Software:</strong> Estándares de calidad de software (ISO/IEC 25000 series) y metodologías ágiles.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Hardware:</strong> Se podrá requerir acceso a infraestructura de computación de alto rendimiento (GPUs, TPUs), equipos especializados para tecnologías cuánticas (ej. criostatos, láseres de precisión) o plataformas de acceso a computadores cuánticos en la nube.</li>
      <li><strong>Software:</strong> Plataformas de desarrollo de IA (Python con librerías como TensorFlow, PyTorch, Scikit-learn), entornos de desarrollo para computación cuántica (Qiskit, Cirq, PennyLane), herramientas de simulación.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li>Ley 1286 de 2009 (Ley de Ciencia, Tecnología e Innovación).</li>
      <li>Ley 1581 de 2012 (Protección de Datos Personales) y sus decretos reglamentarios, en caso de manejar información sensible.</li>
      <li>Regulaciones específicas del sector o territorio donde se implemente la solución.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria exige que los proyectos generen un impacto medible y ayuden a cerrar brechas tecnológicas en los territorios del país, identificando y resolviendo problemáticas específicas de las regiones.</li>
  <li><strong>Enfoque Diferencial:</strong> Aunque no se detalla explícitamente en la información disponible, es común en las convocatorias de Minciencias que se valore la inclusión de poblaciones vulnerables, grupos étnicos, mujeres, víctimas del conflicto, o el enfoque de género en el diseño y ejecución de los proyectos, buscando equidad y diversidad en el acceso y los beneficios de la ciencia y la tecnología.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <ul>
  <li><strong>Director/Gerente:</strong> Profesional con título de Doctorado o Maestría en áreas relacionadas con Ciencias de la Computación, Ingeniería Electrónica, Física, Matemáticas o afines, con al menos 5 años de experiencia en gestión y dirección de proyectos de investigación, desarrollo tecnológico e innovación.</li>
  <li><strong>Investigadores:</strong> Se requiere la participación de investigadores con título de Doctorado o Maestría en Inteligencia Artificial, Tecnologías Cuánticas, Ciencias de la Computación, Física Teórica o Experimental, o disciplinas afines, con experiencia demostrable en publicaciones y proyectos.</li>
  <li><strong>Técnicos:</strong> Profesionales o tecnólogos con experiencia en desarrollo de software, análisis de datos, ingeniería de sistemas, instrumentación, o soporte técnico especializado en las tecnologías relevantes para el proyecto.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <ul>
  <li>Propuesta técnica y económica detallada, siguiendo los formatos establecidos por Minciencias.</li>
  <li>Certificado de Existencia y Representación Legal de la IES ejecutora y de las entidades aliadas (Empresa Nacional y Organización Local/Regional).</li>
  <li>Estados financieros de las entidades participantes, con una antigüedad no mayor a tres meses.</li>
  <li>Declaración de renta del último período gravable de las entidades.</li>
  <li>Hoja de vida de los investigadores y personal clave del proyecto, con soportes académicos y de experiencia.</li>
  <li>Cartas de compromiso o acuerdos de colaboración firmados por los representantes legales de todas las entidades de la alianza.</li>
  <li>Aval institucional de la IES ejecutora.</li>
  <li>Certificaciones de experiencia relevante de la IES y la empresa en proyectos de I+D+i.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> 20.000.000.000,00 COP (Veinte mil millones de pesos colombianos).</li>
  <li><strong>Tope por Proyecto:</strong> No especificado en la información inicial. Se infiere que el monto por proyecto dependerá del alcance y la viabilidad técnica y económica de la propuesta, dentro del presupuesto total.</li>
  <li><strong>Contrapartida:</strong> No especificado en la información inicial. Es común en este tipo de convocatorias que se exija una contrapartida en efectivo y/o en especie por parte de las entidades participantes.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li>Personal científico, técnico y administrativo dedicado al proyecto.</li>
      <li>Adquisición y/o adecuación de equipos e infraestructura.</li>
      <li>Materiales e insumos para la investigación y el desarrollo.</li>
      <li>Servicios técnicos y profesionales especializados.</li>
      <li>Gastos de viaje y manutención para actividades de campo o capacitación.</li>
      <li>Costos de publicación y divulgación de resultados.</li>
      <li>Gastos de administración e imprevistos (con un tope porcentual).</li>
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
  <ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li>Obsolescencia tecnológica rápida en campos como IA y cuántica, afectando la relevancia de los resultados.</li>
      <li>Dificultades en la integración de diferentes tecnologías o plataformas.</li>
      <li>Fallos en el rendimiento esperado de los prototipos o modelos desarrollados.</li>
      <li>Retrasos en el desarrollo debido a la complejidad inherente de las tecnologías.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li>Retrasos en la adquisición o importación de equipos especializados.</li>
      <li>Alta rotación de personal altamente calificado en áreas de IA y cuántica.</li>
      <li>Dificultades en la coordinación y gestión de la alianza entre las diferentes entidades.</li>
      <li>Problemas de acceso a datos de calidad o falta de infraestructura adecuada en los territorios.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li>Fluctuaciones en las tasas de cambio si se requieren importaciones de equipos o software.</li>
      <li>Posibles sobrecostos no previstos en la ejecución de actividades de alta especialización.</li>
      <li>Insuficiencia de la contrapartida prometida por los aliados.</li>
      <li>Recortes presupuestales o cambios en las políticas de financiación.</li>
    </ul>
  </li>
</ul>
</div>

