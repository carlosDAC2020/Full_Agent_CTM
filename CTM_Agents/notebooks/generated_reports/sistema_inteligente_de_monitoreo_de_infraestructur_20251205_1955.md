

## 1. Generalidades del Proyecto

**Título:** Sistema Inteligente de Monitoreo de Infraestructura Crítica con IoT y IA
**Convocatoria:** CONVOCATORIA COLOMBIA INTELIGENTE: CIENCIA Y TECNOLOGÍAS CUÁNTICAS E INTELIGENCIA ARTIFICIAL PARA LOS TERRITORIOS | Convocatoria 966
**Entidad/Persona:** COTECMAR
**Línea Temática:** tecnologías cuánticas, Inteligencia Artificial, Investigación Aplicada, Desarrollo Tecnológico, Innovación, CTeI


* **Descripción:** El proyecto busca desarrollar y validar un sistema inteligente de monitoreo en tiempo real basado en Internet de las Cosas (IoT) e Inteligencia Artificial (IA) para la evaluación de la salud estructural y la detección temprana de anomalías en infraestructuras críticas (puentes y carreteras) en territorios remotos de Colombia. Esto con el fin de mejorar la seguridad pública, optimizar el mantenimiento y contribuir al desarrollo regional, abordando la problemática del monitoreo ineficiente o inexistente en zonas remotas, y ofreciendo una solución disruptiva para el análisis predictivo y la detección temprana de anomalías estructurales.
* **Palabras Clave:** Inteligencia Artificial, IoT, Monitoreo de Infraestructura Crítica, Colombia, Territorios Remotos, Seguridad Pública, Mantenimiento Predictivo, Desarrollo Regional

## 2. Resumen Ejecutivo
La infraestructura crítica de Colombia, vital para el desarrollo regional, enfrenta un monitoreo ineficiente en zonas remotas, lo que genera riesgos de seguridad, altos costos de mantenimiento reactivo y frena el progreso. Para superar esta brecha, proponemos el "Sistema Inteligente de Monitoreo de Infraestructura Crítica con IoT y IA". Esta solución disruptiva integrará redes de sensores IoT robustos para la recolección de datos en tiempo real con algoritmos avanzados de Inteligencia Artificial, permitiendo un análisis predictivo y la detección temprana de anomalías estructurales.

Nuestro plan se estructura en objetivos claros: diseñar e implementar una red piloto de 50 sensores IoT, desarrollar un modelo de IA con una precisión superior al 90% para la detección de anomalías, e implementar un panel de control y sistema de alertas en tiempo real. La ejecución se guiará por un robusto Modelo en V de Ingeniería de Sistemas, complementado con metodologías ágiles como CRISP-DM y Agile/Scrum, asegurando la verificación y validación en cada fase del desarrollo.

Los resultados esperados incluyen una red de sensores operativa, un modelo de IA validado y una plataforma de monitoreo funcional. Esto se traducirá en un impacto multifacético: una reducción de al menos el 20% en el tiempo de respuesta de mantenimiento, la prevención de fallas catastróficas, la optimización de inversiones y la generación de conocimiento de frontera. Socialmente, mejorará drásticamente la seguridad pública y contribuirá al cierre de brechas tecnológicas en regiones apartadas.

Este proyecto representa una inversión estratégica esencial para la modernización de la gestión de infraestructura en Colombia, garantizando su resiliencia, seguridad y sostenibilidad para el desarrollo socioeconómico futuro del país.

## 3. Planteamiento del Problema y Justificación
La infraestructura crítica, como puentes y carreteras, constituye el pilar fundamental para la conectividad y el desarrollo socioeconómico de las regiones colombianas, particularmente en sus vastos y a menudo remotos territorios. Sin embargo, la gestión de estas infraestructuras enfrenta un desafío significativo: la detección temprana y eficiente de daños o amenazas. Actualmente, una gran proporción de estas estructuras críticas carece de sistemas de monitoreo continuo, lo que las expone a riesgos de seguridad pública, interrupciones de servicios vitales y a la necesidad de costosas reparaciones de emergencia. Esta situación no solo compromete la seguridad de los usuarios, sino que también limita el desarrollo regional sostenible al obstaculizar el transporte de bienes y personas.

Como la literatura especializada indica (Khan et al., 2025; Najem et al., 2025), el monitoreo de la salud estructural (SHM) ha avanzado significativamente con la convergencia del Internet de las Cosas (IoT) y la Inteligencia Artificial (IA), transformando el monitoreo reactivo a predictivo. Sin embargo, a pesar de estos avances, persisten brechas críticas, especialmente en contextos específicos. La robustez y autonomía de los sistemas IoT en entornos remotos y con recursos limitados, carentes de infraestructura eléctrica o de comunicación estable, sigue siendo un desafío considerable (Bhushan et al., 2025). Además, los modelos de IA, aunque potentes, luchan con la vasta variabilidad operacional y ambiental en los datos de SHM, lo que dificulta su adaptabilidad y generalización a regiones con características geológicas y climáticas únicas como las de Colombia (Wan et al., 2024). Esto subraya una brecha tecnológica significativa: la ausencia de soluciones SHM holísticas, integradas y específicamente diseñadas para operar de manera resiliente y efectiva en los territorios remotos de Colombia, que consideren no solo los aspectos técnicos sino también los socioeconómicos y logísticos.

Este proyecto, "Sistema Inteligente de Monitoreo de Infraestructura Crítica con IoT y IA", emerge como la respuesta directa e innovadora a esta brecha. Al integrar redes de sensores IoT robustos y de bajo consumo energético, diseñados para operar en condiciones remotas, con algoritmos avanzados de Inteligencia Artificial capaces de procesar y analizar datos en tiempo real, el sistema propuesto abordará las limitaciones de los enfoques actuales. La solución se centrará en desarrollar modelos de IA adaptables a la variabilidad contextual de las infraestructuras colombianas y en implementar una arquitectura de comunicación resiliente, asegurando la detección temprana y predictiva de anomalías estructurales donde los métodos tradicionales son inviables o ineficientes.

La implementación de este sistema es crucial y oportuna, ya que representa un paso estratégico hacia la modernización de la gestión de infraestructura en Colombia. Su impacto potencial es multifacético: mejorará drásticamente la seguridad pública al prevenir fallas catastróficas, optimizará los recursos de mantenimiento mediante una gestión proactiva y predictiva, y contribuirá al cierre de brechas tecnológicas en las regiones más apartadas. Este proyecto no solo es una innovación tecnológica, sino una inversión esencial en la resiliencia y el desarrollo sostenible del país, alineándose con las políticas nacionales de infraestructura y ciencia y tecnología para un futuro más seguro y conectado.

## 4. Marco Teórico y Estado del Arte
### 4.1. Introducción al Dominio

El monitoreo de la salud estructural (SHM, por sus siglas en inglés) es un campo multidisciplinario dedicado a la evaluación no destructiva y continua de la integridad, seguridad y rendimiento de infraestructuras críticas como puentes y carreteras. Su objetivo primordial es detectar daños o degradaciones en sus etapas iniciales para prevenir fallas catastróficas y optimizar las estrategias de mantenimiento (Khan et al., 2025; Najem et al., 2025). Tradicionalmente, la inspección de infraestructuras ha dependido de métodos manuales y periódicos, que a menudo son costosos, lentos y propensos a errores humanos, con limitaciones significativas en la detección temprana de anomalías.

La convergencia del Internet de las Cosas (IoT) y la Inteligencia Artificial (IA) ha revolucionado el SHM, ofreciendo soluciones para superar estas limitaciones. Los sistemas IoT integran redes de sensores inalámbricos (WSN) que recopilan datos en tiempo real sobre diversos parámetros estructurales, como vibraciones, deformaciones, temperatura y humedad. Estos datos son transmitidos a plataformas de almacenamiento y procesamiento, a menudo basadas en la nube o en el borde de la red (edge computing) (Bhushan et al., 2025; Khan et al., 2025). La IA, por su parte, aporta capacidades analíticas avanzadas, permitiendo el procesamiento inteligente de grandes volúmenes de datos para la identificación de patrones, la detección de anomalías y la predicción de fallas, transformando el monitoreo de reactivo a predictivo (Plevris & Papazafeiropoulos, 2024).

### 4.2. Revisión de la Literatura (Literature Review)

La literatura reciente destaca la creciente sinergia entre IoT y IA en el monitoreo de infraestructuras. Khan et al. (2025) realizaron una revisión crítica del SHM basado en IoT para presas, subrayando cómo la combinación de IoT, IA y dispositivos sensores inalámbricos ha transformado el campo. Su estudio enfatiza la capacidad de estas tecnologías para monitorear el comportamiento estructural en tiempo real, utilizando técnicas de aprendizaje automático para analizar datos y predecir problemas potenciales, lo que es crucial para la implementación de medidas de seguridad.

En la misma línea, Najem et al. (2025) exploraron la simbiosis entre sensores embebidos y no embebidos en redes IoT para el SHM de estructuras de hormigón. Destacan la necesidad de soluciones de monitoreo remoto y continuo frente al envejecimiento natural de las construcciones civiles y cómo la infusión de IoT y IA permite una evaluación no intrusiva. Su trabajo resalta la efectividad de SHM en escenarios del mundo real y las ventajas económicas asociadas a su aplicación, aunque también señala los desafíos en la detección automática de daños.

Hossain (2022) investigó el despliegue de sistemas SHM apoyados por IA para puentes en servicio utilizando redes de sensores IoT. Este estudio aborda las limitaciones de las inspecciones tradicionales y los sistemas SHM cableados, como la interpretación manual de datos y la latencia en la detección de daños. La integración de IA en estas redes de sensores IoT representa un avance significativo para mejorar la seguridad y durabilidad de la infraestructura, especialmente en estructuras críticas como puentes.

Plevris y Papazafeiropoulos (2024) ofrecieron una revisión exhaustiva sobre la influencia de la inteligencia artificial en el SHM, identificando siete áreas clave donde la IA avanza significativamente las capacidades de monitoreo. Estas incluyen la adquisición de datos y redes de sensores, el procesamiento de datos y análisis de señales, la detección de anomalías y la identificación de daños mediante aprendizaje automático y profundo, el mantenimiento predictivo, la evaluación de riesgos, la inspección visual remota y la creación de infraestructuras resilientes. Su trabajo es fundamental para comprender el amplio espectro de aplicaciones de la IA en SHM.

En cuanto a la detección de anomalías, Wan et al. (2024) propusieron un enfoque de aprendizaje profundo no supervisado para la detección de anomalías estructurales utilizando características probabilísticas, basado en un autoencoder variacional convolucional profundo (DCVAE) acoplado con la descripción de datos de la máquina de vectores de soporte (SVDD). Este método aborda los desafíos de la variabilidad operacional y ambiental en los datos de SHM y la correlación entre sensores, demostrando una alta precisión en la detección de anomalías, lo que es vital para la alerta temprana.

Finalmente, Bhushan et al. (2025) se enfocaron en el monitoreo en tiempo real de la salud estructural con redes de sensores inalámbricos en la infraestructura IoT. Destacan que las WSNs son ahora una realidad en IoT para SHM, permitiendo la recolección y análisis de datos de supervivencia en tiempo real. Subrayan las ventajas de las WSNs sobre los métodos tradicionales, como las actualizaciones en tiempo real, el bajo costo de implementación y la mínima interferencia con la estructura de grandes construcciones.

### 4.3. Tecnologías y Enfoques Actuales (State of the Art)

El estado del arte en el monitoreo inteligente de infraestructura crítica se caracteriza por la integración profunda de **redes de sensores IoT** y **algoritmos avanzados de Inteligencia Artificial**. Las redes de sensores inalámbricos (WSN) son el pilar de la recolección de datos, implementando una variedad de sensores (acelerómetros, galgas extensométricas, sensores de temperatura y humedad, entre otros) para capturar parámetros estructurales en tiempo real (Najem et al., 2025; Bhushan et al., 2025). Estos sensores pueden ser embebidos o no, y su despliegue flexible permite cubrir grandes infraestructuras.

La **Inteligencia Artificial y el Aprendizaje Automático (ML/DL)** son fundamentales para el análisis de los datos masivos generados por los sistemas IoT. Técnicas como el aprendizaje profundo (Deep Learning) son ampliamente utilizadas para la extracción de características, reducción de ruido, detección de anomalías y diagnóstico preciso de daños (Plevris & Papazafeiropoulos, 2024; Wan et al., 2024). Los modelos de ML permiten identificar patrones complejos que indican el inicio de una degradación estructural o la presencia de anomalías, superando las capacidades de los análisis manuales. El mantenimiento predictivo, impulsado por la IA, se ha convertido en un enfoque dominante, optimizando la programación de las intervenciones y previniendo fallas antes de que ocurran (AFLGlobal, s.f.).

Para el procesamiento y la transmisión de datos, las soluciones actuales combinan la **computación en la nube (cloud computing)** con la **computación en el borde (edge computing)**. Si bien la nube ofrece escalabilidad y potencia de procesamiento, la computación en el borde es crucial para escenarios remotos y de baja latencia (Synaptics, s.f.; IBM, s.f.). Permite el procesamiento inicial de datos cerca de la fuente (los sensores), reduciendo la cantidad de datos que necesitan ser enviados a la nube, minimizando la latencia y mejorando la seguridad y eficiencia energética, aspectos vitales para el monitoreo en tiempo real en ubicaciones con conectividad limitada (Three.com, s.f.; Digi International, s.f.).

Además, el uso de **drones y sistemas de imágenes** potenciados por IA para la inspección visual remota está ganando terreno, complementando los datos de los sensores y ofreciendo una visión integral del estado estructural (Plevris & Papazafeiropoulos, 2024). La tendencia general es hacia sistemas cada vez más autónomos, capaces de aprender de los datos y adaptarse a las condiciones cambiantes de la infraestructura y el entorno.

### 4.4. Brechas de Conocimiento y Oportunidades (Knowledge Gaps & Opportunities)

A pesar de los avances significativos en el SHM basado en IoT y IA, persisten varias brechas de conocimiento y desafíos, especialmente en contextos específicos como los territorios remotos de Colombia. Una limitación clave es la **robustez y autonomía de los sistemas IoT en entornos remotos y con recursos limitados**. Si bien las WSNs ofrecen bajo costo y facilidad de implementación, su operación continua y segura en áreas sin infraestructura eléctrica o de comunicación estable, y con condiciones ambientales adversas, sigue siendo un desafío considerable. La dependencia de la alimentación por batería y la conectividad intermitente requieren soluciones innovadoras de gestión energética y comunicación resiliente.

Otra brecha radica en la **adaptabilidad de los modelos de IA a la variabilidad contextual**. Los modelos de aprendizaje automático, aunque potentes para la detección de anomalías, a menudo luchan con la vasta variabilidad operacional y ambiental que puede corromper los datos de SHM (Wan et al., 2024). La generalización de modelos entrenados en un entorno a otro, especialmente en regiones con características geológicas y climáticas únicas como Colombia, es un área que necesita más investigación. Además, la interpretación de los resultados de los modelos de IA para la toma de decisiones críticas por parte de los ingenieros sigue siendo un área de mejora, buscando una mayor transparencia y explicabilidad (XAI).

Finalmente, existe una oportunidad significativa para desarrollar **soluciones holísticas e integradas que aborden las necesidades específicas de las infraestructuras críticas en territorios remotos**. Los sistemas actuales suelen enfocarse en aspectos técnicos, pero la integración de factores socioeconómicos y logísticos en el diseño y despliegue de SHM es crucial para su éxito en regiones en desarrollo. Esto incluye no solo la tecnología de sensores y IA, sino también la infraestructura de comunicación, las estrategias de despliegue y mantenimiento, y la capacitación del personal local para asegurar la sostenibilidad del sistema. El proyecto propuesto busca precisamente cerrar estas brechas al desarrollar un sistema inteligente que no solo detecte anomalías, sino que esté diseñado específicamente para las condiciones y necesidades de los territorios remotos de Colombia, contribuyendo a la seguridad pública y al desarrollo regional.

## 5. Objetivos
**Objetivo General**

Desarrollar y validar un sistema inteligente de monitoreo en tiempo real basado en Internet de las Cosas (IoT) e Inteligencia Artificial (IA) para la evaluación de la salud estructural y la detección temprana de anomalías en infraestructuras críticas (puentes y carreteras) en territorios remotos de Colombia, con el fin de mejorar la seguridad pública, optimizar el mantenimiento y contribuir al desarrollo regional.

**Objetivos Específicos**

1.  **Objetivo:** Diseñar e Implementar la Red Piloto de Sensores IoT.
    *   **Específico (S):** Diseñar la arquitectura, seleccionar los componentes y desplegar una red piloto de 50 sensores IoT multisensor (ej. vibración, inclinación, temperatura, deformación) en un tramo de infraestructura crítica seleccionado (ej. un puente estratégico y 2 km de carretera adyacente) en una región específica de Colombia.
    *   **Medible (M):** Red de 50 sensores multisensor instalados y operativos, con un mínimo del 95% de disponibilidad de datos.
    *   **Alcanzable (A):** Sí, con un equipo técnico adecuado y una planificación logística robusta.
    *   **Relevante (R):** Es la base para la recolección de datos del sistema, fundamental para la detección de anomalías y la mejora de la seguridad.
    *   **Plazo (T):** En los primeros 9 meses de ejecución del proyecto.

2.  **Objetivo:** Desarrollar y Validar el Modelo de IA para Detección de Anomalías.
    *   **Específico (S):** Desarrollar un modelo de Inteligencia Artificial (ej. redes neuronales recurrentes o transformadores) capaz de procesar y analizar los datos en tiempo real de los sensores IoT para identificar patrones de deterioro, anomalías estructurales (ej. fatiga de materiales, subsidencia del terreno) y eventos críticos.
    *   **Medible (M):** El modelo de IA alcanzará una precisión mínima del 90% en la detección de anomalías estructurales y una tasa de falsos positivos inferior al 5% en un conjunto de datos validado.
    *   **Alcanzable (A):** Sí, con la disponibilidad de datos de entrenamiento y expertos en IA.
    *   **Relevante (R):** Es el componente central para la inteligencia del sistema, permitiendo la detección temprana y predictiva para una gestión proactiva de la infraestructura.
    *   **Plazo (T):** En los primeros 15 meses de ejecución del proyecto.

3.  **Objetivo:** Implementar un Panel de Control y Sistema de Alertas en Tiempo Real.
    *   **Específico (S):** Desarrollar e implementar una plataforma de software (panel de control) intuitiva y un sistema de alertas automatizado, que permita la visualización en tiempo real de los datos de los sensores y las predicciones del modelo de IA, accesible para los equipos de mantenimiento y gestión de infraestructura.
    *   **Medible (M):** Plataforma desplegada y funcional, con un mínimo de 3 perfiles de usuario definidos y un tiempo de notificación de alertas inferior a 5 minutos desde la detección de una anomalía. Se realizará una prueba de aceptación de usuario con el 80% de satisfacción.
    *   **Alcanzable (A):** Sí, con ingenieros de software y UX/UI.
    *   **Relevante (R):** Proporciona la interfaz necesaria para que los usuarios interactúen con el sistema, facilitando la toma de decisiones y la optimización del mantenimiento.
    *   **Plazo (T):** En los primeros 12 meses de ejecución del proyecto.

4.  **Objetivo:** Evaluar el Impacto en la Eficiencia del Mantenimiento.
    *   **Específico (S):** Cuantificar la mejora en la eficiencia operativa de los equipos de mantenimiento de infraestructura en el área piloto, mediante la reducción del tiempo de respuesta ante incidentes detectados por el sistema.
    *   **Medible (M):** Reducir en al menos un 20% el tiempo de respuesta promedio ante incidentes de mantenimiento detectados por el sistema, comparado con el tiempo de respuesta promedio histórico (línea base a definir), durante los primeros 6 meses de operación del sistema piloto.
    *   **Alcanzable (A):** Sí, con colaboración de entidades operadoras.
    *   **Relevante (R):** Demuestra el valor práctico y económico del sistema, contribuyendo directamente a la optimización de recursos y la sostenibilidad de la infraestructura.
    *   **Plazo (T):** Durante los meses 13 a 18 de ejecución del proyecto.

5.  **Objetivo:** Generar un Informe de Viabilidad y Plan de Expansión.
    *   **Específico (S):** Realizar un análisis de viabilidad técnica, económica y operativa, y generar un informe detallado que sirva como hoja de ruta para la expansión del sistema a otras infraestructuras críticas y regiones de Colombia.
    *   **Medible (M):** Informe de viabilidad completo, que incluya un modelo de costos, un cronograma de expansión propuesto y un análisis de retorno de inversión.
    *   **Alcanzable (A):** Sí, basado en los resultados del piloto.
    *   **Relevante (R):** Garantiza la sostenibilidad y escalabilidad a largo plazo del sistema, asegurando su impacto continuo en el desarrollo regional.
    *   **Plazo (T):** En el mes 18 de ejecución del proyecto.

## 6. Metodología Propuesta
**Framework Seleccionado:** Modelo en V de Ingeniería de Sistemas

El Modelo en V se selecciona como la metodología principal debido a su robustez inherente para proyectos que implican la integración crítica de hardware (redes de sensores IoT) y software (modelos de IA y plataforma de monitoreo), donde la verificación y validación en cada etapa son fundamentales para garantizar la fiabilidad y seguridad de la infraestructura. Este enfoque estructurado permite una trazabilidad clara de los requisitos a lo largo de todo el ciclo de vida del proyecto, desde el diseño conceptual hasta la validación en campo, asegurando que cada componente cumpla con las especificaciones técnicas y operativas necesarias para alcanzar los objetivos del proyecto, incluyendo la precisión del modelo de IA (Objetivo 2) y la funcionalidad del sistema piloto (Objetivo 1, 3 y 4).

**Fases Principales de la Metodología:**

*   **Fase 1: Análisis de Requisitos y Diseño Conceptual** - Definición detallada de los requisitos del sistema para los componentes IoT, IA y la plataforma, estableciendo la arquitectura global del sistema y los criterios de aceptación.
*   **Fase 2: Diseño Detallado de Componentes** - Elaboración de los diseños técnicos específicos para la red de sensores IoT, la arquitectura del modelo de IA, la base de datos y la interfaz de usuario del panel de control, incluyendo la selección de tecnologías y protocolos.
*   **Fase 3: Desarrollo y Prototipado de Componentes** - Implementación física de los prototipos de sensores IoT, desarrollo y entrenamiento inicial del modelo de IA utilizando un enfoque iterativo como CRISP-DM, y codificación del software para el panel de control y el sistema de alertas (empleando principios Agile/Scrum).
*   **Fase 4: Integración y Pruebas de Componentes** - Realización de pruebas unitarias exhaustivas para cada componente y pruebas de integración para asegurar la interoperabilidad y comunicación efectiva entre la red IoT, el modelo de IA y la plataforma de monitoreo.
*   **Fase 5: Validación del Sistema Piloto** - Despliegue y calibración del sistema integrado en el entorno de infraestructura crítica seleccionado, seguido de pruebas de sistema y validación en campo para verificar el rendimiento, la precisión del modelo de IA y el cumplimiento de los objetivos operativos.
*   **Fase 6: Operación Piloto, Evaluación y Cierre** - Monitoreo continuo del sistema en operación real, recopilación de datos para la evaluación del impacto en la eficiencia del mantenimiento (Objetivo 4) y generación del informe de viabilidad y plan de expansión (Objetivo 5), marcando el cierre técnico del proyecto.

## 7. Plan de Ejecución y Gestión
**Cronograma de Actividades**

### 7.1. Cronograma de Actividades

| Fase | Actividad / Hito Clave | Entregable Principal | Duración Estimada (Semanas) |
| :--- | :--- | :--- | :--- |
| **Fase 1: Análisis de Requisitos y Diseño Conceptual** | *Establecimiento de las bases conceptuales y técnicas para todo el sistema, definiendo el alcance y las especificaciones.* | | **8** |
| | 1.1. Levantamiento detallado de requisitos funcionales y no funcionales (IoT, IA, plataforma). | Documento de Requisitos del Sistema (DRS) | 4 |
| | 1.2. Diseño de la arquitectura global del sistema y selección de tecnologías clave. | Documento de Arquitectura del Sistema (DAS) y Especificaciones Tecnológicas | 4 |
| **Fase 2: Diseño Detallado y Prototipado de Hardware IoT** | *Desarrollo detallado y fabricación de los prototipos de la red de sensores IoT para su despliegue inicial.* | | **20** |
| | 2.1. Diseño detallado de hardware y firmware de los 50 sensores IoT multisensor. | Planos de Diseño y Firmware de Sensores IoT | 8 |
| | 2.2. Adquisición de componentes y fabricación/ensamblaje de los 50 prototipos de sensores IoT. | 50 Prototipos de Sensores IoT Ensamblados | 12 |
| **Fase 3: Desarrollo de Software (IA y Plataforma)** | *Diseño, desarrollo y entrenamiento del modelo de IA y la plataforma de monitoreo en tiempo real.* | | **40** |
| | 3.1. Diseño detallado del modelo de IA (arquitectura, algoritmos, estrategia de entrenamiento). | Especificaciones de Diseño del Modelo de IA | 8 |
| | 3.2. Desarrollo del software del panel de control y sistema de alertas (funcionalidades principales). | Plataforma de Monitoreo y Alertas v1.0 (funcionalidades principales) | 20 |
| | 3.3. Recolección de datos iniciales, preprocesamiento y entrenamiento iterativo del modelo de IA. | Modelo de IA v1.0 (entrenado y validado internamente) | 12 |
| **Fase 4: Despliegue, Integración y Validación del Piloto** | *Instalación de la red IoT en campo, integración de todos los componentes y validación del sistema en el entorno piloto.* | | **32** |
| | 4.1. Calibración y pruebas de laboratorio de los 50 sensores IoT. | Informe de Calibración y Pruebas de Laboratorio IoT | 4 |
| | 4.2. Despliegue en campo de la red piloto de 50 sensores IoT. | Red Piloto de Sensores IoT Instalada y Operativa (Objetivo 1 Cumplido) | 4 |
| | 4.3. Integración de la red IoT con la plataforma de monitoreo y el modelo de IA. | Sistema Integrado (IoT-Plataforma-IA) para Pruebas | 8 |
| | 4.4. Pruebas de sistema y Prueba de Aceptación de Usuario (UAT) de la plataforma de monitoreo. | Informe de UAT de la Plataforma (Objetivo 3 Cumplido) | 4 |
| | 4.5. Validación de la precisión del modelo de IA con datos reales del piloto. | Informe de Validación del Sistema y Precisión del Modelo de IA (Objetivo 2 Cumplido) | 12 |
| **Fase 5: Operación Piloto, Evaluación y Cierre** | *Operación continua del sistema piloto, evaluación del impacto en la eficiencia y planificación de la expansión a futuro.* | | **24** |
| | 5.1. Operación continua del sistema piloto y monitoreo de datos para evaluación de impacto. | Registros de Operación del Sistema Piloto y Datos de Mantenimiento | 12 |
| | 5.2. Evaluación del impacto en la eficiencia del mantenimiento (reducción de tiempo de respuesta). | Informe de Evaluación de Impacto en Eficiencia de Mantenimiento (Objetivo 4 Cumplido) | 6 |
| | 5.3. Análisis de viabilidad técnica, económica y operativa; desarrollo del plan de expansión. | Informe de Viabilidad y Plan de Expansión (Objetivo 5 Cumplido) | 4 |
| | 5.4. Publicación de resultados científicos, divulgación y cierre administrativo del proyecto. | Artículos Científicos y Acta de Cierre del Proyecto | 2 |

**Matriz de Riesgos**

### 7.2. Matriz de Riesgos

| # | Riesgo Potencial | Probabilidad | Impacto | Estrategia de Mitigación |
| :-: | :--- | :---: | :---: | :--- |
| 1 | **Calidad y Heterogeneidad de Datos para IA**<br>*Relacionado con: Fase 3.3 (Recolección y entrenamiento IA), Fase 4.5 (Validación IA)* | Alta | Alto | Implementar un plan de recolección de datos riguroso con protocolos de etiquetado por expertos en ingeniería civil. Utilizar técnicas de aumento de datos y explorar modelos de IA robustos a ruido. Realizar validaciones cruzadas exhaustivas con datos reales del piloto y establecer un proceso de curación de datos continuo. |
| 2 | **Desafíos Logísticos y de Seguridad en el Despliegue de Sensores IoT en Entornos Remotos**<br>*Relacionado con: Fase 2.2 (Fabricación y ensamblaje), Fase 4.2 (Despliegue en campo), Fase 5.1 (Operación piloto)* | Alta | Medio | Establecer alianzas estratégicas con autoridades locales y comunidades para apoyo logístico y de seguridad. Diseñar sensores robustos y modulares para facilitar su instalación y mantenimiento. Realizar estudios de sitio detallados previos al despliegue y capacitar al personal de campo en protocolos de seguridad y operación en entornos difíciles. |
| 3 | **Problemas de Integración y Escalabilidad entre Componentes del Sistema**<br>*Relacionado con: Fase 1.2 (Diseño de arquitectura), Fase 3.2 (Desarrollo plataforma), Fase 4.3 (Integración IoT-Plataforma-IA)* | Media | Alto | Adoptar una arquitectura de microservicios con APIs bien definidas desde la fase de diseño. Utilizar estándares abiertos de comunicación (ej. MQTT, LoRaWAN). Realizar pruebas de integración continuas y exhaustivas desde las primeras fases del desarrollo. Planificar la infraestructura de cómputo para soportar la expansión futura del sistema. |
| 4 | **Retrasos en la Adquisición de Componentes Críticos y Fabricación de Sensores IoT**<br>*Relacionado con: Fase 2.2 (Adquisición de componentes y fabricación)* | Media | Medio | Identificar y calificar múltiples proveedores para componentes críticos. Realizar pedidos con antelación suficiente, considerando los plazos de entrega del mercado. Mantener un stock mínimo de seguridad de componentes esenciales. Investigar y validar componentes alternativos en la fase de diseño para tener opciones de respaldo. |
| 5 | **Baja Eficiencia o Precisión del Modelo de IA en Condiciones Reales de Operación**<br>*Relacionado con: Fase 3.3 (Entrenamiento IA), Fase 4.5 (Validación IA), Fase 5.1 (Operación piloto)* | Media | Alto | Realizar entrenamiento del modelo de IA con una amplia variedad de escenarios de datos, incluyendo anomalías simuladas y datos históricos. Implementar mecanismos de reentrenamiento continuo del modelo con datos operativos reales. Incorporar técnicas de aprendizaje adaptativo. Establecer métricas de rendimiento claras y umbrales de alerta ajustables. |


## 8. Resultados e Impactos Esperados
### 8.1. Resultados Esperados (Entregables)
*   **Red Piloto de Sensores IoT Operativa:** Despliegue y validación de una red de 50 sensores multisensor en una infraestructura crítica seleccionada, garantizando un mínimo del 95% de disponibilidad de datos (Objetivo Específico 1).
*   **Modelo de IA Validado para Detección de Anomalías:** Desarrollo de un modelo de Inteligencia Artificial con una precisión mínima del 90% en la detección de anomalías estructurales y una tasa de falsos positivos inferior al 5% (Objetivo Específico 2).
*   **Plataforma de Monitoreo y Alertas en Tiempo Real:** Implementación de una plataforma de software intuitiva con panel de control y sistema de alertas automatizado, con un tiempo de notificación inferior a 5 minutos (Objetivo Específico 3).
*   **Informe de Evaluación de la Eficiencia Operativa:** Documento que cuantifica la reducción de al menos un 20% en el tiempo de respuesta promedio ante incidentes de mantenimiento en el área piloto (Objetivo Específico 4).
*   **Informe de Viabilidad y Plan de Expansión:** Análisis técnico, económico y operativo detallado, incluyendo un modelo de costos y un cronograma de expansión propuesto para la escalabilidad del sistema (Objetivo Específico 5).
*   **Producción Científica y Académica:** Generación de artículos científicos (Q1/Q2), tesis de maestría/doctorado, y informes técnicos especializados en IA e IoT para monitoreo estructural.
*   **Activos de Propiedad Intelectual:** Potencial de solicitud de patentes sobre diseños de sensores o algoritmos innovadores, y registro de derechos de autor sobre el software desarrollado.

### 8.2. Impactos Esperados
*   **Impacto Técnico/Científico:**
    El proyecto generará conocimiento de frontera en la aplicación de Inteligencia Artificial e Internet de las Cosas para el monitoreo de infraestructura civil, resultando en publicaciones científicas de alto impacto y la formación de talento humano especializado. Se avanzará significativamente el Nivel de Madurez Tecnológica (TRL) de la solución, pasando de una prueba de concepto a un sistema validado en un entorno real. Asimismo, se fortalecerán las capacidades de investigación aplicada en Colombia mediante la adecuación de laboratorios y la adquisición de equipos de vanguardia, posicionando al país como referente en estas tecnologías.

*   **Impacto Económico:**
    Se logrará una reducción significativa de los costos operativos y de mantenimiento de la infraestructura crítica al pasar de un modelo reactivo a uno predictivo, optimizando la asignación de recursos y prolongando la vida útil de las estructuras. La prevención de fallas catastróficas evitará pérdidas económicas sustanciales por interrupciones viales y daños materiales. Además, el proyecto impulsará la creación de nuevas oportunidades de negocio y servicios tecnológicos especializados en el monitoreo inteligente, contribuyendo a la competitividad de las regiones y generando valor agregado para la economía nacional.

*   **Impacto Social/Ambiental:**
    La mejora en la seguridad de las infraestructuras críticas tendrá un impacto directo en la salvaguarda de vidas y la integridad de los ciudadanos, reduciendo drásticamente los riesgos de accidentes y colapsos. Se contribuirá al cierre de brechas tecnológicas en territorios remotos de Colombia, facilitando el acceso a soluciones avanzadas y fomentando el desarrollo regional sostenible, que incluye el desarrollo ambiental. El proyecto fortalecerá el talento humano a través de la formación de especialistas en IA e IoT, y promoverá la apropiación social del conocimiento mediante talleres y capacitaciones dirigidos a comunidades y entidades locales, asegurando que las poblaciones vulnerables también se beneficien de una infraestructura más resiliente y segura.

## 9. Referencias Bibliográficas
*   AFLGlobal. (s.f.). *Predictive Infrastructure Monitoring | AI-Powered Asset Management*. Recuperado de https://www.aflglobal.com/en/Solutions/Accelerator/Intelligent-Infrastructure-Monitoring
*   Al-Shareeda, M. A., Najm, L. B., Hassan, A. A., Mushtaq, S., & Ali, H. A. (2024). Secure IoT-Based Smart Agriculture System Using Wireless Sensor Networks for Remote Environmental Monitoring. *International Journal of Wireless Information Networks*.
*   Bhushan, B., Pushparajesh, V., Janney, J. B., Sahoo, G. S., Aggarwal, P., & Das, D. (2025). Real-Time Monitoring of Structural Health with Wireless Sensor Networks in IoT Infrastructure. *Journal of Applied Science and Engineering*.
*   Digi International. (s.f.). *Edge Computing Solutions | IoT Enabled Devices*. Recuperado de https://www.digi.com/solutions/by-technology/edge-computing
*   Hossain, M. I. (2022). *DEPLOYMENT OF AI-SUPPORTED STRUCTURAL HEALTH MONITORING SYSTEMS FOR IN-SERVICE BRIDGES USING IOT SENSOR NETWORKS* [Tesis de doctorado, University of Nebraska-Lincoln].
*   IBM. (s.f.). *Edge Computing for IoT*. Recuperado de https://www.ibm.com/think/topics/iot-edge-computing
*   Khan, A., Mishra, S., Pandey, S., Sardar, T., Mishra, A., Mudgal, M., & Singhai, S. (2025). A Critical Review of IoT-Based Structural Health Monitoring for Dams. *Journal of Applied Science and Engineering*.
*   Najem, O., Benbrahim, M., Kabbaj, M., & Boumhidi, J. (2025). Synergy between Embedded and Non-Embedded Sensors in IoT Networks for Structural Health Monitoring of Concrete Structures: A Literature Review. *Journal of Applied Science and Engineering*.
*   Plevris, V., & Papazafeiropoulos, G. (2024). AI in Structural Health Monitoring for Infrastructure Maintenance and Safety. *Artificial Intelligence Review*.
*   Synaptics. (s.f.). *Edge Computing in IoT Devices: Everything You Need to Know*. Recuperado de https://www.synaptics.com/company/blog/iot-edge-computing-ml
*   Three.com. (s.f.). *IoT remote monitoring: benefits, use cases & how to scale*. Recuperado de https://groupsolutions.three.com/insights/iot-remote-monitoring
*   Wan, H. P., Zhu, Y. K., Luo, Y., & Todd, M. D. (2024). Unsupervised deep learning approach for structural anomaly detection using probabilistic features. *Engineering Structures, 301*, 117215.
