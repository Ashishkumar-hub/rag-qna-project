from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
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
    message: str


@router.post(
    "/qa/",
    response_model=AnswerResponse,
    summary="Answer a question using retrieved documents",
)
async def answer_question(query: Query, db: Session = Depends(get_db)):
    """
    Answer a user's question by retrieving relevant documents.
    If no documents are selected, returns a message indicating that.
    """
    try:
        # Validate input question
        question_text = query.question.strip()
        if not question_text:
            logger.warning("Received empty question input.")
            raise HTTPException(status_code=400, detail="Question cannot be empty.")

        # Generate embedding for query
        query_embedding = generate_embedding(question_text)
        if query_embedding is None:
            logger.error("Failed to generate embedding for the query.")
            raise HTTPException(status_code=500, detail="Embedding generation failed.")

        # Retrieve relevant documents
        relevant_docs, message = retrieve_relevant_docs(query_embedding)
        if not relevant_docs:
            logger.info("No relevant documents found for the query.")
            return AnswerResponse(
                answer="No relevant content found.",
                message="No relevant documents found.",
            )

        # Extract and clean text from retrieved documents
        retrieved_texts = list(
            set(doc.text.strip() for doc in relevant_docs if doc.text.strip())
        )

        if not retrieved_texts:
            logger.info("Retrieved documents did not contain useful information.")
            return AnswerResponse(
                answer="No relevant content found in retrieved documents.",
                message="Relevant documents did not contain useful information.",
            )

        # Prepare response
        response_text = " ".join(retrieved_texts)
        logger.info(f"Q&A executed successfully for: {query.question}")

        return AnswerResponse(
            answer=response_text, message="Answer retrieved successfully."
        )

    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in Q&A: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
