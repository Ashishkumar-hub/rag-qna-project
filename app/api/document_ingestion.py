from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.db_models import SessionLocal, Document
from app.services.embedding_service import generate_embedding
from app.models.embedding_store_instance import embedding_store
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
    Only supports .txt files and non-empty content.
    """
    try:
        # Ensure only .txt files are allowed
        if not file.filename.lower().endswith(".txt"):
            logger.error("Unsupported file type uploaded.")
            raise HTTPException(
                status_code=400, detail="Only .txt files are supported."
            )

        content = await file.read()

        try:
            document_text = content.decode("utf-8").strip()
        except UnicodeDecodeError:
            logger.error("File could not be decoded as UTF-8.")
            raise HTTPException(status_code=400, detail="File encoding must be UTF-8.")

        # Ensure the document is not empty
        if not document_text:
            logger.error("Uploaded document is empty.")
            raise HTTPException(status_code=400, detail="Uploaded document is empty.")

        # Generate embedding
        embedding = generate_embedding(document_text)
        if embedding is None:
            logger.error("Error generating embedding.")
            raise HTTPException(status_code=500, detail="Error generating embedding.")

        # Save document
        db_document = Document(text=document_text, embedding=embedding)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        embedding_store.add_embedding(embedding)

        logger.info(f"Document {db_document.id} uploaded successfully.")
        # Reload FAISS after upload
        embedding_store.load_existing_embeddings()

        return UploadResponse(
            message="Document uploaded successfully", document_id=db_document.id
        )

    except HTTPException as http_ex:
        raise http_ex  # Ensure FastAPI handles HTTPExceptions properly

    except Exception as e:
        logger.error(f"Unexpected error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
