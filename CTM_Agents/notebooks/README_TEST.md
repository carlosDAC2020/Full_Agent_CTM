# 🧪 Guía de Uso del Test Completo del Agente

Este documento explica cómo usar el script `test.py` mejorado que ejecuta el flujo completo del Agente de Vigilancia Tecnológica.

## 📋 Descripción del Flujo

El test ejecuta los siguientes pasos en secuencia:

### 1️⃣ Ingesta de Convocatoria
- Procesa la información de una convocatoria de financiamiento
- Extrae datos clave: título, objetivos, financiamiento, palabras clave, fechas
- Genera documentos de presentación (MD, PDF, PPTX)

### 2️⃣ Generación de Ideas de Proyecto
- Genera múltiples ideas de proyecto alineadas con la convocatoria
- Cada idea incluye:
  - Título descriptivo
  - Descripción detallada
  - 5 objetivos SMART

### 3️⃣ Selección de Idea
- Selecciona una idea de proyecto (simulado en el test, pero puede ser interactivo)
- La idea seleccionada se usa como base para el proyecto

### 4️⃣ Generación de Esquema Inicial
- Crea un esquema inicial del proyecto basado en la idea seleccionada
- Genera documentos del esquema inicial (MD y PDF)

### 5️⃣ Investigación y Documentos Finales
- Realiza investigación académica completa
- Genera esquemas detallados del proyecto
- Crea imágenes/posters del proyecto
- Compila el reporte final con todas las secciones:
  - Resumen Ejecutivo
  - Información General
  - Planteamiento del Problema y Justificación
  - Marco Teórico y Estado del Arte
  - Objetivos del Proyecto
  - Metodología Propuesta
  - Plan de Ejecución
  - Resultados e Impactos Esperados
  - Referencias Bibliográficas

## 🚀 Cómo Ejecutar el Test

### Requisitos Previos

1. **Variables de Entorno**: Asegúrate de tener un archivo `.env` con:
   ```env
   GEMINI_API_KEY=tu_api_key_aqui
   ```

2. **Dependencias**: Instala todas las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

Desde el directorio `notebooks/`:

```bash
python test.py
```

O desde el directorio raíz del proyecto:

```bash
python notebooks/test.py
```

## 📊 Salida Esperada

El script mostrará información detallada en cada paso:

```
================================================================================
🔬 TEST COMPLETO DEL AGENTE DE VIGILANCIA TECNOLÓGICA
================================================================================
🔑 Verificando API KEY... ✅ OK

📥 PASO 1: INGESTA DE CONVOCATORIA
--------------------------------------------------------------------------------
🚀 Procesando información de la convocatoria...

✅ Ingesta completada
   📋 Título: CONVOCATORIA COLOMBIA INTELIGENTE...
   🎯 Objetivo: Impulsar proyectos en tecnologías cuánticas...
   💰 Financiamiento: No especificado
   🏷️  Keywords: inteligencia artificial, tecnologías cuánticas, ...
   📄 Presentación MD: /ruta/al/documento.md
   📄 Presentación PDF: /ruta/al/documento.pdf
   📄 Presentación PPTX: /ruta/al/documento.pptx

💡 PASO 2: GENERACIÓN DE IDEAS DE PROYECTO
--------------------------------------------------------------------------------
...
```

## 🔧 Personalización

### Cambiar la Convocatoria

Modifica la variable `texto_convocatoria` en el script con la información de tu convocatoria:

```python
texto_convocatoria = """
Tu texto de convocatoria aquí...
"""
```

### Selección Interactiva de Ideas

Para permitir que el usuario seleccione la idea manualmente, reemplaza:

```python
selected_idea_index = 0  # Por defecto seleccionamos la primera idea
```

Con:

```python
# Solicitar selección al usuario
print("\n¿Qué idea deseas desarrollar?")
selected_idea_index = int(input("Ingresa el número de la idea (1-N): ")) - 1
```

### Ejecutar Solo Ciertos Pasos

Puedes comentar los pasos que no desees ejecutar. Por ejemplo, para ejecutar solo hasta la generación de ideas:

```python
# Comentar desde PASO 3 en adelante
# state_for_schema = state_after_ideas.copy()
# ...
```

## 📁 Documentos Generados

Los documentos se guardan en las siguientes carpetas:

- **Presentaciones**: `generated_presentations/`
- **Reportes**: `generated_reports/`
- **Imágenes**: `generated_images/`

## ⚠️ Notas Importantes

1. **Tiempo de Ejecución**: El proceso completo puede tomar varios minutos, especialmente el paso de investigación académica.

2. **Uso de API**: El test consume créditos de la API de Gemini. Asegúrate de tener suficiente cuota.

3. **Manejo de Errores**: Si algún paso falla, el script mostrará el error. Revisa los logs para más detalles.

4. **Estado del Grafo**: El estado se pasa entre pasos, por lo que cada paso depende del anterior.

## 🐛 Solución de Problemas

### Error: "Falta KEY"
- Verifica que el archivo `.env` existe y contiene `GEMINI_API_KEY`
- Asegúrate de que el archivo `.env` está en el directorio raíz del proyecto

### Error: "No module named 'src'"
- Verifica que estás ejecutando el script desde el directorio correcto
- Asegúrate de que la estructura de carpetas es correcta

### El agente no genera ideas
- Verifica que la información de la convocatoria es suficientemente detallada
- Revisa los logs del agente para ver posibles errores

## 📚 Recursos Adicionales

- Documentación del agente: `../README.md`
- Esquema de estado: `../src/agents/tech_surveillance/state.py`
- Grafo del agente: `../src/agents/tech_surveillance/graph.py`
