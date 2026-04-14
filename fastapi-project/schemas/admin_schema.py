from pydantic import BaseModel

class CreateAdminDTO(BaseModel):
    username: str
    email: str
    password: str

class AdminLoginDTO(BaseModel):
    email: str
    password: str