from sqlalchemy.orm import Session
from ..schemas.admin_schema import CreateAdminDTO, AdminLoginDTO
from ..schemas.token_schema import Token, TokenData
from ..utils.guid import generateGUID
from fastapi import HTTPException, Depends
from ..repositories.admin_repository import (
    create_admin_repo,
    get_admin_by_email_repo,
    get_hashed_password_repo,
)
from ..utils.encryption import get_password_hash, verify_password
from ..utils.token import create_access_token, verify_access_token
from datetime import timedelta
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

load_dotenv()

def create_user(db: Session, admin: CreateAdminDTO):
    try:
        user = get_admin_by_email_repo(db, admin.email)
        if user is not None:
            raise HTTPException(status_code=400, detail="User already exists")
        guid = generateGUID()
        data = CreateAdminDTO(
            username=admin.username,
            email=admin.email,
            password=get_password_hash(admin.password),
        )
        create_admin_repo(db, data, guid)
        db.commit()
        return {"success": True, "message": "User registered successfully"}
    except Exception:
        db.rollback()
        raise

def verify_user(db: Session, user: AdminLoginDTO):
    try:
        user = get_admin_by_email_repo(db, user.email)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        hashed_password = get_hashed_password_repo(db, user.email)
        if verify_password(user.password, hashed_password) == False:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        expiryTime = timedelta(minutes=os.getenv("TOKEN_EXPIRY_MINUTES"))
        access_token = create_access_token(
            data={"username": user.username, "email": user.email, "guid": user.guid},
            expires_delta=expiryTime,
        )
        return Token(access_token=access_token, token_type="bearer")
    except Exception:
        raise