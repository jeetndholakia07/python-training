from app.repositories.employee_repository import (
    update_employee_id_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.builder.employee_builder import EmployeeBuilder
from tests.shared.employee_constants import *
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class TestCompUpdateRepo(BaseRepoTest):
    def test_update_employee_id_repo_should_update_designation(self, db_session):
        company = self.seed_company(db_session)
        employee = self.seed_employee(db=db_session, company_id=company.id)
        request = self.employee_factory.updateEmployeeRequest()
        update_employee_id_repo(db=db_session, emp=request, employeeId=employee.id)
        db_session.commit()
        updated_employee = self.get_employee_by_guid(db_session, EMPLOYEE_GUID)
        assert updated_employee.designation == EMPLOYEE_DESIGNATION2
