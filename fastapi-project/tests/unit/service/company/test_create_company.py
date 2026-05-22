from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.company_constants import *
from app.services.company_service import create_company_func
import pytest
from unittest.mock import patch
from tests.shared.response_constants import *
from fastapi import HTTPException, status

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestCreateCompany(BaseServiceTest):
    def test_create_company_success(self):
        with patch(
            "app.services.company_service.check_company_by_name"
        ) as mock_company, patch(
            "app.services.company_service.generateGUID"
        ) as mock_guid, patch(
            "app.services.company_service.create_company_repo"
        ) as mock_create_repo:
            request = self.company_factory.createCompanyRequest()
            mock_company.return_value = None
            mock_guid.return_value = COMPANY_GUID
            result = create_company_func(self.db, request)
            assert result["success"] is True
            assert result["message"] == COMPANY_CREATION_SUCCESS
            mock_create_repo.assert_called_once()
            self.db.commit.assert_called_once()

    def test_create_company_invalid_status(self):
        request = self.company_factory.createCompanyRequest()
        request.status = INVALID_COMPANY_STATUS
        with pytest.raises(HTTPException) as exc:
            create_company_func(self.db, request)
        self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, INVALID_STATUS_FORMAT)

    def test_create_company_exists(self):
        with patch(
            "app.services.company_service.check_company_by_name"
        ) as mock_company:
            request = self.company_factory.createCompanyRequest()
        mock_company.side_effect = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=COMPANY_EXISTS
        )
        with pytest.raises(HTTPException) as exc:
            create_company_func(self.db, request)

        self.assert_exception(exc, status.HTTP_400_BAD_REQUEST, COMPANY_EXISTS)
