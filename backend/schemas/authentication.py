from pydantic import BaseModel
from datetime import datetime


class LoginSchema(BaseModel):
    username: str
    password: str


class ShowLoginSchema(BaseModel):
    id: str
    email: str

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    name: str
    id: str
    token_type: str
    access_token: str
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    sub: str
    exp: datetime


class RefreshOwnerTokenSchema(BaseModel):
    token: str
    owner_id: str


class RefreshCaretakerTokenSchema(BaseModel):
    token: str
    caretaker_id: str
