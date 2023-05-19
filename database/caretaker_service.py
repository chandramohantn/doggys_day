from sqlalchemy.orm import Session
from models import models


def create_caretaker(
    db: Session, name: str, address: str, email: str, phone: str, lat: int, lon: int
):
    new_caretaker = models.Caretaker(
        name=name,
        address=address,
        email=email,
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


def delete_caretaker(db: Session, caretaker_id: str):
    caretaker_obj = (
        db.query(models.Caretaker).filter(models.Owner.id == caretaker_id).first()
    )
    if not caretaker_obj:
        return None

    db.delete(caretaker_obj)
    db.commit()
    return caretaker_obj
