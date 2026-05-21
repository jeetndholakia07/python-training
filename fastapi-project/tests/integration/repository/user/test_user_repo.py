from app.repositories.user_repository import (
    create_admin_repo,
    get_user_by_email_repo,
    get_hashed_password_repo,
)

from tests.integration.repository.base.base_repo_test import BaseRepoTest
from tests.shared.user_constants import *
import pytest

pytestmark = [pytest.mark.repository, pytest.mark.integration]

class TestUserRepository(BaseRepoTest):
    def test_create_admin_repo_should_create_user(
        self,
        db_session
    ):
        request = self.user_factory.createUserRequest()
        create_admin_repo(
            db=db_session,
            admin=request,
            guid=USER_GUID
        )
        db_session.commit()
        user = self.get_user_by_email(
            db_session,
            VALID_EMAIL
        )
        assert user is not None
        assert user.email == VALID_EMAIL
        assert user.username == USER_NAME
        assert user.guid == USER_GUID
        assert user.role == ROLE_EMPLOYEE

    def test_get_user_by_email_repo_should_return_user(
        self,
        db_session
    ):
        self.seed_user(db_session)
        result = get_user_by_email_repo(
            db=db_session,
            email=VALID_EMAIL
        )
        assert result is not None
        assert result["email"] == VALID_EMAIL
        assert result["username"] == USER_NAME
        assert result["userGuid"] == USER_GUID
        assert result["role"] == ROLE_EMPLOYEE

    def test_get_user_by_email_repo_should_return_none(
        self,
        db_session
    ):
        result = get_user_by_email_repo(
            db=db_session,
            email=VALID_EMAIL
        )
        assert result is None

    def test_get_hashed_password_repo_should_return_hash(
        self,
        db_session
    ):
        self.seed_user(db_session)
        result = get_hashed_password_repo(
            db=db_session,
            email=VALID_EMAIL
        )
        assert result is not None
        assert result.password_hash == PASSWORD_HASH