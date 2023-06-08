from pydantic import BaseModel


class OwnerSchema(BaseModel):
    name: str
    address: str
    email: str
    password: str
    phone: str
    lat: int
    lon: int


class ShowOwnerSchema(BaseModel):
    id: str
    name: str
    address: str
    email: str
    phone: str
    lat: int
    lon: int

    class Config:
        orm_mode = True


class ShowPetOwnerSchema(BaseModel):
    id: str
    name: str
    address: str
    lat: int
    lon: int

    class Config:
        orm_mode = True


class UpdateOwnerSchema(BaseModel):
    id: str
    address: str
    email: str
    phone: str
    lat: int
    lon: int

    class Config:
        orm_mode = True
