import json
from fastapi import APIRouter
from celery.result import AsyncResult
from backend.app.services.tech_surveillance.storage import MinioService

router = APIRouter(prefix="/agent_tasks", tags=["Monitoreo de Tareas"])
storage_service = MinioService()

@router.get("/{task_id}", summary="Estado de tarea", description="Consulta el progreso y resultado de una tarea técnica asíncrona mediante su ID de Celery.")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    
    # Estructura base de la respuesta
    response = {
        "task_id": task_id,
        "status": task_result.status,
        "info": None # <--- NUEVO: Aquí vendrán los mensajes de streaming
    }
    
    # CASO 1: EN PROGRESO (Streaming)
    # Cuando el worker hace self.update_state(state='PROGRESS', meta={'message': '...'})
    # esos datos quedan disponibles en task_result.info
    if task_result.status == 'PROGRESS':
        response["info"] = task_result.info

    # CASO 2: COMPLETADO (SUCCESS / FAILURE)
    elif task_result.ready():
        # Si la tarea falló (excepción no capturada en el worker)
        if task_result.failed():
            response["status"] = "FAILURE"
            response["result"] = {
                "status": "error",
                "message": f"Error interno en el worker: {str(task_result.result)}"
            }
            return response

        result_data = task_result.result # Dict {status, step, data}
        
        # Lógica de procesamiento de URLs de MinIO (Tu código original intacto)
        if isinstance(result_data, dict) and "data" in result_data:
            try:
                # Deserializamos para inyectar URLs firmadas
                state_dict = json.loads(result_data["data"])
                
                # 1. Búscamos si hay 'docs_paths' en el estado
                if "docs_paths" in state_dict and state_dict["docs_paths"]:
                    docs = state_dict["docs_paths"]
                    for key, val in docs.items():
                        if val and isinstance(val, str) and "/" in val: 
                            docs[key] = storage_service.get_presigned_url(val)
                    state_dict["docs_paths"] = docs
                
                # 2. Búscamos si hay 'context_docs' en 'call_info'
                if "call_info" in state_dict and state_dict["call_info"]:
                    call_info = state_dict["call_info"]
                    if "context_docs" in call_info and call_info["context_docs"]:
                        presigned_docs = []
                        for val in call_info["context_docs"]:
                            if val and isinstance(val, str) and "/" in val:
                                presigned_docs.append({
                                    "name": val.split("/")[-1],
                                    "url": storage_service.get_presigned_url(val)
                                })
                            else:
                                presigned_docs.append(val)
                        call_info["context_docs"] = presigned_docs
                    state_dict["call_info"] = call_info

                # Actualizar data y volver a serializar
                result_data["data"] = json.dumps(state_dict)
                    
            except Exception as e:
                print(f"Error procesando URLs de MinIO: {e}")

        response["result"] = result_data

    return response