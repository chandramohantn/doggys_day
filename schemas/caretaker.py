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

    # class Config:
    #     orm_mode = True


class ShowCaretakerSchema(BaseModel):
    name: str
    address: str
    phone: str
    lat: int
    lon: int
    rating: float

    class Config:
        orm_mode = True


class UpdateCaretakerSchema(BaseModel):
    address: str
    lat: int
    lon: int

    class Config:
        orm_mode = True


class UpdateCaretakerRatingSchema(BaseModel):
    rating: float

    class Config:
        orm_mode = True
