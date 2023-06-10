"""
All api calls for admin
"""

import uuid
from typing import List, Optional
from fastapi import APIRouter, status, Depends, HTTPException
from schemas import owner, caretaker, administrator
from sqlalchemy.orm import Session
from database import db, admin_service
from utils import hashing, token

router = APIRouter()


@router.post(
    "/signup",
    summary="Create admin",
    status_code=status.HTTP_201_CREATED,
    response_model=administrator.AdminInfoSchema,
)
async def admin_signup(
    request: administrator.AdminSchema, db_session: Session = Depends(db.get_db)
) -> administrator.AdminInfoSchema:
    """
        POST api call for admin creation
    Args:
        request (administrator.AdminSchema): Admin info
        db (Session, optional): Get db session

    Raises:
        HTTPException: If email already exists
        HTTPException: If phone number already exists

    Returns:
        administrator.AdminInfoSchema: New admin object
    """

    admin_email = request.email
    admin_obj = owner_service.get_admin_by_email(db_session, admin_email)
    if admin_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email already exists !!!",
        )
    admin_phone = request.phone
    admin_obj = admin_service.get_admin_by_phone(db_session, admin_phone)
    if admin_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number already exists !!!",
        )

    unique_id = str(uuid.uuid4())
    hashed_password = hashing.get_hashed_password(request.password)
    new_admin = admin_service.create_admin(
        db_session,
        unique_id,
        request.name,
        request.address,
        request.email,
        hashed_password,
        request.phone,
        request.lat,
        request.lon,
    )
    new_admin_obj = {
        "name": new_admin.name,
        "address": new_admin.address,
        "lat": new_admin.lat,
        "lon": new_admin.lon,
    }
    return administrator.AdminInfoSchema(**new_admin_obj)


@router.get(
    "/owners", status_code=200, response_model=Optional[List[owner.ShowOwnerSchema]]
)
async def get_all_owners(
    db_session: Session = Depends(db.get_db),
) -> Optional[List[owner.ShowOwnerSchema]]:
    """_summary_

    Args:
        db_session (Session, optional): database session object
        get_current_user (_type_, optional): current owner dependency object

    Raises:
        HTTPException: No owners available

    Returns:
        List[owner.ShowOwnerSchema]: List of owner objects
    """

    owner_objs = owner_service.get_all_owners(db_session)
    if not owner_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No owners available !!!",
        )
    return owner_objs


@router.get(
    "/caretakers", status_code=200, response_model=List[caretaker.ShowCaretakerSchema]
)
async def get_all_caretakers(
    db: Session = Depends(db.get_db),
) -> List[caretaker.ShowCaretakerSchema]:
    caretaker_objs = caretaker_service.get_all_caretakers(db)
    if not caretaker_objs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No caretakers available !!!",
        )
    return caretaker_objs
