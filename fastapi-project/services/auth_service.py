from sqlalchemy.orm import Session
from schemas.admin_schema import CreateAdminDTO, AdminLoginDTO
from schemas.token_schema import Token
from utils.guid import generateGUID
from fastapi import HTTPException, Depends
from repositories.admin_repository import (
    create_admin_repo,
    get_admin_by_email_repo,
    get_hashed_password_repo,
)
from utils.encryption import get_password_hash, verify_password
from utils.token import create_access_token, verify_access_token
from datetime import timedelta
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from config.db import get_db

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
        expiryTime = timedelta(minutes=int(os.getenv("TOKEN_EXPIRY_MINUTES")))
        access_token = create_access_token(
            data={"username": user.username, "email": user.email, "guid": user.guid},
            expires_delta=expiryTime,
        )
        return Token(access_token=access_token, token_type="bearer")
    except Exception:
        raise

def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentails"
        )
    email = payload.get("email")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid credentails")
    user = get_admin_by_email_repo(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return payload