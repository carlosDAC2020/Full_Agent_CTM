# Importamos la instancia de la app definida en core
from src.core.celery_app import celery_app

# IMPORTANTE: Importamos las tareas para que el Worker las registre al iniciar.
# Si no haces este import, el worker arrancará pero no sabrá ejecutar "process_agent_step".
import src.tasks.agent_tasks

if __name__ == "__main__":
    celery_app.start()