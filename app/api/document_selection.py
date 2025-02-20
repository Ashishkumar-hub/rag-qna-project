from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.models.db_models import SessionLocal, Document
from app.core.logging_config import logger

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

    - **doc_ids**: List of document IDs to fetch.
    - **Returns**: List of selected document IDs.
    """
    try:
        doc_ids = [int(doc_id) for doc_id in request.doc_ids]
        selected_documents = db.query(Document).filter(Document.id.in_(doc_ids)).all()

        if not selected_documents:
            raise HTTPException(status_code=404, detail="Documents not found")

        logger.info(f"Selected {len(selected_documents)} documents.")
        return DocumentSelectionResponse(
            selected_documents=[doc.id for doc in selected_documents]
        )

    except Exception as e:
        logger.error(f"Error selecting documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
