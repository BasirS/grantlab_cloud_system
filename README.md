# GrantLab Cloud System

> AI-powered grant discovery and application generation for nonprofit organizations

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://grantlab-cloud-system.streamlit.app)

## Overview

GrantLab is a production-ready grant writing assistant built specifically for **Cambio Labs**, a nonprofit empowering underestimated BIPOC youth and adults through technology education and entrepreneurship. The system discovers relevant federal grants and generates authentic, submission-quality proposals in under 2 minutes.

### Key Features

- **🔍 Grant Discovery**: Real-time search of Grants.gov federal opportunities with intelligent relevance scoring
- **✍️ AI Generation**: GPT-4-powered proposal writing with 95.8% voice authenticity
- **🎯 Voice Validation**: Automatic scoring and regeneration to maintain organizational authenticity
- **📊 Multi-Layer RAG**: 6 specialized knowledge collections built from 48 historical grants
- **📄 Professional Export**: Industry-standard Word documents ready for submission
- **🌐 Web Interface**: Streamlit-powered UI accessible from any device

## Technology Stack

- **AI Models**: OpenAI GPT-4-turbo-preview, text-embedding-3-small
- **Vector Database**: ChromaDB with 1,368 specialized items
- **Web Framework**: Streamlit
- **Grant Data**: Grants.gov API integration
- **Python**: 3.9+

## Quick Start

### Prerequisites

```bash
python >= 3.9
pip
OpenAI API key
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/BasirS/grantlab_cloud_system.git
cd grantlab_cloud_system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Build the vector database** (first time only)
```bash
python rebuild_enhanced_database.py
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Usage

### 1. Grant Discovery

Navigate to the **Discovery** tab to search Grants.gov for relevant federal grant opportunities. The system automatically scores each grant based on alignment with your organization's focus areas.

### 2. Generate Application

In the **Generation** tab:

1. Enter the RFP/grant requirements
2. Specify sections to generate (Executive Summary, Need Statement, etc.)
3. Click **Generate Application**
4. Review voice authenticity scores (system auto-retries if < 85%)

### 3. Review & Refine

The **Review** tab allows you to:
- View all generated sections
- Check voice authenticity scores
- Refine individual sections
- Export to Word format

### 4. Export

Export your complete proposal as a professionally formatted Word document with:
- Cover page with organization details
- Proper headers and page numbers
- Times New Roman 12pt, 1" margins
- Table of contents for multi-section proposals

## Voice Authenticity System

GrantLab ensures generated content matches your organization's authentic voice through:

### Required Elements
- ✅ Signature phrases from historical grants
- ✅ Organization-specific terminology ("underestimated communities", "community-powered prosperity")
- ✅ Real data points and metrics from past applications
- ✅ Participant quotes and testimonials

### Forbidden Elements
- ❌ Generic nonprofit buzzwords ("leverage", "catalyze", "ensure")
- ❌ AI-generated tells ("we are committed to", "driven by a mission to")
- ❌ Vague claims without specific data
- ❌ Formatting red flags (timestamps, "generated" labels)

**Average Voice Score**: 95.8/100 across 6-section applications

## Architecture

### Multi-Layer RAG System

The system maintains 6 specialized knowledge collections:

1. **Full Content** (618 items): Complete grant sections for comprehensive retrieval
2. **Voice Phrases** (13 items): Signature language patterns
3. **Data Metrics** (167 items): Specific statistics and outcomes
4. **Participant Voices** (8 items): Direct quotes and testimonials
5. **Co-Design Examples** (7 items): Partnership language samples
6. **Program Descriptions** (555 items): Detailed program information

### Generation Pipeline

```
User Input (RFP Requirements)
    ↓
Multi-Layer Retrieval (Query all 6 collections)
    ↓
Context Assembly (Combine relevant chunks)
    ↓
GPT-4 Generation (Voice-aware prompts)
    ↓
Voice Validation (0-100 scoring)
    ↓
Auto-Retry if needed (< 85% threshold)
    ↓
Professional Formatting
    ↓
Export to Word/PDF
```

## Cost Analysis

### Production Usage
- **Per application** (6 sections): $3-5
- **50 grants/year**: $150-250
- **Vector database**: $0 (local ChromaDB)

### Compare to Traditional
- Professional grant writer: $75-150/hour
- 8 hours per grant × 50 grants = $30,000-60,000/year
- **ROI**: 99% cost reduction

## Deployment

### Streamlit Cloud (Recommended)

1. Push your repository to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository
5. Set `app.py` as the main file
6. Add `OPENAI_API_KEY` in Secrets management
7. Deploy!

### Docker Deployment

```bash
docker build -t grantlab .
docker run -p 8501:8501 --env-file .env grantlab
```

## Configuration

### Streamlit Settings

Edit `.streamlit/config.toml` to customize:
- Page title and favicon
- Theme colors
- Server settings

### Organization Customization

To adapt for your organization:

1. Replace historical grants in `data/historical_grants/`
2. Update `config/internal_keywords.json` with your focus areas
3. Rebuild vector database: `python rebuild_enhanced_database.py`
4. Update voice guidelines in `src/generation/voice_guidelines.py`

## System Performance

### Tested Results (6-Section Grant)

| Section | Voice Score | Status |
|---------|-------------|--------|
| Executive Summary | 100/100 | Perfect ✨ |
| Need Statement | 100/100 | Perfect ✨ |
| Project Description | 95/100 | Excellent ✅ |
| Methodology | 90/100 | Very Good ✅ |
| Evaluation Plan | 95/100 | Excellent ✅ |
| Budget Narrative | 95/100 | Excellent ✅ |
| **AVERAGE** | **95.8/100** | **A+ Grade** 🎯 |

### Speed Metrics
- **Generation**: 5-15 seconds per section
- **Full application**: < 2 minutes (6 sections)
- **Voice validation**: 1-2 seconds per section

## Security & Privacy

- ✅ API keys stored in environment variables (never committed)
- ✅ No participant data leaves your local environment
- ✅ ChromaDB runs locally (no external database)
- ✅ OpenAI API calls comply with their privacy policy
- ✅ Exports contain no "generated" metadata

## Support

For issues, questions, or feature requests:
- **GitHub Issues**: [grantlab_cloud_system/issues](https://github.com/BasirS/grantlab_cloud_system/issues)
- **Email**: abdulbasirsamad@gmail.com

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built for **Cambio Labs** - Empowering underestimated communities through technology, education, and entrepreneurship.

---

**Built by**: Abdul Basir (BasirS)
**Organization**: Cambio Labs
**Version**: 2.1 (Production Ready)
**Last Updated**: November 2025
