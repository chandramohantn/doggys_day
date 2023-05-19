from fastapi import APIRouter, status, Depends, HTTPException
from schemas import owner, pet
from sqlalchemy.orm import Session
from database import db, owner_service
from typing import List

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_owner(request: owner.OwnerSchema, db: Session = Depends(db.get_db)):
    new_owner = owner_service.create_owner(
        db,
        request.name,
        request.address,
        request.email,
        request.phone,
        request.lat,
        request.lon,
    )
    return {"data": f"Owner created with name {new_owner.name}"}


@router.get("/owner/{id}", status_code=200, response_model=owner.ShowOwnerSchema)
def get_owner(owner_id: str, db: Session = Depends(db.get_db)):
    owner_obj = owner_service.get_owner(db, owner_id)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Owner with owner id: {owner_id} not found !!!",
        )
    return owner_obj


@router.get("/owner", status_code=200, response_model=List[owner.ShowOwnerSchema])
def get_all_owners(db: Session = Depends(db.get_db)):
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
    owner_obj = owner_service.get_owner(db, owner_id)
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


@router.get("/owner_pets/{id}", status_code=200, response_model=pet.ShowPetSchema)
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
