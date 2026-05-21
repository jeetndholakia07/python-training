from tests.unit.service.base.base_service_test import BaseServiceTest
from app.services.auth_service import verify_user
from tests.shared.user_constants import *
import pytest
import os
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestVerifyUser(BaseServiceTest):
    def test_verify_user_success(self):
        request = self.user_factory.loginUserRequest()
        with patch(
            "app.services.auth_service.get_user_by_email_repo"
        ) as mock_get_user, patch(
            "app.services.auth_service.get_hashed_password_repo"
        ) as mock_get_password, patch(
            "app.services.auth_service.verify_password"
        ) as mock_verify_password, patch(
            "app.services.auth_service.create_access_token"
        ) as mock_create_token:
            mock_get_user.return_value = {
                "username": USER_NAME,
                "userGuid": USER_GUID,
                "email": VALID_EMAIL,
                "role": ROLE_EMPLOYEE,
            }
            mock_get_password.return_value = [PASSWORD_HASH]
            mock_verify_password.return_value = True
            mock_create_token.return_value = VALID_TOKEN
            os.environ["TOKEN_EXPIRY_MINUTES"] = "30"
            result = verify_user(self.db, request)
            assert result.access_token == (VALID_TOKEN)

    def test_verify_user_not_found(self):
        request = self.user_factory.loginUserRequest()
        with patch("app.services.auth_service.get_user_by_email_repo") as mock_get_user:
            mock_get_user.return_value = None
            with pytest.raises(HTTPException) as exc:
                verify_user(self.db, request)
            self.assert_exception(
                exc,
                401,
                "Invalid email or password.",
            )

    def test_verify_user_invalid_password(self):
        request = self.user_factory.loginUserRequest()
        with patch(
            "app.services.auth_service.get_user_by_email_repo"
        ) as mock_get_user, patch(
            "app.services.auth_service.get_hashed_password_repo"
        ) as mock_get_password, patch(
            "app.services.auth_service.verify_password"
        ) as mock_verify_password:
            mock_get_user.return_value = {
                "username": USER_NAME,
                "userGuid": USER_GUID,
                "email": VALID_EMAIL,
                "role": ROLE_EMPLOYEE,
            }
            mock_get_password.return_value = [PASSWORD_HASH]
            mock_verify_password.return_value = False
            with pytest.raises(HTTPException) as exc:
                verify_user(self.db, request)
            self.assert_exception(
                exc,
                401,
                "Invalid email or password.",
            )

    def test_verify_user_invalid_email(self):
        request = self.user_factory.loginUserRequest()
        request.email = INVALID_EMAIL
        with pytest.raises(HTTPException) as exc:
            verify_user(self.db, request)
        self.assert_exception(
            exc,
            400,
            "Invalid email or password.",
        )

    def test_verify_user_invalid_password_format(self):
        request = self.user_factory.loginUserRequest()
        request.password = INVALID_PASSWORD
        with pytest.raises(HTTPException) as exc:
            verify_user(self.db, request)
        self.assert_exception(
            exc,
            400,
            "Invalid email or password.",
        )
