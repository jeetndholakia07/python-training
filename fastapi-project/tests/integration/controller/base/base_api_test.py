from tests.factory.user_factory import UserFactory

class BaseApiTest:
    @property
    def user_factory(self):
        return UserFactory()