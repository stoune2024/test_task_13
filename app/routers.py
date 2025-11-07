from fastapi import APIRouter
from app.repository import init_db


opencv_app_router = APIRouter(tags=["Роутер сервиса анализа видео"])


@opencv_app_router.on_event("startup")
async def startup_event():
    await init_db()
