from tests.shared.employee_constants import *
from app.models.employee import Employee
from app.schemas.status_schema import StatusEnum

class EmployeeBuilder:
    def __init__(self):
        self._data = {
            "employee_name": EMPLOYEE_NAME,
            "guid": EMPLOYEE_GUID,
            "designation": EMPLOYEE_DESIGNATION,
            "salary": EMPLOYEE_SALARY,
            "status": EMPLOYEE_ACTIVE
        }

    def with_name(self, name: str):
        self._data["employee_name"] = name
        return self

    def with_guid(self, guid: str):
        self._data["guid"] = guid
        return self

    def with_designation(self, designation: str):
        self._data["designation"] = designation
        return self

    def with_role(self, status: StatusEnum):
        self._data["status"] = status
        return self

    def build(self):
        return Employee(**self._data.copy())