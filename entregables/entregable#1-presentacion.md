---
marp: true
theme: default
paginate: true
header: 'Vigilancia Tecnológica - COTECMAR'
footer: 'Entregable N°1 | Septiembre 2025'
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Vigilancia Tecnológica

## Entregable N°1
### Documento de Requerimientos del Sistema

**Organismo:** COTECMAR  
**Proyecto:** Vigilancia Tecnológica  
**Autor:** Carlos Daniel Agamez Palomino  
**Versión:** 001 | **Fecha:** 19/11/2025

---

<!-- _header: '' -->

# Contenido

1. Introducción
2. Flujo de Generación del Reporte
3. Componentes Clave (Resumen No Técnico)
4. Tecnologías Implementadas
5. Estado Actual y Logros de Octubre
6. Próximos Pasos

---

# 1. Introducción

Este documento presenta el funcionamiento del servidor **`ctm_agent`**, diseñado para actuar como un **asistente inteligente** en la formulación de proyectos de vigilancia tecnológica.

## Objetivo Principal

El sistema automatiza la creación de informes complejos, pasando de una idea general a un documento estructurado con rigor académico y metodológico.

---

# 2. Flujo de Generación del Reporte

El valor principal del sistema reside en su capacidad para encadenar diferentes etapas de trabajo, simulando cómo un equipo humano abordaría la formulación de un proyecto.

---

## Paso 1: Entendimiento de la Solicitud (Ingesta)

**Entrada del usuario:**
> *"Quiero un proyecto sobre IA en la agricultura"*

**Lo que hace el sistema:**
- Analiza el texto para extraer datos clave
- Extrae: **Título del Proyecto**, **Descripción** y **Palabras Clave**

**Resultado:**
- El agente "entiende" de qué trata el proyecto
- Prepara una carpeta virtual (estado) donde guardará toda la información

---

## Paso 2: Investigación Académica

**Lo que hace el sistema:**
- Un agente especializado busca información en fuentes científicas reales:
  - ArXiv
  - Semantic Scholar
  - Búsqueda web (Tavily, Brave Search)

**Resultado:**
- Genera un **Marco Teórico** sólido
- Lista de **Referencias Bibliográficas** en formato APA
- Asegura sustento científico (no "alucinaciones" de IA)

---

## Paso 3: Estructuración Metodológica

Con la información teórica lista, el sistema define la estructura del proyecto de forma **secuencial y lógica**:

1. **Justificación** - Por qué es importante el proyecto
2. **Objetivos** - General y específicos medibles (SMART)
3. **Metodología** - Cómo se ejecutará el trabajo
4. **Cronograma** - Tabla de actividades estimada
5. **Riesgos** - Posibles problemas y mitigación
6. **Impactos** - Beneficios sociales, económicos y tecnológicos
7. **Resumen Ejecutivo** - Síntesis general

---

## Paso 4: Generación Visual

**Lo que hace el sistema:**
- Lee el título y descripción del proyecto
- Imagina una portada adecuada
- Crea un "prompt" para un modelo de generación de imágenes

**Resultado:**
- Una **imagen única** y alusiva al tema del proyecto
- Se inserta en el reporte final

---

## Paso 5: Ensamble del Reporte Final

El sistema toma todas las piezas generadas y las une en un solo documento bien formateado:

- Teoría
- Metodología
- Imagen de portada
- Cronograma
- Referencias

**Formato de salida:** Markdown + Presentación Marp

---

# 3. Componentes Clave (Resumen No Técnico)

Para lograr este flujo, el sistema utiliza varios **"expertos" virtuales**:

---

## Los Expertos del Sistema

### 🎯 El Coordinador (Router)
- Recibe al usuario
- Decide si quiere conversar o empezar un proyecto nuevo

### 🔬 El Investigador (Academic Agent)
- Busca en internet y lee papers
- Tiene herramientas para acceder a bases de datos científicas

---

## Los Expertos del Sistema (cont.)

### 📋 El Planificador (Project Schema)
- Sabe de metodología de proyectos
- No busca en internet, sino que piensa y estructura la información

### 🎨 El Artista (Image Generator)
- Se encarga exclusivamente de la parte visual
- Genera portadas personalizadas

---

# 4. Tecnologías Implementadas

El sistema se construye sobre un **stack tecnológico moderno y robusto**:

---

## Stack Principal

### Framework de Orquestación
- **LangGraph** - Definición del flujo de control y estado de los agentes

### Modelo de Lenguaje
- **Google Gemini 2.5 Flash** - Razonamiento, generación de texto y estructuración

### Herramientas de Búsqueda
- **Tavily AI** - Motor de búsqueda optimizado para agentes de IA
- **Brave Search** - Búsqueda web complementaria

---

## Stack Principal (cont.)

### Fuentes Académicas
- **ArXiv** - Repositorio de preprints científicos
- **Semantic Scholar** - Base de datos académica (200M+ papers)

### Infraestructura
- **Python 3.11+** - Lenguaje base
- **LangChain** - Biblioteca para interacción con modelos
- **PostgreSQL 16** - Base de datos
- **Redis 7** - Caché y gestión de colas

---

## Arquitectura de Microservicios

```
┌─────────────────────────────────┐
│   Chainlit Interface (Frontend)  │
└─────────────────────────────────┘
              ↕ HTTP/WebSocket
┌─────────────────────────────────┐
│  LangGraph Agent (Puerto 8000)  │
│  ┌──────────┐   ┌─────────────┐ │
│  │  Router  │   │  Subagents  │ │
│  └──────────┘   └─────────────┘ │
└─────────────────────────────────┘
              ↕
┌──────────────┐   ┌──────────┐
│ PostgreSQL   │   │  Redis   │
└──────────────┘   └──────────┘
```

---

## Servicios Externos (APIs)

| Servicio | Propósito |
|----------|-----------|
| **Google Gemini API** | Modelo de lenguaje principal |
| **LangSmith** | Monitoreo y trazabilidad |
| **Tavily AI** | Búsqueda web optimizada |
| **Brave Search** | Búsqueda web complementaria |
| **Semantic Scholar** | Literatura científica |
| **ArXiv** | Preprints científicos |
| **Google Image Gen** | Generación de imágenes |

---

# 5. Estado Actual y Logros de Octubre

Durante este mes, logramos que todos los "expertos" trabajen en equipo de forma **autónoma**.

---

## ✅ Funcionalidades Completadas

- ✅ Arquitectura de microservicios con Docker Compose
- ✅ Grafo de agentes LangGraph funcional
- ✅ Investigación académica automatizada
- ✅ Generación de estructura metodológica completa
- ✅ Generación de imágenes con IA
- ✅ Generación de presentaciones Marp
- ✅ Ensamblaje de documentos Markdown
- ✅ Interfaz Chainlit conversacional
- ✅ Monitoreo con LangSmith

---

## 📊 Métricas de Desarrollo

- **Líneas de código:** ~5,000+
- **Módulos principales:** 4
- **Subagentes:** 2
- **Subgrafos:** 2
- **Integraciones externas:** 7 APIs
- **Servicios Docker:** 3

---

## 📄 Documentos Generados

El sistema ha generado exitosamente:

- **44 reportes** en formato Markdown
- **16 presentaciones** en formato Marp
- **Múltiples imágenes** de portada

---

# 6. Próximos Pasos

---

## Mejoras Planificadas (Octubre-Noviembre 2025)

### 🔬 Mejora de Investigación Académica
- Aumentar profundidad del marco teórico
- Implementar análisis de relevancia de papers
- Añadir más fuentes (PubMed, IEEE Xplore)

### ✍️ Optimización de Prompts
- Refinar generación de objetivos
- Mejorar prompts de metodología
- Optimizar generación de cronogramas

---

## Mejoras Planificadas (cont.)

### 📐 Mejora de Formato
- Implementar plantillas personalizables
- Añadir soporte para exportación a PDF
- Mejorar estructura de tablas y gráficos

### ✅ Validación y Control de Calidad
- Validación de objetivos SMART
- Verificación de coherencia entre secciones
- Detección de alucinaciones del LLM

---

## Nuevas Funcionalidades

### 🌍 Soporte Multiidioma
- Generación en español e inglés
- Traducción automática de referencias

### 📋 Personalización de Plantillas
- Estructura de documento definida por usuario
- Soporte para diferentes tipos de convocatorias

### 🔍 Análisis de Convocatorias
- Extracción automática de requisitos
- Validación de cumplimiento

---

<!-- _class: lead -->

# ¡Gracias!

## Preguntas y Comentarios

**Contacto:** Carlos Daniel Agamez Palomino  
**Proyecto:** Vigilancia Tecnológica - COTECMAR  
**Versión:** 001 - Septiembre 2025
