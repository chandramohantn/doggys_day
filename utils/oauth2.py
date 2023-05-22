from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils import token
from database import authentication_service
from database import db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/authentication/owner_login")


async def get_current_owner(
    token_data: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_id = token.verify_token(token_data, credentials_exception)
    owner_obj = authentication_service.get_owner(db, token_id)
    return owner_obj


async def get_current_caretaker(
    token_data: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_id = token.verify_token(token_data, credentials_exception)
    caretaker_obj = authentication_service.get_caretaker(db, token_id)
    return caretaker_obj
