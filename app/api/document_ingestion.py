from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.db_models import SessionLocal, Document
from app.services.embedding_service import generate_embedding
from app.models.embedding_store_instance import (
    embedding_store,
)
from app.core.logging_config import logger
from pydantic import BaseModel

router = APIRouter()


def get_db():
    """
    Dependency to get the database session.
    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UploadResponse(BaseModel):
    message: str
    document_id: int


@router.post(
    "/upload/",
    response_model=UploadResponse,
    summary="Upload a document and generate embedding",
)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a document and generate embeddings for it.

    - **file**: The document file to be uploaded (only `.txt` files supported).
    - **Returns**: Document ID and success message.
    """
    try:
        content = await file.read()
        document_text = content.decode("utf-8")

        embedding = generate_embedding(document_text)
        if embedding is None:
            raise HTTPException(status_code=500, detail="Error generating embedding.")

        db_document = Document(text=document_text, embedding=embedding)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        embedding_store.add_embedding(embedding)

        logger.info(f"Document {db_document.id} uploaded successfully.")
        return UploadResponse(
            message="Document uploaded successfully", document_id=db_document.id
        )

    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
