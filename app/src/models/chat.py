from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Json


class Chat(BaseModel):
    chat_id: UUID
    user_id: Optional[UUID]
    connection_id: Optional[UUID]
    chat_title: str
    chat_details: Optional[Json]
    chat_history: Optional[Json]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ChatCreateRequest(BaseModel):
    user_id: UUID
    connection_id: UUID
    chat_title: str
    chat_details: Optional[Json]


class ChatUpdate(BaseModel):
    chat_id: UUID
    chat_title: Optional[str]
    chat_details: Optional[Json]
    chat_history: Optional[Json]
