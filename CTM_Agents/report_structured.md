# {{titulo_del_proyecto}}

---

![Portada del Proyecto]({{ruta_de_la_imagen_generada}})

---

**Entidad Ejecutora Principal:** {{nombre_entidad_principal}}
**Entidades Colaboradoras:** {{lista_de_entidades_colaboradoras}}
**Fecha de Generación:** {{fecha_actual}}

---

## Índice

1.  [Resumen Ejecutivo](#1-resumen-ejecutivo)
2.  [Generalidades del Proyecto](#2-generalidades-del-proyecto)
3.  [Planteamiento del Problema y Justificación](#3-planteamiento-del-problema-y-justificación)
4.  [Marco Teórico y Estado del Arte](#4-marco-teórico-y-estado-del-arte)
5.  [Objetivos](#5-objetivos)
    *   [5.1. Objetivo General](#51-objetivo-general)
    *   [5.2. Objetivos Específicos (SMART)](#52-objetivos-específicos-smart)
6.  [Metodología Propuesta](#6-metodología-propuesta)
7.  [Plan de Ejecución y Gestión](#7-plan-de-ejecución-y-gestión)
    *   [7.1. Cronograma de Actividades](#71-cronograma-de-actividades)
    *   [7.2. Matriz de Riesgos](#72-matriz-de-riesgos)
8.  [Resultados e Impactos Esperados](#8-resultados-e-impactos-esperados)
9.  [Referencias Bibliográficas](#9-referencias-bibliográficas)

---

### **1. Resumen Ejecutivo**

*(Esta sección debe ser generada por un nodo específico que reciba como contexto los puntos clave de las demás secciones para crear un resumen conciso del problema, los objetivos, la metodología y el impacto esperado del proyecto).*

{{resumen_ejecutivo}}

---

### **2. Generalidades del Proyecto**

*   **Título del Proyecto:** {{titulo_del_proyecto}}
*   **Duración Estimada:** {{duracion_en_meses}} meses
*   **Línea Temática:** {{linea_tematica}}
*   **Palabras Clave:** {{palabras_clave}}

---

### **3. Planteamiento del Problema y Justificación**

*(Esta sección deberá ser generada por un nuevo nodo. Su prompt deberá enfocarse en describir el desafío o la oportunidad que el proyecto aborda, utilizando el contexto de la descripción inicial y los hallazgos del marco teórico para darle más peso y relevancia).*

{{planteamiento_y_justificacion}}

---

### **4. Marco Teórico y Estado del Arte**

*(Esta sección es el resultado directo de tu `academic_research_node`. El nodo de reporte final deberá tomar este contenido. **NOTA IMPORTANTE:** Deberás programar el nodo de reporte para que separe el cuerpo del texto de la sección de referencias que este agente genera al final, para colocar estas últimas en la sección 9).*

{{cuerpo_del_marco_teorico}}

---

### **5. Objetivos**

#### **5.1. Objetivo General**

*(Puede ser extraído del prompt de los objetivos específicos o tener su propio pequeño prompt generador).*

{{objetivo_general}}

#### **5.2. Objetivos Específicos (SMART)**

*(Esta sección es el resultado directo de tu nodo `generate_smart_objectives` dentro del subgrafo).*

{{smart_objectives}}

---

### **6. Metodología Propuesta**

*(Sección a generar por un nuevo nodo. Deberá describir el enfoque de trabajo (ej. "Modelo en V", "Metodología Ágil", etc.) y las fases principales que se seguirán para alcanzar los objetivos, basándose en el cronograma que se generará a continuación).*

{{metodologia}}

---

### **7. Plan de Ejecución y Gestión**

#### **7.1. Cronograma de Actividades**

*(Esta sección es el resultado directo de tu nodo `create_activity_schedule` dentro del subgrafo. Ya genera una tabla en Markdown, por lo que se inserta directamente).*

{{activity_schedule}}

#### **7.2. Matriz de Riesgos**

*(Esta sección es el resultado directo de tu nodo `build_risk_matrix` dentro del subgrafo. También es una tabla en Markdown y se inserta directamente).*

{{risk_matrix}}

---

### **8. Resultados e Impactos Esperados**

*(Otra sección para un nuevo nodo generador. Debe describir los entregables concretos (software, artículos, etc.) y los beneficios que el proyecto traerá a las organizaciones involucradas y a la comunidad en general).*

{{resultados_e_impacto}}

---

### **9. Referencias Bibliográficas**

*(Esta sección contendrá únicamente la bibliografía en formato APA extraída del resultado del `academic_research_node`).*

{{referencias_en_formato_apa}}