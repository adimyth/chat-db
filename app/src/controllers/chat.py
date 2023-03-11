import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from supabase import Client, create_client

from app.src.models.chat import Chat, ChatCreateRequest, ChatUpdate

chat_router = APIRouter(
    prefix="/chat", tags=["chat"], responses={404: {"description": "Not found"}}
)

load_dotenv()


supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_KEY")
)


@chat_router.get("/")
def get_chat(user_id: str, connection_id: str = None, chat_id: str = None):
    # return error response if user_id is None
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    query_dict = {}
    query_dict["user_id"] = user_id

    if chat_id:
        query_dict["chat_id"] = chat_id
    if connection_id:
        query_dict["connection_id"] = connection_id

    response = (
        supabase.from_("chat_session")
        .select("*")
        .match(query_dict)
        .execute()
        .dict()["data"]
    )
    return response


@chat_router.post("/")
def create_chat(chat: ChatCreateRequest) -> Chat:
    response = (
        supabase.from_("chat_session").insert(chat.dict()).execute().dict()["data"][0]
    )
    return response


@chat_router.patch("/")
def update_chat(chat_id: str, chat: ChatUpdate) -> Chat:
    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id is required")
    try:
        if chat.chat_history:
            existing_chat = get_chat_history(chat_id)
            if existing_chat:
                chat.chat_history = {**existing_chat, **chat.chat_history}

        response = (
            supabase.from_("chat_session")
            .update(chat.dict(exclude_unset=True))
            .eq("chat_id", chat_id)
            .execute()
            .dict()["data"][0]
        )
        return response
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid chat_id")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_chat_history(chat_id: str) -> str:
    response = (
        supabase.from_("chat_session")
        .select("chat_history")
        .eq("chat_id", chat_id)
        .execute()
        .dict()["data"][0]
    )
    return response["chat_history"]
