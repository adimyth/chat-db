from typing import Optional, Union

from fastapi import HTTPException
from pydantic import BaseModel


class Connection(BaseModel):
    user_id: str
    connection_id: str
    connection_name: str
    connection_type: str
    db_host: str
    db_port: int
    db_username: str
    db_name: str
    db_encrypted_password: Optional[str]
    is_successful: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]


class ConnectionCreateRequest(BaseModel):
    user_id: str
    connection_name: str
    connection_type: str
    db_host: str
    db_port: int
    db_username: str
    db_name: str
    db_password: str


class ConnectionUpdateRequest(BaseModel):
    connection_name: Optional[str]
    connection_type: Optional[str]
    db_host: Optional[str]
    db_port: Optional[str]
    db_username: Optional[str]
    db_name: Optional[str]
    db_password: Optional[str]


ConnectionOrError = Union[Connection, HTTPException]
