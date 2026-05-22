from app.repositories.company_respository import (
    delete_company_by_id_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class TestCompDeleteRepo(BaseRepoTest):
    def test_delete_company_by_id_repo_should_soft_delete_company(self, db_session):
        company = self.seed_company(db_session)
        delete_company_by_id_repo(db=db_session, companyId=company.id)
        db_session.commit()
        deleted_company = self.get_company_by_guid(db_session, COMPANY_GUID)
        assert deleted_company.status == COMPANY_DELETED
