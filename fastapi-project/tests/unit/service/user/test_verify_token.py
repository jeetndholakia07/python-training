import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException, status
from app.services.auth_service import get_current_user
from tests.shared.user_constants import *
from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.response_constants import *

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestVerifyToken(BaseServiceTest):
    def test_get_current_user_success(self):
        credentials = Mock()
        credentials.scheme = "Bearer"
        credentials.credentials = VALID_TOKEN
        fake_payload = {"email": VALID_EMAIL}
        fake_user = {
            "username": USER_NAME,
            "userGuid": USER_GUID,
            "email": VALID_EMAIL,
            "role": ROLE_ADMIN,
        }
        with patch(
            "app.services.auth_service.verify_access_token"
        ) as mock_verify_token, patch(
            "app.services.auth_service.get_user_by_email_repo"
        ) as mock_get_user:
            mock_verify_token.return_value = fake_payload
            mock_get_user.return_value = fake_user
            result = get_current_user(self.db, credentials)
            assert result.email == VALID_EMAIL
            assert result.userGuid == USER_GUID

    def test_get_current_user_invalid_scheme(self):
        credentials = Mock()
        credentials.scheme = "Basic"
        credentials.credentials = VALID_TOKEN
        with pytest.raises(HTTPException) as exc:
            get_current_user(self.db, credentials)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == INVALID_AUTH_SCHEME

    def test_get_current_user_invalid_token(self):
        credentials = Mock()
        credentials.scheme = "Bearer"
        credentials.credentials = INVALID_TOKEN
        with patch("app.services.auth_service.verify_access_token") as mock_verify:
            mock_verify.return_value = None
            with pytest.raises(HTTPException) as exc:
                get_current_user(self.db, credentials)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc.value.detail == INVALID_TOKEN_MSG

    def test_get_current_user_missing_email(self):
        credentials = Mock()
        credentials.scheme = "Bearer"
        credentials.credentials = VALID_TOKEN
        with patch("app.services.auth_service.verify_access_token") as mock_verify:
            mock_verify.return_value = {}
            with pytest.raises(HTTPException) as exc:
                get_current_user(self.db, credentials)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_not_found(self):
        credentials = Mock()
        credentials.scheme = "Bearer"
        credentials.credentials = VALID_TOKEN
        with patch(
            "app.services.auth_service.verify_access_token"
        ) as mock_verify, patch(
            "app.services.auth_service.get_user_by_email_repo"
        ) as mock_get_user:
            mock_verify.return_value = {"email": INVALID_EMAIL}
            mock_get_user.return_value = None
        with pytest.raises(HTTPException) as exc:
            get_current_user(self.db, credentials)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == AUTH_INVALID_MSG
