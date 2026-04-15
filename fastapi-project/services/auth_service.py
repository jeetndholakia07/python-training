from sqlalchemy.orm import Session
from schemas.admin_schema import CreateAdminDTO, AdminLoginDTO
from schemas.token_schema import Token, TokenData
from utils.guid import generateGUID
from fastapi import HTTPException, Depends, status
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
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.db import get_db
import re

load_dotenv()
security = HTTPBearer()
email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%])[A-Za-z\d@#$%]{8,}$"

def create_user(db: Session, admin: CreateAdminDTO):
    try:
        verify_email_password(email=admin.email, password=admin.password)
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
        verify_email_password(email=user.email, password=user.password)
        db_user = get_admin_by_email_repo(db, user.email)
        if db_user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        hashed_password = get_hashed_password_repo(db, db_user.email)
        if verify_password(user.password, hashed_password[0]) == False:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        expiryTime = timedelta(minutes=int(os.getenv("TOKEN_EXPIRY_MINUTES")))
        data = TokenData(
            username=db_user.username, email=db_user.email, userGuid=db_user.guid
        ).model_dump()
        access_token = create_access_token(
            data=data,
            expires_delta=expiryTime,
        )
        return Token(access_token=access_token)
    except Exception:
        raise

def get_current_user(
    db=Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    email = payload.get("email")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = get_admin_by_email_repo(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return payload

def verify_email_password(email: str, password: str):
    emailMatch = re.match(email_regex, email)
    passwordMatch = re.match(password_regex, password)
    if emailMatch is None or passwordMatch is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")