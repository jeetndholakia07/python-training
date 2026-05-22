from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.employee_constants import *
from app.services.employee_service import get_employee_by_id
import pytest
from unittest.mock import patch
from fastapi import HTTPException, status
from tests.shared.response_constants import *

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestGetEmployeeById(BaseServiceTest):
    def test_get_employee_by_id_success(self):
        with patch("app.services.employee_service.is_valid_guid") as mock_guid, patch(
            "app.services.employee_service.get_employee_by_id_repo"
        ) as mock_repo:
            response = self.employee_factory.getEmployeeResponse()

            mock_guid.return_value = True
            mock_repo.return_value = response

            result = get_employee_by_id(self.db, EMPLOYEE_GUID)

            assert result["success"] is True
            assert result["data"] == response

    def test_get_employee_by_id_invalid_guid(self):
        with patch("app.services.employee_service.is_valid_guid") as mock_guid:
            mock_guid.return_value = False

            with pytest.raises(HTTPException) as exc:
                get_employee_by_id(self.db, EMPLOYEE_GUID)

            self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_GUID_MSG)

    def test_get_employee_by_id_not_found(self):
        with patch("app.services.employee_service.is_valid_guid") as mock_guid, patch(
            "app.services.employee_service.get_employee_by_id_repo"
        ) as mock_repo:

            mock_guid.return_value = True
            mock_repo.return_value = None

            with pytest.raises(HTTPException) as exc:
                get_employee_by_id(self.db, EMPLOYEE_GUID)

            self.assert_exception(exc, status.HTTP_404_NOT_FOUND, EMPLOYEE_NOT_FOUND)
