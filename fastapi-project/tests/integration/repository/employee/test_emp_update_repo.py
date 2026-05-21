from app.models.company import Company

from app.repositories.company_respository import (
    update_company_desc_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class UpdateRepoTest(BaseRepoTest):
    def test_update_company_desc_repo_should_update_description(self, db_session):
        company = self.seed_company(db_session)
        request = self.company_factory.updateCompanyRequest()
        update_company_desc_repo(db=db_session, company=request, companyId=company.id)
        db_session.commit()
        updated_company = self.get_company_by_guid(db_session, COMPANY_GUID)
        assert updated_company.description == COMPANY_DESCRIPTION2