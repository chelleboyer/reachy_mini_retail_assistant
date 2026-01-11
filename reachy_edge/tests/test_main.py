"""Tests for main FastAPI application."""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from reachy_edge.main import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


def test_health_endpoint_returns_200(client):
    """Test health endpoint returns 200 status code."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_returns_correct_schema(client):
    """Test health endpoint returns correct JSON schema."""
    response = client.get("/health")
    data = response.json()
    
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"


def test_health_endpoint_timestamp_is_iso8601(client):
    """Test health endpoint timestamp is valid ISO 8601 format."""
    response = client.get("/health")
    data = response.json()
    
    # Should parse without error
    timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    assert timestamp is not None


def test_health_endpoint_status_is_healthy(client):
    """Test health endpoint always returns healthy status."""
    response = client.get("/health")
    data = response.json()
    
    assert data["status"] == "healthy"


def test_health_endpoint_has_correct_version(client):
    """Test health endpoint returns correct API version."""
    from reachy_edge.config import Settings
    
    settings = Settings()
    response = client.get("/health")
    data = response.json()
    
    assert data["version"] == settings.api_version
