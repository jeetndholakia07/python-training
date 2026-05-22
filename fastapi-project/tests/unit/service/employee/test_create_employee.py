from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.employee_constants import *
from tests.shared.company_constants import *
from app.services.employee_service import create_employee_func
import pytest
from unittest.mock import patch
from tests.shared.response_constants import *
from fastapi import HTTPException, status

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestCreateEmployee(BaseServiceTest):
    def test_create_employee_success(self):
        with patch(
            "app.services.employee_service.get_company_id"
        ) as mock_company_id, patch(
            "app.services.employee_service.check_company_active"
        ) as mock_company_active, patch(
            "app.services.employee_service.generateGUID"
        ) as mock_guid, patch(
            "app.services.employee_service.create_employee_repo"
        ) as mock_create_repo:
            request = self.employee_factory.createEmployeeRequest()

            mock_company_id.return_value = 1
            mock_company_active.return_value = None
            mock_guid.return_value = EMPLOYEE_GUID

            result = create_employee_func(self.db, request)

            assert result["success"] is True
            assert result["message"] == EMPLOYEE_CREATE_SUCCESS

            mock_create_repo.assert_called_once_with(self.db, request, 1, EMPLOYEE_GUID)

            self.db.commit.assert_called_once()

    def test_create_employee_invalid_status(self):
        request = self.employee_factory.createEmployeeRequest()
        request.status = INVALID_EMPLOYEE_STATUS

        with pytest.raises(HTTPException) as exc:
            create_employee_func(self.db, request)

        self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_STATUS_FORMAT)

    def test_create_employee_rollback_on_exception(self):
        with patch(
            "app.services.employee_service.get_company_id"
        ) as mock_company_id, patch(
            "app.services.employee_service.check_company_active"
        ) as mock_company_active, patch(
            "app.services.employee_service.generateGUID"
        ) as mock_guid, patch(
            "app.services.employee_service.create_employee_repo"
        ) as mock_create_repo:
            request = self.employee_factory.createEmployeeRequest()

            mock_company_id.return_value = 1
            mock_company_active.return_value = None
            mock_guid.return_value = EMPLOYEE_GUID

            mock_create_repo.side_effect = Exception(DB_ERROR)

            with pytest.raises(Exception):
                create_employee_func(self.db, request)

            self.db.rollback.assert_called_once()
