from fastapi import APIRouter

from backend.app.api.endpoints import auth, magazines, tasks, sources, utils

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(magazines.router) # /magazines, /saved, /history, /generate
api_router.include_router(tasks.router) # /tasks, /flows
api_router.include_router(sources.router) # /sources
api_router.include_router(utils.router) # /upload_pdf, /viewer, /email_settings, /send_email
