from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.models.db_models import SessionLocal, Document
from app.core.logging_config import logger

router = APIRouter()
selected_docs_store = set()


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


class DocumentSelectionRequest(BaseModel):
    """
    Request model for selecting documents.
    """

    doc_ids: List[int]


class DocumentSelectionResponse(BaseModel):
    """
    Response model for selected documents.
    """

    selected_documents: List[int]


@router.post(
    "/select_documents/",
    response_model=DocumentSelectionResponse,
    summary="Select documents by IDs",
)
async def select_documents(
    request: DocumentSelectionRequest, db: Session = Depends(get_db)
):
    """
    Select documents from the database based on provided IDs.
    Stores selected document IDs in memory.
    """
    try:
        if not request.doc_ids:
            logger.warning("No document IDs provided in request.")
            raise HTTPException(status_code=400, detail="No document IDs provided.")

        # Fetch valid documents from the database
        valid_docs = db.query(Document).filter(Document.id.in_(request.doc_ids)).all()
        valid_doc_ids = {doc.id for doc in valid_docs}

        if not valid_doc_ids:
            logger.warning(f"No matching documents found for IDs: {request.doc_ids}")
            raise HTTPException(status_code=404, detail="No matching documents found.")

        # Store selected document IDs in memory
        selected_docs_store.clear()
        selected_docs_store.update(valid_doc_ids)

        logger.info(f"Selected documents: {selected_docs_store}")
        return DocumentSelectionResponse(selected_documents=list(selected_docs_store))

    except HTTPException as http_ex:
        raise http_ex  # Ensure FastAPI handles HTTPExceptions properly

    except Exception as e:
        logger.error(f"Unexpected error selecting documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.post(
    "/clear_selected_documents/",
    response_model=DocumentSelectionResponse,
    summary="Clear selected documents",
)
async def clear_documents():
    """
    Clear selected documents from memory.
    """
    selected_docs_store.clear()
    logger.info("Cleared selected documents.")
    return DocumentSelectionResponse(selected_documents=[])
