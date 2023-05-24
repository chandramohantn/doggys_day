from datetime import datetime, timedelta
from jose import JWTError, jwt
from database.config import jwtsettings
from schemas import authentication


def create_access_token(data: dict, expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=jwtsettings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = data.copy()
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(
        to_encode, jwtsettings.JWT_SECRET_KEY, algorithm=jwtsettings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=jwtsettings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = data.copy()
    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(
        to_encode, jwtsettings.JWT_REFRESH_SECRET_KEY, jwtsettings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(
            token, jwtsettings.JWT_SECRET_KEY, algorithms=[jwtsettings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = authentication.TokenData(email=email)
        return token_data.email
    except JWTError:
        raise credentials_exception
