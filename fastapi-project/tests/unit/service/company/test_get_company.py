from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.company_constants import *
from app.services.company_service import get_company_id
import pytest
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestGetCompanyId(BaseServiceTest):
    def test_get_company_id_success(self):
        with patch("app.services.company_service.get_company_id_repo") as mock_repo:
            mock_repo.return_value = [1]
            result = get_company_id(self.db, COMPANY_GUID)
            assert result == 1

    def test_get_company_id_not_found(self):
        with patch("app.services.company_service.get_company_id_repo") as mock_repo:
            mock_repo.return_value = None
            with pytest.raises(HTTPException) as exc:
                get_company_id(self.db, COMPANY_GUID)
            self.assert_exception(exc, 404, "Company not found")
