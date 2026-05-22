import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import Base
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from app.services.auth_service import get_current_user, require_roles
from tests.config.test_auth_override import (
    override_get_current_user,
    override_require_roles,
)

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

@pytest_asyncio.fixture
async def async_client():
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[require_roles] = override_require_roles
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()