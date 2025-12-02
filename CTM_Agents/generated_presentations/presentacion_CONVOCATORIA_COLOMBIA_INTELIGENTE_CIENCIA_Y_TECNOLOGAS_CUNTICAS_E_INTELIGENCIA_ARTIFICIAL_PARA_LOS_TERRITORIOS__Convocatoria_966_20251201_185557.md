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

  /* --- PORTADA CON FONDO DEGRADADO --- */
  section.title-slide {
    padding: 0;
    /* Degradado usando las variables de color definidas arriba */
    background-image: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
    
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    align-items: center; 
    text-align: center;
    color: white; 
  }

  section.title-slide h1 { 
    color: white; 
    font-size: 2.8em; 
    margin-bottom: 20px; 
    text-shadow: 2px 2px 5px rgba(0,0,0,0.4); /* Sombra para resaltar texto */
  }
  
  section.title-slide h3 { 
    color: var(--secondary); /* Amarillo Cotecmar */
    font-size: 1.5em;
    font-weight: normal;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
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
  <li><strong>Resumen:</strong> La Convocatoria Colombiaura:</strong> 25 de abril de 2025</li>
  <li><strong>Cierre:</strong> 18 de junio de 2025</li>
  <li><strong>Resumen:</strong> La Convocatoria Colombia Inteligente busca potenciar la investigación aplicada, el desarrollo tecnológico y la innovación en tecnologías cuánticas e Inteligencia Artificial. Su objetivo es generar soluciones disruptivas con impacto medible que contribuyan al desarrollo ambiental, social y económico de las regiones, alineándose con la Política de Investigación e Innovación Orientada por Misiones para cerrar brechas tecnológicas en el país.</li>
</ul>
</div>


---
<!-- header: '2. OBJETIVO' -->
<div class="card">
  <h2>🎯 Objetivo General</h2>
  <p>Fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en ciencias y tecnologías cuánticas e Inteligencia Artificial, contribuyendo al desarrollo ambiental, social y económico de las regiones en el marco de la Política de Investigación e Innovación Orientada por Misiones. Busca consolidar a Colombia como un referente en innovación tecnológica, abordando desafíos productivos y sociales con soluciones disruptivas y de impacto medible.</p>
</div>


---
<!-- header: '3. DIRIGIDO A' -->
<h2>👥 Participantes y Alianzas</h2>
<div class="grid-2">
  <div class="card">
    <strong>Requisitos:</strong><br>
    <ul>
  <li><strong>Ejecutor:</strong> Instituciones de Educación Superior (IES).</li>
  <li><strong>Alianzas Obligatorias:</strong> Las propuestas deben ser presentadas a través de una alianza estratégica conformada por una Institución de Educación Superior (IES), una Empresa Nacional y, como mínimo, una Organización Local – Regional.</li>
  <li><strong>Inhabilidades:</strong>
    <ul>
      <li>La ausencia de la carta de experiencia de la empresa nacional o de los documentos que acrediten la experiencia de proyectos ejecutados en los últimos cinco años será causal de rechazo.</li>
      <li>No cumplir con los requisitos legales o financieros establecidos en los términos de referencia, que impidan la contratación con entidades públicas.</li>
    </ul>
  </li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene un enfoque nacional, pero prioriza la generación de impacto medible en los territorios del país, buscando contribuir al desarrollo ambiental, social y económico de las regiones y cerrar brechas tecnológicas. No se especifican departamentos, ciudades o zonas PDET específicas, pero el impacto territorial es un criterio fundamental.</p>
<ul>
  <li>Territorios del país en general, con énfasis en el cierre de brechas tecnológicas regionales.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>Desglosa las líneas temáticas o ejes de investigación:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial:</strong> Promueve el desarrollo, implementación y adopción ética y sostenible de soluciones basadas en IA en sectores estratégicos.
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificación de especies, monitoreo de ecosistemas, conservación y transformación de recursos biológicos.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Aplicaciones de IA en agricultura de precisión, agroindustria, gestión hídrica y trazabilidad para la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de IA para pronóstico, control y uso sostenible de fuentes limpias y modelos predictivos para redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Implementación de IA para apoyar el aprendizaje, personalizar contenidos y promover competencias en diferentes grupos etarios.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Aplicación de IA para detección temprana de desastres y protección de especies silvestres.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo de IA para análisis de imágenes médicas, diagnóstico temprano, tratamientos personalizados y optimización de atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong> Definido por un grupo de expertos para identificar y priorizar áreas clave.
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos cuánticos.
        <ul>
          <li>Algoritmos cuánticos para resolver problemas en física, química, biología, energía, salud, fármacos.</li>
          <li>Simulación cuántica: Investigación y aplicación de herramientas y entornos de desarrollo.</li>
          <li>Circuitos integrados cuánticos y fotónicos: Investigación en arquitectura y diseño.</li>
          <li>Comunicaciones ultra seguras: Investigación e implementación de protocolos de criptografía cuántica.</li>
          <li>Internet cuántico y nodos de red: Investigación e implementación de redes cuánticas.</li>
        </ul>
      </li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías cuánticas para detección, medición y caracterización ultra precisa.
        <ul>
          <li>Sensores cuánticos para agricultura: Dispositivos de medición para control de plagas y calidad de suelos.</li>
          <li>Sensores cuánticos para salud: Dispositivos de medición para medicina de precisión y diagnóstico temprano.</li>
          <li>Sensores cuánticos para medioambiente: Dispositivos de medición para gestión ambiental.</li>
          <li>Tecnologías para el desminado: Investigación y desarrollo de tecnologías de desminado seguro.</li>
          <li>Metrología cuántica: Implementación de patrones y unidades de medida aplicados a insumos médicos, alimentos y materiales.</li>
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
  <li><strong>TRL Esperado:</strong> Se espera que los proyectos abarquen desde la investigación aplicada (TRL 3-4) hasta el desarrollo tecnológico y la innovación con prototipos validados en entornos relevantes (TRL 5-7), buscando soluciones disruptivas con impacto medible que puedan ser escaladas.</li>
  <li><strong>Componentes Obligatorios:</strong>
    <ul>
      <li>Fortalecer la vinculación entre academia, industria y sector público.</li>
      <li>Fomentar la transferencia tecnológica.</li>
      <li>Desarrollo de talento especializado.</li>
      <li>Reducción de brechas tecnológicas en el país.</li>
      <li>Vincular mínimo un (1) semillero de investigación, conformado por al menos diez (10) estudiantes de pregrado de tercer semestre en adelante.</li>
    </ul>
  </li>
  <li><strong>Duración:</strong> La duración máxima de ejecución de los proyectos no está explícitamente definida en la información disponible, pero para proyectos de Investigación Aplicada y Desarrollo Tecnológico de esta envergadura, se infiere un plazo de entre 18 y 24 meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  Clasifica los entregables obligatorios (busca en anexos técnicos):
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos en revistas indexadas.</li>
      <li>Capítulos de libro o libros resultado de investigación.</li>
      <li>Informes técnicos de investigación y desarrollo.</li>
      <li>Tesis de posgrado (Maestría, Doctorado) asociadas a los proyectos.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales o pruebas de concepto validadas de soluciones de IA o tecnologías cuánticas.</li>
      <li>Software o plataformas desarrolladas.</li>
      <li>Patentes, diseños industriales o registros de propiedad intelectual.</li>
      <li>Modelos, algoritmos o frameworks innovadores.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y transferencia de conocimiento a comunidades o sectores productivos.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Manuales de uso o guías de implementación de las soluciones desarrolladas.</li>
      <li>Publicaciones de divulgación para el público general.</li>
      <li>Vínculo con semilleros de investigación y formación de capital humano.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras en laboratorios para el desarrollo de tecnologías cuánticas o IA.</li>
      <li>Adquisición o implementación de equipos especializados (ej. hardware cuántico, servidores de alto rendimiento).</li>
      <li>Creación o fortalecimiento de centros de datos o plataformas computacionales.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  Investiga estándares técnicos específicos. NO digas "No especificado" sin buscar "Anexo Técnico".
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li>Para Inteligencia Artificial: Estándares éticos de IA (ej. Recomendación de la UNESCO sobre la Ética de la IA), ISO/IEC 42001 (Gestión de la IA), FAIR principles para datos (Findable, Accessible, Interoperable, Reusable).</li>
      <li>Para Tecnologías Cuánticas: Estándares emergentes en computación cuántica (ej. Qiskit, Cirq, OpenQASM), protocolos de criptografía cuántica (QKD).</li>
      <li>Estándares de ciberseguridad: ISO 27001 (Sistemas de Gestión de Seguridad de la Información) para la protección de datos y sistemas.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li>Especificaciones de hardware para computación de alto rendimiento (GPUs, TPUs) o acceso a plataformas de computación cuántica (IBM Quantum, Azure Quantum).</li>
      <li>Lenguajes de programación: Python, R, Julia para IA; lenguajes específicos para computación cuántica.</li>
      <li>Frameworks y librerías: TensorFlow, PyTorch, Scikit-learn para IA; Qiskit, Cirq para cuántica.</li>
      <li>Infraestructura de nube: AWS, Google Cloud, Azure para escalabilidad y acceso a recursos.</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li>Política Nacional de Explotación de Datos (CONPES 4144 de 2023) y sus lineamientos para el desarrollo y uso de la IA en Colombia.</li>
      <li>Ley 1581 de 2012 (Protección de Datos Personales en Colombia) y normativas complementarias.</li>
      <li>Regulaciones específicas de los sectores de aplicación (ej. salud, agricultura, energía) que puedan afectar el desarrollo o implementación de las soluciones.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> La convocatoria busca específicamente impulsar proyectos que generen un impacto medible y ayuden a cerrar brechas tecnológicas en los territorios del país. Los proyectos deben contribuir al desarrollo ambiental, social y económico de las regiones, promoviendo la investigación aplicada y el desarrollo de soluciones disruptivas con pertinencia local.</li>
  <li><strong>Enfoque Diferencial:</strong> Se enfatiza la inclusión social y el cierre de brechas, lo que implica considerar la participación y el beneficio de poblaciones diversas, incluyendo niñas, niños, adolescentes, jóvenes y adultos, y potencialmente grupos étnicos, víctimas del conflicto, o mujeres, en la promoción de competencias y el acceso a oportunidades formativas y tecnológicas.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  Detalla el equipo mínimo requerido (Busca en "Condiciones Habilitantes"):
<ul>
  <li><strong>Director/Gerente:</strong> Se infiere que debe ser un profesional con formación de posgrado (Maestría o Doctorado) en áreas afines al proyecto (Ciencias de la Computación, Ingeniería, Física, Matemáticas, etc.) y experiencia demostrable en gestión de proyectos de I+D+i, preferiblemente con al menos 5 años de experiencia relevante.</li>
  <li><strong>Investigadores:</strong> Se requiere la vinculación de investigadores con nivel educativo de Maestría y/o Doctorado en áreas de Inteligencia Artificial, Ciencias Cuánticas, Ingeniería de Sistemas, Electrónica, Física, Matemáticas o disciplinas relacionadas, con experiencia en investigación aplicada y publicaciones científicas.</li>
  <li><strong>Técnicos:</strong> Perfiles de apoyo con formación universitaria o tecnológica en áreas como ingeniería de software, desarrollo de hardware, análisis de datos, o soporte técnico, con experiencia práctica en la implementación de tecnologías de IA o cuánticas. Además, es obligatorio vincular un semillero de investigación conformado por un mínimo de diez (10) estudiantes de pregrado de tercer semestre en adelante.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  Lista tipo checklist de los documentos más críticos para no ser descartado:
<ul>
  <li>Propuesta técnica y económica detallada.</li>
  <li>Certificado de Existencia y Representación Legal de la IES ejecutora y de la Empresa Nacional.</li>
  <li>Cámara de Comercio de la Empresa Nacional y de la Organización Local – Regional.</li>
  <li>Anexo 2 – Carta de Experiencia de la Empresa Nacional y documentos que acrediten la ejecución de al menos tres (3) proyectos en los últimos cinco (5) años.</li>
  <li>Documento que acredite la fecha de constitución del Semillero de Investigación, firmado por el representante legal de la IES.</li>
  <li>Cartas de intención o acuerdos de alianza entre la IES, la Empresa Nacional y la Organización Local – Regional.</li>
  <li>Hoja de vida de los investigadores y del equipo técnico principal, con soportes de formación y experiencia.</li>
  <li>Estados financieros de la IES y la Empresa Nacional.</li>
  <li>Certificaciones de capacidad técnica y financiera, si son requeridas.</li>
  <li>Aval institucional de la IES ejecutora.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> $20.000.000.000,00 (Veinte mil millones de pesos colombianos).</li>
  <li><strong>Tope por Proyecto:</strong> No especificado explícitamente en la información disponible. Se infiere que el monto máximo por proyecto estará sujeto a la complejidad, alcance y justificación presupuestal de cada propuesta, dentro del marco del monto total de la bolsa.</li>
  <li><strong>Contrapartida:</strong> No se especifica un porcentaje exacto de contrapartida. Sin embargo, en convocatorias de Minciencias de esta naturaleza, es común que se exija una contrapartida, tanto en efectivo como en especie, que puede oscilar entre el 10% y el 30% del valor total del proyecto.</li>
  <li><strong>Rubros Financiables:</strong>
    <ul>
      <li>Personal científico, técnico y de apoyo vinculado al proyecto.</li>
      <li>Adquisición o adecuación de equipos, software y licencias especializadas.</li>
      <li>Materiales e insumos para investigación y desarrollo.</li>
      <li>Servicios técnicos y profesionales.</li>
      <li>Salidas de campo y viajes relacionados con la ejecución del proyecto.</li>
      <li>Actividades de apropiación social del conocimiento y divulgación.</li>
      <li>Costos indirectos asociados a la ejecución del proyecto.</li>
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
      <li>Obsolescencia tecnológica rápida en campos como IA y computación cuántica, que podría impactar la relevancia de los resultados.</li>
      <li>Dificultad en la integración o interoperabilidad de las soluciones desarrolladas con infraestructuras existentes en los territorios.</li>
      <li>Fallos inesperados en el desarrollo de algoritmos complejos o en la experimentación con tecnologías cuánticas emergentes.</li>
      <li>Limitaciones en la capacidad computacional o acceso a recursos especializados para el procesamiento de grandes volúmenes de datos o simulaciones cuánticas.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li>Retrasos en la importación o adquisición de equipos y software especializado, afectando los cronogramas del proyecto.</li>
      <li>Rotación de personal altamente calificado o dificultad para encontrar talento con la experiencia específica requerida en IA y cuántica.</li>
      <li>Barreras en la apropiación social del conocimiento o en la transferencia tecnológica a las comunidades o empresas locales.</li>
      <li>Incumplimiento de los requisitos éticos y de privacidad de datos en la implementación de soluciones de IA.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li>Dependencia de la financiación externa y posibles recortes presupuestales que afecten la continuidad del proyecto.</li>
      <li>Sobrecostos inesperados asociados a la adquisición de tecnologías emergentes o a la necesidad de infraestructura especializada.</li>
      <li>Fluctuaciones en el tipo de cambio (dólar) que impacten el costo de componentes importados o licencias de software.</li>
      <li>Dificultad para asegurar la contrapartida exigida por la convocatoria, tanto en efectivo como en especie, por parte de los aliados.</li>
    </ul>
  </li>
</ul>
</div>

