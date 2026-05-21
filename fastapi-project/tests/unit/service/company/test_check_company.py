from tests.unit.service.base.base_service_test import BaseServiceTest
from tests.shared.company_constants import *
from app.services.company_service import check_company_by_name
import pytest
from unittest.mock import patch
from fastapi import HTTPException

pytestmark = [pytest.mark.unit, pytest.mark.service]

class TestCheckCompanyByName(BaseServiceTest):
    def test_check_company_by_name_success(self):
        with patch(
            "app.services.company_service.get_company_by_name_repo"
        ) as mock_repo:
            mock_repo.return_value = None
            result = check_company_by_name(self.db, COMPANY_NAME)
            assert result is None

    def test_check_company_by_name_exists(self):
        with patch(
            "app.services.company_service.get_company_by_name_repo"
        ) as mock_repo:
            mock_repo.return_value = self.company_builder.build()
            with pytest.raises(HTTPException) as exc:
                check_company_by_name(self.db, COMPANY_NAME)
            self.assert_exception(exc, 400, "Company already exists.")
