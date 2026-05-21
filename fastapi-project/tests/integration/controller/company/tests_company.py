import pytest
from unittest.mock import patch

from tests.shared.company_constants import *
from tests.factory.company_factory import CompanyFactory
import pytest

pytestmark = [pytest.mark.controller, pytest.mark.integration]

class TestCompanyController:
    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.company.create_company_func")
    async def test_create_company_success(self, mock_create_company, async_client):
        request = CompanyFactory().createCompanyRequest().model_dump()
        mock_create_company.return_value = {
            "success": True,
            "message": "Company created",
            "data": None,
        }
        response = await async_client.post("/v1/company", json=request)
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        assert body["message"] == "Company created"

        mock_create_company.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.company.get_companies")
    async def test_get_all_companies(self, mock_get_companies, async_client):
        mock_get_companies.return_value = {"success": True, "data": [], "totalItems": 0}
        response = await async_client.get("/v1/company")
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        mock_get_companies.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.company.get_company_by_id")
    async def test_get_company_by_id(self, mock_get_company, async_client):
        mock_get_company.return_value = {
            "success": True,
            "data": CompanyFactory().getCompanyResponse().model_dump(),
        }
        response = await async_client.get(f"/v1/company/{COMPANY_GUID}")
        assert response.status_code == 200
        mock_get_company.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.company.update_company_desc")
    async def test_update_company(self, mock_update_company, async_client):
        request = CompanyFactory().updateCompanyRequest().model_dump()
        mock_update_company.return_value = {"success": True, "message": "Updated"}
        response = await async_client.patch(f"/v1/company/{COMPANY_GUID}", json=request)
        assert response.status_code == 201
        mock_update_company.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.api.v1.endpoints.company.delete_company_by_id")
    async def test_delete_company(self, mock_delete_company, async_client):
        mock_delete_company.return_value = {"success": True, "message": "Deleted"}
        response = await async_client.delete(f"/v1/company/{COMPANY_GUID}")
        assert response.status_code == 200
        mock_delete_company.assert_called_once()
