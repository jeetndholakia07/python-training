from tests.shared.company_constants import *
from app.schemas.company_schema import CreateCompanyDTO, CompanyDTO, UpdateCompanyDTO

class CompanyFactory:
    def __init__(self):
        pass

    def createCompanyRequest(self):
        return CreateCompanyDTO(
            companyName=COMPANY_NAME,
            description=COMPANY_DESCRIPTION,
            status=COMPANY_ACTIVE
        )
    
    def getCompanyResponse(self):
        return CompanyDTO(
            companyGuid=COMPANY_GUID,
            companyName=COMPANY_NAME,
            description=COMPANY_DESCRIPTION,
            status=COMPANY_ACTIVE
        )
    
    def updateCompanyRequest(self):
        return UpdateCompanyDTO(
            description=COMPANY_DESCRIPTION2
        )