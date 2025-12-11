import json
from fastapi import APIRouter
from celery.result import AsyncResult
from src.services.storage import MinioService

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])
storage_service = MinioService()

@router.get("/{task_id}")
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
        result_data = task_result.result # Dict {status, step, data}
        
        # Lógica de procesamiento de URLs de MinIO (Tu código original intacto)
        if isinstance(result_data, dict) and "data" in result_data:
            try:
                # Deserializamos para inyectar URLs firmadas
                state_dict = json.loads(result_data["data"])
                
                # Búscamos si hay 'docs_paths' en el estado
                if "docs_paths" in state_dict and state_dict["docs_paths"]:
                    docs = state_dict["docs_paths"]
                    
                    # Convertir Keys de S3 a URLs Presignadas
                    for key, val in docs.items():
                        # Verificación simple: si es string y tiene "/", asumimos que es una ruta de S3
                        if val and isinstance(val, str) and "/" in val: 
                            docs[key] = storage_service.get_presigned_url(val)
                    
                    # Actualizar data y volver a serializar
                    state_dict["docs_paths"] = docs
                    result_data["data"] = json.dumps(state_dict)
                    
            except Exception as e:
                print(f"Error procesando URLs de MinIO: {e}")

        response["result"] = result_data

    return response