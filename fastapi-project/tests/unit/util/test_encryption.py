from app.utils.encryption import get_password_hash, verify_password
from tests.shared.user_constants import *
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.util]

class TestPasswordUtils:
    def test_get_password_hash_success(self):
        password = VALID_PASSWORD
        hashed_password = get_password_hash(password)
        assert hashed_password is not None
        assert hashed_password != password
        assert isinstance(hashed_password, str)

    def test_verify_password_success(self):
        password = VALID_PASSWORD
        hashed_password = get_password_hash(password)
        result = verify_password(password, hashed_password)
        assert result is True

    def test_verify_password_invalid(self):
        correct_password = VALID_PASSWORD
        wrong_password = INVALID_PASSWORD
        hashed_password = get_password_hash(correct_password)
        result = verify_password(wrong_password, hashed_password)
        assert result is False
