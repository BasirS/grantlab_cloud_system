"""
Configuration settings for Cambio Labs Grant Application AI Agent
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
HISTORICAL_GRANTS_DIR = BASE_DIR.parent / "local" / "examples"
CLOUD_GRANTS_DIR = BASE_DIR / "contextual-docs" / "grant_application_examples"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-4-turbo-preview")

# Vector Database Configuration
VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "chroma")  # chroma for local, pinecone for cloud
CHROMA_PERSIST_DIR = DATA_DIR / "chroma_db"
CHROMA_COLLECTION_NAME = "cambio_grants"

# Pinecone Configuration (optional, for cloud deployment)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "cambio-grants")

# Document Processing
CHUNK_SIZE = 1500  # characters per chunk
CHUNK_OVERLAP = 200  # overlap between chunks
SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".docx", ".doc", ".md"]

# Grant Generation
DEFAULT_SECTIONS = [
    "Executive Summary",
    "Need Statement",
    "Project Description",
    "Methodology",
    "Evaluation Plan",
    "Budget Narrative"
]

# Application Settings
MAX_SIMILAR_DOCS = 5  # number of similar documents to retrieve for RAG
TEMPERATURE = 0.7  # creativity of AI generation (0-1)
MAX_TOKENS = 2000  # max length of generated sections

# Cambio Labs Organization Info
ORGANIZATION_NAME = "Cambio Labs"
ORGANIZATION_MISSION = """Cambio Labs empowers underestimated BIPOC youth and adults through
technology education, workforce development, and entrepreneurship programs."""

KEY_PROGRAMS = [
    "Journey Platform (AI-powered learning with Sparky bot)",
    "StartUp NYCHA (business accelerator for public housing residents)",
    "Cambio Solar/Green Workforce Development",
    "Cambio Coding & AI"
]

TARGET_BENEFICIARIES = """Low-income BIPOC youth and adults, public housing residents,
and underrepresented communities in tech and entrepreneurship."""
