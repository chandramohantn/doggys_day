from pydantic import BaseModel
from datetime import datetime


class BookingSchema(BaseModel):
    caretaker_id: str
    owner_id: str
    instruction: str


class ShowBookingSchema(BaseModel):
    id: str
    caretaker_id: str
    owner_id: str
    date_of_booking: datetime
    instruction: str

    class config:
        orm_mode = True


class ReviewSchema(BaseModel):
    booking_id = str
    rating = int
    comment = str

    class config:
        orm_mode = True


class ShowReviewSchema(BaseModel):
    id: str
    booking_id = str
    rating = int
    date_of_review = datetime
    comment = str

    class config:
        orm_mode = True
