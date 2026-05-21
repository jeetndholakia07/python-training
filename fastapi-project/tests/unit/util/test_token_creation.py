from app.utils.token import create_access_token, verify_access_token
from fastapi import HTTPException, status
from datetime import timedelta
import pytest
from unittest.mock import patch
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from tests.shared.user_constants import *

pytestmark = [pytest.mark.unit, pytest.mark.util]

class TestJWTUtils:
    def test_create_access_token_with_expiry(self):
        data = {USER_NAME: VALID_EMAIL}
        with patch("app.utils.token.jwt.encode") as mock_encode, patch(
            "app.utils.token.os.getenv"
        ) as mock_getenv:
            mock_encode.return_value = VALID_TOKEN
            mock_getenv.side_effect = lambda key: {
                "JWT_SECRET": "secret",
                "JWT_ALGORITHM": "HS256",
            }.get(key)

            result = create_access_token(data, timedelta(minutes=30))
            assert result == VALID_TOKEN
            mock_encode.assert_called_once()

    def test_create_access_token_without_expiry(self):
        data = {USER_NAME: VALID_EMAIL}
        with patch("app.utils.token.jwt.encode") as mock_encode, patch(
            "app.utils.token.os.getenv"
        ) as mock_getenv:
            mock_encode.return_value = VALID_TOKEN
            mock_getenv.side_effect = lambda key: {
                "JWT_SECRET": "secret",
                "JWT_ALGORITHM": "HS256",
            }.get(key)
            result = create_access_token(data, None)
            assert result == VALID_TOKEN
            mock_encode.assert_called_once()

    def test_verify_access_token_success(self):
        token = VALID_TOKEN
        payload = {USER_NAME: VALID_EMAIL}
        with patch("app.utils.token.jwt.decode") as mock_decode, patch(
            "app.utils.token.os.getenv"
        ) as mock_getenv:
            mock_decode.return_value = payload
            mock_getenv.side_effect = lambda key: {
                "JWT_SECRET": "secret",
                "JWT_ALGORITHM": "HS256",
            }.get(key)
            result = verify_access_token(token)
            assert result == payload
            mock_decode.assert_called_once_with(
                token,
                "secret",
                algorithms=["HS256"],
                options={"require": ["exp"]},
            )

    def test_verify_access_token_expired(self):
        token = INVALID_TOKEN
        with patch("app.utils.token.jwt.decode") as mock_decode:
            mock_decode.side_effect = ExpiredSignatureError()
            with pytest.raises(HTTPException) as exc:
                verify_access_token(token)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc.value.detail == "Credentials have expired."
            assert exc.value.headers == {"WWW-Authenticate": "Bearer"}

    def test_verify_access_token_invalid(self):
        token = INVALID_TOKEN
        with patch("app.utils.token.jwt.decode") as mock_decode:
            mock_decode.side_effect = InvalidTokenError()
            with pytest.raises(HTTPException) as exc:
                verify_access_token(token)
            assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
            assert exc.value.detail == "Could not validate credentials."
            assert exc.value.headers == {"WWW-Authenticate": "Bearer"}
