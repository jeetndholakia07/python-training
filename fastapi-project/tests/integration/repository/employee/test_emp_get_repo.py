from datetime import datetime, timedelta

from app.repositories.employee_repository import (
    get_employees_repo,
    get_employee_by_id_repo,
    get_employee_id_repo,
    get_employee_date_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.builder.employee_builder import EmployeeBuilder
from tests.shared.employee_constants import *
from tests.shared.company_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class GetRepoTest(BaseRepoTest):
    def test_get_employees_repo_should_return_all_employees(self, db_session):
        company = self.seed_company(db_session)
        emp1 = EmployeeBuilder().build()
        emp2 = (
            EmployeeBuilder()
            .with_guid(EMPLOYEE_GUID2)
            .with_name(EMPLOYEE_NAME2)
            .with_designation(EMPLOYEE_DESIGNATION2)
            .build()
        )
        emp1.companyId = company.id
        emp2.companyId = company.id
        db_session.add_all([emp1, emp2])
        db_session.commit()
        result = get_employees_repo(
            db=db_session, limit=10, offset=0, companyName=None, status=None
        )
        assert result is not None
        assert len(result["data"]) == 2
        assert result["totalItems"] == 2

    def test_get_employees_repo_should_filter_by_company_name(self, db_session):
        company = self.seed_company(db_session)
        employee = EmployeeBuilder().build()
        employee.companyId = company.id
        db_session.add(employee)
        db_session.commit()
        result = get_employees_repo(
            db=db_session, limit=10, offset=0, companyName=COMPANY_NAME, status=None
        )
        assert result["totalItems"] == 1
        assert len(result["data"]) == 1
        assert result["data"][0]["companyName"] == COMPANY_NAME

    def test_get_employees_repo_should_filter_by_status(self, db_session):
        company = self.seed_company(db_session)
        active_employee = EmployeeBuilder().with_status(EMPLOYEE_ACTIVE).build()
        deleted_employee = (
            EmployeeBuilder()
            .with_guid(EMPLOYEE_GUID2)
            .with_status(EMPLOYEE_DELETED)
            .build()
        )
        active_employee.companyId = company.id
        deleted_employee.companyId = company.id
        db_session.add_all([active_employee, deleted_employee])
        db_session.commit()
        result = get_employees_repo(
            db=db_session, limit=10, offset=0, companyName=None, status=EMPLOYEE_ACTIVE
        )
        assert result["totalItems"] == 1
        assert len(result["data"]) == 1
        assert result["data"][0]["status"] == EMPLOYEE_ACTIVE

    def test_get_employee_by_id_repo_should_return_employee(self, db_session):
        company = self.seed_company(db_session)
        self.seed_employee(db=db_session, company_id=company.id)
        result = get_employee_by_id_repo(db=db_session, empGuid=EMPLOYEE_GUID)
        assert result is not None
        assert result["employeeName"] == EMPLOYEE_NAME
        assert result["designation"] == EMPLOYEE_DESIGNATION
        assert result["salary"] == EMPLOYEE_SALARY
        assert result["employeeGuid"] == EMPLOYEE_GUID
        assert result["companyName"] == COMPANY_NAME

    def test_get_employee_by_id_repo_should_return_none(self, db_session):
        result = get_employee_by_id_repo(db=db_session, empGuid=EMPLOYEE_GUID)
        assert result is None

    def test_get_employee_id_repo_should_return_employee_id(self, db_session):
        company = self.seed_company(db_session)
        employee = self.seed_employee(db=db_session, company_id=company.id)
        result = get_employee_id_repo(db=db_session, empGuid=EMPLOYEE_GUID)
        assert result == employee.id

    def test_get_employee_id_repo_should_return_none(self, db_session):
        result = get_employee_id_repo(db=db_session, empGuid=EMPLOYEE_GUID)
        assert result is None

    def test_get_employee_date_repo_should_return_employees(self, db_session):
        company = self.seed_company(db_session)
        employee = self.seed_employee(db=db_session, company_id=company.id)
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)
        result = get_employee_date_repo(
            db=db_session, startDate=start_date, endDate=end_date, limit=10, offset=0
        )
        assert result is not None
        assert result["totalItems"] == 1
        assert len(result["data"]) == 1
        assert result["data"][0]["employeeGuid"] == EMPLOYEE_GUID

    def test_get_employee_date_repo_should_return_empty(self, db_session):
        start_date = datetime.now() - timedelta(days=10)
        end_date = datetime.now() - timedelta(days=5)
        result = get_employee_date_repo(
            db=db_session, startDate=start_date, endDate=end_date, limit=10, offset=0
        )
        assert result["totalItems"] == 0
        assert result["data"] == []
