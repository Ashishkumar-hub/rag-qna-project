from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_valid_question():
    """Test asking a valid question."""
    response = client.post("/qa/", json={"question": "What is AI?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "message" in response.json()


def test_question_no_documents_selected():
    """Test asking a question without selecting documents."""
    response = client.post("/qa/", json={"question": "What is AI?"})
    assert response.status_code == 200  # Should return a valid message
    assert response.json()["message"] == "No relevant documents found."


def test_empty_question():
    """Test sending an empty question."""
    response = client.post("/qa/", json={"question": ""})
    assert response.status_code == 400  # Assuming empty questions are invalid


def test_no_question_field():
    """Test API behavior when 'question' field is missing."""
    response = client.post("/qa/", json={})
    assert response.status_code == 422  # FastAPI should return a validation error
