from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_valid_document():
    """Test uploading a valid document."""
    response = client.post(
        "/upload/", files={"file": ("test.txt", "Sample document content")}
    )
    assert response.status_code == 200
    assert "document_id" in response.json()


def test_upload_empty_document():
    """Test uploading an empty document."""
    response = client.post("/upload/", files={"file": ("empty.txt", "")})
    assert response.status_code == 400  # Should fail if empty files are not allowed


def test_upload_unsupported_file_type():
    """Test uploading a non-text file."""
    response = client.post(
        "/upload/", files={"file": ("test.pdf", b"%PDF-1.4 some binary content")}
    )
    assert response.status_code == 400  # Assuming only `.txt` files are supported


def test_upload_no_file():
    """Test API behavior when no file is provided."""
    response = client.post("/upload/")
    assert response.status_code == 422  # FastAPI should return a validation error
