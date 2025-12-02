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
  <li><strong>Resumen:</strong> La convocatoria "Colombia Inteligente" busca fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación en tecnologías cuánticas e Inteligencia Artificial. Su propósito es generar un impacto medible que contribuya al desarrollo ambiental, social y económico de las regiones colombianas, en línea con la Política de Investigación e Innovación Orientada por Misiones. Prioriza la transferencia tecnológica, el desarrollo de talento especializado y la reducción de brechas tecnológicas en el país.</li>
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
  <li><strong>Ejecutor:</strong> Las propuestas deberán ser presentadas por una Institución de Educación Superior (IES) que actuará como entidad ejecutora principal.</li>
  <li><strong>Alianzas Obligatorias:</strong> Se exige una alianza estratégica conformada por la Institución de Educación Superior (IES) ejecutora, una Empresa Nacional y al menos una (1) Organización Local – Regional.</li>
  <li><strong>Inhabilidades:</strong> Aunque no se detallan explícitamente en la información inicial, por inferencia en convocatorias similares, se considerarían inhábiles: <br><ul><li>Entidades que no cumplan con la conformación de la alianza estratégica obligatoria (IES, Empresa Nacional y Organización Local-Regional).</li><li>Entidades o personas naturales que presenten conflictos de interés con los evaluadores o el comité de la convocatoria.</li></ul></li>
</ul>
  </div>
</div>


---
<!-- header: '4. DEMANDAS TERRITORIALES' -->
<h2>🗺️ Focalización</h2>
<div class="col-2">
  <p>La convocatoria tiene una focalización geográfica amplia, buscando un impacto a nivel nacional, específicamente en los territorios del país. Su objetivo es cerrar brechas tecnológicas y contribuir al desarrollo ambiental, social y económico de las regiones. No se especifican departamentos, ciudades o zonas PDET particulares, lo que sugiere una aplicabilidad generalizada a nivel regional.</p>
<ul>
  <li>No se especifican lugares geográficos concretos, el alcance es nacional con énfasis en el desarrollo regional.</li>
</ul>
</div>


---
<!-- header: '5. LÍNEAS TEMÁTICAS' -->
<h2>📚 Áreas de Investigación</h2>
<!-- Usamos columnas para que quepan las 5 líneas -->
<div class="col-2" style="font-size: 0.9em;">
  <p>La convocatoria establece dos ejes estratégicos principales, permitiendo la integración de elementos complementarios del otro eje si se justifica su impacto, viabilidad y madurez tecnológica:</p>
<ul>
  <li><strong>Eje Temático Inteligencia Artificial:</strong> Responde a lo establecido en el CONPES 4144, promoviendo el desarrollo y la adopción ética y sostenible de soluciones basadas en IA en sectores estratégicos.
    <ul>
      <li><strong>Gestión de la Biodiversidad y Bioeconomía:</strong> Desarrollo y aplicaciones de IA para clasificación de especies, monitoreo de ecosistemas y fomento de innovación colaborativa con conocimientos locales para transformar recursos biológicos en bienes o servicios de alto valor agregado.</li>
      <li><strong>Sistemas Agroalimentarios Inteligentes:</strong> Desarrollo y aplicaciones de IA en agricultura de precisión, agroindustria, gestión de recursos hídricos y trazabilidad de productos, orientado a la soberanía alimentaria.</li>
      <li><strong>Energías Renovables y Transición Energética:</strong> Desarrollo y aplicaciones de IA para el pronóstico, control y uso sostenible de fuentes limpias (solar, eólica, biomasa), complementada con modelos predictivos para la toma de decisiones en redes energéticas.</li>
      <li><strong>Tecnologías de IA para la Transformación Educativa en los Territorios:</strong> Desarrollo e implementación de tecnologías basadas en IA para apoyar el aprendizaje en áreas como matemáticas y programación, personalización de contenidos y reducción de brechas tecnológicas.</li>
      <li><strong>Gestión de Riesgos y Conservación de Fauna con IA:</strong> Desarrollo y aplicación de tecnologías que integren modelos de IA para la detección temprana de desastres (inundaciones, incendios, deslizamientos) y la protección de especies silvestres en riesgo.</li>
      <li><strong>IA en Diagnóstico Médico y Medicina Personalizada:</strong> Desarrollo y aplicaciones de tecnologías para el análisis de imágenes médicas para mejorar la precisión en el diagnóstico temprano de enfermedades, personalizar tratamientos y optimizar la atención sanitaria.</li>
    </ul>
  </li>
  <li><strong>Eje Temático Ciencia y Tecnologías Cuánticas:</strong> Definido por un grupo de expertos nacionales para identificar y priorizar áreas clave alineadas con capacidades y desafíos estratégicos del país.
    <ul>
      <li><strong>Procesamiento Cuántico de la Información y Comunicaciones Seguras:</strong> Exploración y desarrollo de algoritmos y métodos que utilicen principios cuánticos.
        <ul>
          <li><strong>Algoritmos cuánticos:</strong> Investigación e implementación para resolver problemas en física, química, biología, energía, salud y fármacos.</li>
          <li><strong>Simulación cuántica:</strong> Investigación y aplicación de herramientas y entornos de desarrollo (software y hardware) para simulación cuántica.</li>
          <li><strong>Circuitos integrados cuánticos y fotónicos:</strong> Investigación en arquitectura y diseño, incluyendo una perspectiva hacia la producción nacional.</li>
          <li><strong>Comunicaciones ultra seguras:</strong> Investigación e implementación de protocolos de criptografía cuántica para la protección de datos sensibles.</li>
          <li><strong>Internet cuántico y nodos de red:</strong> Investigación e implementación de redes cuánticas de comunicación con nodos distribuidos, seguros y estandarizados.</li>
        </ul>
      </li>
      <li><strong>Sensórica Cuántica y Metrología:</strong> Diseño y aplicación de tecnologías basadas en principios cuánticos para detección, medición, trazabilidad y caracterización ultra precisa.
        <ul>
          <li><strong>Sensores cuánticos para agricultura:</strong> Desarrollo de dispositivos de medición con alta sensibilidad para variables críticas en agroindustria.</li>
          <li><strong>Sensores cuánticos para salud:</strong> Desarrollo de dispositivos de medición con alta sensibilidad para variables críticas en medicina de precisión y diagnóstico temprano.</li>
          <li><strong>Sensores cuánticos para medioambiente:</strong> Desarrollo de dispositivos de medición con alta sensibilidad para variables críticas en gestión ambiental.</li>
          <li><strong>Tecnologías para el desminado:</strong> Investigación y desarrollo de tecnologías para desminado seguro articulando capacidades sensóricas cuánticas.</li>
          <li><strong>Metrología cuántica:</strong> Implementación de patrones y unidades de medida y su trazabilidad aplicados a insumos médicos, alimentos y materiales estratégicos.</li>
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
  <li><strong>TRL Esperado:</strong> Dado el enfoque en "Investigación Aplicada, Desarrollo Tecnológico y la Innovación", se infiere que los proyectos deben iniciar en niveles de madurez tecnológica intermedios (TRL 3-4, prueba de concepto, validación en laboratorio) y aspirar a alcanzar niveles más altos (TRL 6-7, prototipo a escala o sistema demostrado en entorno relevante), buscando la implementación efectiva y escalabilidad de la tecnología resultante.</li>
  <li><strong>Componentes Obligatorios:</strong> Los proyectos deberán fomentar activamente la transferencia tecnológica, el desarrollo de talento humano especializado en ciencias y tecnologías cuánticas e Inteligencia Artificial, y contribuir a la reducción de brechas tecnológicas en el país. Es mandatorio fortalecer la vinculación entre la academia, la industria y el sector público para impulsar un ecosistema de innovación competitivo.</li>
  <li><strong>Duración:</strong> La duración máxima de los proyectos no se especifica explícitamente en la información disponible. Sin embargo, para proyectos de Investigación Aplicada y Desarrollo Tecnológico de esta envergadura, se infiere una duración típica que podría oscilar entre 12 y 36 meses.</li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '7. PRODUCTOS E INDICADORES' -->
<h2>📦 Entregables Esperados</h2>
<!-- Clase compact reduce la fuente para que quepa todo -->
<div class="col-2">
  <p>Basado en el objetivo de fortalecer la Investigación Aplicada, el Desarrollo Tecnológico y la Innovación, se infieren los siguientes tipos de entregables:</p>
<ul>
  <li><strong>Generación de Conocimiento:</strong>
    <ul>
      <li>Artículos científicos publicados en revistas indexadas.</li>
      <li>Ponencias y presentaciones en congresos nacionales e internacionales.</li>
      <li>Informes técnicos y de investigación detallados.</li>
      <li>Tesis de posgrado (maestría y doctorado) asociadas a los proyectos.</li>
    </ul>
  </li>
  <li><strong>Desarrollo Tecnológico:</strong>
    <ul>
      <li>Prototipos funcionales de hardware o software relacionados con IA o tecnologías cuánticas.</li>
      <li>Desarrollo de nuevas metodologías, algoritmos o modelos computacionales.</li>
      <li>Software especializado o plataformas tecnológicas.</li>
      <li>Solicitudes de patentes, registros de propiedad intelectual o secretos industriales.</li>
      <li>Demostradores de concepto y pruebas de validación tecnológica.</li>
    </ul>
  </li>
  <li><strong>Apropiación Social:</strong>
    <ul>
      <li>Talleres de capacitación y transferencia de conocimiento a comunidades o sectores productivos.</li>
      <li>Eventos de divulgación científica y tecnológica.</li>
      <li>Manuales de usuario o guías técnicas para la implementación de las soluciones desarrolladas.</li>
      <li>Creación de redes de conocimiento o comunidades de práctica.</li>
      <li>Programas de formación para el desarrollo de talento especializado.</li>
    </ul>
  </li>
  <li><strong>Infraestructura:</strong>
    <ul>
      <li>Adecuaciones o mejoras en laboratorios y centros de investigación.</li>
      <li>Adquisición o desarrollo de equipos especializados para investigación en IA o cuántica.</li>
      <li>Implementación de plataformas computacionales o servidores de alto rendimiento.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '8. CONSIDERACIONES TÉCNICAS' -->
<h2>⚙️ Estándares</h2>
<div class="card warning col-2">
  <p>Aunque no se detallan estándares técnicos específicos en la información inicial, la naturaleza de la convocatoria en tecnologías cuánticas e Inteligencia Artificial implica la adopción de buenas prácticas y normativas internacionales.</p>
<ul>
  <li><strong>Estándares:</strong>
    <ul>
      <li><strong>Inteligencia Artificial:</strong> Se infiere la aplicación de principios éticos para el desarrollo de IA (Ej: Recomendación de la UNESCO sobre la Ética de la Inteligencia Artificial), estándares de calidad de datos (ISO/IEC 25012) y, potencialmente, estándares de seguridad de la información (ISO 27001) para el manejo de datos sensibles.</li>
      <li><strong>Tecnologías Cuánticas:</strong> Se esperaría la adherencia a estándares emergentes en computación cuántica, criptografía cuántica y sensórica cuántica, así como las mejores prácticas en el diseño y validación de sistemas cuánticos.</li>
    </ul>
  </li>
  <li><strong>Hardware/Software:</strong>
    <ul>
      <li><strong>Inteligencia Artificial:</strong> Para el desarrollo y despliegue de soluciones de IA, se requeriría el uso de plataformas de computación de alto rendimiento (GPUs, TPUs), frameworks de IA (TensorFlow, PyTorch), y lenguajes de programación como Python, R o Julia.</li>
      <li><strong>Tecnologías Cuánticas:</strong> Para el desarrollo en este campo, se necesitarían plataformas de simulación cuántica, acceso a hardware cuántico (si es aplicable), y herramientas de desarrollo específicas para algoritmos y circuitos cuánticos (Qiskit, Cirq).</li>
    </ul>
  </li>
  <li><strong>Normatividad:</strong>
    <ul>
      <li>La convocatoria se enmarca en lo establecido por el <strong>CONPES 4144</strong> para el eje de Inteligencia Artificial, que orienta el desarrollo, la implementación y la adopción ética y sostenible de soluciones basadas en IA.</li>
      <li>Se deberá cumplir con la normativa colombiana vigente en materia de protección de datos personales (Ley 1581 de 2012) y ciberseguridad, especialmente si los proyectos manejan información sensible.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- header: '9. ENFOQUES TRANSVERSALES' -->
<h2>🤝 Social y Diferencial</h2>
<ul>
  <li><strong>Enfoque Territorial:</strong> Los proyectos deben estar diseñados para generar un impacto medible en el desarrollo ambiental, social y económico de las regiones del país. Se busca activamente que las soluciones contribuyan a cerrar brechas tecnológicas en los territorios, promoviendo la investigación aplicada y el desarrollo de soluciones disruptivas con pertinencia local y potencial de escalabilidad.</li>
  <li><strong>Enfoque Diferencial:</strong> La convocatoria promueve la inclusión social y el cierre de brechas, con un énfasis en la transformación educativa a través de la IA, impulsando la promoción de competencias en niñas, niños, adolescentes, jóvenes y adultos. Esto implica considerar la diversidad de poblaciones y sus necesidades específicas en el diseño e implementación de los proyectos.</li>
</ul>


---
<!-- _class: compact -->
<!-- header: '10. TALENTO HUMANO' -->
<h2>🧑‍🔬 Equipo de Trabajo</h2>
<div class="col-2">
  <p>Aunque la información inicial no detalla explícitamente los perfiles del equipo mínimo requerido, la naturaleza de la convocatoria en CTeI de alto nivel permite inferir los siguientes requisitos típicos para proyectos de esta magnitud:</p>
<ul>
  <li><strong>Director/Gerente:</strong>
    <ul>
      <li><strong>Perfil:</strong> Profesional con experiencia comprobada en gestión de proyectos de investigación, desarrollo tecnológico e innovación (I+D+i), preferiblemente en áreas de IA o tecnologías cuánticas.</li>
      <li><strong>Formación:</strong> Mínimo Maestría, deseable Doctorado en áreas afines a la ciencia, ingeniería o tecnología.</li>
      <li><strong>Años de Experiencia:</strong> Al menos 5 años de experiencia liderando equipos de investigación o proyectos tecnológicos complejos.</li>
    </ul>
  </li>
  <li><strong>Investigadores:</strong>
    <ul>
      <li><strong>Nivel Educativo Requerido:</strong> Se requerirá un equipo de investigadores con formación de alto nivel, incluyendo profesionales con Doctorado (PhD) y Maestría, especializados en las líneas temáticas de la convocatoria (IA, computación cuántica, criptografía cuántica, sensórica cuántica, etc.).</li>
      <li><strong>Experiencia:</strong> Experiencia demostrada en investigación y publicaciones científicas en los campos relevantes.</li>
    </ul>
  </li>
  <li><strong>Técnicos:</strong>
    <ul>
      <li><strong>Perfiles de Apoyo:</strong> Se requerirán profesionales y técnicos de apoyo con experiencia en desarrollo de software, ciencia de datos, ingeniería de hardware, gestión de infraestructuras tecnológicas y otras habilidades técnicas específicas para la implementación de las soluciones propuestas.</li>
      <li><strong>Formación:</strong> Ingenieros, tecnólogos o profesionales con especializaciones técnicas relevantes.</li>
    </ul>
  </li>
</ul>
</div>


---
<!-- _class: compact -->
<!-- header: '11. REQUISITOS DOCUMENTALES' -->
<h2>📄 Checklist</h2>
<div class="col-2">
  <p>Basado en la información de la convocatoria y la experiencia en procesos de Minciencias, los documentos críticos para la habilitación y evaluación de propuestas incluirían:</p>
<ul>
  <li><strong>Documento Jurídico 1:</strong> Certificado de Existencia y Representación Legal de la Institución de Educación Superior (IES) ejecutora y de la Empresa Nacional y la Organización Local – Regional aliadas.</li>
  <li><strong>Documento Financiero 1:</strong> Estados Financieros auditados de las entidades participantes que demuestren solidez financiera para ejecutar el proyecto.</li>
  <li><strong>Certificaciones específicas:</strong> Certificaciones de cumplimiento de buenas prácticas en investigación o gestión de calidad (ej. ISO 9001, si aplica a la gestión del proyecto).</li>
  <li><strong>Avales institucionales:</strong> Cartas de aval o compromiso de las directivas de la IES ejecutora y de las entidades aliadas, garantizando el apoyo institucional al proyecto.</li>
  <li><strong>Cartas de intención:</strong> Acuerdos de colaboración o cartas de intención firmadas entre la IES, la Empresa Nacional y la Organización Local – Regional, detallando roles, responsabilidades y aportes.</li>
  <li><strong>Propuesta Técnica y Económica:</strong> Documento detallado del proyecto, cronograma, presupuesto y plan de trabajo.</li>
  <li><strong>Perfiles y Hojas de Vida:</strong> Documentación que acredite la formación y experiencia del equipo de trabajo.</li>
</ul>
</div>


---
<!-- header: '12. DURACIÓN Y FINANCIACIÓN' -->
<h2>💰 Recursos</h2>
<div class="grid-2">
  <div class="card">
    <ul>
  <li><strong>Monto Total de la Bolsa:</strong> 20.000.000.000,00 COP (Veinte mil millones de pesos colombianos).</li>
  <li><strong>Tope por Proyecto:</strong> No se especifica un tope máximo de financiación por proyecto en la información disponible. Este dato se buscaría en los términos de referencia detallados de la convocatoria.</li>
  <li><strong>Contrapartida:</strong> No se especifica un porcentaje de contrapartida exigido en efectivo y/o especie en la información disponible. Este detalle sería crucial y se encontraría en los términos de referencia completos.</li>
  <li><strong>Rubros Financiables:</strong> Por la naturaleza de la convocatoria de CTeI, se infieren rubros financiables comunes:
    <ul>
      <li>Personal científico, técnico y de apoyo.</li>
      <li>Adquisición y/o adecuación de equipos e infraestructura tecnológica.</li>
      <li>Materiales e insumos para la investigación y desarrollo.</li>
      <li>Gastos de operación, mantenimiento y administración del proyecto.</li>
      <li>Servicios técnicos y profesionales especializados.</li>
      <li>Actividades de divulgación, transferencia tecnológica y apropiación social del conocimiento.</li>
      <li>Movilidad de investigadores.</li>
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
  <p>Dado que no se proporciona una matriz de riesgos explícita, se infieren los siguientes riesgos basados en la naturaleza de proyectos de alta tecnología como la IA y las tecnologías cuánticas:</p>
<ul>
  <li><strong>Riesgo Técnico:</strong>
    <ul>
      <li><strong>Obsolescencia Tecnológica:</strong> Las tecnologías cuánticas y de IA evolucionan rápidamente, lo que puede llevar a que las soluciones propuestas queden desactualizadas antes o durante la ejecución del proyecto.</li>
      <li><strong>Fallos en Integración o Desarrollo:</strong> Dificultades técnicas imprevistas en la integración de componentes complejos o en el desarrollo de algoritmos novedosos, afectando el cumplimiento de los objetivos técnicos.</li>
      <li><strong>Disponibilidad de Datos y Calidad:</strong> La falta de acceso a conjuntos de datos adecuados o la baja calidad de los mismos puede comprometer el entrenamiento y la validación de modelos de IA.</li>
    </ul>
  </li>
  <li><strong>Riesgo Operativo:</strong>
    <ul>
      <li><strong>Retrasos en Importaciones/Adquisiciones:</strong> La dependencia de equipos especializados o componentes de hardware/software de proveedores internacionales puede generar demoras significativas debido a procesos aduaneros o logísticos.</li>
      <li><strong>Rotación de Personal Especializado:</strong> La escasez de talento altamente calificado en IA y tecnologías cuánticas puede llevar a la rotación de personal clave, afectando la continuidad y el avance del proyecto.</li>
      <li><strong>Problemas de Coordinación en la Alianza:</strong> Dificultades en la coordinación y comunicación efectiva entre la IES, la Empresa Nacional y la Organización Local – Regional, afectando la ejecución conjunta.</li>
    </ul>
  </li>
  <li><strong>Riesgo Financiero:</strong>
    <ul>
      <li><strong>Fluctuación del Dólar:</strong> Para proyectos que requieran la importación de equipos o el pago de licencias en moneda extranjera, la devaluación del peso colombiano puede generar sobrecostos no previstos.</li>
      <li><strong>Recortes Presupuestales o Retrasos en Desembolsos:</strong> Posibles ajustes presupuestales por parte de la entidad financiadora o demoras en los desembolsos de los recursos, afectando la liquidez y el cronograma del proyecto.</li>
      <li><strong>Costos Inesperados:</strong> Surgimiento de gastos no contemplados inicialmente debido a la complejidad inherente a la investigación y desarrollo en estas áreas de frontera tecnológica.</li>
    </ul>
  </li>
</ul>
</div>

