from pydantic import BaseModel
from uuid import UUID
from database.config import jwtsettings
from typing import List


class LoginSchema(BaseModel):
    email: str
    password: str


class ShowLoginSchema(BaseModel):
    id: UUID
    email: str

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenPayloadSchema(BaseModel):
    sub: str
    exp: int


class RefreshOwnerTokenSchema(BaseModel):
    # id: UUID
    token: str
    owner_id: UUID


class RefreshCaretakerTokenSchema(BaseModel):
    # id: UUID
    token: str
    caretaker_id: UUID
