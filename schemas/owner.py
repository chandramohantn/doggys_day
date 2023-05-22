from pydantic import BaseModel


class OwnerSchema(BaseModel):
    name: str
    address: str
    email: str
    password: str
    phone: str
    lat: int
    lon: int

    # class Config:
    #     orm_mode = True


class ShowOwnerSchema(BaseModel):
    name: str
    address: str
    phone: str
    lat: int
    lon: int

    class Config:
        orm_mode = True


class ShowPetOwnerSchema(BaseModel):
    name: str
    address: str
    lat: int
    lon: int

    class Config:
        orm_mode = True


class UpdateOwnerSchema(BaseModel):
    address: str
    lat: int
    lon: int

    class Config:
        orm_mode = True
