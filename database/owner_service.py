from sqlalchemy.orm import Session
from models import models


def create_owner(
    db: Session, name: str, address: str, email: str, phone: str, lat: int, lon: int
):
    new_owner = models.Owner(
        name=name,
        address=address,
        email=email,
        phone=phone,
        lat=lat,
        lon=lon,
    )
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return new_owner


def get_owner(db: Session, owner_id: str):
    owner_obj = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    return owner_obj


def get_all_owners(db: Session):
    owner_objs = db.query(models.Owner).all()
    return owner_objs


def edit_owner(db: Session, owner_obj: models.Owner, address: str, lat: int, lon: int):
    owner_obj.address = address
    owner_obj.lat = lat
    owner_obj.lon = lon
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
    db: Session, name: str, age: int, breed: str, gender: str, owner_id: str
):
    new_pet = models.Pet(
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
