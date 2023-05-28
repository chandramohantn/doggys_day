from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from jose import jwt
from database import db, authentication_service, owner_service, caretaker_service
from schemas import authentication
from database.config import jwtsettings
from sqlalchemy.orm import Session

oauth2_owner_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/authentication/owner_login"
)
oauth2_caretaker_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/authentication/caretaker_login"
)


async def get_current_owner(
    token_data: str = Depends(oauth2_owner_scheme), db: Session = Depends(db.get_db)
):
    try:
        payload = jwt.decode(
            token_data,
            jwtsettings.JWT_SECRET_KEY,
            algorithms=[jwtsettings.JWT_ALGORITHM],
        )
        token_data = authentication.TokenPayloadSchema(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    owner_email = token_data.sub

    if owner_email is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    owner_obj = owner_service.get_owner_by_email(db, owner_email)
    owner_obj = authentication_service.get_owner(db, owner_obj.id)
    owner_dict = {"owner_id": owner_obj.id, "token": owner_obj.access_token}
    return authentication.RefreshOwnerTokenSchema(**owner_dict)


async def get_current_caretaker(
    token_data: str = Depends(oauth2_caretaker_scheme), db: Session = Depends(db.get_db)
):
    try:
        payload = jwt.decode(
            token_data,
            jwtsettings.JWT_SECRET_KEY,
            algorithms=[jwtsettings.JWT_ALGORITHM],
        )
        token_data = authentication.TokenPayloadSchema(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    caretaker_email = token_data.sub

    if caretaker_email is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    caretaker_obj = caretaker_service.get_caretaker_by_email(db, caretaker_email)
    caretaker_obj = authentication_service.get_owner(db, caretaker_obj.id)
    caretaker_dict = {
        "caretaker_id": caretaker_obj.id,
        "token": caretaker_obj.access_token,
    }
    return authentication.RefreshCaretakerTokenSchema(**caretaker_dict)
