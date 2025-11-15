import chainlit as cl
import httpx
import os
import json
import boto3
import asyncio
from botocore.client import Config
from typing import List, Tuple, Optional

# --- Configuración del Agente y S3 ---
AGENT_API_URL = "http://agent:8000"
GRAPH_ID = "tech_surveillance"

# Configuración para nuestro S3 falso (LocalStack)
S3_ENDPOINT_URL = os.environ.get("DEV_AWS_ENDPOINT")
S3_BUCKET_NAME = os.environ.get("BUCKET_NAME")
S3_ACCESS_KEY = os.environ.get("APP_AWS_ACCESS_KEY")
S3_SECRET_KEY = os.environ.get("APP_AWS_SECRET_KEY")
S3_REGION = os.environ.get("APP_AWS_REGION")

# Creamos un cliente de S3 configurado para apuntar a LocalStack
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION,
    config=Config(signature_version="s3v4"),
)

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.on_chat_start
async def on_chat_start():
    """
    Se llama al iniciar un chat NUEVO.
    Crea un hilo en LangGraph y guarda su ID de forma persistente.
    """
    try:
        # 1. Crear el hilo en LangGraph
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AGENT_API_URL}/threads", json={})
            response.raise_for_status()
            thread_data = response.json()
            langgraph_thread_id = thread_data.get("thread_id")

            if not langgraph_thread_id:
                await cl.Message(content="Error: No se pudo crear el hilo de conversación en el agente.").send()
                return

        # 2. Guardar el ID en la sesión del usuario (CLAVE: usar el mismo nombre)
        cl.user_session.set("langgraph_thread_id", langgraph_thread_id)
        
        # 3. Guardar en los metadatos del contexto para persistencia
        if hasattr(cl.context, 'session') and cl.context.session:
            cl.context.session.user.metadata = cl.context.session.user.metadata or {}
            cl.context.session.user.metadata["langgraph_thread_id"] = langgraph_thread_id

        await cl.Message(
            content=(
                "### ¡Bienvenido al Asistente de Proyectos!\n\n"
                "Para comenzar, por favor, sigue estos pasos en **un solo mensaje**:\n\n"
                "1.  **Describe tu proyecto:** Escribe una descripción detallada de lo que quieres lograr.\n"
                "2.  **Adjunta tus documentos:** Usa el botón de adjuntar (📎) para subir todos los archivos de referencia (PDF, TXT, etc.).\n\n"
                "El sistema extraerá el título, la descripción y procesará tus archivos."
            )
        ).send()

    except Exception as e:
        await cl.Message(content=f"Ocurrió un error inesperado al iniciar el chat: {e}").send()


@cl.on_chat_resume
async def on_chat_resume(thread):
    """
    Se llama cuando el usuario vuelve a una conversación ANTIGUA.
    Recupera el ID del hilo de LangGraph de los metadatos.
    """
    try:
        # Intentar recuperar el ID del hilo desde los metadatos
        thread_id = thread.metadata.get("langgraph_thread_id") if thread.metadata else None
        
        if thread_id:
            # Restaurar en la sesión del usuario actual (CLAVE: mismo nombre)
            cl.user_session.set("langgraph_thread_id", thread_id)
            await cl.Message(content=f"Reanudando conversación.\n(ID de conversación: `{thread_id}`)").send()
        else:
            await cl.Message(content="Error: No se pudo recuperar el ID de la conversación anterior.").send()
    except Exception as e:
        await cl.Message(content=f"Error al reanudar conversación: {type(e).__name__} - {str(e)}").send()


@cl.step(name="Procesar Archivos Adjuntos", type="tool")
async def process_and_upload_files(
    thread_id: str, elements
) -> Tuple[List[str], list]:
    """
    Sube archivos a S3 y crea los elementos visuales correspondientes para Chainlit.
    """
    # Obtenemos el paso actual para poder enviarle contenido
    current_step = cl.context.current_step
    
    # Creamos las carpetas en S3
    context_folder_key = f"{thread_id}/context/"
    reports_folder_key = f"{thread_id}/reports/"
    await asyncio.to_thread(s3_client.put_object, Bucket=S3_BUCKET_NAME, Key=context_folder_key, Body=b'')
    await asyncio.to_thread(s3_client.put_object, Bucket=S3_BUCKET_NAME, Key=reports_folder_key, Body=b'')
    
    document_urls = []
    ui_elements = []


    for file in elements:
        try:
            with open(file.path, "rb") as f:
                file_content = f.read()
            
            file_key = f"{context_folder_key}{file.name}"
            
            # Subir el objeto a S3
            await asyncio.to_thread(
                s3_client.put_object,
                Bucket=S3_BUCKET_NAME, Key=file_key, Body=file_content
            )
            
            file_url = f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{file_key}"
            document_urls.append(file_url)
            
            # --- Lógica de Visualización Inteligente ---
            file_name_lower = file.name.lower()
            if file_name_lower.endswith(".pdf"):
                ui_elements.append(cl.Pdf(name=file.name, display="side", path=file.path))
                await cl.Message(content=f" guardando pdf ", parent_id=current_step.id).send()
            elif file_name_lower.endswith((".png", ".jpg", ".jpeg", ".gif")):
                ui_elements.append(cl.Image(name=file.name, display="inline", path=file.path, size="large"))
            else:
                ui_elements.append(cl.File(name=file.name, display="inline", path=file.path))
            

        except Exception as e:
            await cl.Message(content=f"❌ Error al subir `{file.name}`: {e}", parent_id=current_step.id).send()
            raise # Detenemos la ejecución si un archivo falla

    return document_urls, ui_elements


@cl.step(name="Análisis con Agente de IA", type="tool")
async def invoke_langgraph_agent(thread_id: str, message_content: str, document_urls: List[str]) -> List[dict]:
    """
    Invoca al agente LangGraph y recopila todos los eventos del stream.
    """
    payload = {
        "assistant_id": GRAPH_ID,
        "input": {"messages": [{"role": "user", "content": message_content}], "document_urls": document_urls},
        "stream_mode": "events"
    }
    
    all_events = []
    async with httpx.AsyncClient(timeout=300) as client:
        async with client.stream(
            "POST", f"{AGENT_API_URL}/threads/{thread_id}/runs/stream",
            json=payload, headers={"Content-Type": "application/json"}
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    data_str = line[len("data:"):].strip()
                    if data_str:
                        try:
                            all_events.append(json.loads(data_str))
                        except json.JSONDecodeError:
                            print(f"Advertencia: No se pudo decodificar JSON: {data_str}")
    
    return all_events


@cl.step(name="Generando Respuesta Final", type="run")
async def process_agent_response(events: List[dict]) -> Optional[str]:
    """
    Procesa los eventos del agente para extraer la respuesta final.
    """
    final_content = None
    for event_data in events:
        event_type = event_data.get("event")
        event_name = event_data.get("name")
        data = event_data.get("data", {})

        # Buscamos el evento que marca el final de la ejecución de todo el grafo
        if event_type == "on_chain_end" and event_name == GRAPH_ID:
            output = data.get("output", {})
            if output and "messages" in output and output["messages"]:
                last_message = output["messages"][-1]
                if isinstance(last_message, dict) and "content" in last_message:
                    final_content = last_message["content"]
                    break # Encontramos lo que buscábamos
    
    if final_content:
         cl.context.current_step.output = final_content

    return final_content


# ==============================================================================
# === NUEVA FUNCIÓN on_message ORQUESTADORA ===
# ==============================================================================

@cl.on_message
async def on_message(message: cl.Message):
    """
    Orquesta el flujo de trabajo: crea una lista de tareas,
    ejecuta cada paso y actualiza la interfaz de usuario.
    """
    thread_id = cl.user_session.get("langgraph_thread_id")
    if not thread_id:
        await cl.Message(content="Error: No se encontró un hilo. Por favor, reinicia el chat.").send()
        return

    task_list = cl.TaskList(status="Iniciando...", auto_done=False)
    await task_list.send()

    task_file_processing = cl.Task(title="Procesando archivos adjuntos", status=cl.TaskStatus.READY)
    await task_list.add_task(task_file_processing)
    task_agent_analysis = cl.Task(title="Análisis con Agente de IA", status=cl.TaskStatus.READY)
    await task_list.add_task(task_agent_analysis)
    task_final_response = cl.Task(title="Generando respuesta final", status=cl.TaskStatus.READY)
    await task_list.add_task(task_final_response)

    try:
        task_file_processing.status = cl.TaskStatus.RUNNING
        await task_list.send()

        document_urls, ui_elements = await process_and_upload_files(thread_id, message.elements)
        
        # CAMBIO 1: Construir un mensaje dinámico que contenga los nombres de los archivos
        if ui_elements:
            # Creamos una lista con los nombres de los elementos
            element_names = [e.name for e in ui_elements]
            # Creamos un texto que los incluya
            content_text = f"Archivos adjuntos recibidos:."
            
            await cl.Message(
                content=content_text,
            ).send()

        task_file_processing.status = cl.TaskStatus.DONE
        await task_list.send()

        task_agent_analysis.status = cl.TaskStatus.RUNNING
        await task_list.send()
        agent_events = await invoke_langgraph_agent(thread_id, message.content, document_urls)
        task_agent_analysis.status = cl.TaskStatus.DONE
        await task_list.send()
        
        task_final_response.status = cl.TaskStatus.RUNNING
        await task_list.send()
        final_content = await process_agent_response(agent_events)

        if final_content:
            await cl.Message(content=final_content).send()
        else:
            await cl.Message(content="El agente no produjo una respuesta final.").send()
        
        task_final_response.status = cl.TaskStatus.DONE
        await task_list.send()

    except Exception as e:
        task_list.status = "Error"
        await cl.Message(content=f"Ha ocurrido un error en el proceso: {e}").send()
        for task in task_list.tasks:
            if task.status != cl.TaskStatus.DONE:
                task.status = cl.TaskStatus.FAILED
        await task_list.send()
    finally:
        if task_list.status != "Error":
            task_list.status = "Completado"
        task_list.auto_done = True
        await task_list.send()
        
        # CAMBIO 2: Esperar un momento y luego limpiar la lista de tareas
        await cl.sleep(2)  # Darle al usuario 2 segundos para ver el estado "Completado"
        await cl.TaskList().send() # Enviar una lista vacía para ocultar el panel