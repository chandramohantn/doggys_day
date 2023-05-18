from pydantic import BaseModel


class CaretakerSchema(BaseModel):
    name: str
    address: str
    email: str
    phone: str
    lat: int
    lon: int

    # class Config:
    #     orm_mode = True


class ShowCaretakerSchema(BaseModel):
    name: str
    address: str
    phone: str
    lat: int
    lon: int

    class Config:
        orm_mode = True


class UpdateCaretakerSchema(BaseModel):
    address: str
    lat: int
    lon: int

    class Config:
        orm_mode = True
