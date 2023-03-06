from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class Chat(BaseModel):
    chat_id: str
    user_id: Optional[str]
    connection_id: Optional[str]
    chat_title: str
    chat_details: Optional[Dict]
    chat_history: Optional[Dict]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ChatCreateRequest(BaseModel):
    user_id: str
    connection_id: str
    chat_title: str
    chat_details: Optional[Dict]


class ChatUpdate(BaseModel):
    chat_title: Optional[str]
    chat_details: Optional[Dict]
    chat_history: Optional[Dict]
