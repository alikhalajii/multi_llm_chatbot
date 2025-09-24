import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Generator

from app.main import app as fastapi_app
from app.core.db import Base, engine, SessionLocal
import app.models.user_document  # noqa: F401


# Reset DB before each test
@pytest.fixture(autouse=True)
def setup_db() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(fastapi_app)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
