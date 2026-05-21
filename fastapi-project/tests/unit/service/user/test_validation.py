from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.user_constants import *
from app.services.auth_service import verify_email_password
from fastapi import HTTPException
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestValidation(BaseServiceTest):
    def test_verify_email_password_success(self):
        verify_email_password(
            VALID_EMAIL,
            VALID_PASSWORD,
        )

    def test_verify_email_invalid_email(self):
        with pytest.raises(HTTPException) as exc:
            verify_email_password(
                INVALID_EMAIL,
                VALID_PASSWORD,
            )
        self.assert_exception(
            exc,
            400,
            "Invalid email or password.",
        )

    def test_verify_invalid_password(self):
        with pytest.raises(HTTPException) as exc:
            verify_email_password(
                VALID_EMAIL,
                INVALID_PASSWORD,
            )
        self.assert_exception(
            exc,
            400,
            "Invalid email or password.",
        )
