from app.models.company import Company

from app.repositories.company_respository import create_company_repo

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class CreateRepoTest(BaseRepoTest):
    def test_create_company_repo_should_create_company(self, db_session):
        request = self.company_factory.createCompanyRequest()
        create_company_repo(db=db_session, company=request, guid=COMPANY_GUID)
        db_session.commit()
        company = self.get_company_by_guid(db_session, COMPANY_GUID)
        assert company is not None
        assert company.companyName == COMPANY_NAME
        assert company.description == COMPANY_DESCRIPTION
        assert company.guid == COMPANY_GUID
        assert company.status == COMPANY_ACTIVE
