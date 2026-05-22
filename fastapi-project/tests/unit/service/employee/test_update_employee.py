from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.employee_constants import *
from app.services.employee_service import update_employee_by_id
import pytest
from unittest.mock import patch
from fastapi import HTTPException, status
from tests.shared.response_constants import *

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestUpdateEmployee(BaseServiceTest):
    def test_update_employee_success(self):
        with patch("app.services.employee_service.is_valid_guid") as mock_guid, patch(
            "app.services.employee_service.get_employee_id"
        ) as mock_employee_id, patch(
            "app.services.employee_service.update_employee_id_repo"
        ) as mock_update_repo:
            request = self.employee_factory.updateEmployeeRequest()
            mock_guid.return_value = True
            mock_employee_id.return_value = 1
            result = update_employee_by_id(self.db, EMPLOYEE_GUID, request)
            assert result["success"] is True
            assert result["message"] == EMPLOYEE_UPDATE_SUCCESS
            mock_update_repo.assert_called_once_with(self.db, request, 1)
            self.db.commit.assert_called_once()

    def test_update_employee_invalid_guid(self):
        request = self.employee_factory.updateEmployeeRequest()
        with patch("app.services.employee_service.is_valid_guid") as mock_guid:
            mock_guid.return_value = False

            with pytest.raises(HTTPException) as exc:
                update_employee_by_id(self.db, EMPLOYEE_GUID, request)

            self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_GUID_MSG)
