from fastapi import APIRouter, status, Depends, HTTPException
from schemas import caretaker, booking
from sqlalchemy.orm import Session
from database import db, caretaker_service
from typing import List
from utils import oauth2, hashing

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_caretaker(
    request: caretaker.CaretakerSchema, db: Session = Depends(db.get_db)
):
    new_caretaker = caretaker_service.create_caretaker(
        db,
        request.name,
        request.address,
        request.email,
        hashing.get_hashed_password(request.password),
        request.phone,
        request.lat,
        request.lon,
    )
    return {"data": f"Caretaker created with name {new_caretaker.name}"}


@router.get(
    "/caretaker/{id}", status_code=200, response_model=caretaker.ShowCaretakerSchema
)
def get_caretaker(caretaker_id: str, db: Session = Depends(db.get_db)):
    caretaker_obj = caretaker_service.get_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    return caretaker_obj


@router.get(
    "/caretaker", status_code=200, response_model=List[caretaker.ShowCaretakerSchema]
)
def get_all_caretakers(db: Session = Depends(db.get_db)):
    caretaker_objs = caretaker_service.get_all_caretakers(db)
    if not caretaker_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No caretakers available !!!",
        )
    return caretaker_objs


@router.put("/caretaker/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_caretaker(
    caretaker_id: str,
    request: caretaker.UpdateCaretakerSchema,
    db: Session = Depends(db.get_db),
):
    caretaker_obj = caretaker_service.get_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    caretaker_obj = caretaker_service.edit_caretaker(
        db, caretaker_obj, request.address, request.lat, request.lon
    )
    return caretaker_obj


@router.delete("/caretaker/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_caretaker(caretaker_id: str, db: Session = Depends(db.get_db)):
    caretaker_obj = caretaker_service.delete_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )

    return None


@router.get(
    "/caretaker_booking/{id}",
    status_code=200,
    response_model=List[booking.BookingSchema],
)
def get_owner_bookings(caretaker_id: str, db: Session = Depends(db.get_db)):
    caretaker_obj = caretaker_service.get_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id {caretaker_id} not found ...",
        )
    booking_objs = caretaker_service.get_caretaker_bookings(db, caretaker_id)
    if not booking_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id {caretaker_id} has no bookings ...",
        )
    return booking_objs


@router.get("/booking/{id}", status_code=200, response_model=booking.BookingSchema)
def get_booking_info(booking_id: str, db: Session = Depends(db.get_db)):
    booking_obj = caretaker_service.get_booking_info(db, booking_id)
    if not booking_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking id {booking_id} not found ...",
        )
    return booking_obj


@router.get("/rating/{id}", status_code=200, response_model=int)
def get_caretaker_rating(caretaker_id: str, db: Session = Depends(db.get_db)):
    caretaker_obj = caretaker_service.get_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id {caretaker_id} not found ...",
        )
    caretaker_rating = caretaker_service.compute_caretaker_rating(db, caretaker_id)
    return caretaker_rating


@router.put("/caretaker_rating/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_caretaker(
    caretaker_id: str,
    request: caretaker.UpdateCaretakerRatingSchema,
    db: Session = Depends(db.get_db),
):
    caretaker_obj = caretaker_service.get_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    caretaker_obj = caretaker_service.edit_caretaker_rating(
        db, caretaker_obj, request.rating
    )
    return caretaker_obj
