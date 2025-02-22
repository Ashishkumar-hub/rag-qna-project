from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_select_existing_documents():
    """Test selecting documents that exist in the database."""
    response = client.post("/select_documents/", json={"doc_ids": [1, 2]})
    assert response.status_code == 200
    assert "selected_documents" in response.json()


def test_select_non_existent_documents():
    """Test selecting documents that do not exist."""
    response = client.post("/select_documents/", json={"doc_ids": [99999, 88888]})
    assert response.status_code == 404  # Assuming API returns 404 for non-existent docs


def test_select_no_documents():
    """Test API behavior when no document IDs are provided."""
    response = client.post("/select_documents/", json={"doc_ids": []})
    assert response.status_code == 400  # Should fail if an empty list is invalid
