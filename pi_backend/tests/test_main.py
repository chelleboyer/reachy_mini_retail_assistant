"""Tests for pi_backend API."""
from fastapi.testclient import TestClient

from pi_backend.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'


def test_events_ingest() -> None:
    client = TestClient(app)
    response = client.post('/events/ingest', json={'events': [{'event_type': 'product_query'}]})
    assert response.status_code == 200
    data = response.json()
    assert data['accepted'] == 1
    assert data['stored'] == 1
