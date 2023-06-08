"""
Apis related to owner and caretaker authentication
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas import authentication
from database import db, owner_service, caretaker_service
from utils import token, hashing


router = APIRouter()


@router.post(
    "/owner_signin", summary="Login owner", response_model=authentication.TokenSchema
)
async def owner_login(
    request: authentication.LoginSchema,
    db_session: Session = Depends(db.get_db),
) -> authentication.TokenSchema:
    """
        POST api call for owner login
    Args:
        request (authentication.LoginSchema): Request from client
        db_session (Session, optional): database session object

    Raises:
        HTTPException: Invalid credentials
        HTTPException: Invalid credentials

    Returns:
        authentication.TokenSchema: Token object
    """

    owner_obj = owner_service.get_owner_by_email(db_session, request.username)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    if not hashing.verify_password(request.password, owner_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    owner_id, owner_name = owner_obj.id, owner_obj.name
    access_token = token.create_access_token(owner_id)
    refresh_token = token.create_refresh_token(owner_id)
    token_obj = {
        "name": owner_name,
        "id": owner_id,
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    return authentication.TokenSchema(**token_obj)


@router.post(
    "/caretaker_signin",
    summary="Login careatker",
    response_model=authentication.TokenSchema,
)
async def caretaker_login(
    request: authentication.LoginSchema,
    db_session: Session = Depends(db.get_db),
):
    """
        POST api call for caretaker login
    Args:
        request (authentication.LoginSchema): Request from client
        db_session (Session, optional): database session object

    Raises:
        HTTPException: Invalid credentials
        HTTPException: Invalid credentials

    Returns:
        authentication.TokenSchema: Token object
    """
    caretaker_obj = caretaker_service.get_caretaker_by_email(
        db_session, request.username
    )
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )
    if not hashing.verify_password(request.password, caretaker_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    caretaker_id, caretaker_name = caretaker_obj.id, caretaker_obj.name
    access_token = token.create_access_token(caretaker_id)
    refresh_token = token.create_refresh_token(caretaker_id)
    token_obj = {
        "name": caretaker_name,
        "id": caretaker_obj.id,
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    return authentication.TokenSchema(**token_obj)


@router.post(
    "/owner_refresh",
    summary="Refresh owner token",
    response_model=authentication.TokenSchema,
)
async def owner_refresh(
    request: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(db.get_db),
):
    """
        POST api call for owner refresh
    Args:
        request (OAuth2PasswordRequestForm, optional): dependency request.
        db_session (Session, optional): database session object

    Raises:
        HTTPException: Invalid credentials
        HTTPException: Invalid credentials

    Returns:
        authentication.TokenSchema: Token object
    """
    owner_obj = owner_service.get_owner_by_email(db_session, request.username)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )
    if not hashing.verify_password(request.password, owner_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    owner_id = owner_obj.id
    access_token = token.create_access_token(owner_id)
    refresh_token = token.create_refresh_token(owner_id)
    token_obj = {
        "name": owner_obj.name,
        "id": owner_obj.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    return authentication.TokenSchema(**token_obj)


@router.post(
    "/caretaker_refresh",
    summary="Refresh caretaker token",
    response_model=authentication.TokenSchema,
)
async def caretaker_refresh(
    request: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(db.get_db),
):
    """
        POST api call for caretaker refresh
    Args:
        request (OAuth2PasswordRequestForm, optional): dependency request.
        db_session (Session, optional): database session object

    Raises:
        HTTPException: Invalid credentials
        HTTPException: Invalid credentials

    Returns:
        authentication.TokenSchema: Token object
    """
    caretaker_obj = caretaker_service.get_caretaker_by_email(
        db_session, request.username
    )
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )
    if not hashing.verify_password(request.password, caretaker_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    caretaker_id = caretaker_obj.id
    access_token = token.create_access_token(caretaker_id)
    refresh_token = token.create_refresh_token(caretaker_id)
    token_obj = {
        "name": caretaker_obj.name,
        "id": caretaker_obj.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    return authentication.TokenSchema(**token_obj)


@router.post(
    "/swagger_owner_login",
    summary="Swagger owner login",
    response_model=authentication.TokenSchema,
)
async def swagger_owner_login(
    request: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(db.get_db),
) -> authentication.TokenSchema:
    """
        POST api call for owner login
    Args:
        request (OAuth2PasswordRequestForm, optional): dependency request.
        db_session (Session, optional): database session object

    Raises:
        HTTPException: Invalid credentials
        HTTPException: Invalid credentials

    Returns:
        authentication.TokenSchema: Token object
    """

    owner_obj = owner_service.get_owner_by_email(db_session, request.username)
    if not owner_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    if not hashing.verify_password(request.password, owner_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    owner_id = owner_obj.id
    access_token = token.create_access_token(owner_id)
    refresh_token = token.create_refresh_token(owner_id)
    token_obj = {"access_token": access_token, "refresh_token": refresh_token}
    return authentication.TokenSchema(**token_obj)


@router.post(
    "/swagger_caretaker_login",
    summary="Swagger caretaker login",
    response_model=authentication.TokenSchema,
)
async def swagger_caretaker_login(
    request: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(db.get_db),
):
    """
        POST api call for caretaker login
    Args:
        request (OAuth2PasswordRequestForm, optional): dependency request.
        db_session (Session, optional): database session object

    Raises:
        HTTPException: Invalid credentials
        HTTPException: Invalid credentials

    Returns:
        authentication.TokenSchema: Token object
    """
    caretaker_obj = caretaker_service.get_caretaker_by_email(
        db_session, request.username
    )
    if not caretaker_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )
    if not hashing.verify_password(request.password, caretaker_obj.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials !!!",
        )

    caretaker_id = caretaker_obj.id
    access_token = token.create_access_token(caretaker_id)
    refresh_token = token.create_refresh_token(caretaker_id)
    token_obj = {"access_token": access_token, "refresh_token": refresh_token}
    return authentication.TokenSchema(**token_obj)
