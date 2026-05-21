from app.schemas.employee_schema import (
    CreateEmployeeDTO,
    UpdateEmployeeDTO,
    EmployeeDTO
)
from tests.shared.employee_constants import *
from tests.shared.company_constants import COMPANY_GUID, COMPANY_NAME

class EmployeeFactory:
    def __init__(self):
        pass

    def createEmployeeRequest(self):
        return CreateEmployeeDTO(
            employeeName=EMPLOYEE_NAME,
            designation=EMPLOYEE_DESIGNATION,
            salary=EMPLOYEE_SALARY,
            companyGuid=COMPANY_GUID,
            status=EMPLOYEE_ACTIVE,
        )
    
    def getEmployeeResponse(self):
        return EmployeeDTO(
            employeeGuid=EMPLOYEE_GUID,
            employeeName=EMPLOYEE_NAME,
            designation=EMPLOYEE_DESIGNATION,
            salary=EMPLOYEE_SALARY,
            companyName=COMPANY_NAME,
            status=EMPLOYEE_ACTIVE
        )
    
    def updateEmployeeRequest(self):
        return UpdateEmployeeDTO(
            designation=EMPLOYEE_DESIGNATION2
        )
