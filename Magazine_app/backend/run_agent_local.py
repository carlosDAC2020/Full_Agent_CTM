# backend/run_agent_local.py
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde la raíz del proyecto ANTES de importar el grafo
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from agent.graph import app  # Importamos la app compilada

# Verificamos que las claves estén cargadas
if not os.getenv("GEMINI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
    raise ValueError("Asegúrate de configurar tus claves de API en el archivo .env")

def run_agent():
    # Definimos la entrada inicial
    inputs = {"tema": "convocatorias sobre Inteligencia Artificial y tecnología para startups en LATAM"}

    # Ejecutamos el grafo
    # Usamos .stream() para ver el progreso paso a paso
    for event in app.stream(inputs):
        for key, value in event.items():
            print(f"--- Evento del Nodo: {key} ---")
            print(value)
            print("\n")
            
    print("✅ Proceso completado. Revisa la carpeta /outputs para ver las imágenes.")

if __name__ == "__main__":
    run_agent()
