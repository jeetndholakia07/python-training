from app.schemas.user_schema import CreateUserDTO, UserLoginDTO
from tests.shared.user_constants import *

class UserFactory:
    def __init__(self):
        pass

    def createUserRequest(self):
        return CreateUserDTO(
            username=USER_NAME,
            email=VALID_EMAIL,
            password=VALID_PASSWORD,
            role=ROLE_EMPLOYEE
        )
    
    def loginUserRequest(self):
        return UserLoginDTO(
            email=VALID_EMAIL,
            password=VALID_PASSWORD
        )