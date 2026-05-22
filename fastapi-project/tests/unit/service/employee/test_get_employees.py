from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.employee_constants import *
from tests.shared.company_constants import COMPANY_NAME
from app.services.employee_service import get_employees_by_company
import pytest
from unittest.mock import patch

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestGetEmployees(BaseServiceTest):
    def test_get_employees_success(self):
        with patch("app.services.employee_service.get_employees_repo") as mock_repo:
            response = self.employee_factory.getEmployeeResponse()
            pageLimit = DEFAULT_PAGE_LIMIT
            pageNo = DEFAULT_PAGE_NUMBER
            paginatedRes = {
                "data": response,
                "totalItems": DEFAULT_TOTAL_ITEMS,
                "page": DEFAULT_PAGE_NUMBER,
                "limit": DEFAULT_PAGE_LIMIT,
            }

            mock_repo.return_value = paginatedRes

            result = get_employees_by_company(
                self.db, COMPANY_NAME, EMPLOYEE_ACTIVE, pageLimit, pageNo
            )

            assert result["success"] is True
            assert result["data"]["page"] == pageNo
            assert result["data"]["limit"] == pageLimit
            assert result["data"]["data"] == response
            assert result["data"]["totalItems"] == DEFAULT_TOTAL_ITEMS

            mock_repo.assert_called_once()
