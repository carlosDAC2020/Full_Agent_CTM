# prompts.py

ACTIVITY_SCHEDULE_PROMPT = """
Rol: Eres un experimentado Project Manager.
Tarea: Crear un cronograma de actividades de alto nivel para el proyecto descrito.

Contexto del Proyecto:
- Título del Proyecto: "{title}"
- Descripción del Proyecto: "{description}"

Instrucciones:
1.  Basándote en el proyecto, divide el trabajo en 4 a 6 fases principales (ej. Investigación, Diseño, Desarrollo, Pruebas, Despliegue).
2.  Para cada fase, lista 2-3 actividades o hitos clave.
3.  Asigna una duración estimada (en semanas o meses) para cada fase.
4.  Presenta el cronograma en un formato claro, como una tabla o una lista anidada.

Ejemplo de formato:
**Cronograma del Proyecto: [Título del Proyecto]**

*   **Fase 1: Investigación y Análisis (Semanas 1-2)**
    *   Hito 1.1: Definición de requisitos detallados.
    *   Hito 1.2: Análisis de mercado y competidores.
*   **Fase 2: Diseño y Prototipado (Semanas 3-5)**
    *   Hito 2.1: Diseño de la arquitectura del sistema.
    *   Hito 2.2: Creación de prototipos de interfaz de usuario.
"""

RISK_MATRIX_PROMPT = """
Rol: Eres un analista de riesgos senior.
Tarea: Construir una matriz de riesgos básica para el proyecto.

Contexto del Proyecto:
- Título del Proyecto: "{title}"
- Descripción del Proyecto: "{description}"

Instrucciones:
1.  Identifica de 4 a 6 riesgos potenciales que podrían afectar el éxito del proyecto (técnicos, operativos, de mercado, etc.).
2.  Para cada riesgo, evalúa su **Probabilidad** (Baja, Media, Alta) y su **Impacto** (Bajo, Medio, Alto) en el proyecto.
3.  Propón una **Estrategia de Mitigación** simple para cada riesgo.
4.  Presenta la información en formato de tabla o lista estructurada.

Ejemplo de formato:
**Matriz de Riesgos del Proyecto**

| Riesgo Potencial                      | Probabilidad | Impacto | Estrategia de Mitigación                                    |
|---------------------------------------|--------------|---------|-------------------------------------------------------------|
| Retrasos en la entrega de proveedores | Media        | Alto    | Establecer acuerdos de nivel de servicio (SLAs) claros y tener proveedores alternativos. |
| Adopción del usuario más baja de lo esperado | Baja         | Alto    | Realizar campañas de marketing y pruebas de usabilidad tempranas. |
"""