from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_document():
    """
    Test the document upload API.

    Sends a sample text file to the `/upload/` endpoint and verifies that:
    - The response status code is 200 (successful upload).
    - The response JSON contains a "document_id" key.

    Assertions:
        - The API should return a 200 status code.
        - The response JSON must include "document_id".
    """
    response = client.post(
        "/upload/", files={"file": ("test.txt", "Sample document content")}
    )
    assert response.status_code == 200
    assert "document_id" in response.json()
