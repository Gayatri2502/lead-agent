"""Backend test suite"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import database and app
from app.main import app
from app.database.db import Base, get_db


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Setup and teardown database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestHealth:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestAuth:
    def test_register_user(self):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPassword123",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"

    def test_login_user(self):
        # First register
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "username": "loginuser",
                "password": "TestPassword123",
                "first_name": "Login",
                "last_name": "User",
            },
        )

        # Then login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "TestPassword123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


class TestAppointments:
    def test_get_appointments_empty(self):
        response = client.get("/api/v1/appointments?business_id=1")
        assert response.status_code == 200
        assert response.json() == []


class TestCustomers:
    def test_get_customers_empty(self):
        response = client.get("/api/v1/customers?business_id=1")
        assert response.status_code == 200
        assert response.json() == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
