import pytest
from unittest.mock import patch
from tests.shared.employee_constants import *
from tests.factory.employee_factory import EmployeeFactory
from tests.shared.response_constants import *
from fastapi import status
import pytest

pytestmark = [pytest.mark.controller, pytest.mark.integration]

class TestEmployeeController:
    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.create_employee_func")
    async def test_create_employee_success(self, mock_create, async_client):
        request = EmployeeFactory().createEmployeeRequest().model_dump()
        mock_create.return_value = {"success": True, "message": EMPLOYEE_CREATE_SUCCESS}
        response = await async_client.post("/v1/employee", json=request)
        assert response.status_code == status.HTTP_201_CREATED
        body = response.json()
        assert body["success"] is True
        assert body["message"] == EMPLOYEE_CREATE_SUCCESS
        mock_create.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.get_employees_by_company")
    async def test_get_all_employees(self, mock_get_all, async_client):
        mock_get_all.return_value = {
            "success": True,
            "data": {
                "data": [],
                "page": DEFAULT_PAGE_NUMBER,
                "limit": DEFAULT_PAGE_LIMIT,
                "totalItems": DEFAULT_TOTAL_ITEMS,
            },
        }
        response = await async_client.get("/v1/employee")
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert "data" in body
        mock_get_all.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.get_employee_by_id")
    async def test_get_employee_by_id(self, mock_get_by_id, async_client):
        mock_get_by_id.return_value = {
            "success": True,
            "data": EmployeeFactory().getEmployeeResponse().model_dump(),
        }
        response = await async_client.get(f"/v1/employee/{EMPLOYEE_GUID}")
        assert response.status_code == status.HTTP_200_OK
        mock_get_by_id.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.update_employee_by_id")
    async def test_update_employee(self, mock_update, async_client):
        request = EmployeeFactory().updateEmployeeRequest().model_dump()
        mock_update.return_value = {"success": True, "message": EMPLOYEE_UPDATE_SUCCESS}
        response = await async_client.patch(
            f"/v1/employee/{EMPLOYEE_GUID}", json=request
        )
        assert response.status_code == status.HTTP_201_CREATED
        mock_update.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.delete_employee_by_id")
    async def test_delete_employee(self, mock_delete, async_client):
        mock_delete.return_value = {"success": True, "message": EMPLOYEE_DELETE_SUCCESS}
        response = await async_client.delete(f"/v1/employee/{EMPLOYEE_GUID}")
        assert response.status_code == status.HTTP_200_OK
        mock_delete.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.get_employee_date")
    async def test_get_employee_by_date(self, mock_get_date, async_client):
        mock_get_date.return_value = {
            "success": True,
            "data": {
                "data": [],
                "page": DEFAULT_PAGE_NUMBER,
                "limit": DEFAULT_PAGE_LIMIT,
                "totalItems": DEFAULT_TOTAL_ITEMS,
            },
        }
        response = await async_client.get(
            "/v1/employee/date",
            params={
                "start_date": SEARCH_END_DATE,
                "end_date": SEARCH_END_DATE,
                "pageLimit": DEFAULT_PAGE_LIMIT,
                "pageNo": DEFAULT_PAGE_NUMBER,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        mock_get_date.assert_called_once()
