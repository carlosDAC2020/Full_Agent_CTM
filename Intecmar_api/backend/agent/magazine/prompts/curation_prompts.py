def build_curation_prompt(datos: dict) -> str:
    return f"""
        Eres un redactor para un magazine de tecnología para startups.
        Escribe un párrafo corto (máximo 60 palabras), atractivo y claro sobre la convocatoria.
        Destaca el beneficio principal y el público objetivo. No incluyas URLs.

        Información:
        - Título: {datos.get('titulo', 'N/A')}
        - Dirigido a: {datos.get('dirigido_a', 'N/A')}
        - Beneficios: {datos.get('beneficios', 'N/A')}
        - Cierre: {datos.get('fecha_cierre', 'N/A')}
        """
