from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import authentication, owner, caretaker
from database import db, authentication_service, owner_service, caretaker_service
from utils import token, hashing


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
    hashed_password = hashing.get_hashed_password(request.password)
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


@router.post(
    "/owner_login", summary="Login owner", response_model=authentication.TokenSchema
)
def owner_login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db.get_db),
):
    owner_obj = owner_service.get_owner_by_email(db, request.username)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )

    if not hashing.verify_password(request.password, owner_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )

    owner_email, owner_id = owner_obj.email, owner_obj.id
    owner_token_obj = authentication_service.get_owner_tokens(db, owner_id)
    if owner_token_obj:
        if not token.token_expired(owner_token_obj.refresh_token_expiry):
            if token.token_expired(owner_token_obj.access_token_expiry):
                access_token_obj = token.create_access_token(owner_email)
                token_obj = authentication_service.edit_owner_access_token(
                    db,
                    owner_token_obj,
                    access_token_obj["access_token"],
                    access_token_obj["access_token_expiry"],
                )
                return {
                    "access_token": access_token_obj["access_token"],
                    "token_type": "bearer",
                }

            return {
                "access_token": owner_token_obj.access_token,
                "token_type": "bearer",
            }

        access_token_obj = token.create_access_token(owner_email)
        refresh_token_obj = token.create_refresh_token(owner_email)
        token_obj = authentication_service.edit_owner_all_tokens(
            db,
            owner_token_obj,
            access_token_obj["access_token"],
            access_token_obj["access_token_expiry"],
            refresh_token_obj["refresh_token"],
            refresh_token_obj["refresh_token_expiry"],
        )
        return {
            "access_token": access_token_obj["access_token"],
            "token_type": "bearer",
        }

    access_token_obj = token.create_access_token(owner_email)
    refresh_token_obj = token.create_refresh_token(owner_email)
    token_obj = authentication_service.store_owner_tokens(
        db,
        owner_id,
        access_token_obj["access_token"],
        access_token_obj["access_token_expiry"],
        refresh_token_obj["refresh_token"],
        refresh_token_obj["refresh_token_expiry"],
    )
    return {"access_token": access_token_obj["access_token"], "token_type": "bearer"}


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
    hashed_password = hashing.get_hashed_password(request.password)
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
    "/caretaker_login",
    summary="Login careatker",
    response_model=authentication.TokenSchema,
)
def caretaker_login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db.get_db),
):
    caretaker_obj = caretaker_service.get_caretaker_by_email(db, request.username)
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )
    if not hashing.verify_password(request.password, caretaker_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials !!!",
        )

    caretaker_email, caretaker_id = caretaker_obj.email, caretaker_obj.id
    caretaker_token_obj = authentication_service.get_caretaker_tokens(db, caretaker_id)
    if caretaker_token_obj:
        if not token.token_expired(caretaker_token_obj.refresh_token_expiry):
            if token.token_expired(caretaker_token_obj.access_token_expiry):
                access_token_obj = token.create_access_token(caretaker_email)
                token_obj = authentication_service.edit_caretaker_access_token(
                    db,
                    caretaker_token_obj,
                    access_token_obj["access_token"],
                    access_token_obj["access_token_expiry"],
                )
                return {
                    "access_token": access_token_obj["access_token"],
                    "token_type": "bearer",
                }

            return {
                "access_token": caretaker_token_obj.access_token,
                "token_type": "bearer",
            }

        access_token_obj = token.create_access_token(caretaker_email)
        refresh_token_obj = token.create_refresh_token(caretaker_email)
        token_obj = authentication_service.edit_caretaker_all_tokens(
            db,
            caretaker_token_obj,
            access_token_obj["access_token"],
            access_token_obj["access_token_expiry"],
            refresh_token_obj["refresh_token"],
            refresh_token_obj["refresh_token_expiry"],
        )
        return {
            "access_token": access_token_obj["access_token"],
            "token_type": "bearer",
        }

    access_token_obj = token.create_access_token(caretaker_email)
    refresh_token_obj = token.create_refresh_token(caretaker_email)
    token_obj = authentication_service.store_caretaker_tokens(
        db,
        caretaker_id,
        access_token_obj["access_token"],
        access_token_obj["access_token_expiry"],
        refresh_token_obj["refresh_token"],
        refresh_token_obj["refresh_token_expiry"],
    )
    return {"access_token": access_token_obj["access_token"], "token_type": "bearer"}


# @router.get("/protected")
# def protected_route(Authorize: AuthJWT = Depends(token.validate_access_token)):
#     current_user = Authorize.get_jwt_identity()
#     return {"message": f"Hello, {current_user}"}
