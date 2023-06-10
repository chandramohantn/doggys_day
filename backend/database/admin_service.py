from sqlalchemy.orm import Session
from models import models
from datetime import datetime


def get_owner_by_email(db: Session, owner_email: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.email == owner_email).first()
    return owner_obj


def get_owner_by_phone(db: Session, owner_phone: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.phone == owner_phone).first()
    return owner_obj


def get_all_owners(db: Session):
    owner_objs = db.query(models.Owner).all()
    return owner_objs


def get_caretaker_by_email(db: Session, caretaker_email: str):
    caretaker_obj = (
        db.query(models.Caretaker)
        .filter(models.Caretaker.id == caretaker_email)
        .first()
    )
    return caretaker_obj


def get_caretaker_by_phone(db: Session, caretaker_phone: str):
    caretaker_obj = (
        db.query(models.Caretaker)
        .filter(models.Caretaker.id == caretaker_phone)
        .first()
    )
    return caretaker_obj
