from app.utils.guid import generateGUID, is_valid_guid
from tests.shared.company_constants import COMPANY_GUID
import pytest
import uuid
from tests.shared.user_constants import *

pytestmark = [pytest.mark.unit, pytest.mark.util]

class TestGuidUtils:
    def test_generate_guid_success(self):
        guid = generateGUID()
        assert guid is not None
        assert isinstance(guid, str)
        parsed_guid = uuid.UUID(guid, version=4)
        assert str(parsed_guid) == guid

    def test_is_valid_guid_success(self):
        result = is_valid_guid(COMPANY_GUID)
        assert result is True

    def test_is_valid_guid_invalid(self):
        invalid_guid = INVALID_GUID
        result = is_valid_guid(invalid_guid)
        assert result is False

    def test_is_valid_guid_empty(self):
        result = is_valid_guid("")
        assert result is False

    def test_is_valid_guid_none(self):
        result = is_valid_guid(None)
        assert result is False
