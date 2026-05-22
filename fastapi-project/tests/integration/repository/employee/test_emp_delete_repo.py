from app.repositories.employee_repository import (
    delete_employee_by_id_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.shared.employee_constants import *
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class TestEmpDeleteRepo(BaseRepoTest):
    def test_delete_employee_by_id_repo_should_soft_delete_employee(self, db_session):
        company = self.seed_company(db_session)
        employee = self.seed_employee(db=db_session, company_id=company.id)
        delete_employee_by_id_repo(db=db_session, employeeId=employee.id)
        db_session.commit()
        deleted_employee = self.get_employee_by_guid(db_session, EMPLOYEE_GUID)
        assert deleted_employee.status == EMPLOYEE_DELETED
