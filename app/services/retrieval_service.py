from app.models.embedding_store_instance import embedding_store
from app.core.logging_config import logger
from app.models.db_models import Document, SessionLocal
from app.api.document_selection import selected_docs_store


def retrieve_relevant_docs(query_embedding, k=5):
    """
    Retrieve relevant documents based on selected documents or all documents.

    Args:
        query_embedding (numpy.ndarray): Vector representation of the query text.
        k (int, optional): Retrieves top k closest matching documents. Defaults to 5.

    Returns:
        tuple: A tuple containing:
            - list[Document]: A list of relevant Document objects.
            - str: A string indicating the source of the retrieved documents.
               Possible values: "Answer is based on selected documents.",
               "No documents selected. Answer is based on all available documents.",
               "No relevant documents found.", "Error retrieving documents."

    If documents are selected, only search within those.
    If no documents are selected, search all and return a message.
    """
    try:
        # Uses FAISS to find k nearest neighbors. Returns indices of matching document embeddings.
        doc_indices = embedding_store.search(query_embedding, k)

        if not doc_indices:  # If no valid results
            logger.info("No relevant documents found.")
            return [], "No relevant documents found."

        # Convert FAISS indices to actual document IDs stored in the database.
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
        # Remove duplicate documents by using a dictionary with doc.id as a key.
        unique_documents = list({doc.id: doc for doc in documents}.values())
        return unique_documents, message

    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        return [], "Error retrieving documents."
