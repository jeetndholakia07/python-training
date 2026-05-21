from tests.shared.company_constants import *
from app.models.company import Company
from app.schemas.status_schema import StatusEnum

class CompanyBuilder:
    def __init__(self):
        self._data = {
            "company_name": COMPANY_NAME,
            "guid": COMPANY_GUID,
            "description": COMPANY_DESCRIPTION,
            "status": COMPANY_ACTIVE
        }

    def with_name(self, name: str):
        self._data["company_name"] = name
        return self

    def with_guid(self, guid: str):
        self._data["guid"] = guid
        return self

    def with_description(self, description: str):
        self._data["description"] = description
        return self

    def with_role(self, status: StatusEnum):
        self._data["status"] = status
        return self

    def build(self):
        return Company(**self._data.copy())