from fastapi import APIRouter

from app.src.controllers.chat import chat_router
from app.src.controllers.connection import connection_router

router = APIRouter()
router.include_router(chat_router)
router.include_router(connection_router)
