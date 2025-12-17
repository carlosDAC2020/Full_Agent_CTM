# backend/agent/nodes.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from .state import AgentState
from .tools import tools, search_all
import json
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from dateutil import parser
from urllib.parse import urlparse

from backend.app.db.session import SessionLocal
from backend.app.db import models
from backend.app.core.config import settings

# Configuración del LLM que usaremos (Gemini)
_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=_api_key)

# --- DEFINICIÓN DE NODOS ---

# Fuentes institucionales solicitadas (se gestionan vía JSON externo)
INSTITUTIONAL_SOURCES = []

def _load_institutional_sources_json() -> list:
    """Carga `outputs/sources.json` y devuelve la lista de fuentes visibles.
    Cada fuente debe tener al menos: {"id", "name", "type", "url", "hidden"}.
    Si el archivo no existe o está vacío, retorna lista vacía.
    """
    try:
        src_path = os.path.join("outputs", "sources.json")
        if not os.path.exists(src_path):
            return []
        with open(src_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            # Filtrar ocultas
            visibles = [s for s in data if not str(s.get("hidden", False)).lower() in ("true", "1")]
            return visibles
        return []
    except Exception:
        return []

def nodo_planificador(state: AgentState) -> AgentState:
    print("--- 🧠 PLANIFICANDO ---")
    prompt = f"""
    Eres un experto en investigación. Tu tarea es crear 5 consultas de búsqueda para la herramienta Tavily con el objetivo de encontrar:
    - Convocatorias de financiación ACTIVAS con fechas de cierre FUTURAS
    - Eventos relevantes (conferencias, summits, workshops, hackathons) con fechas FUTURAS
    sobre "{state['tema']}".

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
    response = llm.invoke(prompt)
    consultas = response.content.strip().split('\n')
    return {"plan": "Plan generado con éxito.", "consultas_busqueda": consultas}

def nodo_busqueda(state: AgentState) -> AgentState:
    print("--- 🔍 BUSCANDO EN LA WEB ---")
    resultados = []
    for query in state['consultas_busqueda']:
        print(f"Buscando: {query}")
        # Combinar Tavily + Brave, deduplicado
        combinados = search_all(query, tavily_max=1, brave_max=1)
        resultados.extend(combinados)
    # Añadir fuentes institucionales como semillas (dinámicas desde JSON)
    dynamic_sources = _load_institutional_sources_json() or INSTITUTIONAL_SOURCES
    for src in dynamic_sources:
        resultados.append({
            "url": src["url"],
            "title": src["name"],
            "content": ""
        })
    return {"resultados_busqueda": resultados}

def nodo_extraccion(state: AgentState) -> AgentState:
    print("--- 🔬 EXtrayendo Y CLASIFICANDO ---")
    
    urls_a_visitar = [res['url'] for res in state['resultados_busqueda']]
    datos_extraidos = []
    
    # Añadimos un User-Agent para parecer un navegador real y evitar bloqueos
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    for i, url in enumerate(urls_a_visitar):
        print(f"Procesando URL ({i+1}/{len(urls_a_visitar)}): {url}")
        try:
            resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')
            texto_web = soup.get_text(separator=' ')
            texto_limpio = ' '.join(texto_web.split())[:10000]

            # --- PROMPT MEJORADO Y CLASIFICACIÓN ---
            prompt = f"""
            Tu tarea es analizar el texto de una página web y clasificar su contenido. Luego, extrae la información relevante en un formato JSON estricto.
            
            1. Clasifica el contenido en uno de tres tipos: "convocatoria_nacional", "convocatoria_internacional", o "evento".
               - Considera "convocatoria_nacional" como convocatorias de COLOMBIA.
               - Si encuentras una fecha de cierre o evento que ya pasó, devuelve: {{"error": "Fecha pasada"}}
            
            2. Extrae los siguientes campos para convocatorias:
               - "titulo": Título de la convocatoria
               - "dirigido_a": A quién está dirigida la convocatoria
               - "fecha_inicio": Fecha de inicio en formato YYYY-MM-DD si está disponible
               - "fecha_cierre": Fecha de cierre en formato YYYY-MM-DD (si hay múltiples fechas, usa la más cercana)
               - "deadline": Fecha y hora exacta de cierre en formato ISO 8601 (si está disponible)
               - "type_financy": Tipo de financiamiento (ej: "beca", "capital semilla", "premio en efectivo", "aceleración", "mentoría", etc.)
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
            - Si la fecha de cierre o el evento ya pasaron, devuelve: {{"error": "Fecha pasada"}}
            - Si falta información, usa "No especificado"
            - Si el contenido no es relevante, devuelve: {{"error": "Contenido no relevante"}}
            - Tu respuesta DEBE SER ÚNICAMENTE un objeto JSON válido, sin texto adicional

            Texto a analizar:
            {texto_limpio}
            """

            # Llamar al LLM y obtener la respuesta de texto
            respuesta_llm = llm.invoke(prompt).content

            # --- PARSEO DE JSON MÁS ROBUSTO ---
            # A veces el LLM envuelve el JSON con texto. Intentamos extraerlo.
            match = re.search(r'\{.*\}', respuesta_llm, re.DOTALL)
            if match:
                json_str = match.group(0)
                try:
                    info_json = json.loads(json_str)
                    if isinstance(info_json, dict) and "error" not in info_json:
                        info_json['url_original'] = url
                        datos_extraidos.append(info_json)
                        print(f"  -> Éxito: '{info_json.get('titulo', 'Sin título')}'")
                except json.JSONDecodeError:
                    print(f"  -> Error: Se encontró un JSON, pero es inválido.")
            else:
                print(f"  -> Error: No se encontró ningún objeto JSON en la respuesta del LLM.")

        except requests.RequestException as e:
            print(f"  -> Error: No se pudo acceder a la URL. {e}")
    return {"datos_extraidos": datos_extraidos}

def nodo_curacion(state: AgentState) -> AgentState:
    print("--- ✍️ CURANDO Y REDACTANDO ---")
    convocatorias_curadas = []
    for datos in state.get('datos_extraidos', []):
        prompt = f"""
        Eres un redactor para un magazine de tecnología para startups.
        Escribe un párrafo corto (máximo 60 palabras), atractivo y claro sobre la convocatoria.
        Destaca el beneficio principal y el público objetivo. No incluyas URLs.

        Información:
        - Título: {datos.get('titulo', 'N/A')}
        - Dirigido a: {datos.get('dirigido_a', 'N/A')}
        - Beneficios: {datos.get('beneficios', 'N/A')}
        - Cierre: {datos.get('fecha_cierre', 'N/A')}
        """

        try:
            resumen = llm.invoke(prompt).content
        except Exception:
            resumen = "Resumen no disponible."

        datos_enriquecidos = dict(datos)
        datos_enriquecidos['resumen_magazine'] = resumen
        convocatorias_curadas.append(datos_enriquecidos)

    return {"contenido_curado": convocatorias_curadas}


def is_future_date(date_str: str) -> bool:
    """Verifica si una fecha es futura. Acepta múltiples formatos."""
    if not date_str or date_str.lower() == 'no especificado':
        return True  # Si no hay fecha, asumimos que es futura
        
    from dateutil import parser
    from datetime import datetime
    from urllib.parse import urlparse
    
    try:
        # Intentar parsear la fecha
        date = parser.parse(date_str, fuzzy=True)
        # Si la fecha no tiene zona horaria, asumir UTC
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        return date > datetime.now(timezone.utc)
    except Exception:
        # Si hay error al parsear, asumir que es futura
        return True


def nodo_guardado_db(state: AgentState) -> AgentState:
    """Persiste cada convocatoria/evento en la tabla "convocatorias".
    Filtra eventos pasados y asegura que los datos tengan el formato correcto.
    """
    print("--- 💾 GUARDANDO EN BASE DE DATOS (convocatorias) ---")

    db = SessionLocal()

    # Cargar fuentes para inferir tipo por host si es necesario
    sources_list = []
    try:
        src_path = settings.SOURCES_FILE or os.path.join(settings.OUTPUTS_DIR, "sources.json")
        if os.path.exists(src_path):
            with open(src_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    sources_list = data
    except Exception:
        sources_list = []

    def _host(u: str) -> str:
        try:
            p = urlparse(u)
            h = (p.netloc or "").lower().lstrip("www.")
            return h
        except Exception:
            return ""

    def _normalize_tipo(tipo_raw: str, url_original: str) -> str:
        t = (tipo_raw or "").strip().lower()
        if "evento" in t:
            return "evento"
        if "internacional" in t:
            return "convocatoria_internacional"
        if "nacional" in t:
            return "convocatoria_nacional"
        # fallback por fuente
        h_item = _host(url_original)
        if h_item and sources_list:
            for s in sources_list:
                su = str(s.get("url") or "")
                hs = _host(su)
                if hs and hs == h_item:
                    st = (s.get("type") or "").strip().lower()
                    if st.startswith("nacion"):
                        return "convocatoria_nacional"
                    if "internacional" in st:
                        return "convocatoria_internacional"
        # default conservador
        return "convocatoria_nacional"

    def _normalize_kw(s: str) -> str:
        s = re.sub(r"\s+", " ", s.strip())
        s = re.sub(r"^[\-–—•·\s]+|[\-–—•·\s]+$", "", s)
        return s

    def _is_short_phrase(s: str) -> bool:
        if not s:
            return False
        if len(s) > 40:
            return False
        words = [w for w in re.split(r"\s+", s) if w]
        if len(words) == 0 or len(words) > 3:
            return False
        if re.search(r"[\.!?]", s):
            return False
        return True

    now_utc = datetime.now(timezone.utc)
    created = 0

    try:
        for item in state.get("contenido_curado", []):
            # Verificar fechas (filtro de eventos/convocatorias pasadas)
            fecha_cierre_raw = item.get("fecha_cierre") or item.get("deadline") or item.get("fecha_fin")
            if not is_future_date(fecha_cierre_raw):
                print(
                    f"⚠️  Omitiendo evento/convocatoria pasada: {item.get('titulo', 'Sin título')} - Fecha: {fecha_cierre_raw}"
                )
                continue

            titulo = item.get("titulo") or "Sin título"
            desc = (
                item.get("resumen_magazine")
                or item.get("objetivo")
                or item.get("descripcion")
                or "Sin descripción"
            )

            # Keywords
            kws: list[str] = []
            if "dirigido_a" in item and item["dirigido_a"]:
                dirigido_a = item["dirigido_a"]
                if isinstance(dirigido_a, list):
                    dirigido_a = ", ".join(str(x) for x in dirigido_a if x)
                for part in re.split(r"[,\n;]", str(dirigido_a)):
                    kw = _normalize_kw(part)
                    if not kw or kw.lower() == "no especificado":
                        continue
                    if _is_short_phrase(kw):
                        norm = kw.lower()
                        if norm not in [k.lower() for k in kws]:
                            kws.append(kw)

            url_original = item.get("url_original", "")
            tipo_norm = _normalize_tipo(item.get("tipo", ""), url_original)
            if tipo_norm and tipo_norm not in kws:
                kws.append(tipo_norm)

            if (
                "type_financy" in item
                and item["type_financy"]
                and str(item["type_financy"]).lower() != "no especificado"
            ):
                if item["type_financy"] not in kws:
                    kws.append(item["type_financy"])

            url = url_original or None

            # Evitar duplicados por URL o por título si no hay URL
            q = db.query(models.Convocatoria)
            if url:
                q = q.filter(models.Convocatoria.url == url)
            else:
                q = q.filter(models.Convocatoria.title == titulo)
            if q.first():
                continue

            conv = models.Convocatoria(
                title=str(titulo),
                description=str(desc),
                keywords=kws,
                source=url_original or None,
                type=str(tipo_norm),
                url=url,
                created_at=now_utc,
                fecha_inicio=item.get("fecha_inicio") or item.get("inicio"),
                deadline=None,  # deadline detallado no se parsea aquí; ya se filtró por fecha_cierre_raw
                fecha_cierre=item.get("fecha_cierre") or None,
                type_financy=item.get("type_financy"),
                monto=item.get("monto"),
                requisitos=item.get("requisitos") or ["No especificado"],
                beneficios=item.get("beneficios") or ["No especificados"],
                lugar=item.get("lugar") or "No especificado",
            )
            db.add(conv)
            created += 1

        if created:
            db.commit()
        print(f"✅ Guardado en BD: {created} nuevas convocatorias")
    except Exception as e:
        print(f"⚠️ Error guardando convocatorias en BD: {e}")
        db.rollback()
    finally:
        db.close()

    # Importante: devolver una actualización válida del estado
    return {"contenido_curado": state.get("contenido_curado", [])}

# nodo_generador_pdf eliminado: el backend genera PDF directamente en main_api.py
