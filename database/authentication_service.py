from sqlalchemy.orm import Session
from models import models
from datetime import datetime


def get_owner(db: Session, owner_id: str):
    owner_obj = (
        db.query(models.OwnerToken)
        .filter(models.OwnerToken.owner_id == owner_id)
        .first()
    )
    return owner_obj


def get_caretaker(db: Session, caretaker_id: str):
    caretaker_obj = (
        db.query(models.CaretakerToken)
        .filter(models.CaretakerToken.caretaker_id == caretaker_id)
        .first()
    )
    return caretaker_obj


def get_owner_tokens(db: Session, owner_id: str):
    owner_obj = (
        db.query(models.OwnerToken)
        .filter(models.OwnerToken.owner_id == owner_id)
        .first()
    )
    return owner_obj


def get_caretaker_tokens(db: Session, caretaker_id: str):
    caretaker_obj = (
        db.query(models.CaretakerToken)
        .filter(models.CaretakerToken.caretaker_id == caretaker_id)
        .first()
    )
    return caretaker_obj


def store_owner_tokens(
    db: Session,
    owner_id: str,
    access_token: str,
    access_token_expiry: datetime,
    refresh_token: str,
    refresh_token_expiry: datetime,
):
    new_token = models.OwnerToken(
        owner_id=owner_id,
        access_token=access_token,
        access_token_expiry=access_token_expiry,
        refresh_token=refresh_token,
        refresh_token_expiry=refresh_token_expiry,
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token


def store_caretaker_tokens(
    db: Session,
    caretaker_id: str,
    access_token: str,
    access_token_expiry: datetime,
    refresh_token: str,
    refresh_token_expiry: datetime,
):
    new_token = models.CaretakerToken(
        caretaker_id=caretaker_id,
        access_token=access_token,
        access_token_expiry=access_token_expiry,
        refresh_token=refresh_token,
        refresh_token_expiry=refresh_token_expiry,
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token


def edit_owner_access_token(
    db: Session,
    owner_obj: models.OwnerToken,
    access_token: str,
    access_token_expiry: datetime,
):
    owner_obj.access_token = access_token
    owner_obj.access_token_expiry = access_token_expiry
    db.commit()
    db.refresh(owner_obj)
    return owner_obj


def edit_caretaker_access_token(
    db: Session,
    caretaker_obj: models.CaretakerToken,
    access_token: str,
    access_token_expiry: datetime,
):
    caretaker_obj.access_token = access_token
    caretaker_obj.access_token_expiry = access_token_expiry
    db.commit()
    db.refresh(caretaker_obj)
    return caretaker_obj


def edit_owner_all_tokens(
    db: Session,
    owner_obj: models.OwnerToken,
    access_token: str,
    access_token_expiry: datetime,
    refresh_token: str,
    refresh_token_expiry: datetime,
):
    owner_obj.access_token = access_token
    owner_obj.access_token_expiry = access_token_expiry
    owner_obj.refresh_token = refresh_token
    owner_obj.refresh_token_expiry = refresh_token_expiry
    db.commit()
    db.refresh(owner_obj)
    return owner_obj


def edit_caretaker_all_tokens(
    db: Session,
    caretaker_obj: models.CaretakerToken,
    access_token: str,
    access_token_expiry: datetime,
    refresh_token: str,
    refresh_token_expiry: datetime,
):
    caretaker_obj.access_token = access_token
    caretaker_obj.access_token_expiry = access_token_expiry
    caretaker_obj.refresh_token = refresh_token
    caretaker_obj.refresh_token_expiry = refresh_token_expiry
    db.commit()
    db.refresh(caretaker_obj)
    return caretaker_obj
