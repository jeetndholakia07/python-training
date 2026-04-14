from pydantic import BaseModel
from .status_schema import StatusEnum

class CreateEmployeeDTO(BaseModel):
    employeeName: str
    designation: str
    salary: float
    companyGuid: str
    status: StatusEnum

class EmployeeDTO(BaseModel):
    employeeGuid: str
    employeeName: str
    designation: str
    salary: float
    companyName: str
    status: StatusEnum

class UpdateEmployeeDTO(BaseModel):
    designation: str