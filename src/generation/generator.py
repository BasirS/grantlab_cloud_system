"""
Grant Application Generator using OpenAI GPT-4 with RAG
This is the core module that generates grant sections grounded in past successful grants
"""
import openai
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import (
    OPENAI_API_KEY, OPENAI_LLM_MODEL, MAX_SIMILAR_DOCS,
    TEMPERATURE, MAX_TOKENS, DEFAULT_SECTIONS
)
from src.rag.vector_store import GrantVectorStore
from src.generation.prompts import (
    SYSTEM_PROMPT, get_section_prompt, REFINEMENT_PROMPT,
    SECTION_EXTENSION_PROMPT, get_full_application_prompt
)


class GrantApplicationGenerator:
    """
    Generate grant application sections using GPT-4 with RAG
    Retrieves similar examples from past grants to ground the generation
    """

    def __init__(self, api_key: str = None, model: str = None, vector_store: GrantVectorStore = None):
        """
        Initialize the generator

        Args:
            api_key: OpenAI API key
            model: GPT model to use (gpt-4-turbo-preview recommended)
            vector_store: Vector store with historical grants
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_LLM_MODEL

        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file")

        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)

        # Initialize or use provided vector store
        self.vector_store = vector_store or GrantVectorStore()

        print(f"✓ Generator initialized with {self.model}")

    def retrieve_similar_examples(self, query: str, n_results: int = MAX_SIMILAR_DOCS) -> str:
        """
        Retrieve similar grant examples from the vector store

        Args:
            query: Search query (RFP text or section description)
            n_results: Number of examples to retrieve

        Returns:
            Formatted string with relevant examples
        """
        results = self.vector_store.search(query, n_results=n_results)

        if not results:
            return "No similar examples found in the database."

        # Format results for the prompt
        examples = []
        for i, result in enumerate(results, 1):
            source = result["metadata"].get("filename", "Unknown source")
            text = result["text"]
            examples.append(f"Example {i} (from {source}):\n{text}\n")

        return "\n".join(examples)

    def generate_section(self, section_name: str, rfp_context: str,
                        temperature: float = TEMPERATURE,
                        max_tokens: int = MAX_TOKENS) -> Dict[str, Any]:
        """
        Generate a single section of a grant application

        Args:
            section_name: Name of the section (e.g., "Need Statement")
            rfp_context: Context from the RFP or grant opportunity
            temperature: Creativity level (0-1, higher = more creative)
            max_tokens: Maximum length of generated text

        Returns:
            Dict with 'text' and 'metadata'
        """
        print(f"\nGenerating {section_name}...")

        # Retrieve similar examples
        query = f"{section_name}: {rfp_context}"
        similar_examples = self.retrieve_similar_examples(query)

        # Build the prompt
        user_prompt = get_section_prompt(section_name, rfp_context, similar_examples)

        # Generate with GPT-4
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            generated_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            print(f"✓ Generated {section_name} ({tokens_used} tokens)")

            return {
                "text": generated_text,
                "section_name": section_name,
                "tokens_used": tokens_used,
                "model": self.model,
                "examples_used": len(similar_examples.split("Example")) - 1
            }

        except Exception as e:
            print(f"✗ Error generating {section_name}: {e}")
            raise

    def generate_full_application(self, rfp_context: str,
                                  sections: List[str] = None,
                                  temperature: float = TEMPERATURE) -> Dict[str, Any]:
        """
        Generate a complete grant application with multiple sections

        Args:
            rfp_context: Context from the RFP or grant opportunity
            sections: List of section names to generate (default: all standard sections)
            temperature: Creativity level

        Returns:
            Dict with all sections and metadata
        """
        sections = sections or DEFAULT_SECTIONS
        print(f"\n{'='*60}")
        print(f"Generating full application with {len(sections)} sections...")
        print(f"{'='*60}")

        application = {
            "sections": {},
            "metadata": {
                "total_tokens": 0,
                "model": self.model,
                "sections_generated": len(sections)
            }
        }

        # Generate each section
        for section_name in sections:
            result = self.generate_section(section_name, rfp_context, temperature)
            application["sections"][section_name] = result["text"]
            application["metadata"]["total_tokens"] += result["tokens_used"]

        print(f"\n{'='*60}")
        print(f"✓ Application complete!")
        print(f"  Total tokens: {application['metadata']['total_tokens']}")
        print(f"  Sections: {len(application['sections'])}")
        print(f"{'='*60}")

        return application

    def refine_section(self, original_text: str, user_feedback: str,
                      context: str = "") -> str:
        """
        Refine a section based on user feedback

        Args:
            original_text: The original generated text
            user_feedback: User's feedback or revision instructions
            context: Additional context about the grant

        Returns:
            Refined text
        """
        print(f"\nRefining section based on feedback...")

        # Retrieve similar examples for reference
        similar_examples = self.retrieve_similar_examples(context or original_text)

        # Build refinement prompt
        prompt = REFINEMENT_PROMPT.format(
            original_text=original_text,
            user_feedback=user_feedback,
            similar_examples=similar_examples
        )

        # Generate refinement
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS  # Ensure we don't truncate mid-word
            )

            refined_text = response.choices[0].message.content

            # Debug: Show first 200 chars of response
            print(f"   Response preview: {refined_text[:200]}...")

            # Clean up any formatting issues
            refined_text = refined_text.strip()

            # Check for AI slop phrases
            ai_slop_phrases = [
                "core mission is to",
                "carefully crafted",
                "testament to",
                "transformative movement",
                "pathways that challenge",
                "dedicated to creating",
                "commitment to excellence",
                "proven track record",
                "state-of-the-art",
                "cutting-edge",
                "we are proud to",
                "we are excited to",
                "we are committed to",
                "we are dedicated to"
            ]

            slop_count = sum(1 for phrase in ai_slop_phrases if phrase.lower() in refined_text.lower())
            if slop_count >= 3:
                print(f"⚠️  WARNING: Refined text contains {slop_count} AI slop phrases")
                print(f"   Detected phrases: {[p for p in ai_slop_phrases if p.lower() in refined_text.lower()]}")
                print(f"   Returning original text instead.")
                return original_text

            # Check if response looks corrupted (missing spaces)
            # Count space-to-character ratio - normal text has ~15-20% spaces
            if len(refined_text) > 100:
                space_ratio = refined_text.count(' ') / len(refined_text)
                print(f"   Space ratio: {space_ratio:.2%} ({refined_text.count(' ')} spaces in {len(refined_text)} chars)")

                if space_ratio < 0.10:  # Less than 10% spaces indicates corruption
                    print(f"⚠️  WARNING: Refined text appears corrupted (space ratio: {space_ratio:.2%})")
                    print(f"   First 300 chars: {refined_text[:300]}")
                    print(f"   Returning original text instead.")
                    return original_text

            print(f"✓ Section refined ({len(refined_text)} chars, {response.usage.total_tokens} tokens)")

            return refined_text

        except Exception as e:
            print(f"✗ Error refining section: {e}")
            raise

    def extend_section(self, current_text: str, extension_request: str,
                      context: str = "") -> str:
        """
        Extend or elaborate on an existing section

        Args:
            current_text: Current section text
            extension_request: What to add or elaborate on
            context: Additional context

        Returns:
            Extended text
        """
        print(f"\nExtending section...")

        # Retrieve similar examples
        similar_examples = self.retrieve_similar_examples(context or current_text)

        # Build extension prompt
        prompt = SECTION_EXTENSION_PROMPT.format(
            current_text=current_text,
            extension_request=extension_request,
            similar_examples=similar_examples
        )

        # Generate extension
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMPERATURE
            )

            extended_text = response.choices[0].message.content
            print(f"✓ Section extended")

            return extended_text

        except Exception as e:
            print(f"✗ Error extending section: {e}")
            raise


if __name__ == "__main__":
    # Test the generator
    print("Testing Grant Application Generator...")

    # Note: This requires the vector store to be populated with historical grants
    # Run the document loading script first

    generator = GrantApplicationGenerator()

    # Test single section generation
    test_rfp = """We are seeking proposals for programs that provide workforce development
    and entrepreneurship training to underserved communities, particularly BIPOC youth
    and public housing residents. Programs should include mentorship, skills training,
    and support for launching businesses."""

    result = generator.generate_section(
        section_name="Need Statement",
        rfp_context=test_rfp
    )

    print("\n" + "="*60)
    print("GENERATED NEED STATEMENT:")
    print("="*60)
    print(result["text"])
    print("\n" + "="*60)
    print(f"Tokens used: {result['tokens_used']}")
    print(f"Examples used: {result['examples_used']}")

    print("\n✓ Generator test complete!")
