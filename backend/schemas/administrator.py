from pydantic import BaseModel


class AdminSchema(BaseModel):
    name: str
    address: str
    email: str
    password: str
    phone: str
    lat: int
    lon: int


class AdminInfoSchema(BaseModel):
    name: str
    address: str
    lat: int
    lon: int
