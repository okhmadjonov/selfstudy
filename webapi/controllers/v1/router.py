from fastapi import APIRouter
from webapi.controllers.v1.endpoints import health

api_router = APIRouter()
api_router.include_router(health.router)
