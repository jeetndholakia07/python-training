from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.company_constants import *
from app.services.company_service import update_company_desc
import pytest
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestUpdateCompany(BaseServiceTest):
    def test_update_company_success(self):
        with patch("app.services.company_service.is_valid_guid") as mock_guid, patch(
            "app.services.company_service.get_company_id"
        ) as mock_company_id, patch(
            "app.services.company_service.update_company_desc_repo"
        ) as mock_update_repo:
            request = self.company_factory.updateCompanyRequest()
            mock_guid.return_value = True
            mock_company_id.return_value = 1
            result = update_company_desc(self.db, COMPANY_GUID, request)
            assert result["success"] is True
            assert result["message"] == "Company updated successfully"
            mock_update_repo.assert_called_once_with(self.db, request, 1)
            self.db.commit.assert_called_once()

    def test_update_company_invalid_guid(self):
        request = self.company_factory.updateCompanyRequest()
        with patch("app.services.company_service.is_valid_guid") as mock_guid:
            mock_guid.return_value = False
            with pytest.raises(HTTPException) as exc:
                update_company_desc(self.db, COMPANY_GUID, request)
            self.assert_exception(exc, 400, "Invalid GUID")

    def test_update_company_rollback_on_exception(self):
        request = self.company_factory.updateCompanyRequest()
        with patch("app.services.company_service.is_valid_guid") as mock_guid, patch(
            "app.services.company_service.get_company_id"
        ) as mock_company_id, patch(
            "app.services.company_service.update_company_desc_repo"
        ) as mock_update_repo:
            mock_guid.return_value = True
            mock_company_id.return_value = 1
            mock_update_repo.side_effect = Exception("DB Error")
            with pytest.raises(Exception):
                update_company_desc(self.db, COMPANY_GUID, request)
            self.db.rollback.assert_called_once()
