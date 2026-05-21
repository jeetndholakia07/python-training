from app.models.user import User
from app.models.company import Company
from app.models.employee import Employee
from tests.builder.user_builder import UserBuilder
from tests.factory.user_factory import UserFactory
from tests.factory.company_factory import CompanyFactory
from tests.builder.company_builder import CompanyBuilder
from tests.builder.employee_builder import EmployeeBuilder
from tests.factory.employee_factory import EmployeeFactory

class BaseRepoTest:
    def seed_user(self, db, user=None):
        user = user or UserBuilder().build()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_email(self, db, email):
        return db.query(User).filter(User.email == email).first()

    @property
    def user_factory(self):
        return UserFactory()

    def seed_company(self, db, company=None):
        company = company or CompanyBuilder().build()

        db.add(company)
        db.commit()
        db.refresh(company)

        return company

    def get_company_by_guid(self, db, guid):
        return db.query(Company).filter(Company.guid == guid).first()

    @property
    def company_factory(self):
        return CompanyFactory()

    def seed_employee(self, db, company_id, employee=None):
        employee = employee or EmployeeBuilder().build()
        employee.companyId = company_id
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee

    def get_employee_by_guid(self, db, guid):
        return db.query(Employee).filter(Employee.guid == guid).first()

    @property
    def employee_factory(self):
        return EmployeeFactory()