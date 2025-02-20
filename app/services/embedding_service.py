from sentence_transformers import SentenceTransformer
from app.core.logging_config import logger

# Load the pre-trained sentence embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def generate_embedding(text):
    """
    Generate an embedding vector for the given text using the SentenceTransformer model.

    Args:
        text (str): The input text to be converted into an embedding.
    Returns:
        np.ndarray or None: The generated embedding vector as a NumPy array if successful,
        otherwise None in case of an error.
    """
    try:
        embedding = model.encode(text)
        logger.info("Generated embedding successfully.")
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None
