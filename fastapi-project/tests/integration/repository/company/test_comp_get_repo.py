from app.models.company import Company

from app.repositories.company_respository import (
    get_all_company_repo,
    get_company_by_id_repo,
    get_company_id_repo,
    get_company_status_repo,
    get_company_by_name_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.builder.company_builder import CompanyBuilder
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class GetRepoTest(BaseRepoTest):
    def test_get_all_company_repo_should_return_all_companies(self, db_session):
        company1 = CompanyBuilder().build()
        company2 = (
            CompanyBuilder()
            .with_guid(COMPANY_GUID2)
            .with_name(COMPANY_NAME2)
            .with_description(COMPANY_DESCRIPTION2)
            .build()
        )
        db_session.add_all([company1, company2])
        db_session.commit()
        result = get_all_company_repo(db=db_session, status=None, limit=10, offset=0)
        assert result is not None
        assert result["totalItems"] == 2
        assert len(result["data"]) == 2

    def test_get_all_company_repo_should_filter_by_status(self, db_session):
        active_company = CompanyBuilder().with_status(COMPANY_ACTIVE).build()
        deleted_company = (
            CompanyBuilder()
            .with_guid(COMPANY_GUID2)
            .with_status(COMPANY_DELETED)
            .build()
        )
        db_session.add_all([active_company, deleted_company])
        db_session.commit()
        result = get_all_company_repo(
            db=db_session, status=COMPANY_ACTIVE, limit=10, offset=0
        )
        assert result["totalItems"] == 1
        assert len(result["data"]) == 1
        assert result["data"][0]["status"] == COMPANY_ACTIVE

    def test_get_company_by_id_repo_should_return_company(self, db_session):
        self.seed_company(db_session)
        result = get_company_by_id_repo(db=db_session, companyGuid=COMPANY_GUID)
        assert result is not None
        assert result["companyName"] == COMPANY_NAME
        assert result["description"] == COMPANY_DESCRIPTION
        assert result["companyGuid"] == COMPANY_GUID
        assert result["status"] == COMPANY_ACTIVE

    def test_get_company_by_id_repo_should_return_none(self, db_session):
        result = get_company_by_id_repo(db=db_session, companyGuid=COMPANY_GUID)
        assert result is None

    def test_get_company_id_repo_should_return_company_id(self, db_session):
        company = self.seed_company(db_session)
        result = get_company_id_repo(db=db_session, companyGuid=COMPANY_GUID)
        assert result is not None
        assert result.id == company.id

    def test_get_company_status_repo_should_return_status(self, db_session):
        self.seed_company(db_session)
        result = get_company_status_repo(db=db_session, companyGuid=COMPANY_GUID)
        assert result is not None
        assert result.status == COMPANY_ACTIVE

    def test_get_company_by_name_repo_should_return_company(self, db_session):
        self.seed_company(db_session)
        result = get_company_by_name_repo(db=db_session, name=COMPANY_NAME)
        assert result is not None
        assert result.companyName == COMPANY_NAME

    def test_get_company_by_name_repo_should_return_none(self, db_session):
        result = get_company_by_name_repo(db=db_session, name=COMPANY_NAME)
        assert result is None
