"""
Authentication related methods
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from jose import jwt
from database import db, owner_service, caretaker_service
from schemas import owner, caretaker
from database.config import jwtsettings
from sqlalchemy.orm import Session
from utils import token


oauth2_owner_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/authentication/swagger_owner_login"
)
oauth2_caretaker_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/authentication/swagger_caretaker_login"
)


async def get_current_owner(
    token_data: str = Depends(oauth2_owner_scheme),
    db_session: Session = Depends(db.get_db),
) -> owner.ShowOwnerSchema:
    """
        Validate the current owner
    Args:
        token_data (str, optional): token passed from the client
        db_session (Session, optional): database session object

    Raises:
        credentials_exception: Invalid credentials
        HTTPException: Token expired

    Returns:
        owner.OwnerSchemaWithPermission: owner object
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.decode(
        token_data,
        jwtsettings.JWT_SECRET_KEY,
        algorithms=[jwtsettings.JWT_ALGORITHM],
    )

    owner_id, expiry_datetime = payload.get("sub", None), payload.get("exp", None)
    if (owner_id is None) or (expiry_datetime is None):
        raise credentials_exception

    if datetime.fromtimestamp(expiry_datetime) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    owner_obj = owner_service.get_owner_by_id(db_session, owner_id)
    if owner_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found !!!",
        )

    return owner_obj


async def get_current_caretaker(
    token_data: str = Depends(oauth2_owner_scheme),
    db_session: Session = Depends(db.get_db),
) -> caretaker.ShowCaretakerSchema:
    """
        Validate the current caretaker
    Args:
        token_data (str, optional): token passed from the client
        db_session (Session, optional): database session object

    Raises:
        credentials_exception: Invalid credentials
        HTTPException: Token expired

    Returns:
        caretaker.CaretakerSchemaWithPermission: caretaker object
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.decode(
        token_data,
        jwtsettings.JWT_SECRET_KEY,
        algorithms=[jwtsettings.JWT_ALGORITHM],
    )

    caretaker_id, expiry_datetime = payload.get("sub", None), payload.get("exp", None)
    if (caretaker_id is None) or (expiry_datetime is None):
        raise credentials_exception

    if datetime.fromtimestamp(expiry_datetime) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    caretaker_obj = caretaker_service.get_caretaker_by_id(db_session, caretaker_id)
    if caretaker_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found !!!",
        )

    return caretaker_obj


async def refresh_current_owner(
    token_data: str = Depends(oauth2_owner_scheme),
) -> dict:
    """
        Refresh the current owner token
    Args:
        token_data (str, optional): token passed from the client
        db_session (Session, optional): database session object

    Raises:
        credentials_exception: Invalid credentials
        HTTPException: Token expired

    Returns:
        authentication.TokenSchema: Token object
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.decode(
        token_data,
        jwtsettings.JWT_REFRESH_SECRET_KEY,
        algorithms=[jwtsettings.JWT_ALGORITHM],
    )

    owner_id, expiry_datetime = payload.get("sub", None), payload.get("exp", None)
    if (owner_id is None) or (expiry_datetime is None):
        raise credentials_exception

    if datetime.fromtimestamp(expiry_datetime) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = token.create_access_token(owner_id)
    token_obj = {"access_token": access_token}
    return token_obj


async def refresh_current_caretaker(
    token_data: str = Depends(oauth2_caretaker_scheme),
) -> dict:
    """
        Refresh the current caretaker token
    Args:
        token_data (str, optional): token passed from the client
        db_session (Session, optional): database session object

    Raises:
        credentials_exception: Invalid credentials
        HTTPException: Token expired

    Returns:
        authentication.TokenSchema: Token object
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.decode(
        token_data,
        jwtsettings.JWT_REFRESH_SECRET_KEY,
        algorithms=[jwtsettings.JWT_ALGORITHM],
    )

    caretaker_id, expiry_datetime = payload.get("sub", None), payload.get("exp", None)
    if (caretaker_id is None) or (expiry_datetime is None):
        raise credentials_exception

    if datetime.fromtimestamp(expiry_datetime) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = token.create_access_token(caretaker_id)
    token_obj = {"access_token": access_token}
    return token_obj
