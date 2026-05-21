from tests.unit.service.base.base_service_test import BaseServiceTest
from app.services.employee_service import get_employee_date
import pytest
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestGetEmployeeDate(BaseServiceTest):
    def test_get_employee_date_success(self):
        with patch("app.services.employee_service.get_employee_date_repo") as mock_repo:

            response = self.employee_factory.getEmployeeResponse()

            mock_repo.return_value = {"data": response, "totalItems": 1}

            result = get_employee_date(self.db, "01-01-2024", "10-01-2024")

            assert result["success"] is True
            assert result["data"]["data"] == response
            assert result["data"]["totalItems"] == 1

    def test_get_employee_date_invalid_date(self):
        with pytest.raises(HTTPException) as exc:
            get_employee_date(self.db, "2024-01-01", "10-01-2024")

        self.assert_exception(exc, 400, "Invalid start or end date")

    def test_get_employee_date_invalid_range(self):
        with pytest.raises(HTTPException) as exc:
            get_employee_date(self.db, "10-01-2024", "01-01-2024")

        self.assert_exception(exc, 400, "End date cannot be shorter than start date")
