from app.models.embedding_store_instance import (
    embedding_store,
)
from app.core.logging_config import logger
import numpy as np
from app.models.db_models import Document, SessionLocal


def retrieve_relevant_docs(query_embedding, k=5):
    """
    Retrieve the most relevant documents based on the given query embedding.

    Args:
        query_embedding (np.ndarray): The embedding vector of the query text.
        k (int, optional): The number of top relevant documents to retrieve. Defaults to 5.

    Returns:
        list: A list of retrieved Document objects from the database.
    """
    try:
        doc_indices = embedding_store.search(query_embedding, k)
        valid_indices = np.array(doc_indices)
        valid_indices = valid_indices[valid_indices != -1]

        if len(valid_indices) == 0:
            logger.info("No relevant documents found.")
            return []

        document_ids = [int(doc_id) for doc_id in valid_indices]

        db = SessionLocal()
        documents = db.query(Document).filter(Document.id.in_(document_ids)).all()
        db.close()

        logger.info(f"Retrieved {len(documents)} relevant documents.")
        unique_documents = list(
            {doc.id: doc for doc in documents}.values()
        )  # Ensure unique docs
        return unique_documents

    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return []
