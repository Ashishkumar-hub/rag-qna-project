from app.models.embedding_store_instance import embedding_store
from app.core.logging_config import logger
import numpy as np
from app.models.db_models import Document, SessionLocal
from app.api.document_selection import selected_docs_store  # Import selected docs


def retrieve_relevant_docs(query_embedding, k=5):
    """
    Retrieve relevant documents based on selected documents or all documents.

    If documents are selected, only search within those.
    If no documents are selected, search all and return a message.
    """
    try:
        doc_indices = embedding_store.search(query_embedding, k)

        if not doc_indices:  # If no valid results
            logger.info("No relevant documents found.")
            return [], "No relevant documents found."

        document_ids = [int(doc_id) for doc_id in doc_indices]

        db = SessionLocal()
        if selected_docs_store:
            # Filter search results to only include selected documents
            documents = (
                db.query(Document)
                .filter(
                    Document.id.in_(document_ids), Document.id.in_(selected_docs_store)
                )
                .all()
            )
            message = "Answer is based on selected documents."
        else:
            documents = db.query(Document).filter(Document.id.in_(document_ids)).all()
            message = (
                "No documents selected. Answer is based on all available documents."
            )

        db.close()

        if not documents:
            logger.info("No relevant documents found after filtering.")
            return [], "No relevant documents found."

        logger.info(f"Retrieved {len(documents)} relevant documents.")
        unique_documents = list(
            {doc.id: doc for doc in documents}.values()
        )  # Ensure unique docs
        return unique_documents, message

    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return [], "Error retrieving documents."
