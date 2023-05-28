from fastapi import APIRouter, status, Depends, HTTPException
from schemas import owner, pet, booking, caretaker
from sqlalchemy.orm import Session
from database import db, owner_service, caretaker_service
from typing import List
from utils import oauth2, hashing

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_owner(request: owner.OwnerSchema, db: Session = Depends(db.get_db)):
    new_owner = owner_service.create_owner(
        db,
        request.name,
        request.address,
        request.email,
        hashing.get_hashed_password(request.password),
        request.phone,
        request.lat,
        request.lon,
    )
    return {"data": f"Owner created with name {new_owner.name}"}


@router.get("/owner/{id}", status_code=200, response_model=owner.ShowOwnerSchema)
def get_owner(owner_id: str, db: Session = Depends(db.get_db)):
    owner_obj = owner_service.get_owner_by_id(db, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    return owner_obj


@router.get("/owner", status_code=200, response_model=List[owner.ShowOwnerSchema])
def get_all_owners(
    db: Session = Depends(db.get_db),
    get_current_user=Depends(oauth2.get_current_owner),
):
    owner_objs = owner_service.get_all_owners(db)
    if not owner_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No owners available !!!",
        )
    return owner_objs


@router.put("/owner/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_owner(
    owner_id: str, request: owner.UpdateOwnerSchema, db: Session = Depends(db.get_db)
):
    owner_obj = owner_service.get_owner_by_id(db, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    owner_obj = owner_service.edit_owner(
        db, owner_obj, request.address, request.lat, request.lon
    )
    return owner_obj


@router.delete("/owner/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(owner_id: str, db: Session = Depends(db.get_db)):
    owner_obj = owner_service.delete_owner(db, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )

    return None


@router.post("/add_pet", status_code=status.HTTP_201_CREATED)
def add_pet(request: pet.PetSchema, db: Session = Depends(db.get_db)):
    new_pet = owner_service.create_pet(
        db, request.name, request.age, request.breed, request.gender, request.owner_id
    )
    return {"data": f"Pet {new_pet.name} created for owner ..."}


@router.get("/owner_pets/{id}", status_code=200, response_model=List[pet.ShowPetSchema])
def get_owner_pets(
    owner_id: str,
    db: Session = Depends(db.get_db),
):
    owner_obj = owner_service.get_owner(db, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )

    pets_obj = owner_service.get_owner_pets(db, owner_id)
    if not pets_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} has not pets !!!",
        )
    return pets_obj


@router.get("/pet_info/{id}", status_code=200, response_model=pet.PetSchema)
def get_pet_info(
    pet_id: str,
    db: Session = Depends(db.get_db),
):
    pet_obj = owner_service.get_pet_info(db, pet_id)
    if not pet_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with pet id: {pet_id} not found !!!",
        )
    return pet_obj


@router.get("/pet_owner/{id}", status_code=200, response_model=owner.ShowPetOwnerSchema)
def get_pet_owner(
    pet_id: str,
    db: Session = Depends(db.get_db),
):
    pet_obj = owner_service.get_pet_info(db, pet_id)
    if not pet_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with pet id: {pet_id} not found !!!",
        )

    owner_id = owner_service.get_pet_owner_id(db, pet_id)
    owner_obj = owner_service.get_owner(db, owner_id)
    return owner_obj


@router.post("/booking", status_code=status.HTTP_201_CREATED)
def create_booking(request: booking.BookingSchema, db: Session = Depends(db.get_db)):
    new_booking = owner_service.create_booking(
        db,
        request.caretaker_id,
        request.owner_id,
        request.date_of_booking,
        request.instruction,
    )
    return {
        "data": f"Booking created for owner {request.owner_id} with booking id: {new_booking.booking_id} ..."
    }


@router.get(
    "/owner_booking/{id}", status_code=200, response_model=List[booking.BookingSchema]
)
def get_owner_bookings(owner_id: str, db: Session = Depends(db.get_db)):
    owner_obj = owner_service.get_owner(db, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id {owner_id} not found ...",
        )
    booking_objs = owner_service.get_owner_bookings(db, owner_id)
    if not booking_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id {owner_id} has no bookings ...",
        )
    return booking_objs


@router.get("/booking/{id}", status_code=200, response_model=booking.BookingSchema)
def get_booking_info(booking_id: str, db: Session = Depends(db.get_db)):
    booking_obj = owner_service.get_booking_info(db, booking_id)
    if not booking_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking id {booking_id} not found ...",
        )
    return booking_obj


@router.post("/review", status_code=status.HTTP_201_CREATED)
def create_review(request: booking.ReviewSchema, db: Session = Depends(db.get_db)):
    new_review = owner_service.create_review(
        db,
        request.booking_id,
        request.rating,
        request.date_of_review,
        request.comment,
    )
    return {
        "data": f"Review created for booking with booking id: {new_review.booking_id} ..."
    }


@router.get(
    "/recommend/{id}",
    status_code=200,
    response_model=List[caretaker.ShowCaretakerSchema],
)
def recommend_caretaker(owner_id: str, db: Session = Depends(db.get_db)):
    owner_obj = owner_service.get_owner(db, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    caretaker_objs = caretaker_service.find_nearby_caretakers(
        db, owner_obj.lat, owner_obj.lon
    )
    if not caretaker_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No caretakers nearby for Owner with owner id {owner_id} ...",
        )
    return caretaker_objs
