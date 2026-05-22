from tests.unit.service.base.base_service_test import BaseServiceTest
from app.services.employee_service import get_employee_date
import pytest
from unittest.mock import patch
from fastapi import HTTPException, status
from tests.shared.employee_constants import *
from tests.shared.response_constants import *

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestGetEmployeeDate(BaseServiceTest):
    def test_get_employee_date_success(self):
        with patch("app.services.employee_service.get_employee_date_repo") as mock_repo:
            response = self.employee_factory.getEmployeeResponse()

            mock_repo.return_value = {
                "data": response,
                "page": DEFAULT_PAGE_NUMBER,
                "limit": DEFAULT_PAGE_LIMIT,
                "totalItems": DEFAULT_TOTAL_ITEMS,
            }

            result = get_employee_date(self.db, SEARCH_START_DATE, SEARCH_END_DATE)

            assert result["success"] is True
            assert result["data"]["data"] == response
            assert result["data"]["totalItems"] == DEFAULT_TOTAL_ITEMS

    def test_get_employee_date_invalid_date(self):
        with pytest.raises(HTTPException) as exc:
            get_employee_date(self.db, INVALID_DATE, SEARCH_END_DATE)

        self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_DATE)

    def test_get_employee_date_invalid_range(self):
        with pytest.raises(HTTPException) as exc:
            get_employee_date(self.db, SEARCH_START_DATE, SEARCH_END_DATE_INVALID)

        self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, END_DATE_LONGER_MSG)
