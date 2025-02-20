from fastapi import FastAPI
from app.api import document_ingestion, document_selection, question_answering
from app.core.logging_config import logger

# Initialize FastAPI
app = FastAPI(title="Document Q&A API", version="1.0")

# Include API routers
app.include_router(document_ingestion.router, tags=["Document Ingestion"])
app.include_router(document_selection.router, tags=["Document Selection"])
app.include_router(question_answering.router, tags=["Question Answering"])


@app.get("/")
def root():
    """
    Root endpoint of the API.

    Returns a welcome message to indicate that the API is running.

    Returns:
        dict: A JSON response with a welcome message.
    """
    logger.info("Root endpoint hit.")
    return {"message": "Welcome to the Document Q&A API"}


# Log successful startup of the FastAPI application
logger.info("FastAPI application started successfully.")
