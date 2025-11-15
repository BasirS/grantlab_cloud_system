"""
Enhanced Multi-Layer Vector Store for Cambio Labs Grants
Provides specialized collections for voice, data, quotes, and co-design language
to achieve 95-98% authenticity in generated applications
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import sys
import os
from pathlib import Path
import re

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import CHROMA_PERSIST_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from src.rag.embeddings import OpenAIEmbeddings


class EnhancedGrantVectorStore:
    """
    Enhanced vector store with specialized collections for different content types

    Collections:
    1. full_content: Full grant documents (existing functionality)
    2. voice_phrases: Signature phrases and language patterns
    3. data_metrics: Specific data points and statistics
    4. participant_voices: Quotes and testimonials
    5. codesign_examples: Co-design and partnership language
    6. program_descriptions: Detailed program-specific content
    """

    def __init__(self, persist_directory: str = None):
        """
        Initialize the enhanced vector store with multiple specialized collections

        Args:
            persist_directory: Where to save the database
        """
        self.persist_directory = persist_directory or str(CHROMA_PERSIST_DIR)

        # Create directory if it doesn't exist
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Initialize embeddings
        self.embedder = OpenAIEmbeddings()

        # Create all specialized collections
        self.collections = {
            "full_content": self.client.get_or_create_collection(
                name="grants_full_content",
                metadata={"description": "Full grant documents"}
            ),
            "voice_phrases": self.client.get_or_create_collection(
                name="grants_voice_phrases",
                metadata={"description": "Signature phrases and authentic language patterns"}
            ),
            "data_metrics": self.client.get_or_create_collection(
                name="grants_data_metrics",
                metadata={"description": "Specific statistics and data points"}
            ),
            "participant_voices": self.client.get_or_create_collection(
                name="grants_participant_voices",
                metadata={"description": "Participant quotes and testimonials"}
            ),
            "codesign_examples": self.client.get_or_create_collection(
                name="grants_codesign",
                metadata={"description": "Co-design and partnership language"}
            ),
            "program_descriptions": self.client.get_or_create_collection(
                name="grants_programs",
                metadata={"description": "Program-specific detailed descriptions"}
            ),
        }

        print(f"✓ Enhanced Vector Store initialized with {len(self.collections)} specialized collections")
        self._print_stats()

    def _print_stats(self):
        """Print statistics for all collections"""
        for name, collection in self.collections.items():
            count = collection.count()
            print(f"  - {name}: {count} items")

    # ========================================================================
    # CONTENT EXTRACTION AND CATEGORIZATION
    # ========================================================================

    def extract_voice_phrases(self, text: str, metadata: dict) -> List[Dict]:
        """
        Extract signature phrases and language patterns from text

        Args:
            text: Full grant text
            metadata: Document metadata

        Returns:
            List of extracted phrases with metadata
        """
        phrases = []

        # Mission statement patterns
        mission_patterns = [
            r"(?i)we (firmly )?believe that [^.!?]{20,150}[.!?]",
            r"(?i)when people (gain )?access [^.!?]{20,150}[.!?]",
            r"(?i)entrepreneurship is (more than|not just) [^.!?]{20,150}[.!?]",
            r"(?i)we champion [^.!?]{20,150}[.!?]",
            r"(?i)those (who are )?closest to the issues [^.!?]{20,150}[.!?]",
        ]

        for pattern in mission_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                phrases.append({
                    "text": match.strip(),
                    "category": "mission",
                    **metadata
                })

        # Community empowerment phrases
        empowerment_patterns = [
            r"(?i)for (thousands|hundreds) of [^.!?]{20,200}[.!?]",
            r"(?i)(more than|over) \d+%[^.!?]{20,150}[.!?]",
            r"(?i)(untapped potential|community-powered prosperity)[^.!?]{0,100}[.!?]",
            r"(?i)transforms? [^.!?]{10,100} into [^.!?]{10,100}[.!?]",
        ]

        for pattern in empowerment_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    full_match = ''.join(match) if match else ""
                else:
                    full_match = match
                if len(full_match) > 20:  # Filter very short matches
                    phrases.append({
                        "text": full_match.strip(),
                        "category": "empowerment",
                        **metadata
                    })

        return phrases

    def extract_data_metrics(self, text: str, metadata: dict) -> List[Dict]:
        """
        Extract specific statistics and data points

        Args:
            text: Full grant text
            metadata: Document metadata

        Returns:
            List of data points with context
        """
        metrics = []

        # Number patterns with context
        number_patterns = [
            r"(?i)\d+\+ (signups|participants|residents|entrepreneurs)[^.!?]{0,150}[.!?]",
            r"(?i)\d+%[^.!?]{5,150}[.!?]",
            r"(?i)\$[\d,]+ [^.!?]{5,100}[.!?]",
            r"(?i)(over|more than|less than|under) \d+ [^.!?]{10,150}[.!?]",
            r"(?i)\d+ (weeks?|months?|years?|hours?)[^.!?]{10,150}[.!?]",
        ]

        for pattern in number_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    full_match = ''.join(match) if match else ""
                else:
                    full_match = match
                if len(full_match) > 10:
                    metrics.append({
                        "text": full_match.strip(),
                        "category": "statistics",
                        **metadata
                    })

        return metrics

    def extract_participant_voices(self, text: str, metadata: dict) -> List[Dict]:
        """
        Extract participant quotes and testimonials

        Args:
            text: Full grant text
            metadata: Document metadata

        Returns:
            List of quotes with context
        """
        quotes = []

        # Look for quoted text
        quote_patterns = [
            r'"([^"]{20,300})"',
            r'"([^"]{20,300})"',  # Smart quotes
        ]

        for pattern in quote_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Filter out likely non-testimonial quotes
                if not any(x in match.lower() for x in ['http', 'www', '@']):
                    quotes.append({
                        "text": match.strip(),
                        "category": "testimonial",
                        **metadata
                    })

        return quotes

    def extract_codesign_language(self, text: str, metadata: dict) -> List[Dict]:
        """
        Extract co-design and partnership language

        Args:
            text: Full grant text
            metadata: Document metadata

        Returns:
            List of co-design examples
        """
        codesign_examples = []

        # Co-design patterns
        codesign_patterns = [
            r"(?i)co-design(ed)? with [^.!?]{10,150}[.!?]",
            r"(?i)co-creat(ed)? with [^.!?]{10,150}[.!?]",
            r"(?i)(designed|developed) (in partnership|in collaboration) with [^.!?]{10,150}[.!?]",
            r"(?i)(center|centering) [^.!?]{5,50}(as experts|as leaders)[^.!?]{0,100}[.!?]",
            r"(?i)tenant leaders? [^.!?]{10,150}[.!?]",
            r"(?i)user-centered design[^.!?]{10,150}[.!?]",
        ]

        for pattern in codesign_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    full_match = ' '.join(str(m) for m in match if m)
                else:
                    full_match = match
                if len(full_match) > 15:
                    codesign_examples.append({
                        "text": full_match.strip(),
                        "category": "codesign",
                        **metadata
                    })

        return codesign_examples

    def extract_program_descriptions(self, text: str, metadata: dict) -> List[Dict]:
        """
        Extract program-specific descriptions

        Args:
            text: Full grant text
            metadata: Document metadata

        Returns:
            List of program descriptions
        """
        programs = []

        # Program name patterns
        program_names = [
            "Journey Platform", "Journey",
            "StartUp NYCHA", "Startup NYCHA",
            "Cambio Solar",
            "Cambio Coding", "Cambio Coding & AI",
            "Social Entrepreneurship Incubator"
        ]

        for program_name in program_names:
            # Find sentences mentioning the program
            pattern = rf"(?i)([^.!?]*{program_name}[^.!?]{{0,200}}[.!?])"
            matches = re.findall(pattern, text)

            for match in matches:
                if len(match) > 30:  # Filter very short mentions
                    programs.append({
                        "text": match.strip(),
                        "program": program_name,
                        "category": "program_description",
                        **metadata
                    })

        return programs

    # ========================================================================
    # DOCUMENT PROCESSING
    # ========================================================================

    def chunk_text(self, text: str, chunk_size: int = CHUNK_SIZE,
                   overlap: int = CHUNK_OVERLAP) -> List[str]:
        """
        Split text into overlapping chunks for better retrieval
        (Same as base implementation)
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

                if break_point > chunk_size * 0.7:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return chunks

    def add_document_enhanced(self, text: str, metadata: Dict[str, Any]) -> Dict[str, int]:
        """
        Add a document to ALL specialized collections

        Args:
            text: Full grant text
            metadata: Document metadata

        Returns:
            Dict with counts of items added to each collection
        """
        counts = {}

        # 1. Add to full_content collection (standard chunking)
        chunks = self.chunk_text(text)
        chunks = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]

        if chunks:
            embeddings = self.embedder.embed_documents(chunks)
            doc_id = metadata.get("filename", "unknown")
            ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

            metadatas = []
            for i in range(len(chunks)):
                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_id"] = i
                chunk_metadata["total_chunks"] = len(chunks)
                metadatas.append(chunk_metadata)

            self.collections["full_content"].add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            counts["full_content"] = len(chunks)
        else:
            counts["full_content"] = 0

        # 2. Extract and add voice phrases
        voice_phrases = self.extract_voice_phrases(text, metadata)
        if voice_phrases:
            texts = [p["text"] for p in voice_phrases]
            embeddings = self.embedder.embed_documents(texts)
            ids = [f"{metadata.get('filename', 'unknown')}_voice_{i}" for i in range(len(texts))]

            self.collections["voice_phrases"].add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=voice_phrases
            )
        counts["voice_phrases"] = len(voice_phrases)

        # 3. Extract and add data metrics
        data_metrics = self.extract_data_metrics(text, metadata)
        if data_metrics:
            texts = [m["text"] for m in data_metrics]
            embeddings = self.embedder.embed_documents(texts)
            ids = [f"{metadata.get('filename', 'unknown')}_data_{i}" for i in range(len(texts))]

            self.collections["data_metrics"].add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=data_metrics
            )
        counts["data_metrics"] = len(data_metrics)

        # 4. Extract and add participant voices
        participant_voices = self.extract_participant_voices(text, metadata)
        if participant_voices:
            texts = [q["text"] for q in participant_voices]
            embeddings = self.embedder.embed_documents(texts)
            ids = [f"{metadata.get('filename', 'unknown')}_quote_{i}" for i in range(len(texts))]

            self.collections["participant_voices"].add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=participant_voices
            )
        counts["participant_voices"] = len(participant_voices)

        # 5. Extract and add co-design examples
        codesign_examples = self.extract_codesign_language(text, metadata)
        if codesign_examples:
            texts = [c["text"] for c in codesign_examples]
            embeddings = self.embedder.embed_documents(texts)
            ids = [f"{metadata.get('filename', 'unknown')}_codesign_{i}" for i in range(len(texts))]

            self.collections["codesign_examples"].add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=codesign_examples
            )
        counts["codesign_examples"] = len(codesign_examples)

        # 6. Extract and add program descriptions
        program_descriptions = self.extract_program_descriptions(text, metadata)
        if program_descriptions:
            texts = [p["text"] for p in program_descriptions]
            embeddings = self.embedder.embed_documents(texts)
            ids = [f"{metadata.get('filename', 'unknown')}_program_{i}" for i in range(len(texts))]

            self.collections["program_descriptions"].add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=program_descriptions
            )
        counts["program_descriptions"] = len(program_descriptions)

        total = sum(counts.values())
        print(f"✓ Added {metadata.get('filename', 'document')} to enhanced store:")
        for collection, count in counts.items():
            print(f"  - {collection}: {count} items")
        print(f"  Total: {total} items across all collections")

        return counts

    # ========================================================================
    # MULTI-LAYER RETRIEVAL
    # ========================================================================

    def retrieve_multi_layer(self, query: str, section_name: str = "",
                             n_content: int = 3,
                             n_voice: int = 5,
                             n_data: int = 3,
                             n_quotes: int = 2,
                             n_codesign: int = 2,
                             n_programs: int = 3) -> Dict[str, List[Dict]]:
        """
        Retrieve from multiple collections for comprehensive context

        Args:
            query: Search query
            section_name: Section being generated (for context)
            n_content: Number of full content chunks
            n_voice: Number of voice phrases
            n_data: Number of data points
            n_quotes: Number of quotes
            n_codesign: Number of co-design examples
            n_programs: Number of program descriptions

        Returns:
            Dict with results from each collection
        """
        results = {}

        # 1. Retrieve full content
        query_embedding = self.embedder.embed_text(query)
        content_results = self.collections["full_content"].query(
            query_embeddings=[query_embedding],
            n_results=n_content
        )
        results["content"] = self._format_results(content_results)

        # 2. Retrieve voice phrases
        voice_results = self.collections["voice_phrases"].query(
            query_embeddings=[query_embedding],
            n_results=n_voice
        )
        results["voice"] = self._format_results(voice_results)

        # 3. Retrieve data metrics
        data_results = self.collections["data_metrics"].query(
            query_embeddings=[query_embedding],
            n_results=n_data
        )
        results["data"] = self._format_results(data_results)

        # 4. Retrieve participant voices (if needed)
        if section_name.lower() in ["need statement", "evaluation plan"]:
            quote_results = self.collections["participant_voices"].query(
                query_embeddings=[query_embedding],
                n_results=n_quotes
            )
            results["quotes"] = self._format_results(quote_results)
        else:
            results["quotes"] = []

        # 5. Retrieve co-design examples (critical for methodology/project description)
        if section_name.lower() in ["methodology", "project description"]:
            codesign_results = self.collections["codesign_examples"].query(
                query_embeddings=[query_embedding],
                n_results=n_codesign
            )
            results["codesign"] = self._format_results(codesign_results)
        else:
            results["codesign"] = []

        # 6. Retrieve program descriptions
        program_results = self.collections["program_descriptions"].query(
            query_embeddings=[query_embedding],
            n_results=n_programs
        )
        results["programs"] = self._format_results(program_results)

        return results

    def _format_results(self, raw_results: Dict) -> List[Dict]:
        """Format ChromaDB results into clean list"""
        formatted = []
        if raw_results["documents"] and raw_results["documents"][0]:
            for i in range(len(raw_results["documents"][0])):
                formatted.append({
                    "text": raw_results["documents"][0][i],
                    "metadata": raw_results["metadatas"][0][i],
                    "distance": raw_results["distances"][0][i] if "distances" in raw_results else None
                })
        return formatted

    def format_retrieval_for_prompt(self, results: Dict[str, List[Dict]]) -> str:
        """
        Format multi-layer retrieval results for use in generation prompt

        Args:
            results: Dict from retrieve_multi_layer

        Returns:
            Formatted string for prompt
        """
        output = []

        # Content examples
        if results.get("content"):
            output.append("=== SIMILAR GRANT CONTENT (for structure and detail) ===")
            for i, item in enumerate(results["content"], 1):
                source = item["metadata"].get("filename", "Unknown")
                output.append(f"\nExample {i} (from {source}):")
                output.append(item["text"])

        # Voice phrases (signature language)
        if results.get("voice"):
            output.append("\n\n=== AUTHENTIC CAMBIO LABS PHRASES (use these exact patterns) ===")
            for item in results["voice"]:
                category = item["metadata"].get("category", "")
                output.append(f"- {item['text']} [{category}]")

        # Data metrics
        if results.get("data"):
            output.append("\n\n=== SPECIFIC DATA POINTS (use these exact numbers) ===")
            for item in results["data"]:
                output.append(f"- {item['text']}")

        # Quotes
        if results.get("quotes") and results["quotes"]:
            output.append("\n\n=== PARTICIPANT VOICES (consider including) ===")
            for item in results["quotes"]:
                output.append(f'- "{item["text"]}"')

        # Co-design examples (CRITICAL)
        if results.get("codesign") and results["codesign"]:
            output.append("\n\n=== CO-DESIGN LANGUAGE (MUST INCLUDE SIMILAR PHRASING) ===")
            for item in results["codesign"]:
                output.append(f"- {item['text']}")

        # Program descriptions
        if results.get("programs"):
            output.append("\n\n=== PROGRAM DESCRIPTIONS (for accurate details) ===")
            for item in results["programs"]:
                program = item["metadata"].get("program", "")
                output.append(f"\n[{program}]: {item['text']}")

        return "\n".join(output)

    # ========================================================================
    # UTILITY FUNCTIONS
    # ========================================================================

    def get_all_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        stats = {}
        for name, collection in self.collections.items():
            stats[name] = collection.count()
        stats["total_items"] = sum(stats.values())
        return stats

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics in format compatible with Streamlit app

        Returns:
            Dict with 'total_chunks', 'collection_name', and per-collection counts
        """
        all_stats = self.get_all_stats()

        return {
            "total_chunks": all_stats.get("total_items", 0),
            "collection_name": "Enhanced Multi-Layer RAG (6 collections)",
            "full_content": all_stats.get("full_content", 0),
            "voice_phrases": all_stats.get("voice_phrases", 0),
            "data_metrics": all_stats.get("data_metrics", 0),
            "participant_voices": all_stats.get("participant_voices", 0),
            "codesign_examples": all_stats.get("codesign_examples", 0),
            "program_descriptions": all_stats.get("program_descriptions", 0)
        }

    def clear_all_collections(self):
        """Clear ALL collections - USE WITH CAUTION"""
        collection_names = [
            "grants_full_content",
            "grants_voice_phrases",
            "grants_data_metrics",
            "grants_participant_voices",
            "grants_codesign",
            "grants_programs"
        ]

        for name in collection_names:
            try:
                self.client.delete_collection(name=name)
                print(f"  ✓ Deleted {name}")
            except Exception as e:
                print(f"  ⚠ {name} not found (creating new)")

        # Recreate collections
        self.__init__(self.persist_directory)
        print("✓ All collections cleared and recreated")


if __name__ == "__main__":
    # Test the enhanced vector store
    print("Testing Enhanced Multi-Layer Vector Store\n")

    store = EnhancedGrantVectorStore()

    test_text = """
    For thousands of New Yorkers living in public housing, entrepreneurship is one of the few viable paths to income and ownership. Less than 1% of NYCHA residents report business revenue.

    Through our six-month StartUp NYCHA accelerator, co-designed with NYCHA residents and tenant leaders, we create pathways to economic empowerment. At our Fulton Houses pilot, we had 60+ signups in the first week, with 95% being women of color. More than 80% of participants reported they would not have pursued their venture without this program.

    Our Journey platform is a gamified learning experience where participants earn gemstones they can cash in for prizes, mentorship, and workshops. All participants gain lifetime access to our alumni community.

    We firmly believe that those who are closest to the issues are best equipped to solve them. With your support, we will continue to scale a model that transforms untapped potential into community-powered prosperity.

    One participant shared: "This program gave me the confidence to finally start my business. I never thought I could be an entrepreneur."
    """

    metadata = {
        "filename": "test_grant_enhanced.txt",
        "grant_type": "StartUp NYCHA",
        "year": "2024"
    }

    # Add document
    print("Adding test document with enhanced extraction...\n")
    counts = store.add_document_enhanced(test_text, metadata)

    # Test multi-layer retrieval
    print("\n" + "="*70)
    print("Testing multi-layer retrieval for 'Need Statement'...\n")

    results = store.retrieve_multi_layer(
        query="entrepreneurship for NYCHA residents economic empowerment",
        section_name="Need Statement"
    )

    formatted = store.format_retrieval_for_prompt(results)
    print(formatted)

    # Stats
    print("\n" + "="*70)
    print("Collection Statistics:")
    stats = store.get_all_stats()
    for collection, count in stats.items():
        print(f"  {collection}: {count}")

    print("\n✓ Enhanced vector store test complete!")
