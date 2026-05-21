from tests.shared.user_constants import *
from app.models.user import User
from app.schemas.user_schema import Role

class UserBuilder:
    def __init__(self):
        self._data = {
            "username": USER_NAME,
            "guid": USER_GUID,
            "email": VALID_EMAIL,
            "password_hash": PASSWORD_HASH,
            "role": ROLE_EMPLOYEE
        }

    def with_guid(self, guid: str):
        self._data["guid"] = guid
        return self

    def with_email(self, email: str):
        self._data["email"] = email
        return self

    def with_password(self, pwd: str):
        self._data["password_hash"] = pwd
        return self

    def with_username(self, username: str):
        self._data["username"] = username
        return self

    def with_role(self, role: Role):
        self._data["role"] = role
        return self

    def build(self):
        return User(**self._data.copy())
