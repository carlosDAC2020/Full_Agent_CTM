def build_extraction_prompt(texto_limpio: str) -> str:
    return f"""
            Tu tarea es analizar el texto de una página web y clasificar su contenido. Luego, extrae TODAS las convocatorias y eventos vigentes en una LISTA JSON estricta.
            
            1. Clasifica el contenido en uno de tres tipos: "convocatoria_nacional", "convocatoria_internacional", o "evento".
               - Considera "convocatoria_nacional" como convocatorias de COLOMBIA.
               - Si encuentras una fecha de cierre o evento que ya pasó, devuelve: {{"error": "Fecha pasada"}}
            
            2. Extrae los siguientes campos para convocatorias:
               - "titulo": Título de la convocatoria
               - "dirigido_a": A quién está dirigida la convocatoria
               - "fecha_inicio": Fecha de inicio en formato YYYY-MM-DD si está disponible
               - "fecha_cierre": Fecha de cierre en formato YYYY-MM-DD (si hay múltiples fechas, usa la más cercana)
               - "deadline": Fecha y hora exacta de cierre en formato ISO 8601 (si está disponible)
               - "type_financy": Tipo(s) de financiamiento como string o lista de strings (ej: "beca", ["capital semilla", "mentoría"], "premio en efectivo", etc.)
               - "monto": Monto del financiamiento si está especificado (ej: "USD 10,000", "Hasta $50,000,000 COP")
               - "objetivo": Objetivo de la convocatoria
               - "beneficios": Lista de beneficios adicionales
               - "requisitos": Lista de requisitos principales
            
            3. Para eventos, extrae:
               - "titulo": Título del evento
               - "descripcion": Descripción detallada
               - "fecha_inicio" y "fecha_fin": Fechas en formato YYYY-MM-DD
               - "lugar": Ubicación física o virtual
               - "costo": Información sobre costos de participación
               - "tipo_evento": Tipo de evento (conferencia, taller, hackathon, etc.)
               - "beneficios": Beneficios de asistir
            
            Reglas importantes:
            - Si la fecha de cierre o el evento ya pasaron con claridad, omite esa convocatoria/evento de la lista.
            - Si no estás seguro de la fecha de cierre o de si el evento sigue vigente, ASUME que sigue vigente y extráela.
            - Si falta información, usa "No especificado".
            - Si el contenido no es relevante, devuelve una lista vacía: []
            - Tu respuesta DEBE SER EXCLUSIVAMENTE una LISTA JSON válida (ejemplo: [{{"titulo": "..."}}, {{"titulo": "..."}}]), sin texto adicional.

            Texto a analizar:
            {texto_limpio}
            """
