from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.company_constants import *
from app.services.company_service import get_companies
import pytest
from unittest.mock import patch

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestGetCompanies(BaseServiceTest):
    def test_get_companies_success(self):
        with patch(
            "app.services.company_service.get_all_company_repo"
        ) as mock_companies:
            response = self.company_factory.getCompanyResponse()
            pageLimit = DEFAULT_PAGE_LIMIT
            pageNo = DEFAULT_PAGE_NUMBER
            paginatedRes = {
                "data": response,
                "page": pageNo,
                "limit": pageLimit,
                "totalItems": DEFAULT_TOTAL_ITEMS,
            }
            mock_companies.return_value = paginatedRes
            result = get_companies(
                self.db, COMPANY_ACTIVE, pageLimit=pageLimit, pageNo=pageNo
            )
            assert result["success"] is True
            assert result["data"]["page"] == pageNo
            assert result["data"]["limit"] == pageLimit
            assert result["data"]["data"] == response
            assert result["data"]["totalItems"] == DEFAULT_TOTAL_ITEMS

            mock_companies.assert_called_once()
