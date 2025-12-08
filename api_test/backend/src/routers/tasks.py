import json
from fastapi import APIRouter
from celery.result import AsyncResult
from src.services.storage import MinioService

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])
storage_service = MinioService()

@router.get("/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "status": task_result.status,
    }
    
    if task_result.ready():
        result_data = task_result.result # Dict {status, step, data}
        
        # Lógica de procesamiento de URLs de MinIO
        if isinstance(result_data, dict) and "data" in result_data:
            try:
                state_dict = json.loads(result_data["data"])
                
                # Búscamos si hay 'docs_paths' en el estado
                if "docs_paths" in state_dict and state_dict["docs_paths"]:
                    docs = state_dict["docs_paths"]
                    
                    # Convertir Keys de S3 a URLs Presignadas
                    for key, val in docs.items():
                        # Verificación simple: si es string y tiene "/", asumimos que es una ruta de S3
                        if val and isinstance(val, str) and "/" in val: 
                            docs[key] = storage_service.get_presigned_url(val)
                    
                    # Actualizar data
                    state_dict["docs_paths"] = docs
                    result_data["data"] = json.dumps(state_dict)
                    
            except Exception as e:
                print(f"Error procesando URLs de MinIO: {e}")

        response["result"] = result_data

    return response