from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.company_constants import *
from app.services.company_service import delete_company_by_id
import pytest
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestDeleteCompany(BaseServiceTest):
    def test_delete_company_success(self):
        with patch("app.services.company_service.is_valid_guid") as mock_guid, patch(
            "app.services.company_service.get_company_id"
        ) as mock_company_id, patch(
            "app.services.company_service.delete_company_by_id_repo"
        ) as mock_delete_repo:
            mock_guid.return_value = True
            mock_company_id.return_value = 1
            result = delete_company_by_id(self.db, COMPANY_GUID)
            assert result["success"] is True
            assert result["message"] == "Company deleted successfully"
            mock_delete_repo.assert_called_once_with(self.db, 1)
            self.db.commit.assert_called_once()

    def test_delete_company_invalid_guid(self):
        with patch("app.services.company_service.is_valid_guid") as mock_guid:
            mock_guid.return_value = False
            with pytest.raises(HTTPException) as exc:
                delete_company_by_id(self.db, COMPANY_GUID)
            self.assert_exception(exc, 400, "Invalid GUID")

    def test_delete_company_rollback_on_exception(self):
        with patch("app.services.company_service.is_valid_guid") as mock_guid, patch(
            "app.services.company_service.get_company_id"
        ) as mock_company_id, patch(
            "app.services.company_service.delete_company_by_id_repo"
        ) as mock_delete_repo:
            mock_guid.return_value = True
            mock_company_id.return_value = 1
            mock_delete_repo.side_effect = Exception("DB Error")
            with pytest.raises(Exception):
                delete_company_by_id(self.db, COMPANY_GUID)
            self.db.rollback.assert_called_once()
