from fastapi import APIRouter, status, Depends, HTTPException
from schemas import owner, pet
from sqlalchemy.orm import Session
from config import database
from models import models
from typing import List

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_owner(request: owner.OwnerSchema, db: Session = Depends(database.get_db)):
    new_owner = models.Owner(
        name=request.name,
        address=request.address,
        email=request.email,
        phone=request.phone,
        lat=request.lat,
        lon=request.lon,
    )
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return {"data": f"Owner created with name {request.name}"}


@router.get("/owner/{id}", status_code=200, response_model=owner.ShowOwnerSchema)
def get_owner(
    owner_id: str,
    db: Session = Depends(database.get_db),
):
    owner_obj = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    return owner_obj


@router.get("/owner", status_code=200, response_model=List[owner.ShowOwnerSchema])
def get_all_owners(
    db: Session = Depends(database.get_db),
):
    owner_objs = db.query(models.Owner).all()
    if not owner_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No owners available !!!",
        )
    return owner_objs


@router.put("/owner/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_owner(
    owner_id: str,
    request: owner.UpdateOwnerSchema,
    db: Session = Depends(database.get_db),
):
    owner_obj = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    owner_obj.address = request.address
    owner_obj.lat = request.lat
    owner_obj.lon = request.lon
    db.commit()
    db.refresh(owner_obj)
    return owner_obj


@router.delete("/owner/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_owner(owner_id: str, db: Session = Depends(database.get_db)):
    db.query(models.Owner).filter(models.Owner.id == owner_id).delete(
        synchronize_session=False
    )
    db.commit()
    return "Done !!!"


@router.post("/add_pet", status_code=status.HTTP_201_CREATED)
def add_pet(request: pet.PetSchema, db: Session = Depends(database.get_db)):
    new_pet = models.Owner(
        name=request.name,
        age=request.age,
        breed=request.breed,
        gender=request.gender,
        owner_id=request.owner_id,
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return {"data": f"Pet {request.name} created for owner ..."}


@router.get("/owner_pets/{id}", status_code=200, response_model=pet.ShowPetSchema)
def get_owner_pets(
    owner_id: str,
    db: Session = Depends(database.get_db),
):
    pets_obj = db.query(models.Pet).filter(models.Pet.owner_id == owner_id).all()
    if not pets_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    return pets_obj


@router.get("/pet_info/{id}", status_code=200, response_model=pet.PetSchema)
def get_pet_info(
    pet_id: str,
    db: Session = Depends(database.get_db),
):
    pet_obj = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with pet id: {pet_id} not found !!!",
        )
    return pet_obj
