from sqlalchemy.orm import Session
from models import models
from datetime import datetime


def create_owner(
    db: Session,
    unique_id: str,
    name: str,
    address: str,
    email: str,
    password: str,
    phone: str,
    lat: int,
    lon: int,
):
    new_owner = models.Owner(
        id=unique_id,
        name=name,
        address=address,
        email=email,
        password=password,
        phone=phone,
        lat=lat,
        lon=lon,
    )
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return new_owner


def get_owner_by_id(db: Session, owner_id: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    return owner_obj


def get_owner_by_email(db: Session, owner_email: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.email == owner_email).first()
    return owner_obj


def get_owner_by_phone(db: Session, owner_phone: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.phone == owner_phone).first()
    return owner_obj


def edit_owner(
    db: Session,
    owner_obj: models.Owner,
    address: str,
    email: str,
    phone: str,
    lat: int,
    lon: int,
):
    owner_obj.address = address
    owner_obj.email = email
    owner_obj.phone = phone
    owner_obj.lat = lat
    owner_obj.lon = lon
    db.commit()
    db.refresh(owner_obj)
    return owner_obj


def edit_owner_email(db: Session, owner_obj: models.Owner, email: str):
    owner_obj.email = email
    db.commit()
    db.refresh(owner_obj)
    return owner_obj


def edit_owner_phone(db: Session, owner_obj: models.Owner, phone: str):
    owner_obj.phone = phone
    db.commit()
    db.refresh(owner_obj)
    return owner_obj


def delete_owner(db: Session, owner_id: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    if not owner_obj:
        return None

    db.delete(owner_obj)
    db.commit()
    return owner_obj


def create_pet(
    db: Session,
    unique_id: str,
    name: str,
    age: int,
    breed: str,
    gender: str,
    owner_id: str,
):
    new_pet = models.Pet(
        id=unique_id,
        name=name,
        age=age,
        breed=breed,
        gender=gender,
        owner_id=owner_id,
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet


def get_pet_info(db: Session, pet_id: str):
    pet_obj = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    return pet_obj


def get_owner_pets(db: Session, owner_id: str):
    pets_obj = db.query(models.Pet).filter(models.Pet.owner_id == owner_id).all()
    return pets_obj


def get_pet_owner_id(db: Session, pet_id: str):
    pet_obj = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    owner_id = pet_obj.owner_id
    return owner_id


def create_booking(
    db: Session,
    unique_id: str,
    caretaker_id: str,
    owner_id: str,
    date_of_booking: datetime,
    instruction: str,
):
    new_booking = models.Booking(
        id=unique_id,
        caretaker_id=caretaker_id,
        owner_id=owner_id,
        date_of_booking=date_of_booking,
        instruction=instruction,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def get_owner_bookings(db: Session, owner_id: str):
    booking_objs = (
        db.query(models.Booking).filter(models.Booking.owner_id == owner_id).all()
    )
    return booking_objs


def get_booking_info(db: Session, booking_id: str):
    booking_obj = (
        db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    )
    return booking_obj


def create_review(
    db: Session,
    unique_id: str,
    booking_id: str,
    rating: int,
    date_of_review: datetime,
    comment: str,
):
    new_review = models.Review(
        id=unique_id,
        booking_id=booking_id,
        rating=rating,
        date_of_review=date_of_review,
        comment=comment,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review
