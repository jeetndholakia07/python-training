from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.employee_constants import *
from app.services.employee_service import delete_employee_by_id
import pytest
from unittest.mock import patch
from tests.shared.response_constants import *
from fastapi import HTTPException, status

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestDeleteEmployee(BaseServiceTest):
    def test_delete_employee_success(self):
        with patch("app.services.employee_service.is_valid_guid") as mock_guid, patch(
            "app.services.employee_service.get_employee_id"
        ) as mock_employee_id, patch(
            "app.services.employee_service.delete_employee_by_id_repo"
        ) as mock_delete_repo:
            mock_guid.return_value = True
            mock_employee_id.return_value = 1

            result = delete_employee_by_id(self.db, EMPLOYEE_GUID)

            assert result["success"] is True
            assert result["message"] == EMPLOYEE_DELETE_SUCCESS

            mock_delete_repo.assert_called_once_with(self.db, 1)

            self.db.commit.assert_called_once()

    def test_delete_employee_invalid_guid(self):
        with patch("app.services.employee_service.is_valid_guid") as mock_guid:
            mock_guid.return_value = False

            with pytest.raises(HTTPException) as exc:
                delete_employee_by_id(self.db, EMPLOYEE_GUID)

            self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_GUID_MSG)
