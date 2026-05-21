import pytest
from fastapi import HTTPException, status
from app.services.auth_service import require_roles
from tests.shared.user_constants import *
from app.schemas.token_schema import TokenData
from tests.unit.service.base.base_service_test import BaseServiceTest

class TestRequireRole(BaseServiceTest):
    def test_require_roles_allowed(self):
        user = TokenData(
            username=USER_NAME,
            userGuid=USER_GUID,
            email=VALID_EMAIL,
            role=ROLE_ADMIN,
        )
        checker = require_roles(ROLE_ADMIN, ROLE_EMPLOYEE)
        result = checker(user)
        assert result.role == ROLE_ADMIN

    def test_require_roles_forbidden(self):
        user = TokenData(
            username=USER_NAME,
            userGuid=INVALID_GUID,
            email=INVALID_EMAIL,
            role=ROLE_COMPANY,
        )
        checker = require_roles(ROLE_ADMIN)

        with pytest.raises(HTTPException) as exc:
            checker(user)

        assert exc.value.status_code == status.HTTP_403_FORBIDDEN
        assert exc.value.detail == "Access denied."
