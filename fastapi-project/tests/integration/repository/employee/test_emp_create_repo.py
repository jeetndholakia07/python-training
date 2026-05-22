from app.repositories.employee_repository import (
    create_employee_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.shared.employee_constants import *
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class TestEmpCreateRepo(BaseRepoTest):
    def test_create_employee_repo_should_create_employee(self, db_session):
        company = self.seed_company(db_session)
        request = self.employee_factory.createEmployeeRequest()
        create_employee_repo(
            db=db_session, emp=request, companyId=company.id, guid=EMPLOYEE_GUID
        )
        db_session.commit()
        employee = self.get_employee_by_guid(db_session, EMPLOYEE_GUID)
        assert employee is not None
        assert employee.employeeName == EMPLOYEE_NAME
        assert employee.designation == EMPLOYEE_DESIGNATION
        assert employee.salary == EMPLOYEE_SALARY
        assert employee.guid == EMPLOYEE_GUID
        assert employee.companyId == company.id
