from pydantic import BaseModel
from uuid import UUID


class LoginSchema(BaseModel):
    email: str
    password: str


class ShowLoginSchema(BaseModel):
    id: UUID
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
