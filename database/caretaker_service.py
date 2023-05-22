from sqlalchemy.orm import Session
from models import models
from utils import recommendation


def create_caretaker(
    db: Session,
    name: str,
    address: str,
    email: str,
    password: str,
    phone: str,
    lat: int,
    lon: int,
):
    new_caretaker = models.Caretaker(
        name=name,
        address=address,
        email=email,
        password=password,
        phone=phone,
        lat=lat,
        lon=lon,
    )
    db.add(new_caretaker)
    db.commit()
    db.refresh(new_caretaker)
    return new_caretaker


def get_caretaker(db: Session, caretaker_id: str):
    caretaker_obj = (
        db.query(models.Caretaker).filter(models.Caretaker.id == caretaker_id).first()
    )
    return caretaker_obj


def get_all_caretakers(db: Session):
    caretaker_objs = db.query(models.Caretaker).all()
    return caretaker_objs


def edit_caretaker(
    db: Session, caretaker_obj: models.Caretaker, address: str, lat: int, lon: int
):
    caretaker_obj.address = address
    caretaker_obj.lat = lat
    caretaker_obj.lon = lon
    db.commit()
    db.refresh(caretaker_obj)
    return caretaker_obj


def edit_caretaker_rating(db: Session, caretaker_obj: models.Caretaker, rating: float):
    caretaker_obj.rating = rating
    db.commit()
    db.refresh(caretaker_obj)
    return caretaker_obj


def delete_caretaker(db: Session, caretaker_id: str):
    caretaker_obj = (
        db.query(models.Caretaker).filter(models.Owner.id == caretaker_id).first()
    )
    if not caretaker_obj:
        return None

    db.delete(caretaker_obj)
    db.commit()
    return caretaker_obj


def get_caretaker_bookings(db: Session, caretaker_id: str):
    booking_objs = (
        db.query(models.Booking)
        .filter(models.Booking.caretaker_id == caretaker_id)
        .all()
    )
    return booking_objs


def get_booking_info(db: Session, booking_id: str):
    booking_obj = (
        db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    )
    return booking_obj


def find_nearby_caretakers(db: Session, lat: int, lon: int):
    caretaker_objs = db.query(models.Caretaker).all()
    caretaker_dist = [
        (
            recommendation.compute_distance(
                lat, lon, caretaker_obj.lat, caretaker_obj.lon
            ),
            caretaker_obj,
        )
        for caretaker_obj in caretaker_objs
    ]
    sorted_caretaker_dist = sorted(caretaker_dist, key=lambda x: x[0])
    return [sorted_caretaker_dist[1] for _ in range(3)]


def compute_caretaker_rating(db: Session, caretaker_id: str):
    caretaker_bookings = (
        db.query(models.Booking)
        .filter(models.Booking.caretaker_id == caretaker_id)
        .all()
    )
    booking_ids = [
        caretaker_booking.booking_id for caretaker_booking in caretaker_bookings
    ]
    booking_review_objs = [
        db.query(models.Review).filter(models.Review.booking_id == booking_id).first()
        for booking_id in booking_ids
    ]
    caretaker_ratings = [
        booking_review_obj.rating for booking_review_obj in booking_review_objs
    ]
    return sum(caretaker_ratings) / len(caretaker_ratings)
