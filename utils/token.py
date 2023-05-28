from typing import Union, Any
from jose import jwt
from datetime import timedelta, datetime
from database.config import jwtsettings


def create_access_token(subject: Union[str, Any]) -> dict:
    expires_delta = datetime.utcnow() + timedelta(
        minutes=jwtsettings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, jwtsettings.JWT_SECRET_KEY, jwtsettings.JWT_ALGORITHM
    )
    return {"access_token": encoded_jwt, "access_token_expiry": expires_delta}


def create_refresh_token(subject: Union[str, Any]) -> dict:
    expires_delta = datetime.utcnow() + timedelta(
        minutes=jwtsettings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, jwtsettings.JWT_REFRESH_SECRET_KEY, jwtsettings.JWT_ALGORITHM
    )
    return {"refresh_token": encoded_jwt, "refresh_token_expiry": expires_delta}


def token_expired(token_expiry):
    current_time = datetime.utcnow()
    return token_expiry < current_time
