"""
All api calls for owners
"""

import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, status, Depends, HTTPException, Request
from schemas import owner, pet, booking, caretaker
from sqlalchemy.orm import Session
from database import db, owner_service, caretaker_service
from utils import hashing, token

router = APIRouter()


@router.post(
    "/signup",
    summary="Create an owner",
    status_code=status.HTTP_201_CREATED,
    response_model=owner.OwnerInfoSchema,
)
async def owner_signup(
    request: owner.OwnerSchema, db_session: Session = Depends(db.get_db)
) -> owner.OwnerInfoSchema:
    """
        POST api call for owner creation
    Args:
        request (owner.OwnerSchema): Owner info
        db (Session, optional): Get db session

    Raises:
        HTTPException: If email already exists
        HTTPException: If phone number already exists

    Returns:
        owner.OwnerInfoSchema: New owner object
    """

    owner_email = request.email
    owner_obj = owner_service.get_owner_by_email(db_session, owner_email)
    if owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email already exists !!!",
        )
    owner_phone = request.phone
    owner_obj = owner_service.get_owner_by_phone(db_session, owner_phone)
    if owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number already exists !!!",
        )

    unique_id = str(uuid.uuid4())
    hashed_password = hashing.get_hashed_password(request.password)
    new_owner = owner_service.create_owner(
        db_session,
        unique_id,
        request.name,
        request.address,
        request.email,
        hashed_password,
        request.phone,
        request.lat,
        request.lon,
    )
    new_owner_obj = {
        "name": new_owner.name,
        "address": new_owner.address,
        "lat": new_owner.lat,
        "lon": new_owner.lon,
    }
    return owner.OwnerInfoSchema(**new_owner_obj)


@router.get("/{owner_id}", status_code=200, response_model=owner.ShowOwnerSchema)
async def get_owner_by_id(
    header: Request, owner_id: str, db_session: Session = Depends(db.get_db)
) -> owner.ShowOwnerSchema:
    """
        GET api call to get the owner corresponding to the provided owner_id
    Args:
        header (Request): Request headers
        owner_id (str): ID of the owner
        db_session (Session, optional): database session object

    Raises:
        HTTPException: Owner not found

    Returns:
        owner.ShowOwnerSchema: Owner object
    """

    userid = token.authenticate_user(header.headers.get("authorization"))
    if userid != owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    owner_obj = owner_service.get_owner_by_id(db_session, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    owner_obj_dict = {
        "id": owner_obj.id,
        "name": owner_obj.name,
        "email": owner_obj.email,
        "phone": owner_obj.phone,
        "address": owner_obj.address,
        "lat": owner_obj.lat,
        "lon": owner_obj.lon,
    }
    return owner.ShowOwnerSchema(**owner_obj_dict)


@router.put("/{owner_id}", status_code=status.HTTP_202_ACCEPTED)
async def edit_owner(
    header: Request,
    owner_id: str,
    request: owner.UpdateOwnerSchema,
    db_session: Session = Depends(db.get_db),
):
    userid = token.authenticate_user(header.headers.get("authorization"))
    if userid != owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    owner_obj = owner_service.get_owner_by_id(db_session, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    owner_obj = owner_service.edit_owner(
        db_session,
        owner_obj,
        request.address,
        request.email,
        request.phone,
        request.lat,
        request.lon,
    )
    return owner_obj


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_owner(
    request: Request, owner_id: str, db_session: Session = Depends(db.get_db)
) -> None:
    userid = token.authenticate_user(request.headers.get("authorization"))
    if userid != owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    owner_obj = owner_service.delete_owner(db_session, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )

    return None


@router.post(
    "/add_pet", status_code=status.HTTP_201_CREATED, response_model=pet.ShowPetSchema
)
async def add_pet(
    header: Request,
    request: pet.PetSchema,
    db_session: Session = Depends(db.get_db),
) -> pet.ShowPetSchema:
    userid = token.authenticate_user(header.headers.get("authorization"))
    if userid != request.owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    unique_id = str(uuid.uuid4())
    new_pet = owner_service.create_pet(
        db_session,
        unique_id,
        request.name,
        request.age,
        request.breed,
        request.gender,
        request.owner_id,
    )
    return new_pet


@router.get(
    "/owner_pet/{owner_id}",
    status_code=200,
    response_model=Optional[List[pet.ShowPetSchema]],
)
async def get_owner_pets(
    request: Request,
    owner_id: str,
    db_session: Session = Depends(db.get_db),
) -> Optional[List[pet.ShowPetSchema]]:
    userid = token.authenticate_user(request.headers.get("authorization"))
    if userid != owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    owner_obj = owner_service.get_owner_by_id(db_session, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )

    pets_obj = owner_service.get_owner_pets(db_session, owner_id)
    if not pets_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} has not pets !!!",
        )
    return pets_obj


@router.get("/pet/{pet_id}", status_code=200, response_model=pet.ShowPetSchema)
async def get_pet_info(
    request: Request,
    pet_id: str,
    db_session: Session = Depends(db.get_db),
) -> pet.ShowPetSchema:
    userid = token.authenticate_user(request.headers.get("authorization"))

    # PASS OWNER_ID ALONG WITH PET_ID (Need to implement)

    # if userid != owner_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Invalid owner. Authentication failed !!!",
    #     )
    pet_obj = owner_service.get_pet_info(db_session, pet_id)
    if not pet_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with pet id: {pet_id} not found !!!",
        )
    return pet_obj


# @router.get(
#     "/pet/{pet_id}", status_code=200, response_model=owner.ShowPetOwnerSchema
# )
# async def get_pet_owner(
#     pet_id: str,
#     db_session: Session = Depends(db.get_db),
# ):
#     pet_obj = owner_service.get_pet_info(db_session, pet_id)
#     if not pet_obj:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Pet with pet id: {pet_id} not found !!!",
#         )

#     owner_id = owner_service.get_pet_owner_id(db_session, pet_id)
#     owner_obj = owner_service.get_owner(db_session, owner_id)
#     return owner_obj


@router.post(
    "/booking",
    status_code=status.HTTP_201_CREATED,
    response_model=booking.ShowBookingSchema,
)
async def create_booking(
    header: Request,
    request: booking.BookingSchema,
    db_session: Session = Depends(db.get_db),
) -> booking.ShowBookingSchema:
    print(header.headers.get("authorization"))
    userid = token.authenticate_user(header.headers.get("authorization"))
    print(request.owner_id, userid)
    print(request)
    print(type(request))
    if userid != request.owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    unique_id = str(uuid.uuid4())
    date_of_booking = datetime.utcnow()
    new_booking = owner_service.create_booking(
        db_session,
        unique_id,
        request.caretaker_id,
        request.owner_id,
        date_of_booking,
        request.instruction,
    )
    new_booking_obj = {
        "id": unique_id,
        "owner_id": request.owner_id,
        "caretaker_id": request.caretaker_id,
        "date_of_booking": date_of_booking,
        "instruction": request.instruction,
    }
    return booking.ShowBookingSchema(**new_booking_obj)


@router.get(
    "/owner_booking/{owner_id}",
    status_code=200,
    response_model=Optional[List[booking.ShowBookingSchema]],
)
async def get_owner_bookings(
    request: Request,
    owner_id: str,
    db_session: Session = Depends(db.get_db),
) -> Optional[List[booking.ShowBookingSchema]]:
    userid = token.authenticate_user(request.headers.get("authorization"))
    if userid != owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    owner_obj = owner_service.get_owner_by_id(db_session, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id {owner_id} not found ...",
        )
    booking_objs = owner_service.get_owner_bookings(db_session, owner_id)
    if not booking_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id {owner_id} has no bookings ...",
        )
    owner_bookings = []
    for booking_obj in booking_objs:
        value = {
            "id": booking_obj.id,
            "caretaker_id": booking_obj.caretaker_id,
            "owner_id": booking_obj.owner_id,
            "date_of_booking": booking_obj.date_of_booking,
            "instruction": booking_obj.instruction,
        }
        owner_bookings.append(booking.ShowBookingSchema(**value))
    return owner_bookings


@router.get(
    "/booking/{booking_id}", status_code=200, response_model=booking.ShowBookingSchema
)
async def get_booking_info(
    request: Request,
    booking_id: str,
    db_session: Session = Depends(db.get_db),
) -> booking.ShowBookingSchema:
    userid = token.authenticate_user(request.headers.get("authorization"))

    # PASS OWNER_ID ALONG WITH BOOKING_ID (Need to implement)

    # if userid != owner_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Invalid owner. Authentication failed !!!",
    #     )

    booking_obj = owner_service.get_booking_info(db_session, booking_id)
    if not booking_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking id {booking_id} not found ...",
        )
    value = {
        "id": booking_obj.id,
        "caretaker_id": booking_obj.caretaker_id,
        "owner_id": booking_obj.owner_id,
        "date_of_booking": booking_obj.date_of_booking,
        "instruction": booking_obj.instruction,
    }
    return booking.ShowBookingSchema(**value)


@router.post(
    "/review",
    status_code=status.HTTP_201_CREATED,
    response_model=booking.ShowReviewSchema,
)
async def create_review(
    header: Request,
    request: booking.ReviewSchema,
    db_session: Session = Depends(db.get_db),
) -> booking.ShowReviewSchema:
    userid = token.authenticate_user(header.headers.get("authorization"))

    # PASS OWNER_ID ALONG (Need to implement)

    # if userid != owner_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Invalid owner. Authentication failed !!!",
    #     )
    unique_id = str(uuid.uuid4())
    date_of_review = datetime.utcnow()
    new_review = owner_service.create_review(
        db_session,
        unique_id,
        request.booking_id,
        request.rating,
        date_of_review,
        request.comment,
    )
    new_review_obj = {
        "id": unique_id,
        "booking_id": request.booking_id,
        "rating": request.rating,
        "date_of_review": date_of_review,
        "comment": request.comment,
    }
    return booking.ShowBookingSchema(**new_review_obj)


@router.get(
    "/recommend/{owner_id}",
    status_code=200,
    response_model=Optional[List[caretaker.ShowCaretakerSchema]],
)
async def recommend_caretaker(
    request: Request,
    owner_id: str,
    db_session: Session = Depends(db.get_db),
) -> Optional[List[caretaker.ShowCaretakerSchema]]:
    userid = token.authenticate_user(request.headers.get("authorization"))
    if userid != owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid owner. Authentication failed !!!",
        )
    owner_obj = owner_service.get_owner_by_id(db_session, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    caretaker_objs = caretaker_service.find_nearby_caretakers(
        db_session, owner_obj.lat, owner_obj.lon
    )

    if not caretaker_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No caretakers nearby for Owner with owner id {owner_id} ...",
        )
    return caretaker_objs
