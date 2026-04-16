from pydantic import BaseModel
from .status_schema import StatusEnum

class CreateCompanyDTO(BaseModel):
    companyName: str
    description: str
    status: StatusEnum

class CompanyDTO(BaseModel):
    companyGuid: str
    companyName: str
    description: str
    status: StatusEnum

class UpdateCompanyDTO(BaseModel):
    description: str