def build_planner_prompt(tema: str) -> str:
    return f"""
    Eres un experto en investigación. Tu tarea es crear 5 consultas de búsqueda para la herramienta Tavily con el objetivo de encontrar:
    - Convocatorias de financiación ACTIVAS con fechas de cierre FUTURAS
    - Eventos relevantes (conferencias, summits, workshops, hackathons) con fechas FUTURAS
    sobre "{tema}".

    Incluye siempre los siguientes términos en tus búsquedas:
    - Para convocatorias: "deadline", "fecha límite", "cierre de postulaciones", "apply by"
    - Para eventos: "2025", "2026", "próximo", "futuro", "vencimiento"
    
    Usa también términos específicos como: "open call", "apply now", "funding opportunity", "grants", "conference", "summit", "workshop", "call for papers", "hackathon".
    Combina estos términos con el tema principal. 

    Enfócate en resultados con fechas futuras y asegúrate de incluir el tipo de financiamiento o beneficio (ej: "beca", "capital semilla", "premio en efectivo").

    Devuelve SOLAMENTE una lista de strings con las consultas, una por línea. No añadas numeración ni texto introductorio.
    Ejemplo:
    "open call" AI tech startups funding 2025 deadline "beca" OR "capital semilla"
    "conference" AI 2025 "call for papers" future event
    "hackathon" inteligencia artificial 2025 premio "USD 10,000"
    """
