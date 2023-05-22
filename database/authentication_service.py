from sqlalchemy.orm import Session
from models import models


def get_owner(db: Session, owner_email: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.email == owner_email).first()
    return owner_obj


def get_caretaker(db: Session, caretaker_email: str):
    caretaker_obj = (
        db.query(models.Caretaker)
        .filter(models.Caretaker.email == caretaker_email)
        .first()
    )
    return caretaker_obj
