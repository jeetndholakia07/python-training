from unittest.mock import Mock
from tests.factory.user_factory import UserFactory
from tests.factory.company_factory import CompanyFactory
from tests.factory.employee_factory import EmployeeFactory
from tests.builder.company_builder import CompanyBuilder

class BaseServiceTest:
    def setup_method(self):
        self.db = Mock()
        self.user_factory = UserFactory()
        self.company_factory = CompanyFactory()
        self.employee_factory = EmployeeFactory()
        self.company_builder = CompanyBuilder()

    def assert_exception(
            self, 
            exc,
            status_code,
            detail=None
    ):
        assert exc.value.status_code == status_code
        if detail:
            assert exc.value.detail == detail