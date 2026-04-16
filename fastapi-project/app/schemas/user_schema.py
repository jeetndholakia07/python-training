from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    A = "Admin"
    E = "Employee"
    C = "Company"

class CreateUserDTO(BaseModel):
    username: str
    email: str
    password: str
    role: Role

class UserLoginDTO(BaseModel):
    email: str
    password: str