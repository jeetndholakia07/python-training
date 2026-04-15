from pydantic import BaseModel
from schemas.user_schema import Role

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: str
    userGuid: str
    email: str
    role: Role