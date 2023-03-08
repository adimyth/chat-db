import os
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from supabase import Client, create_client

from app.src.models.connection import (  # ConnectionOrError,
    ConnectionCreateRequest, ConnectionUpdateRequest)
from app.src.utils import check_valid_connection, encrypt_password

connection_router = APIRouter(
    prefix="/db-connection",
    tags=["connection"],
    responses={404: {"description": "Not found"}},
)

# create supabase client
supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_KEY")
)


@connection_router.get("/")
def get_connection(user_id: str, connection_id: str = None) -> Any:
    # return error response if user_id is not provided
    if not user_id:
        return HTTPException(status_code=400, detail="user_id is required")

    query_dict = {"user_id": user_id}
    if connection_id:
        query_dict["connection_id"] = connection_id

    try:
        response = (
            supabase.from_("db_connections")
            .select("*")
            .match(query_dict)
            .execute()
            .dict()["data"]
        )
        return response
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@connection_router.post("/")
def create_connection(
    connection: ConnectionCreateRequest,
) -> Any:
    # save connection only when it is valid
    if check_valid_connection(connection):
        new_connection = connection.dict()
        del new_connection["db_password"]
        new_connection["db_encrypted_password"] = encrypt_password(
            connection.db_password
        )
        response = (
            supabase.from_("db_connections")
            .insert(new_connection)
            .execute()
            .dict()["data"][0]
        )
        return response
    else:
        raise HTTPException(status_code=400, detail="Invalid connection")


@connection_router.patch("/")
def update_connection(connection_id: str, connection: ConnectionUpdateRequest) -> Any:
    if not connection_id:
        raise HTTPException(status_code=400, detail="connection_id is required")
    updated_connection = connection.dict(exclude_unset=True)
    if connection.db_password:
        updated_connection["db_encrypted_password"] = encrypt_password(
            connection.db_password
        )
        del updated_connection["db_password"]
    try:
        response = (
            supabase.from_("db_connections")
            .update(updated_connection)
            .match({"connection_id": connection_id})
            .execute()
            .dict()["data"][0]
        )
        return response
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid connection_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@connection_router.delete("/")
def delete_connection(connection_id: str) -> Any:
    try:
        response = (
            supabase.from_("db_connections")
            .delete()
            .match({"connection_id": connection_id})
            .execute()
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
