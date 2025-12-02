

## 1. Generalidades del Proyecto

**Título:** Sistema Predictivo Inteligente para Optimización Energética en Microrredes de la Amazonía Colombiana
**Convocatoria:** CONVOCATORIA COLOMBIA INTELIGENTE: CIENCIA Y TECNOLOGÍAS CUÁNTICAS E INTELIGENCIA ARTIFICIAL PARA LOS TERRITORIOS | Convocatoria 966
**Entidad/Persona:** COTECMAR
**Línea Temática:** Tecnologías Cuánticas, Inteligencia Artificial, Territorios, Investigación Aplicada, Desarrollo Tecnológico, Innovación


* **Descripción:** Las zonas rurales no interconectadas del país enfrentan desafíos significativos en la gestión eficiente de sus recursos energéticos, lo que genera intermitencia y altos costos. Este proyecto propone desarrollar un sistema inteligente basado en algoritmos de aprendizaje automático para predecir patrones de demanda y optimizar la distribución de energía en microrredes híbridas. Implementaremos una solución piloto en dos comunidades amazónicas, colaborando con operadores locales para su integración. El objetivo es incrementar la estabilidad del suministro energético en un 25% y reducir los gastos operativos en un 15%, mejorando la calidad de vida en la región.
* **Palabras Clave:** Inteligencia Artificial, Optimización Energética, Microrredes, Aprendizaje Automático, Amazonía Colombiana, Desarrollo Territorial

## 2. Resumen Ejecutivo
Las comunidades rurales no interconectadas de la Amazonía colombiana enfrentan desafíos energéticos sistémicos, caracterizados por un suministro inestable y altos costos operativos, lo que perpetúa una significativa brecha tecnológica y limita su desarrollo. Nuestro proyecto propone una solución innovadora: un sistema predictivo inteligente basado en Inteligencia Artificial y Machine Learning, diseñado para optimizar la gestión energética de microrredes híbridas. Esta iniciativa busca transformar la realidad de estas regiones, elevando la calidad de vida y fomentando un desarrollo regional sostenible al abordar directamente estas carencias críticas.

Para lograr esta visión, el proyecto se centrará en el desarrollo de algoritmos de IA adaptativos capaces de predecir la demanda y la generación renovable incluso con datos limitados. Estos algoritmos se integrarán en un Sistema de Gestión Energética (EMS) basado en Control Predictivo por Modelo (MPC), optimizando el despacho de energía en tiempo real. La metodología Ágil (Scrum) guiará un proceso iterativo, asegurando una validación piloto efectiva en al menos dos microrredes amazónicas y fomentando la transferencia de conocimiento a las comunidades locales.

El impacto esperado es transformador: proyectamos un incremento del 25% en la estabilidad del suministro energético y una reducción del 15% en los costos operativos anuales para los operadores. Esto no solo mejorará la calidad de vida y la productividad local, sino que también impulsará la bioeconomía regional, promoverá el uso de energías renovables y contribuirá al cierre de brechas tecnológicas. El proyecto elevará el Nivel de Madurez Tecnológica (TRL) de 5 a 7, generando propiedad intelectual y sentando un precedente metodológico.

Este sistema predictivo inteligente es una inversión estratégica para la Amazonía colombiana, esencial para fortalecer la soberanía energética, la innovación en IA y el desarrollo sostenible de una región de vital importancia para el país.

## 3. Planteamiento del Problema y Justificación
Las zonas rurales no interconectadas de la Amazonía colombiana enfrentan desafíos energéticos sistémicos que obstaculizan su desarrollo y la calidad de vida de sus habitantes. La intermitencia y la falta de confiabilidad en el suministro eléctrico son comunes, lo que restringe el acceso a servicios básicos y limita las actividades productivas. A esto se suman los altos costos operativos de las microrredes existentes, a menudo dependientes de combustibles fósiles y caracterizadas por una gestión ineficiente debido a la ausencia de capacidades predictivas y sistemas inteligentes avanzados. Esta situación perpetúa una significativa brecha tecnológica y de desarrollo territorial en una región de vital importancia estratégica. 

Si bien la literatura científica (Duan et al., 2024; Patty y Malakar, 2025; Arcos-Aviles et al., 2024; Ponce y Mandal, 2024; Nallolla et al., 2023; Li et al., 2022) demuestra avances significativos en la aplicación de la Inteligencia Artificial y el Aprendizaje Automático para la optimización de microrredes en entornos controlados, existe una clara brecha de conocimiento y tecnológica en la adaptación de estas soluciones a contextos únicos y desafiantes como el de la Amazonía. Las investigaciones actuales rara vez abordan la escasez de datos históricos, la necesidad de robustez ante condiciones ambientales extremas, la implementación de soluciones de bajo costo computacional y la integración de factores socioeconómicos y culturales, aspectos críticos para la sostenibilidad en comunidades remotas. Esta limitación en el estado del arte subraya la insuficiencia de las soluciones convencionales para resolver los problemas energéticos específicos de estas regiones. 

Este proyecto surge como la respuesta directa e innovadora a estas brechas identificadas. Proponemos el desarrollo de un sistema predictivo inteligente que, mediante algoritmos avanzados de Inteligencia Artificial y Aprendizaje Automático, está diseñado para operar eficazmente en entornos con datos limitados y bajo condiciones climáticas variables. Al integrar un Sistema de Gestión Energética (EMS) basado en Control Predictivo por Modelo (MPC) con estas capacidades de pronóstico adaptativo, el proyecto abordará directamente la optimización del despacho de energía en microrredes híbridas, trascendiendo las limitaciones de los enfoques existentes y proporcionando una solución tecnológica diseñada específicamente para el contexto amazónico. 

La implementación de este sistema es una necesidad imperativa y oportuna para las zonas no interconectadas de la Amazonía colombiana. Al ofrecer una solución innovadora que incrementará la estabilidad del suministro energético en un 25% y reducirá los costos operativos en un 15%, el proyecto tendrá un impacto directo en la mejora de la calidad de vida, el fomento del desarrollo ambiental, social y económico regional, y el cierre de brechas tecnológicas territoriales. Esto alinea el proyecto con los objetivos de la Convocatoria Minciencias 966, consolidándolo como una iniciativa estratégica para fortalecer la soberanía energética y la innovación en Inteligencia Artificial en Colombia.

## 4. Marco Teórico y Estado del Arte
### 4.1. Introducción al Dominio

La gestión energética eficiente en microrredes es un campo de investigación y desarrollo crítico, especialmente en el contexto de la transición hacia sistemas energéticos más sostenibles y resilientes. Una microrred es un sistema energético localizado que puede operar conectado a la red eléctrica principal o de forma aislada, integrando diversas fuentes de generación, como energía solar fotovoltaica y eólica, sistemas de almacenamiento de energía (baterías microrred es un sistema energético localizado que puede operar conectado a la red eléctrica principal o de forma aislada, integrando diversas fuentes de generación, como energía solar fotovoltaica y eólica, sistemas de almacenamiento de energía (baterías) y cargas controlables. Su capacidad para operar de manera autónoma las convierte en una solución idónea para zonas remotas o no interconectadas, donde la estabilidad y el acceso a la energía son desafíos persistentes.

La optimización energética en microrredes busca maximizar la eficiencia en la generación, distribución y consumo de energía, minimizando los costos operativos, las emisiones y mejorando la confiabilidad del suministro. En este contexto, la Inteligencia Artificial (IA) y el Aprendizaje Automático (AA) han emergido como herramientas fundamentales. Estos enfoques permiten predecir con mayor precisión los patrones de demanda y generación de energía renovable, así como implementar estrategias de control dinámicas y adaptativas que superan las limitaciones de los métodos tradicionales, facilitando una gestión proactiva y robusta de los recursos energéticos.

### 4.2. Revisión de la Literatura (Literature Review)

La literatura reciente demuestra un interés creciente en la aplicación de técnicas avanzadas de IA y AA para la optimización y gestión de microrredes. **Duan et al. (2024)** propusieron un marco difuso multi-objetivo para la optimización de microrredes híbridas (fotovoltaica/eólica/baterías) en redes de distribución. Su estudio empleó una red neuronal artificial de perceptrón multicapa (MLP-ANN) para la predicción de datos de radiación solar, velocidad del viento, temperatura y carga, integrando estos pronósticos en un algoritmo de optimización de Kepler mejorado. Los resultados subrayan la importancia de los datos pronosticados para minimizar pérdidas de energía, desviaciones de voltaje y el costo de la energía comprada.

En línea con la gestión de la incertidumbre, **Patty y Malakar (2025)** investigaron el comportamiento operativo de los sistemas de almacenamiento de energía en baterías (BES) en microrredes bajo diversas incertidumbres de demanda. Utilizaron la regresión de procesos gaussianos (GPR) basada en AA para predecir la producción volátil de fuentes de energía renovable (RES) y la simulación Monte Carlo para estimar la demanda incierta. Su enfoque estocástico de optimización busca minimizar el costo operativo total de la microrred, destacando cómo la precisión de la predicción influye directamente en la eficiencia y los costos.

El Control Predictivo por Modelo (MPC) se ha establecido como una estrategia de control robusta para la gestión energética en microrredes. **Arcos-Aviles et al. (2024)** presentaron un sistema de gestión de energía (EMS) basado en MPC para una microrred electro-térmica aislada en la región amazónica de Ecuador. Este trabajo es particularmente relevante dado el contexto geográfico de nuestro proyecto, demostrando la aplicabilidad de MPC en entornos rurales y aislados. Complementariamente, **Ponce y Mandal (2024)** propusieron una estrategia de control basada en MPC incremental para un EMS de microrred híbrida que integra la tecnología Vehículo a la Red (V2G). Este enfoque optimiza la carga y descarga de los sistemas de almacenamiento de energía en baterías de microrred (BESS) y la gestión de vehículos eléctricos, logrando una programación económica que reduce los costos generales y promueve el autoconsumo de RES.

Desde una perspectiva más amplia de optimización, **Nallolla et al. (2023)** ofrecieron una revisión exhaustiva de algoritmos de optimización multi-objetivo para microrredes híbridas AC/DC que utilizan fuentes de energía renovables. Analizaron métodos evolutivos para determinar la capacidad y el diseño óptimo de estos sistemas, buscando minimizar el costo de la energía, el costo neto presente, los costos operativos y las emisiones de carbono, al tiempo que se maximiza la fracción de energía renovable. Esta revisión proporciona una base teórica sólida sobre las diversas técnicas de optimización aplicables. Finalmente, **Li et al. (2022)** exploraron un enfoque de Aprendizaje por Refuerzo Profundo (DRL) multi-agente federado para la gestión de energía en multi-microrredes, demostrando el potencial de las arquitecturas de IA más avanzadas para el control en tiempo real y la minimización de costos económicos en sistemas complejos.

### 4.3. Tecnologías y Enfoques Actuales (State of the Art)

El estado del arte en la optimización energética de microrredes se caracteriza por la convergencia de diversas tecnologías y metodologías avanzadas, con un fuerte énfasis en la inteligencia artificial.

1.  **Predicción de Demanda y Generación**: Las técnicas de aprendizaje automático son fundamentales para pronosticar la demanda de carga y la generación de energía renovable (solar, eólica). Modelos como las Redes Neuronales Artificiales (ANN), incluyendo MLP-ANN (Duan et al., 2024) y Long Short-Term Memory (LSTM) para series temporales (Roselyn et al., 2024), así como la Regresión de Procesos Gaussianos (Patty & Malakar, 2025), son ampliamente utilizados para mejorar la precisión de los pronósticos, lo cual es crucial para una planificación energética efectiva.

2.  **Algoritmos de Optimización**: Se emplean algoritmos de optimización heurísticos y metaheurísticos para resolver problemas complejos de despacho de energía y dimensionamiento de componentes. Estos incluyen algoritmos multi-objetivo mejorados (Duan et al., 2024), algoritmos basados en la física como el Artificial Electric Field Algorithm (Patty & Malakar, 2025), y métodos evolutivos como el Multi-Objective Grey Wolf Optimizer (MOGWO) y Multi-Objective Particle Swarm Optimization (MOPSO) (Nallolla et al., 2023). Estos algoritmos buscan equilibrar múltiples objetivos, como la minimización de costos, la maximización de la confiabilidad y la reducción de emisiones.

3.  **Estrategias de Control**: El Control Predictivo por Modelo (MPC) es el enfoque dominante para los sistemas de gestión de energía (EMS) en microrredes (Arcos-Aviles et al., 2024; Ponce & Mandal, 2024; Touré et al., 2024). El MPC permite una planificación a corto plazo considerando restricciones del sistema y predicciones futuras, adaptándose dinámicamente a las condiciones cambiantes. Más recientemente, el Aprendizaje por Refuerzo Profundo (DRL) está ganando terreno para el control en tiempo real y la optimización adaptativa, especialmente en entornos multi-agente (Li et al., 2022).

4.  **Sistemas de Gestión Energética Inteligentes (IEMS)**: La integración de las tecnologías mencionadas da lugar a IEMS que pueden tomar decisiones autónomas para la operación de microrredes. Estos sistemas combinan módulos de pronóstico, algoritmos de optimización y estrategias de control para coordinar la generación distribuida, el almacenamiento de energía y las cargas, buscando eficiencia y resiliencia. La investigación en este ámbito también explora la implementación de estos sistemas en arquitecturas multi-agente para una gestión más descentralizada y robusta (ResearchGate, 2024; MDPI, 2023).

### 4.4. Brechas de Conocimiento y Oportunidades (Knowledge Gaps & Opportunities)

A pesar de los avances significativos en la optimización energética de microrredes, existen brechas importantes, particularmente en la aplicación práctica de estas tecnologías en contextos específicos como las zonas rurales no interconectadas de la Amazonía colombiana. La mayoría de las investigaciones se centran en entornos más controlados o urbanos, y no abordan completamente las particularidades de las microrredes aisladas en regiones remotas.

Las principales brechas incluyen:
*   **Adaptación a la escasez de datos**: En muchas comunidades rurales, la disponibilidad de datos históricos de demanda y generación puede ser limitada o de baja calidad, lo que representa un desafío para los modelos de AA que requieren grandes volúmenes de datos para su entrenamiento.
*   **Robustez ante condiciones extremas y variabilidad**: Las condiciones ambientales en la Amazonía (alta humedad, variaciones climáticas) pueden afectar el rendimiento de los equipos y la fiabilidad de los pronósticos, requiriendo algoritmos más robustos y adaptativos.
*   **Desarrollo de soluciones de bajo costo y fácil implementación**: La complejidad computacional de algunos algoritmos avanzados puede ser un obstáculo para su implementación en hardware de bajo costo y con recursos limitados, lo cual es esencial para la sostenibilidad en zonas rurales.
*   **Integración de factores socioeconómicos y territoriales**: La optimización no solo debe ser técnica, sino también considerar los impactos socioeconómicos y las particularidades culturales y geográficas de las comunidades, aspectos que a menudo no se abordan en la literatura técnica.

El presente proyecto surge como una oportunidad para llenar estas brechas, desarrollando un sistema predictivo inteligente que no solo incorpore lo último en algoritmos de AA y optimización, sino que esté específicamente diseñado y validado para las condiciones únicas de las microrredes híbridas en la Amazonía colombiana. Esto incluye la adaptación de modelos de pronóstico para entornos con datos limitados, la implementación de estrategias de control robustas y la colaboración con operadores locales para asegurar una solución práctica, sostenible y que mejore la calidad de vida en la región.

## 5. Objetivos
**Objetivo General**

Desarrollar y validar un sistema predictivo inteligente, basado en Inteligencia Artificial, para optimizar la gestión energética y operativa de microrredes híbridas en zonas rurales no interconectadas de la Amazonía Colombiana, incrementando la estabilidad del suministro energético y reduciendo los costos operacionales para mejorar la calidad de vida y fomentar el desarrollo regional sostenible.

**Objetivos Específicos**

1.  **Objetivo:** Diseñar y desarrollar algoritmos de aprendizaje automático adaptativos para la predicción de demanda energética y generación renovable en entornos con datos limitados.
    *   **Específico (S):** Desarrollo de algoritmos de IA (MLP-ANN, GPR, o similar) específicamente adaptados para la predicción de demanda energética y generación renovable en condiciones de datos escasos.
    *   **Medible (M):** Lograr una precisión de predicción promedio (MAPE) inferior al 10% para la demanda de carga y al 15% para la generación renovable (solar/eólica), bajo escenarios de datos incompletos o ruidosos.
    *   **Alcanzable (A):** Alcanzable a través de técnicas novedosas de aumento de datos, aprendizaje por transferencia y métodos estadísticos robustos.
    *   **Relevante (R):** Esencial para la inteligencia fundamental del sistema general y para abordar una brecha de conocimiento clave.
    *   **Plazo (T):** Al finalizar el Mes 9.

2.  **Objetivo:** Implementar un Sistema de Gestión Energética (EMS) basado en Control Predictivo por Modelo (MPC) que integre las predicciones de IA para la optimización en tiempo real del despacho de energía en microrredes híbridas.
    *   **Específico (S):** Creación de un EMS inteligente que utilice la estrategia MPC para gestionar dinámicamente el flujo de energía de fuentes solares, almacenamiento en baterías y generación suplementaria dentro de microrredes.
    *   **Medible (M):** Lograr una reducción mínima del 15% en los costos operativos anuales del despacho energético del piloto, en comparación con los métodos de control existentes en las comunidades intervenidas, y optimizar el uso de energía renovable en un 20%.
    *   **Alcanzable (A):** Factible adaptando marcos MPC establecidos (Arcos-Aviles et al., Ponce & Mandal) con las entradas de predicción de IA específicas del proyecto.
    *   **Relevante (R):** Aborda directamente el objetivo principal del proyecto de reducción de costos operativos y aumento de la eficiencia.
    *   **Plazo (T):** Al finalizar el Mes 18.

3.  **Objetivo:** Realizar una implementación piloto y validar el sistema predictivo inteligente en al menos dos microrredes rurales seleccionadas de la Amazonía Colombiana, en colaboración con los operadores locales y comunidades.
    *   **Específico (S):** Despliegue y prueba operativa del sistema desarrollado en entornos reales de microrredes con la participación activa de la comunidad y los operadores.
    *   **Medible (M):** Demostrar un incremento en la estabilidad y continuidad del suministro energético del 25% (medido como reducción de interrupciones o duración de cortes) en las comunidades piloto, y registrar un nivel de satisfacción del usuario y del operador > 80% en la usabilidad del sistema y su impacto percibido. Validar el prototipo a TRL 6-7.
    *   **Alcanzable (A):** Alcanzable a través de una implementación por fases, capacitación de usuarios y ciclos de retroalimentación iterativos.
    *   **Relevante (R):** Crucial para la validación práctica, la transferencia de tecnología y la garantía de un impacto regional directo.
    *   **Plazo (T):** Al finalizar el Mes 24.

4.  **Objetivo:** Fomentar el desarrollo de talento especializado y la apropiación social del conocimiento en IA aplicada a la gestión energética en las comunidades y el equipo técnico local.
    *   **Específico (S):** Desarrollo y entrega de programas de capacitación, talleres y manuales de usuario para operadores locales y miembros de la comunidad sobre la funcionalidad y los beneficios del sistema inteligente de gestión energética.
    *   **Medible (M):** Capacitar a al menos 20 operadores locales y miembros de la comunidad, obteniendo un índice de conocimiento del sistema del 70% post-capacitación, y generar un kit de divulgación que alcance al 100% de la población piloto.
    *   **Alcanzable (A):** Realista a través de iniciativas de capacitación dirigidas y culturalmente sensibles y talleres de co-creación.
    *   **Relevante (R):** Aborda componentes clave de la convocatoria relacionados con el desarrollo de talento, la inclusión social y el cierre de brechas tecnológicas.
    *   **Plazo (T):** Al finalizar el Mes 24 (con actividades continuas de seguimiento hasta el Mes 30 si el proyecto es de mayor duración).

## 6. Metodología Propuesta
**Framework Seleccionado:** Metodología Ágil (Scrum)

La Metodología Ágil (Scrum) se selecciona por su idoneidad para proyectos de I+D que involucran el desarrollo de algoritmos de Inteligencia Artificial complejos para entornos con datos limitados y una implementación piloto en condiciones reales. Su naturaleza iterativa y flexible, con énfasis en ciclos de retroalimentación continuos de los stakeholders (operadores locales, comunidades), es fundamental para adaptarse a requisitos cambiantes, prototipar rápidamente soluciones y asegurar que el sistema desarrollado sea robusto, fácil de usar y aborde eficazmente los desafíos únicos de las microrredes amazónicas. Este enfoque permite una entrega incremental de valor, la identificación temprana de problemas y la validación efectiva en campo, contribuyendo directamente al logro de los objetivos de precisión, reducción de costos, estabilidad del suministro y apropiación social del conocimiento.

**Fases Principales de la Metodología:**

*   **Fase 1: Planificación y Diseño Conceptual** - Se definen los requisitos detallados del sistema, se establece la arquitectura inicial y se prioriza el Backlog del Producto, sentando las bases para el desarrollo futuro.
*   **Fase 2: Desarrollo Iterativo de Módulos de IA** - Se desarrollan, entrenan y validan los algoritmos de predicción de demanda y generación renovable en Sprints, con revisiones continuas para asegurar el cumplimiento de los objetivos de precisión (SO1).
*   **Fase 3: Integración del Sistema de Gestión Energética** - Se integra el EMS basado en MPC con los módulos de IA, construyendo las interfaces de usuario y realizando pruebas de funcionalidad en entornos controlados, siguiendo un enfoque incremental (SO2).
*   **Fase 4: Implementación Piloto y Optimización en Campo** - Se despliega el sistema en las microrredes piloto, se recopila feedback de los operadores y comunidades, y se realizan ajustes y optimizaciones continuas en Sprints para validar el rendimiento y la usabilidad en el entorno real (SO3).
*   **Fase 5: Apropiación Social, Transferencia y Diseminación** - Se desarrollan y ejecutan programas de capacitación y talleres para los usuarios finales, se documenta la solución, se generan productos de conocimiento y se planifican estrategias de escalabilidad y sostenibilidad (SO4).

## 7. Plan de Ejecución y Gestión
**Cronograma de Actividades**

### 7.1. Cronograma de Actividades

| Fase | Actividad / Hito Clave | Entregable Principal | Duración Estimada (Semanas) |
| :--- | :--- | :--- | :--- |
| **Fase 1: Planificación y Diseño Conceptual** | *Definición de requisitos detallados, arquitectura inicial del sistema y planificación estratégica.* | | **12** |
| | 1.1. Constitución de equipos, planificación detallada y establecimiento de metodologías ágiles. | Acta de Constitución y Plan de Gestión de Proyecto. | 4 |
| | 1.2. Levantamiento de requisitos de campo en comunidades piloto y análisis de datos históricos disponibles. | Documento de Requisitos Detallados del Sistema. | 4 |
| | 1.3. Diseño arquitectónico del sistema, selección y adaptación de modelos de IA, y priorización del Backlog del Producto. | Diseño Conceptual del Sistema y Backlog del Producto Priorizado. | 4 |
| **Fase 2: Desarrollo Iterativo de Módulos de IA** | *Desarrollo, entrenamiento y validación de algoritmos de IA para predicción de demanda y generación renovable (Hito SO1).* | | **28** |
| | 2.1. Implementación de estrategia de recolección, preprocesamiento y aumento de datos para entornos limitados. | Base de Datos Optimizada y Estrategia de Preprocesamiento. | 7 |
| | 2.2. Desarrollo y entrenamiento de algoritmos de aprendizaje automático para la predicción de demanda energética. | Módulo de Predicción de Demanda (v1.0). | 9 |
| | 2.3. Desarrollo y entrenamiento de algoritmos de aprendizaje automático para la predicción de generación renovable. | Módulo de Predicción de Generación Renovable (v1.0). | 7 |
| | 2.4. Validación y ajuste iterativo de modelos de IA para cumplir con la precisión (MAPE) requerida. | Informe de Validación de Modelos IA (Hito SO1). | 5 |
| **Fase 3: Integración del Sistema de Gestión Energética** | *Diseño e integración del EMS basado en MPC con módulos de IA, y pruebas en laboratorio (Hito Clave Mes 15).* | | **28** |
| | 3.1. Diseño e implementación del motor de optimización del EMS basado en Control Predictivo por Modelo (MPC). | Diseño y Código del Núcleo MPC del EMS. | 10 |
| | 3.2. Integración de los módulos de IA predictivos desarrollados con el núcleo del EMS. | EMS Integrado (v1.0). | 8 |
| | 3.3. Desarrollo de interfaces de usuario y funcionalidades para operadores locales y sistemas de visualización. | Interfaces de Usuario y Manual de Operación Preliminar. | 6 |
| | 3.4. Pruebas unitarias, de integración y simulación del EMS en ambiente de laboratorio (TRL 5-6). | Informe de Pruebas y Simulación del EMS. | 4 |
| **Fase 4: Implementación Piloto y Optimización en Campo** | *Despliegue del sistema en microrredes piloto, monitoreo, optimización y validación de impacto (Hitos SO2 y SO3).* | | **40** |
| | 4.1. Preparación de sitios piloto y despliegue inicial del hardware y software del sistema en las microrredes. | Informe de Despliegue en Sitios Piloto. | 8 |
| | 4.2. Monitoreo del rendimiento del sistema en tiempo real y recolección de datos operativos de campo. | Informes de Monitoreo de Rendimiento. | 12 |
| | 4.3. Optimización iterativa del sistema y ajustes basados en el feedback de operadores y datos reales. | Informe de Optimización y Ajustes del Sistema. | 10 |
| | 4.4. Verificación y validación de la reducción de costos operativos y aumento de la estabilidad del suministro (TRL 7). | Informe Final de Validación de Impacto (Hitos SO2 y SO3). | 10 |
| **Fase 5: Apropiación Social, Transferencia y Diseminación** | *Capacitación, documentación, generación de conocimiento y plan de escalabilidad (Hito SO4).* | | **16** |
| | 5.1. Desarrollo de material didáctico y manuales de usuario para operadores locales y comunidades. | Material Didáctico y Manuales de Usuario Completos. | 4 |
| | 5.2. Ejecución de programas de capacitación, talleres de co-creación y sesiones de feedback con usuarios finales. | Informes de Capacitación y Talleres (Hito SO4). | 6 |
| | 5.3. Documentación final de la solución, generación de productos de conocimiento (publicaciones, patentes). | Documentación Técnica Final y Productos de Conocimiento. | 3 |
| | 5.4. Elaboración del plan de escalabilidad, sostenibilidad y diseminación de resultados del proyecto. | Plan de Escalabilidad y Diseminación. | 3 |

**Matriz de Riesgos**

### 7.2. Matriz de Riesgos

| # | Riesgo Potencial | Probabilidad | Impacto | Estrategia de Mitigación |
| :-: | :--- | :---: | :---: | :--- |
| 1 | **Calidad y Escasez de Datos Iniciales**<br>*Relacionado con: Fase 1 (1.2), Fase 2 (2.1)* | Alta | Alto | 1. Implementación de una estrategia robusta de recolección y preprocesamiento de datos desde el inicio. 2. Desarrollo y aplicación de técnicas de aumento de datos (data augmentation) y aprendizaje por transferencia (transfer learning) para compensar la escasez. 3. Diseño de modelos de IA intrínsecamente robustos a datos ruidosos o incompletos. |
| 2 | **Fallo en la Integración de Módulos (IA y EMS)**<br>*Relacionado con: Fase 3 (3.2)* | Media | Alto | 1. Establecimiento de una arquitectura modular clara y APIs bien definidas entre los módulos de IA y el EMS. 2. Implementación de un ciclo de pruebas de integración continuo desde las primeras etapas de desarrollo. 3. Uso de herramientas de control de versiones y metodologías ágiles para una integración incremental y detección temprana de fallos. |
| 3 | **Retrasos Logísticos en el Despliegue Piloto**<br>*Relacionado con: Fase 4 (4.1)* | Media | Medio | 1. Elaboración de un plan logístico detallado con rutas alternativas y proveedores de respaldo. 2. Fortalecimiento de alianzas con operadores locales y comunidades para facilitar el acceso y soporte en campo. 3. Asignación de un presupuesto de contingencia para imprevistos logísticos. 4. Despliegue por fases para minimizar la interrupción y aprender de cada etapa. |
| 4 | **Baja Adopción o Usabilidad del Sistema por Operadores Locales**<br>*Relacionado con: Fase 3 (3.3), Fase 5 (5.2)* | Media | Alto | 1. Co-diseño de las interfaces de usuario con la participación activa de futuros operadores. 2. Desarrollo de una interfaz intuitiva y simplificada, con documentación clara en español. 3. Implementación de programas de capacitación prácticos y recurrentes, con retroalimentación continua para ajustes del sistema y material didáctico. |
| 5 | **Incumplimiento de Métricas de Rendimiento en Campo (SO2/SO3)**<br>*Relacionado con: Fase 4 (4.4)* | Media | Alto | 1. Definición clara de KPIs y un sistema de monitoreo en tiempo real para evaluar el rendimiento. 2. Implementación de un proceso de optimización iterativa y ajustes continuos del sistema basado en los datos de campo. 3. Desarrollo de estrategias de respaldo o modos de operación degradados para asegurar la continuidad del servicio ante fallos parciales. 4. Revisiones periódicas de rendimiento con el equipo de I+D. |

## 8. Resultados e Impactos Esperados
### **8.1. Resultados Esperados (Entregables)**
*   **Algoritmos de IA para Predicción Energética Adaptativa:** Desarrollo y validación de algoritmos de Machine Learning (MLP-ANN, GPR o similares) específicamente adaptados para la predicción de demanda energética y generación renovable (solar/eólica) con una precisión de MAPE inferior al 10% y 15% respectivamente, en entornos con datos limitados. Corresponde al Objetivo Específico 1.
*   **Sistema de Gestión Energética Inteligente (IEMS) con MPC:** Prototipo funcional del Sistema de Gestión Energética (EMS) que integra los algoritmos de IA predictivos y la estrategia de Control Predictivo por Modelo (MPC) para la optimización en tiempo real del despacho de energía en microrredes híbridas, probado en ambiente simulado/laboratorio. Corresponde al Objetivo Específico 2.
*   **Sistema Predictivo Inteligente Validado en Campo (TRL 7):** Implementación y validación operativa del sistema predictivo inteligente de gestión energética (IEMS) en al menos dos microrredes rurales seleccionadas de la Amazonía Colombiana, demostrando un incremento del 25% en la estabilidad del suministro energético. Incluye informes de validación técnica y operativa. Corresponde al Objetivo Específico 3.
*   **Programas de Capacitación y Materiales de Apropiación Social:** Diseño e implementación de programas de capacitación, talleres y manuales de usuario para al menos 20 operadores locales y miembros de la comunidad, junto con un kit de divulgación que asegura la apropiación social del conocimiento y el desarrollo de talento especializado. Corresponde al Objetivo Específico 4.

### **8.2. Impactos Esperados**
*   **Impacto Técnico/Científico:**
    Este proyecto representa un avance significativo en el estado del arte de la gestión energética de microrredes, particularmente en contextos de datos limitados y condiciones operativas desafiantes. Se logrará el desarrollo y la validación de un sistema predictivo inteligente de gestión energética (IEMS), elevando su Nivel de Madurez Tecnológica (TRL) de 5 a 7. La generación de algoritmos de IA robustos y adaptativos para la predicción en escenarios con información escasa o ruidosa es un resultado clave que puede ser susceptible de protección intelectual. Además, la optimización del desempeño de las microrredes híbridas, mediante la integración de IA y Control Predictivo por Modelo (MPC), sentará un precedente metodológico para futuras aplicaciones en regiones similares.

*   **Impacto Económico:**
    El proyecto impactará directamente en la sostenibilidad económica de las microrredes en la Amazonía Colombiana, proyectando una reducción mínima del 15% en los costos operativos anuales para los operadores de las microrredes piloto. Esta disminución se traduce en una mayor eficiencia en el uso de recursos y una menor dependencia de combustibles fósiles, liberando capital para otras inversiones locales. La mayor estabilidad energética fomentará el desarrollo de actividades productivas locales, como la agroindustria y el turismo sostenible, contribuyendo a la bioeconomía regional y la generación de nuevas oportunidades económicas, fortaleciendo así las cadenas de valor en la Amazonía.

*   **Impacto Social/Ambiental:**
    Socialmente, el proyecto mejorará sustancialmente la calidad de vida de las comunidades rurales no interconectadas, con un incremento del 25% en la estabilidad y continuidad del suministro energético. Esto garantizará un mejor acceso a servicios esenciales como salud, educación y comunicación, y promoverá una vida nocturna más segura y productiva. El proyecto contribuirá directamente al cierre de brechas tecnológicas y a la equidad territorial, empoderando a las comunidades mediante la capacitación y el desarrollo de talento especializado en IA aplicada a la gestión energética. Ambientalmente, se promoverá la transición hacia una matriz energética más limpia mediante la optimización del uso de fuentes renovables (solar, eólica), reduciendo la huella de carbono y la dependencia de diésel. El apoyo a la construcción de sistemas energéticos autónomos y ambientalmente responsables reforzará la soberanía energética sostenible de estas regiones estratégicas, fomentando prácticas de monitoreo y conservación del entorno amazónico.

## 9. Referencias Bibliográficas
*   Arcos-Aviles, D., Salazar, A., Rodríguez, M., Martinez, W., & Guinjoan, F. (2024). Model predictive control-based energy management system for an isolated electro-thermal microgrid in the Amazon region of Ecuador. *Energy Reports, 10*, 4381-4394. https://doi.org/10.1016/j.egyr.2024.03.012
*   Duan, F., Eslami, M., Khajehzadeh, M., Basem, A., Jasim, D. J., & Palani, S. (2024). Optimization of a photovoltaic/wind/battery energy-based microgrid in distribution network using machine learning and fuzzy multi-objective improved Kepler optimizer algorithms. *Energy Reports, 10*, 2390-2404. https://doi.org/10.1016/j.egyr.2024.01.037
*   Li, Y., He, S., Li, Y., Shi, Y., & Zeng, Z. (2022). *Federated Multi-Agent Deep Reinforcement Learning Approach via Physics-Informed Reward for Multi-Microgrid Energy Management*. arXiv preprint arXiv:2212.14659.
*   Nallolla, C. A., P, V., Chittathuru, D., & Padmanaban, S. (2023). Multi-Objective Optimization Algorithms for a Hybrid AC/DC Microgrid Using RES: A Comprehensive Review. *Journal of Energy and Power Technology, 5*(4). https://doi.org/10.21926/jept.2304008
*   Patty, S., & Malakar, T. (2025). Assessment of battery energy storage uses in microgrid operation under varied demand uncertainties through a machine learning based stochastic optimization approach. *Applied Energy, 378*, 125078. https://doi.org/10.1016/j.apenergy.2024.125078
*   Ponce, G., & Mandal, P. (2024). Model Predictive Control for Hybrid Microgrid Energy Management System Implementing V2G. *IEEE Access, 12*, 26867-26880. https://doi.org/10.1109/ACCESS.2024.3387134
*   Pourbabak, H., Chen, T., Zhang, B., & Su, W. (2017). *Control and Energy Management System in Microgrids*. arXiv preprint arXiv:1705.10545.
*   ResearchGate. (2024). *Intelligent Energy Management System for Microgrids using Reinforcement Learning*. Retrieved from https://www.researchgate.net/publication/381968797_Intelligent_Energy_Management_System_for_Microgrids_using_Reinforcement_Learning
*   Roselyn, J. P., Sundaravadivel, P., Babu, V. V., Nithya, C., & Devaraj, D. (2024). LSTM Based Model Predictive Control Approach for Energy Management System in PV-Battery Integrated Microgrid Network. *Journal of Energy and Power Technology, 6*(1).
*   Sustainable Intelligent Energy Management System for Microgrid based on a Multi-Agent System. (2023). *Sustainability, 15*(16), 12546. https://doi.org/10.3390/su151612546
*   Touré, I., Payman, A., Camara, M., & Dakyo, B. (2024). Energy Management in a Renewable-Based Microgrid Using a Model Predictive Control Method for Electrical Energy Storage Devices. *Journal of Energy and Power Technology, 6*(1). https://doi.org/10.21926/jept.2401002
