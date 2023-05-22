from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import authentication
from sqlalchemy.orm import Session
from database import db, authentication_service
from utils.hashing import Hash
from utils import token

router = APIRouter()


@router.post("/owner_login")
def owner_login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)
):
    owner_obj = authentication_service.get_owner(db, request.username)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )

    if not Hash.verify_password(request.password, owner_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )

    access_token = token.create_access_token(data={"sub": owner_obj.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/caretaker_login", response_model=authentication.ShowLoginSchema)
def caretaker_login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)
):
    caretaker_obj = authentication_service.get_owner(db, request.username)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )
    hashed_password = Hash.get_password_hash(request.password)
    if not Hash.verify_password(caretaker_obj.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )

    access_token = token.create_access_token(data={"sub": caretaker_obj.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "caretaker_id": caretaker_obj.id,
    }
