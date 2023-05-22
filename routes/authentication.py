from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import authentication, owner, caretaker
from sqlalchemy.orm import Session
from database import db, authentication_service, owner_service, caretaker_service
from utils.hashing import Hash
from utils import token

router = APIRouter()


@router.post(
    "/owner_signup",
    summary="Create an owner",
    status_code=status.HTTP_201_CREATED,
    response_model=owner.ShowOwnerSchema,
)
def owner_signup(request: owner.OwnerSchema, db: Session = Depends(db.get_db)):
    owner_email = request.email
    owner_obj = owner_service.get_owner_by_email(db, owner_email)
    if owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email already exists !!!",
        )
    owner_phone = request.phone
    owner_obj = owner_service.get_owner_by_phone(db, owner_phone)
    if owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number already exists !!!",
        )
    hashed_password = Hash.get_password_hash(request.password)
    new_owner = owner_service.create_owner(
        db,
        request.name,
        request.address,
        request.email,
        hashed_password,
        request.phone,
        request.lat,
        request.lon,
    )
    return new_owner


@router.post("/owner_login", summary="Login owner", response_model=authentication.Token)
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


@router.post(
    "/caretaker_signup",
    summary="Create a caretaker",
    status_code=status.HTTP_201_CREATED,
    response_model=caretaker.ShowCaretakerSchema,
)
def caretaker_signup(
    request: caretaker.CaretakerSchema, db: Session = Depends(db.get_db)
):
    caretaker_email = request.email
    caretaker_obj = caretaker_service.get_caretaker_by_email(db, caretaker_email)
    if caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email already exists !!!",
        )
    caretaker_phone = request.phone
    caretaker_obj = caretaker_service.get_caretaker_by_phone(db, caretaker_phone)
    if caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number already exists !!!",
        )
    hashed_password = Hash.get_password_hash(request.password)
    new_caretaker = caretaker_service.create_caretaker(
        db,
        request.name,
        request.address,
        request.email,
        hashed_password,
        request.phone,
        request.lat,
        request.lon,
    )
    return new_caretaker


@router.post(
    "/caretaker_login", summary="Login careatker", response_model=authentication.Token
)
def caretaker_login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)
):
    caretaker_obj = authentication_service.get_caretaker(db, request.username)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )
    if not Hash.verify_password(request.password, caretaker_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )

    access_token = token.create_access_token(data={"sub": caretaker_obj.email})
    return {"access_token": access_token, "token_type": "bearer"}
