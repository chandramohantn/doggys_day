import uuid
from fastapi import APIRouter, status, Depends, HTTPException
from schemas import caretaker, booking
from sqlalchemy.orm import Session
from database import db, caretaker_service
from typing import List
from utils import oauth2, hashing

router = APIRouter()


@router.post(
    "/signup",
    summary="Create a caretaker",
    status_code=status.HTTP_201_CREATED,
    response_model=caretaker.ShowCaretakerSchema,
)
async def caretaker_signup(
    request: caretaker.CaretakerSchema, db_session: Session = Depends(db.get_db)
) -> caretaker.ShowCaretakerSchema:
    """
        POST api call for caretaker creation
    Args:
        request (caretaker.CaretakerSchema): Caretaker info
        db_session (Session, optional): database session object.

    Raises:
        HTTPException: If email already exists
        HTTPException: If phone number already exists

    Returns:
        caretaker.ShowCaretakerSchema: New caretaker object
    """

    caretaker_email = request.email
    caretaker_obj = caretaker_service.get_caretaker_by_email(
        db_session, caretaker_email
    )
    if caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email already exists !!!",
        )
    caretaker_phone = request.phone
    caretaker_obj = caretaker_service.get_caretaker_by_phone(
        db_session, caretaker_phone
    )
    if caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number already exists !!!",
        )

    unique_id = str(uuid.uuid4())
    hashed_password = hashing.get_hashed_password(request.password)
    new_caretaker = caretaker_service.create_caretaker(
        db_session,
        unique_id,
        request.name,
        request.address,
        request.email,
        hashed_password,
        request.phone,
        request.lat,
        request.lon,
        request.rating,
    )
    return new_caretaker


@router.get(
    "/{caretaker_id}",
    status_code=200,
    response_model=caretaker.ShowCaretakerSchema,
)
async def get_caretaker(
    caretaker_id: str, db: Session = Depends(db.get_db)
) -> caretaker.ShowCaretakerSchema:
    caretaker_obj = caretaker_service.get_caretaker_by_id(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    return caretaker_obj


@router.put("/{caretaker_id}", status_code=status.HTTP_202_ACCEPTED)
async def edit_caretaker(
    caretaker_id: str,
    request: caretaker.UpdateCaretakerSchema,
    db: Session = Depends(db.get_db),
):
    caretaker_obj = caretaker_service.get_caretaker_by_id(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    caretaker_obj = caretaker_service.edit_caretaker(
        db,
        caretaker_obj,
        request.address,
        request.email,
        request.phone,
        request.lat,
        request.lon,
    )
    return caretaker_obj


@router.delete("/{caretaker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_caretaker(caretaker_id: str, db: Session = Depends(db.get_db)) -> None:
    caretaker_obj = caretaker_service.delete_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )

    return None


@router.get(
    "/booking/{caretaker_id}",
    status_code=200,
    response_model=List[booking.ShowBookingSchema],
)
async def get_caretaker_bookings(
    caretaker_id: str, db: Session = Depends(db.get_db)
) -> List[booking.ShowBookingSchema]:
    caretaker_obj = caretaker_service.get_caretaker_by_id(db, caretaker_id)
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


@router.get(
    "/booking/{booking_id}", status_code=200, response_model=booking.ShowBookingSchema
)
async def get_booking_info(
    booking_id: str, db: Session = Depends(db.get_db)
) -> booking.ShowBookingSchema:
    booking_obj = caretaker_service.get_booking_info(db, booking_id)
    if not booking_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking id {booking_id} not found ...",
        )
    return booking_obj


@router.get("/rating/{caretaker_id}", status_code=200, response_model=int)
async def get_caretaker_rating(
    caretaker_id: str, db: Session = Depends(db.get_db)
) -> int:
    caretaker_obj = caretaker_service.get_caretaker_by_id(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id {caretaker_id} not found ...",
        )
    caretaker_rating = caretaker_service.compute_caretaker_rating(db, caretaker_id)
    return caretaker_rating


@router.put(
    "/rating/{caretaker_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=caretaker.UpdateCaretakerRatingSchema,
)
async def edit_caretaker_rating(
    caretaker_id: str,
    request: caretaker.UpdateCaretakerRatingSchema,
    db: Session = Depends(db.get_db),
) -> caretaker.ShowCaretakerSchema:
    caretaker_obj = caretaker_service.get_caretaker_by_id(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    caretaker_obj = caretaker_service.edit_caretaker_rating(
        db, caretaker_obj, request.rating
    )
    return caretaker_obj
