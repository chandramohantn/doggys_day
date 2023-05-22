from datetime import datetime, timedelta
from jose import JWTError, jwt
from database.config import jwtsettings
from schemas import authentication


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwtsettings.SECRET_KEY, algorithm=jwtsettings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(
            token, jwtsettings.SECRET_KEY, algorithms=[jwtsettings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = authentication.TokenData(email=email)
        print(token_data, token_data.email)
        return token_data.email
    except JWTError:
        raise credentials_exception
