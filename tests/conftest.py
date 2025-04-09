# tests/conftest.py
import pytest
from app.database import engine
from app.models import Base

@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Optionally drop tables after the tests run
    Base.metadata.drop_all(bind=engine)
