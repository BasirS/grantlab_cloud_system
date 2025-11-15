"""
Vector Store for storing and retrieving grant document embeddings
Uses ChromaDB for local storage (can be deployed to cloud later)
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from src.rag.embeddings import OpenAIEmbeddings


class GrantVectorStore:
    """
    Vector store for grant documents using ChromaDB
    Stores document chunks with embeddings for semantic search
    """

    def __init__(self, persist_directory: str = None, collection_name: str = None):
        """
        Initialize the vector store

        Args:
            persist_directory: Where to save the database
            collection_name: Name of the collection to store documents
        """
        self.persist_directory = persist_directory or str(CHROMA_PERSIST_DIR)
        self.collection_name = collection_name or CHROMA_COLLECTION_NAME

        # Create directory if it doesn't exist
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Initialize embeddings
        self.embedder = OpenAIEmbeddings()

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Cambio Labs historical grant applications"}
        )

        print(f"Vector store initialized: {self.collection.count()} documents in collection")

    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE,
                   overlap: int = CHUNK_OVERLAP) -> List[str]:
        """
        Split text into overlapping chunks for better retrieval

        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Number of characters to overlap between chunks

        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)

                if break_point > chunk_size * 0.7:  # Only break if we're past 70% of chunk
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return chunks

    def add_document(self, text: str, metadata: Dict[str, Any]) -> int:
        """
        Add a single document to the vector store

        Args:
            text: Document text
            metadata: Metadata about the document (filename, grant type, etc.)

        Returns:
            Number of chunks added
        """
        # Chunk the document
        chunks = self.chunk_text(text)
        
        # Filter out empty chunks and ensure all are strings
        chunks = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
        
        if not chunks:
            print(f"⚠ Warning: No valid chunks extracted from document")
            return 0
        
        print(f"Split document into {len(chunks)} chunks")

        # Create embeddings for each chunk
        embeddings = self.embedder.embed_documents(chunks)

        # Create unique IDs for each chunk
        doc_id = metadata.get("filename", "unknown")
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

        # Add metadata to each chunk
        metadatas = []
        for i in range(len(chunks)):
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = i
            chunk_metadata["total_chunks"] = len(chunks)
            metadatas.append(chunk_metadata)

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        print(f"✓ Added {len(chunks)} chunks from {doc_id}")
        return len(chunks)

    def add_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Add multiple documents to the vector store

        Args:
            documents: List of dicts with 'text' and 'metadata' keys

        Returns:
            Total number of chunks added
        """
        total_chunks = 0

        for doc in documents:
            text = doc.get("text", "")
            metadata = doc.get("metadata", {})

            if text:
                chunks_added = self.add_document(text, metadata)
                total_chunks += chunks_added

        print(f"\n✓ Total: Added {total_chunks} chunks from {len(documents)} documents")
        return total_chunks

    def search(self, query: str, n_results: int = 5,
               filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents using semantic search

        Args:
            query: Search query text
            n_results: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of matching documents with metadata and similarity scores
        """
        # Create embedding for query
        query_embedding = self.embedder.embed_text(query)

        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )

        # Format results
        formatted_results = []
        if results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                result = {
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None,
                    "id": results["ids"][0][i]
                }
                formatted_results.append(result)

        return formatted_results

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection

        Returns:
            Dict with collection info
        """
        count = self.collection.count()

        # Get sample to analyze
        sample = self.collection.peek(limit=min(10, count))

        # Get unique documents
        unique_docs = set()
        if sample["metadatas"]:
            for metadata in sample["metadatas"]:
                if "filename" in metadata:
                    unique_docs.add(metadata["filename"])

        return {
            "total_chunks": count,
            "collection_name": self.collection_name,
            "sample_unique_docs": len(unique_docs),
            "persist_directory": self.persist_directory
        }

    def clear_collection(self):
        """
        Delete all documents from the collection
        USE WITH CAUTION
        """
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Cambio Labs historical grant applications"}
        )
        print(f"✓ Cleared collection: {self.collection_name}")

    def delete_document(self, filename: str):
        """
        Delete all chunks from a specific document

        Args:
            filename: Name of the file to delete
        """
        # Get all IDs for this document
        results = self.collection.get(
            where={"filename": filename}
        )

        if results["ids"]:
            self.collection.delete(ids=results["ids"])
            print(f"✓ Deleted {len(results['ids'])} chunks from {filename}")
        else:
            print(f"No chunks found for {filename}")


if __name__ == "__main__":
    # Test the vector store
    print("Testing Grant Vector Store...")

    store = GrantVectorStore()

    # Test adding documents
    test_docs = [
        {
            "text": """Cambio Labs is seeking funding to expand our StartUp NYCHA program,
            which provides entrepreneurship training to public housing residents. Our program
            has successfully helped 150 participants launch businesses, creating economic
            opportunities in underserved communities.""",
            "metadata": {
                "filename": "test_grant_1.txt",
                "grant_type": "StartUp NYCHA",
                "year": "2024"
            }
        },
        {
            "text": """We propose to use AI and technology education to empower BIPOC youth.
            Through our Journey Platform with Sparky AI bot, students learn coding and
            digital literacy skills. This program addresses the digital divide and creates
            pathways to tech careers.""",
            "metadata": {
                "filename": "test_grant_2.txt",
                "grant_type": "Tech Education",
                "year": "2024"
            }
        }
    ]

    # Add test documents
    store.add_documents(test_docs)

    # Test search
    print("\n" + "="*60)
    print("Testing search...")
    results = store.search("entrepreneurship programs for public housing", n_results=2)

    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Text: {result['text'][:150]}...")
        print(f"Source: {result['metadata'].get('filename')}")
        print(f"Distance: {result['distance']:.4f}")

    # Get stats
    print("\n" + "="*60)
    stats = store.get_collection_stats()
    print("Collection Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n✓ Vector store test complete!")
