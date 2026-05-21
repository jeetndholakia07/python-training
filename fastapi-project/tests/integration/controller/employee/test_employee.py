import pytest
from unittest.mock import patch
from tests.shared.employee_constants import *
from tests.factory.employee_factory import EmployeeFactory
import pytest

pytestmark = [pytest.mark.controller, pytest.mark.integration]

class TestEmployeeController:
    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.create_employee_func")
    async def test_create_employee_success(self, mock_create, async_client):
        request = EmployeeFactory().createEmployeeRequest().model_dump()
        mock_create.return_value = {"success": True, "message": "Employee created"}
        response = await async_client.post("/v1/employee", json=request)
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        assert body["message"] == "Employee created"
        mock_create.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.get_employees_by_company")
    async def test_get_all_employees(self, mock_get_all, async_client):
        mock_get_all.return_value = {
            "success": True,
            "data": {"data": [], "page": 0, "limit": 5, "totalItems": 0},
        }
        response = await async_client.get("/v1/employee")
        assert response.status_code == 200
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
        assert response.status_code == 200
        mock_get_by_id.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.update_employee_by_id")
    async def test_update_employee(self, mock_update, async_client):
        request = EmployeeFactory().updateEmployeeRequest().model_dump()
        mock_update.return_value = {"success": True, "message": "Updated"}
        response = await async_client.patch(
            f"/v1/employee/{EMPLOYEE_GUID}", json=request
        )
        assert response.status_code == 201
        mock_update.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.delete_employee_by_id")
    async def test_delete_employee(self, mock_delete, async_client):
        mock_delete.return_value = {"success": True, "message": "Deleted"}
        response = await async_client.delete(f"/v1/employee/{EMPLOYEE_GUID}")
        assert response.status_code == 200
        mock_delete.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.employee.get_employee_date")
    async def test_get_employee_by_date(self, mock_get_date, async_client):
        mock_get_date.return_value = {
            "success": True,
            "data": {"data": [], "page": 0, "limit": 5, "totalItems": 0},
        }
        response = await async_client.get(
            "/v1/employee/date",
            params={
                "start_date": SEARCH_END_DATE,
                "end_date": SEARCH_END_DATE,
                "pageLimit": 5,
                "pageNo": 1,
            },
        )
        assert response.status_code == 200
        mock_get_date.assert_called_once()
