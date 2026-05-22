import pytest
from unittest.mock import patch
from tests.integration.controller.base.base_api_test import BaseApiTest
from tests.shared.user_constants import *
from tests.shared.response_constants import *
from fastapi import status
import pytest

pytestmark = [pytest.mark.controller, pytest.mark.integration]

class TestAuthController(BaseApiTest):
    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.auth.create_user")
    async def test_register_user_should_return_201(
        self, mock_create_user, async_client
    ):
        request = self.user_factory.createUserRequest().model_dump()
        mock_create_user.return_value = {
            "message": USER_REGISTER_SUCCESS,
            "success": True,
            "data": None,
        }
        response = await async_client.post("/v1/auth/register", json=request)
        assert response.status_code == status.HTTP_201_CREATED
        body = response.json()
        assert body["success"] is True
        assert body["message"] == USER_REGISTER_SUCCESS
        mock_create_user.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.auth.verify_user")
    async def test_login_user_should_return_200(self, mock_verify_user, async_client):
        request = self.user_factory.loginUserRequest().model_dump()
        mock_verify_user.return_value = {
            "accessToken": VALID_TOKEN,
            "tokenType": "bearer",
        }
        response = await async_client.post("/v1/auth/login", json=request)
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["accessToken"] == VALID_TOKEN
        assert body["tokenType"] == "bearer"
        mock_verify_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_user_should_return_400_for_invalid_email(
        self, async_client
    ):
        request = {
            "username": USER_NAME,
            "email": INVALID_EMAIL,
            "password": VALID_PASSWORD,
            "role": ROLE_EMPLOYEE,
        }
        response = await async_client.post("/v1/auth/register", json=request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_register_user_should_return_400_for_invalid_password(
        self, async_client
    ):
        request = {
            "username": USER_NAME,
            "email": VALID_EMAIL,
            "password": INVALID_PASSWORD,
            "role": ROLE_EMPLOYEE,
        }
        response = await async_client.post("/v1/auth/register", json=request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_login_user_should_return_400_for_invalid_email(self, async_client):
        request = {"email": INVALID_EMAIL, "password": VALID_PASSWORD}
        response = await async_client.post("/v1/auth/login", json=request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_login_user_should_return_422_when_body_missing(self, async_client):
        response = await async_client.post("/v1/auth/login", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
