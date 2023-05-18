from pydantic import BaseModel


class PetSchema(BaseModel):
    name: str
    age: int
    breed: str
    gender: str
    owner_id: str

    class Config:
        orm_mode = True


class ShowPetSchema(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True
