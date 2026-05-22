import pytest
from unittest.mock import patch
from fastapi import HTTPException, status
from app.services.auth_service import create_user
from tests.shared.user_constants import *
from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.response_constants import *

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestCreateUser(BaseServiceTest):
    def test_create_user_success(self):
        request = self.user_factory.createUserRequest()
        with patch(
            "app.services.auth_service.get_user_by_email_repo"
        ) as mock_get_user, patch(
            "app.services.auth_service.generateGUID"
        ) as mock_guid, patch(
            "app.services.auth_service.get_password_hash"
        ) as mock_hash, patch(
            "app.services.auth_service.create_admin_repo"
        ) as mock_create_repo:
            mock_get_user.return_value = None
            mock_guid.return_value = USER_GUID
            mock_hash.return_value = PASSWORD_HASH
            result = create_user(self.db, request)
            assert result["success"] is True
            assert result["message"] == USER_REGISTER_SUCCESS
            mock_create_repo.assert_called_once()
            self.db.commit.assert_called_once()

    def test_create_user_exists(self):
        request = self.user_factory.createUserRequest()
        with patch("app.services.auth_service.get_user_by_email_repo") as mock_get_user:
            mock_get_user.return_value = {"email": VALID_EMAIL}
            with pytest.raises(HTTPException) as exc:
                create_user(self.db, request)

            self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, USER_EXISTS)

    def test_create_user_invalid_email(self):
        request = self.user_factory.createUserRequest()
        request.email = INVALID_EMAIL
        with pytest.raises(HTTPException) as exc:
            create_user(self.db, request)
        self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_CREDENTIALS)

    def test_create_user_invalid_password(self):
        request = self.user_factory.createUserRequest()
        request.password = INVALID_PASSWORD
        with pytest.raises(HTTPException) as exc:
            create_user(self.db, request)
        self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_CREDENTIALS)
