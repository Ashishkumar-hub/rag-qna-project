import faiss
import numpy as np
from app.core.logging_config import logger
from app.models.db_models import Document
from app.models.db_models import SessionLocal


class EmbeddingStore:
    """
    A class to manage document embeddings using FAISS.

    Attributes:
        dimension (int): The dimension of the embedding vectors.
        index (faiss.IndexFlatL2): FAISS index to store and retrieve embeddings.
    """

    def __init__(self, dimension=384):
        """
        Initialize the FAISS index and load existing embeddings from the database.

        Args:
            dimension (int, optional): The dimensionality of the embeddings. Defaults to 384.
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.load_existing_embeddings()  # Load on startup

    def load_existing_embeddings(self):
        """
        Load all stored embeddings from the database into the FAISS index.

        Retrieves all document embeddings from the database and adds them to the FAISS index
        for efficient similarity search.
        """
        try:
            db = SessionLocal()
            documents = db.query(Document).all()
            db.close()

            if not documents:
                logger.info("No existing embeddings found in database.")
                return

            embeddings = [
                np.frombuffer(doc.embedding, dtype=np.float32) for doc in documents
            ]
            embeddings = np.array(embeddings, dtype=np.float32)

            if embeddings.shape[0] > 0:
                self.index.add(embeddings)
                logger.info(f"✅ Loaded {len(embeddings)} embeddings into FAISS index.")
            else:
                logger.warning("No valid embeddings found in database.")
        except Exception as e:
            logger.error(f"Error loading existing embeddings: {e}")

    def add_embedding(self, embedding):
        """
        Add a new embedding vector to the FAISS index.

        Args:
            embedding (np.ndarray): A numpy array representing the embedding vector.
        """
        try:
            self.index.add(np.array([embedding], dtype=np.float32))
            logger.info("Embedding added to FAISS index.")
        except Exception as e:
            logger.error(f"Error adding embedding: {e}")

    def search(self, query_embedding, k=5, threshold=0.5):
        """
        Perform a nearest neighbor search on the FAISS index.

        Args:
            query_embedding (np.ndarray): The query embedding vector.
            k (int, optional): The number of nearest neighbors to retrieve. Defaults to 5.
            threshold (float, optional): Minimum similarity score to consider a valid match.

        Returns:
            list: A list of indices of the closest matching embeddings.
        """
        try:
            if self.index.ntotal == 0:
                logger.warning(
                    "FAISS index is empty. No documents available for retrieval."
                )
                return []

            distances, indices = self.index.search(
                np.array([query_embedding], dtype=np.float32), k
            )

            # Convert distances to similarity scores
            similarities = 1 / (1 + distances)

            # Filter out low-similarity results
            valid_indices = [
                idx for sim, idx in zip(similarities[0], indices[0]) if sim >= threshold
            ]

            return valid_indices
        except Exception as e:
            logger.error(f"Error searching embeddings: {e}")
            return []
