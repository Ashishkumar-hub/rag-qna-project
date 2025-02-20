from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_select_documents():
    """
    Test the document selection API.

    Sends a POST request to the `/select_documents/` endpoint with a list of document IDs.
    Verifies that:
    - The response status code is either 200 (success) or 404 (documents not found).

    Assertions:
        - The API should return a 200 status code if documents are found.
        - The API may return a 404 status code if the documents do not exist.
    """
    response = client.post("/select_documents/", json={"doc_ids": [1, 2]})
    assert response.status_code in [200, 404]
