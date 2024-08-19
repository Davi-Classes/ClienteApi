from typing import Optional
from sqlmodel import SQLModel, Field


class ClienteIn(SQLModel):
    nome: str
    email: str
    endereco: str


class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    endereco: str


class MessageResponse(SQLModel):
    detail: str
