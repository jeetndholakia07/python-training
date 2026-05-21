from app.schemas.user_schema import Role
from app.schemas.token_schema import TokenData
from tests.shared.user_constants import *

def override_get_current_user():
    return TokenData(
        email=VALID_EMAIL, userGuid=USER_GUID, username=USER_NAME, role=ROLE_ADMIN
    )

def override_require_roles(*roles):
    def _inner():
        return override_get_current_user()
    return _inner
