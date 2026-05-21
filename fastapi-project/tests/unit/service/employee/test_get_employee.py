from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.employee_constants import *
from app.services.employee_service import get_employee_id
import pytest
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestGetEmployeeId(BaseServiceTest):
    def test_get_employee_id_success(self):
        with patch("app.services.employee_service.get_employee_id_repo") as mock_repo:

            mock_repo.return_value = 1

            result = get_employee_id(self.db, EMPLOYEE_GUID)

            assert result == 1

    def test_get_employee_id_not_found(self):
        with patch("app.services.employee_service.get_employee_id_repo") as mock_repo:

            mock_repo.return_value = None

            with pytest.raises(HTTPException) as exc:
                get_employee_id(self.db, EMPLOYEE_GUID)

            self.assert_exception(exc, 404, "Employee not found")
