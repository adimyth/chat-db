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
async def get_chat(user_id: str, connection_id: str = None, chat_id: str = None):
    # return error response if user_id is None
    if user_id is None:
        return HTTPException(status_code=400, detail="user_id is required")

    # create query based on user_id
    query = f"user_id=eq.{user_id}"

    # add connection_id and chat_id to query if provided
    if chat_id:
        query += f" AND chat_id=eq.{chat_id} "
    if connection_id:
        query += f" AND connection_id=eq.{connection_id} "

    # fetch data from supabase
    response = await supabase.from_("chat").select("*").text(query).execute()
    return {"all_chats": response}


@chat_router.post("/")
async def create_chat(chat: ChatCreateRequest) -> Chat:
    # create chat in supabase
    response = await supabase.from_("chat").insert(chat.dict()).execute()
    return response


@chat_router.put("/")
async def update_chat(chat: ChatUpdate) -> Chat:
    # update chat in supabase
    response = await supabase.from_("chat").update(chat.dict()).execute()
    return response
