from pydantic import BaseModel


class CaretakerSchema(BaseModel):
    name: str
    address: str
    email: str
    password: str
    phone: str
    lat: int
    lon: int
    rating: float


class ShowCaretakerSchema(BaseModel):
    id: str
    name: str
    address: str
    email: str
    phone: str
    lat: int
    lon: int
    rating: float

    class Config:
        orm_mode = True


class UpdateCaretakerSchema(BaseModel):
    id: str
    address: str
    email: str
    phone: str
    lat: int
    lon: int

    class Config:
        orm_mode = True


class UpdateCaretakerRatingSchema(BaseModel):
    id: str
    rating: float

    class Config:
        orm_mode = True
