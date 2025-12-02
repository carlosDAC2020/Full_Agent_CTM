import asyncio
import uvicorn
import httpx # Librería moderna para peticiones HTTP
import uuid
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Configurar plantillas
templates = Jinja2Templates(directory="templates")

# URL de tu servidor de Agente (Asegúrate que el puerto sea correcto, ej: 8123, 8000, o 80)
AGENT_SERVER_URL = "http://127.0.0.1:2024"
AGENT_ID = "tech_surveillance"  

# Modelo de datos
class MessageInput(BaseModel):
    content: str

class AgentClient:
    """Cliente para interactuar con el servidor de hilos/agente."""
    
    def __init__(self, base_url: str, agent_id: str = AGENT_ID):
        self.base_url = base_url
        self.agent_id = agent_id    

    async def create_thread(self) -> dict:
        """
        Crea un hilo enviando el payload específico al servidor externo.
        """   
        # URL del endpoint externo
        url = f"{self.base_url}/threads"
        # Usamos AsyncClient para no bloquear el servidor FastAPI
        async with httpx.AsyncClient() as client:
            try:
                print(f"Enviando petición a: {url}")
                response = await client.post(url, json={}, timeout=10.0)
                response.raise_for_status() # Lanza error si no es 200 OK
                return response.json()
            except httpx.RequestError as e:
                print(f"Error de conexión: {e}")
                return {"error": "No se pudo conectar al servidor del agente"}
            except httpx.HTTPStatusError as e:
                print(f"Error del servidor agente: {e.response.text}")
                return {"error": f"El agente respondió con error: {e.response.status_code}"}
    
    async def run_thread(self, thread_id: str, message: str) -> dict:
        """
        Ejecuta el hilo (RUN) y espera a que termine para obtener el estado final.
        """
        url = f"{self.base_url}/threads/{thread_id}/runs"
        
        payload = {
            "assistant_id": self.agent_id, 
            "input": {
                'messages': [{
                    "role": "user",
                    "content": message
                }]
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                print(f"Ejecutando Run en: {url}")
                response = await client.post(url, json=payload, timeout=60.0)
                response.raise_for_status()
                
                # Primera línea: metadata del run creado
                lines = response.text.strip().split('\n')
                if not lines:
                    return {"error": "Sin respuesta del servidor"}
                
                first_event = json.loads(lines[0])
                run_id = first_event.get("run_id")
                
                print(f"Run creado: {run_id}, esperando completación...")
                
                # ESPERAR y obtener el estado final
                result = await self._get_run_state(thread_id, run_id)
                
                if "error" in result:
                    return result
                
                return {
                    "run_id": run_id,
                    "thread_id": thread_id,
                    "ai_messages": result.get("ai_messages", []),
                    "graph_state": result.get("graph_state", {}),
                    "status": result.get("status"),
                    "full_response": result.get("full_state")
                }
                    
            except httpx.HTTPStatusError as e:
                print(f"Error en Run: {e.response.text}")
                return {"error": f"Error {e.response.status_code}: {e.response.text}"}
            except Exception as e:
                print(f"Error: {e}")
                return {"error": str(e)}

    async def _get_run_state(self, thread_id: str, run_id: str) -> dict:
        """
        Obtiene el estado final de un run completado y extrae mensajes del AI.
        """
        url = f"{self.base_url}/threads/{thread_id}/runs/{run_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                # Hacer polling hasta que el run termine
                max_attempts = 30  # 30 segundos de espera
                ai_messages = []
                graph_state = {}
                
                for attempt in range(max_attempts):
                    response = await client.get(url, timeout=10.0)
                    response.raise_for_status()
                    
                    run_data = response.json()
                    status = run_data.get("status")
                    
                    print(f"Estado del run (intento {attempt + 1}): {status}")
                    
                    if status in ["success", "completed", "failed"]:
                        # Obtener el estado del thread
                        state_response = await client.get(
                            f"{self.base_url}/threads/{thread_id}/state",
                            timeout=10.0
                        )
                        state_response.raise_for_status()
                        state_data = state_response.json()
                        
                        # EXTRAER CORRECTAMENTE la estructura
                        # State tiene: {'values': {...}, 'metadata': {...}, 'next': [], ...}
                        values = state_data.get("values", {})
                        graph_state = values  # Guardar solo los valores
                        
                        # EXTRAER MENSAJES DEL AI desde values['messages']
                        messages = values.get("messages", [])
                        for msg in messages:
                            msg_type = msg.get("type")
                            if msg_type == "ai":  # Solo mensajes del AI
                                ai_messages.append({
                                    "content": msg.get("content"),
                                    "type": "ai",
                                    "id": msg.get("id"),
                                    "usage_metadata": msg.get("usage_metadata")
                                })
                        
                        print(f"✓ Mensajes del AI encontrados: {len(ai_messages)}")
                        
                        return {
                            "ai_messages": ai_messages,
                            "graph_state": graph_state,
                            "status": status,
                            "full_state": state_data  # Por si necesitas algo más
                        }
                    
                    # Esperar 1 segundo antes de reintentar
                    await asyncio.sleep(1)
                
                return {
                    "error": "Run tardó demasiado en completarse",
                    "ai_messages": [],
                    "graph_state": {}
                }
                
            except Exception as e:
                print(f"Error obteniendo estado del run: {e}")
                return {
                    "error": str(e),
                    "ai_messages": [],
                    "graph_state": {}
                }
        
# Instanciamos el cliente
agent_client = AgentClient(base_url=AGENT_SERVER_URL, agent_id=AGENT_ID)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/send")
async def receive_message(message: MessageInput):
    print(f"1. Mensaje recibido del frontend: {message.content}")
    
    thread_data = await agent_client.create_thread()
    
    if "error" in thread_data:
        return {"status": "error", "message": f"Fallo al crear hilo: {thread_data['error']}"}
    
    thread_id = thread_data.get("thread_id")
    print(f"2. Hilo creado con ID: {thread_id}")

    run_data = await agent_client.run_thread(thread_id, message.content)
    
    if "error" in run_data:
        return {"status": "error", "message": f"Fallo al ejecutar agente: {run_data['error']}"}
    
    print(f"✓ Mensajes del AI: ")
    for ai_msg in run_data.get("ai_messages", []):
        print(f"    - {ai_msg['content']}")

    print(f"✓ Estado del grafo:")
    print(json.dumps(run_data.get("graph_state"), indent=4, sort_keys=True, default=str))
    return {
        "status": "success",
        "thread_id": thread_id,
        "run_id": run_data.get("run_id"),
        "ai_messages": run_data.get("ai_messages", []),
        "graph_state": run_data.get("graph_state", {}),
        "full_response": run_data.get("full_response")
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)