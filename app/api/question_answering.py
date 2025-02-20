from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app.models.db_models import SessionLocal
from app.services.embedding_service import generate_embedding
from app.services.retrieval_service import retrieve_relevant_docs
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


class Query(BaseModel):
    """
    Request model for question answering.
    """

    question: str


class AnswerResponse(BaseModel):
    """
    Response model for answering questions.
    """

    answer: str


@router.post(
    "/qa/",
    response_model=AnswerResponse,
    summary="Answer a question using retrieved documents",
)
async def answer_question(query: Query, db: Session = Depends(get_db)):
    """
    Answer a user's question by retrieving relevant documents.

    - **question**: The question to be answered.
    - **Returns**: A textual answer based on retrieved documents.
    """
    try:
        query_embedding = generate_embedding(query.question)
        relevant_docs = retrieve_relevant_docs(query_embedding)

        if not relevant_docs:
            return AnswerResponse(answer="No relevant documents found.")

        # Extract text from retrieved documents
        retrieved_texts = list(
            set(
                doc.text.strip()
                for doc in relevant_docs
                if doc.text.strip() and "Sample document content" not in doc.text
            )
        )

        if not retrieved_texts:
            return AnswerResponse(
                answer="No relevant content found in retrieved documents."
            )

        response_text = " ".join(retrieved_texts)

        logger.info(f"Q&A executed successfully for: {query.question}")
        return AnswerResponse(answer=response_text)

    except Exception as e:
        logger.error(f"Error in Q&A API: {e}")
        raise HTTPException(status_code=500, detail=str(e))
