from fastapi import APIRouter, status, Depends, HTTPException
from schemas import caretaker
from sqlalchemy.orm import Session
from database import db
from models import models
from typing import List

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_caretaker(
    request: caretaker.CaretakerSchema, db: Session = Depends(db.get_db)
):
    new_caretaker = models.Caretaker(
        name=request.name,
        address=request.address,
        email=request.email,
        phone=request.phone,
        lat=request.lat,
        lon=request.lon,
    )
    db.add(new_caretaker)
    db.commit()
    db.refresh(new_caretaker)
    return {"data": f"Caretaker created with name {request.name}"}


@router.get(
    "/caretaker/{id}", status_code=200, response_model=caretaker.ShowCaretakerSchema
)
def get_caretaker(
    caretaker_id: str,
    db: Session = Depends(db.get_db),
):
    caretaker_obj = (
        db.query(models.Caretaker).filter(models.Caretaker.id == caretaker_id).first()
    )
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    return caretaker_obj


@router.get(
    "/caretaker", status_code=200, response_model=List[caretaker.ShowCaretakerSchema]
)
def get_all_caretakers(
    db: Session = Depends(db.get_db),
):
    caretaker_objs = db.query(models.Caretaker).all()
    if not caretaker_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No caretakers available !!!",
        )
    return caretaker_objs


@router.put("/caretaker/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_caretaker(
    caretaker_id: str,
    request: caretaker.UpdateCaretakerSchema,
    db: Session = Depends(db.get_db),
):
    caretaker_obj = (
        db.query(models.Caretaker).filter(models.Caretaker.id == caretaker_id).first()
    )
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    caretaker_obj.address = request.address
    caretaker_obj.lat = request.lat
    caretaker_obj.lon = request.lon
    db.commit()
    db.refresh(caretaker_obj)
    return caretaker_obj


@router.delete("/caretaker/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_caretaker(caretaker_id: str, db: Session = Depends(db.get_db)):
    db.query(models.Caretaker).filter(models.Caretaker.id == caretaker_id).delete(
        synchronize_session=False
    )
    db.commit()
    return "Done !!!"
