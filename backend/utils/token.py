"""
Methods related to authentication tokens
"""

from typing import Optional
from datetime import timedelta, datetime
from fastapi import HTTPException, Header, status
from jose import jwt, JWTError
from database.config import jwtsettings


def create_access_token(user_id: str) -> str:
    """
        Method for creating access token
    Args:
        user_id (str): User id

    Returns:
        str: Access token
    """
    expires_delta = datetime.utcnow() + timedelta(
        minutes=jwtsettings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": user_id}
    encoded_jwt = jwt.encode(
        to_encode, jwtsettings.JWT_SECRET_KEY, jwtsettings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(user_id: str) -> str:
    """
        Method for creating refresh token
    Args:
        user_id (str): User id

    Returns:
        str: Refresh token
    """

    expires_delta = datetime.utcnow() + timedelta(
        minutes=jwtsettings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": user_id}
    encoded_jwt = jwt.encode(
        to_encode, jwtsettings.JWT_REFRESH_SECRET_KEY, jwtsettings.JWT_ALGORITHM
    )
    return encoded_jwt


def token_expired(token_expiry: datetime) -> bool:
    """
        Check if the access token is expired
    Args:
        token_expiry (datetime): Token expiry datetime

    Returns:
        bool: True if token is expired else False
    """

    current_time = datetime.utcnow()
    return token_expiry < current_time


def authenticate_user(headers: str) -> Optional[str]:
    """
        Middleware function to authenticate the user
    Args:
        request (Request): Request from the client
        authorization (str, optional): _description_. Defaults to Header(...).

    Raises:
        HTTPException: Invalid token type
        HTTPException: Invalid access token
    """

    try:
        token_type, token = headers.split()
        if token_type.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Bearer token required.",
            )

        payload = jwt.decode(
            token, jwtsettings.JWT_SECRET_KEY, jwtsettings.JWT_ALGORITHM
        )
        return payload["sub"]
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )
