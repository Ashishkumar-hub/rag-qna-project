from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_qa():
    """
    Test the question-answering (QA) API.

    Sends a POST request to the `/qa/` endpoint with a sample question.
    Verifies that:
    - The response status code is 200 (success).
    - The response contains an "answer" field.

    Assertions:
        - The API should return a 200 status code indicating successful processing.
        - The response JSON must include an "answer" key with the generated response.
    """
    response = client.post("/qa/", json={"question": "What is AI?"})
    assert response.status_code == 200
    assert "answer" in response.json()
