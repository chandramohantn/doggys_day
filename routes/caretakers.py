from fastapi import APIRouter, status, Depends, HTTPException
from schemas import caretaker
from sqlalchemy.orm import Session
from database import db, caretaker_service
from typing import List

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_caretaker(
    request: caretaker.CaretakerSchema, db: Session = Depends(db.get_db)
):
    new_caretaker = caretaker_service.create_caretaker(
        db,
        request.name,
        request.address,
        request.email,
        request.phone,
        request.lat,
        request.lon,
    )
    return {"data": f"Caretaker created with name {new_caretaker.name}"}


@router.get(
    "/caretaker/{id}", status_code=200, response_model=caretaker.ShowCaretakerSchema
)
def get_caretaker(caretaker_id: str, db: Session = Depends(db.get_db)):
    caretaker_obj = caretaker_service.get_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    return caretaker_obj


@router.get(
    "/caretaker", status_code=200, response_model=List[caretaker.ShowCaretakerSchema]
)
def get_all_caretakers(db: Session = Depends(db.get_db)):
    caretaker_objs = caretaker_service.get_all_caretakers(db)
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
    caretaker_obj = caretaker_service.get_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )
    caretaker_obj = caretaker_service.edit_caretaker(
        db, caretaker_obj, request.address, request.lat, request.lon
    )
    return caretaker_obj


@router.delete("/caretaker/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_caretaker(caretaker_id: str, db: Session = Depends(db.get_db)):
    caretaker_obj = caretaker_service.delete_caretaker(db, caretaker_id)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Caretaker with caretaker id: {caretaker_id} not found !!!",
        )

    return None
