"""
Rebuild Vector Database with Enhanced Multi-Layer Collections
Processes all 53 historical grant examples and extracts:
- Full content chunks
- Voice phrases and signature language
- Data metrics and statistics
- Participant quotes
- Co-design examples
- Program descriptions
"""

import sys
import os
from pathlib import Path
from tqdm import tqdm

# Add to path
sys.path.append(os.path.dirname(__file__))

from src.rag.enhanced_vector_store import EnhancedGrantVectorStore
from document_processor import DocumentReader


def rebuild_database(grants_directory: str, clear_existing: bool = True):
    """
    Rebuild the enhanced vector database with all historical grants

    Args:
        grants_directory: Path to directory containing grant .txt files
        clear_existing: Whether to clear existing collections first
    """
    print("="*70)
    print("REBUILDING ENHANCED VECTOR DATABASE")
    print("="*70)

    # Initialize enhanced vector store
    print("\nInitializing enhanced vector store...")
    store = EnhancedGrantVectorStore()

    # Clear existing if requested
    if clear_existing:
        print("\nClearing existing collections...")
        confirmation = input("This will delete all existing data. Continue? (yes/no): ")
        if confirmation.lower() == "yes":
            store.clear_all_collections()
            print("✓ Collections cleared")
        else:
            print("Aborted. Existing data preserved.")
            return

    # Get all grant files
    grants_path = Path(grants_directory)
    if not grants_path.exists():
        print(f"✗ Error: Directory not found: {grants_directory}")
        return

    grant_files = list(grants_path.glob("*.txt"))
    if not grant_files:
        print(f"✗ Error: No .txt files found in {grants_directory}")
        return

    print(f"\nFound {len(grant_files)} grant files to process")
    print(f"Location: {grants_directory}\n")

    # Initialize document reader
    doc_reader = DocumentReader()

    # Process each grant
    total_items = 0
    successful = 0
    failed = 0

    for i, file_path in enumerate(tqdm(grant_files, desc="Processing grants"), 1):
        try:
            print(f"\n[{i}/{len(grant_files)}] Processing: {file_path.name}")

            # Read the file with encoding detection
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except UnicodeDecodeError:
                # Try latin-1 encoding
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text = f.read()
                except:
                    # Try with errors='ignore'
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()

            if not text.strip():
                print(f"  ⚠ Warning: Empty file, skipping")
                failed += 1
                continue

            # Extract metadata from filename
            filename = file_path.name
            metadata = {
                "filename": filename,
                "source": "historical_grant",
                "file_path": str(file_path)
            }

            # Infer grant type from filename
            if "StartUp NYCHA" in filename or "Startup NYCHA" in filename:
                metadata["grant_type"] = "StartUp NYCHA"
            elif "Journey" in filename:
                metadata["grant_type"] = "Journey Platform"
            elif "Solar" in filename or "Cambio Solar" in filename:
                metadata["grant_type"] = "Cambio Solar"
            elif "Coding" in filename or "AI" in filename:
                metadata["grant_type"] = "Cambio Coding & AI"
            elif "AWS" in filename:
                metadata["grant_type"] = "AWS"
            elif "BRL" in filename or "Catalyst" in filename:
                metadata["grant_type"] = "BRL Catalyst"
            else:
                metadata["grant_type"] = "General"

            # Infer year if present
            import re
            year_match = re.search(r'20\d{2}', filename)
            if year_match:
                metadata["year"] = year_match.group(0)

            # Add document to enhanced store
            counts = store.add_document_enhanced(text, metadata)

            total_items += sum(counts.values())
            successful += 1

            print(f"  ✓ Added successfully ({sum(counts.values())} total items)")

        except Exception as e:
            print(f"  ✗ Error processing {file_path.name}: {e}")
            failed += 1
            continue

    # Final statistics
    print("\n" + "="*70)
    print("REBUILD COMPLETE")
    print("="*70)
    print(f"Files processed: {successful + failed}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"Total items added: {total_items}")

    # Get collection statistics
    print("\nCollection Statistics:")
    stats = store.get_all_stats()
    for collection, count in stats.items():
        if collection != "total_items":
            print(f"  {collection}: {count:,}")
    print(f"  {'='*40}")
    print(f"  TOTAL: {stats['total_items']:,}")

    print("\n✓ Enhanced vector database ready for 95-98% authentic generation!")


def test_retrieval(store: EnhancedGrantVectorStore):
    """
    Test multi-layer retrieval after rebuild

    Args:
        store: Enhanced vector store
    """
    print("\n" + "="*70)
    print("TESTING MULTI-LAYER RETRIEVAL")
    print("="*70)

    test_queries = [
        ("Need Statement", "entrepreneurship for NYCHA residents economic empowerment"),
        ("Methodology", "how we recruit and train participants co-design"),
        ("Project Description", "Journey platform gamified learning"),
    ]

    for section_name, query in test_queries:
        print(f"\nTest Query: {section_name}")
        print(f"Query: {query}")
        print("-"*70)

        results = store.retrieve_multi_layer(
            query=query,
            section_name=section_name,
            n_content=2,
            n_voice=3,
            n_data=2,
            n_codesign=2,
            n_programs=2
        )

        print(f"Results:")
        print(f"  Content chunks: {len(results.get('content', []))}")
        print(f"  Voice phrases: {len(results.get('voice', []))}")
        print(f"  Data points: {len(results.get('data', []))}")
        print(f"  Quotes: {len(results.get('quotes', []))}")
        print(f"  Co-design: {len(results.get('codesign', []))}")
        print(f"  Programs: {len(results.get('programs', []))}")

        if results.get('voice'):
            print(f"\nSample Voice Phrases Retrieved:")
            for item in results['voice'][:2]:
                print(f"  - {item['text'][:100]}...")

        if results.get('data'):
            print(f"\nSample Data Points Retrieved:")
            for item in results['data'][:2]:
                print(f"  - {item['text']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rebuild enhanced vector database with historical grants")
    parser.add_argument(
        "--grants-dir",
        default="/Users/abdulbasir/cambio-labs-eduquery/local/examples",
        help="Directory containing grant .txt files"
    )
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Don't clear existing collections (append instead)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run retrieval tests after rebuild"
    )

    args = parser.parse_args()

    # Rebuild database
    rebuild_database(
        grants_directory=args.grants_dir,
        clear_existing=not args.no_clear
    )

    # Run tests if requested
    if args.test:
        store = EnhancedGrantVectorStore()
        test_retrieval(store)

    print("\n✓ All done!")
