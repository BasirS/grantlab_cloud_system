"""
OpenAI Embeddings module for creating vector representations of grant documents
"""
import openai
from typing import List
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL


class OpenAIEmbeddings:
    """
    Create embeddings using OpenAI's API
    This converts text into numerical vectors that capture semantic meaning
    """

    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the embeddings client

        Args:
            api_key: OpenAI API key (defaults to settings)
            model: Embedding model to use (defaults to text-embedding-3-small)
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_EMBEDDING_MODEL

        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file")

        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)

    def embed_text(self, text: str) -> List[float]:
        """
        Create embedding for a single text string

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error creating embedding: {e}")
            raise

    def embed_documents(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Create embeddings for multiple documents

        Args:
            texts: List of text strings to embed
            batch_size: Number of texts to process at once (OpenAI limit is 2048)

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        # Process in batches to avoid rate limits
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            try:
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )

                # Extract embeddings from response
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

                print(f"Embedded {min(i + batch_size, len(texts))}/{len(texts)} documents")

            except Exception as e:
                print(f"Error embedding batch {i//batch_size + 1}: {e}")
                raise

        return all_embeddings

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model

        Returns:
            Integer dimension size
        """
        # text-embedding-3-small produces 1536-dimensional vectors
        # text-embedding-3-large produces 3072-dimensional vectors
        # ada-002 produces 1536-dimensional vectors

        if "large" in self.model:
            return 3072
        return 1536

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        Useful for finding similar documents

        Args:
            vec1: First embedding vector
            vec2: Second embedding vector

        Returns:
            Similarity score between -1 and 1 (1 is most similar)
        """
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)

        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)


if __name__ == "__main__":
    # Test the embeddings
    print("Testing OpenAI Embeddings...")

    embedder = OpenAIEmbeddings()
    print(f"Using model: {embedder.model}")
    print(f"Embedding dimension: {embedder.get_embedding_dimension()}")

    # Test single embedding
    test_text = "Cambio Labs empowers underestimated BIPOC youth through technology education"
    embedding = embedder.embed_text(test_text)
    print(f"\nTest embedding length: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")

    # Test similarity
    text1 = "workforce development and entrepreneurship programs"
    text2 = "job training and business creation initiatives"
    text3 = "quantum physics and theoretical mathematics"

    emb1 = embedder.embed_text(text1)
    emb2 = embedder.embed_text(text2)
    emb3 = embedder.embed_text(text3)

    sim_12 = embedder.cosine_similarity(emb1, emb2)
    sim_13 = embedder.cosine_similarity(emb1, emb3)

    print(f"\nSimilarity test:")
    print(f"'{text1}' vs '{text2}': {sim_12:.3f}")
    print(f"'{text1}' vs '{text3}': {sim_13:.3f}")
    print("\n✓ Embeddings working correctly!")
