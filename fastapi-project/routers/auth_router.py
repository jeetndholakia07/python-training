from fastapi import APIRouter, Depends, Body
from schemas.user_schema import CreateUserDTO, UserLoginDTO
from config.db import get_db
from schemas.response_schema import ResponseModel
from services.auth_service import create_user, verify_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=ResponseModel[None],
    status_code=201,
    response_model_exclude_none=True,
)
async def register_user(user: CreateUserDTO, db=Depends(get_db)):
    return create_user(db, user)

@router.post("/login")
async def login_user(db=Depends(get_db), user: UserLoginDTO = Body()):
    return verify_user(db, user)