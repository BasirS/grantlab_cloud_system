# GrantLab Cloud System

AI-powered grant discovery and writing assistant for Cambio Labs.  

## What This Is

GrantLab is a web application that helps Cambio Labs, a nonprofit focused on empowering BIPOC youth and adults through technology and entrepreneurship programs, discover relevant federal grants and write authentic grant proposals. The system was built to solve a real problem: Cambio Labs applies for 30 to 50 grants every year, and hiring professional grant writers costs between $30,000 and $60,000 annually. Beyond the cost, external writers often struggle to capture the organization's unique voice and mission.

This system generates complete grant applications in under 2 minutes while maintaining a 95.8% voice authenticity score, which means the proposals sound like Cambio Labs actually wrote them, not a generic AI tool.

## How It Works

The application uses a specialized approach called multi-layer Retrieval Augmented Generation, or RAG. Instead of just dumping everything into one big database, the system organizes 48 historical grant applications into six different collections. Each collection serves a specific purpose.

The first collection stores complete grant sections that provide comprehensive context. The second focuses on voice phrases, which are the distinctive ways Cambio Labs describes their work, like using "underestimated communities" instead of "underserved populations" or talking about "community-powered prosperity." The third collection holds data and metrics, real numbers from actual programs like the fact that 95% of participants were women of color or that less than 1% of NYCHA residents report business revenue. The fourth stores participant voices, direct quotes and testimonials from people who actually went through the programs. The fifth captures co-design examples, which show how programs are developed in partnership with community members. The sixth maintains detailed descriptions of each program, like Journey Platform, StartUp NYCHA, Cambio Solar, and Cambio Coding.

When you ask the system to generate a grant section, it searches across all six collections simultaneously, pulls relevant information from each, and uses that context to guide GPT-4 in writing content that matches Cambio Labs' authentic style. After generating each section, a voice validation system scores it on a 0 to 100 scale. If the score drops below 85, the system automatically regenerates that section up to three times until it meets the quality threshold.

## Technology Stack

The system is built on OpenAI's GPT-4 for text generation and their text-embedding-3-small model for semantic search. ChromaDB handles the vector database storage, which currently holds 1,368 specialized items across those six collections. The web interface runs on Streamlit, which made it possible to build a clean, functional interface quickly without dealing with complicated front-end frameworks. Grant discovery connects directly to the Grants.gov API to pull live federal funding opportunities.

Everything runs on Python 3.9 or higher, and the whole system can be deployed to Streamlit Cloud for free or run locally on your own machine.

## Getting Started

You need Python 3.9 or later and an OpenAI API key to run this. Here is how you set it up.

First, clone the repository from GitHub and navigate into the project directory:

```bash
git clone https://github.com/BasirS/grantlab_cloud_system.git
cd grantlab_cloud_system
```

Install all the dependencies using pip:

```bash
pip install -r requirements.txt
```

Create a file called `.env` in the project root and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

The first time you run the system, you need to build the vector database from the historical grant documents. This takes a few minutes but only needs to happen once:

```bash
python rebuild_enhanced_database.py
```

After that finishes, start the Streamlit application:

```bash
streamlit run app.py
```

The interface will open in your browser at http://localhost:8501.

## Using the Application

The interface has three main tabs that follow the natural workflow of grant writing.

The Discovery tab connects to Grants.gov and searches for relevant federal grant opportunities. The system automatically scores each grant based on how well it aligns with your organization's focus areas. Instead of manually searching through hundreds of opportunities, you get a filtered list of the 10 to 30 most relevant matches. You can review the details of each grant, including the funding agency, deadline, and opportunity number, then select one to move forward with.

The Generation tab is where you actually create the grant application. You can either paste in the RFP requirements directly or select a grant from the discovery results, which automatically populates the requirements field. Select which sections you want to generate - typically Executive Summary, Need Statement, Project Description, Methodology, Evaluation Plan, and Budget Narrative - then click generate. The system processes each section and shows you real-time progress along with voice authenticity scores. If a section scores below 85%, the system automatically tries again.

The Review tab lets you look at all the generated sections together, check the voice scores, make edits if needed, and export everything to a professionally formatted Word document. The export includes a cover page with your organization's logo and contact information, a table of contents with page numbers, proper headers and formatting, and standard grant proposal styling with Times New Roman 12pt font and 1 inch margins.

## Voice Authenticity System

Getting the voice right was one of the hardest technical challenges. The system had to learn what makes Cambio Labs' writing distinctive and then replicate that in generated content.

The voice validation system looks for several things. First, it checks that the writing avoids generic nonprofit buzzwords like "leverage," "catalyze," "stakeholders," or "impactful." These words appear constantly in template-based grant writing but rarely in Cambio Labs' actual applications. Second, it verifies that organization-specific terminology appears correctly, using phrases like "underestimated communities" and "community-powered prosperity" that reflect Cambio Labs' values and approach. Third, it looks for real data points and metrics from past applications, like specific participant numbers, program outcomes, and demographic information. Fourth, it checks for participant quotes and testimonials that add authenticity and human impact.

The system also actively avoids common tells that make writing sound AI-generated, phrases like "we are committed to," "driven by a mission to," or "at the heart of our work." It removes formatting red flags like timestamps or labels that say "generated." The goal is to produce content that reads like a person who deeply understands the organization sat down and wrote it, not content that was obviously produced by a template or algorithm.

Testing across multiple grant applications showed an average voice authenticity score of 95.8 out of 100, which is high enough that team members familiar with Cambio Labs' writing cannot reliably distinguish generated sections from human-written ones in blind tests.

## System Architecture

The core of the system is the multi-layer RAG architecture described earlier. When you request a grant section, here is what happens behind the scenes.

Your input goes to the retrieval system, which queries all six specialized collections simultaneously. Each collection returns the most relevant chunks based on semantic similarity to your request. The full content collection might return paragraphs from similar grant sections written in the past. The voice phrases collection pulls characteristic language patterns. The data metrics collection finds specific statistics that support your narrative. The participant voices collection retrieves relevant testimonials. The co-design examples collection locates descriptions of partnership approaches. The program descriptions collection grabs details about whichever programs are relevant to this particular grant.

All those retrieved chunks get assembled into a comprehensive context package that gets passed to GPT-4 along with carefully crafted prompts that emphasize voice authenticity. The prompts explicitly tell the model to write like Cambio Labs, avoid generic nonprofit language, use the organization's distinctive terminology, include specific data points, and structure sentences in the longer, more explanatory style that characterizes their writing.

GPT-4 generates an initial draft using that context as examples rather than as text to copy verbatim. The draft goes to the voice validation system, which scores it across multiple dimensions. If the score meets the threshold, the content moves forward to formatting. If not, the system identifies specific issues, like too many buzzwords or not enough concrete data, and makes targeted revisions before trying again.

The final step is professional formatting, where the text gets converted into a properly styled Word document with all the structural elements that grant reviewers expect to see.

## Cost Analysis

Running this system is dramatically cheaper than hiring professional grant writers. Each full grant application, with six complete sections, costs between $3 and $5 in OpenAI API usage. If Cambio Labs generates 50 grants per year, the total API cost would be $150 to $250 annually.

Compare that to professional grant writers who charge $75 to $150 per hour and typically spend 8 hours on a comprehensive grant proposal. For 50 grants per year, that works out to $30,000 to $60,000 in external costs. The ROI is obvious, a 99% cost reduction while maintaining quality and improving voice authenticity.

The vector database runs locally using ChromaDB, which means there are no recurring database hosting fees. The one-time cost to generate embeddings for 48 historical documents was about $2. If you deploy to Streamlit Cloud, the hosting is free for public applications or $20 per month for private ones.

## Deploying to Streamlit Cloud

Getting this running in the cloud is straightforward. Streamlit Cloud offers free hosting for public applications, which makes this accessible even for small nonprofits.

First, make sure your code is pushed to a GitHub repository. Go to share.streamlit.io and connect your GitHub account. Select your repository from the list and set `app.py` as the main file. In the Secrets management section, add your OpenAI API key so the deployed app can access it. Click deploy, and within a few minutes your application will be live at a public URL.

The one consideration with Streamlit Cloud deployment is that ChromaDB creates local files for the vector database. You need to run the database rebuild script locally first, then commit the generated `data/chroma_db` directory to your repository. The deployed app can then read from those files. This approach works well for a database that does not change frequently, like one built from historical documents.

For organizations that need more control or want to keep everything private, Docker deployment is also supported. The repository includes a Dockerfile that sets up all the dependencies and configuration.

## Adapting for Your Organization

While this system was built specifically for Cambio Labs, the architecture can be adapted for other organizations. The key is having a collection of historical grant applications that represent your organization's voice and programs.

To customize the system, replace the historical grants in the `data/historical_grants/` directory with your own documents. Update the keywords in `config/internal_keywords.json` to reflect your organization's focus areas and mission. Run the database rebuild script to process your documents and create the vector collections. Then modify the voice guidelines in `src/generation/voice_guidelines.py` to reflect your organization's distinctive language patterns and prohibited terms.

The generation system will then learn from your historical applications instead of Cambio Labs' materials, producing content that matches your organization's authentic voice.

## Performance Results

The system was tested extensively with real grant applications. Here are the results from generating a complete six-section application:

Executive Summary scored 100 out of 100 for voice authenticity. Need Statement also scored 100 out of 100. Project Description scored 95 out of 100. Methodology scored 90 out of 100. Evaluation Plan scored 95 out of 100. Budget Narrative scored 95 out of 100.

The average across all six sections was 95.8 out of 100, which represents excellent alignment with authentic organizational voice. Generation speed ranged from 5 to 15 seconds per section, with the complete six-section application taking less than 2 minutes total. Voice validation added just 1 to 2 seconds per section.

These numbers demonstrate that the system is both fast enough for practical use and accurate enough to produce submission-quality content without extensive human editing.

## Security and Privacy Considerations

Grant applications often contain sensitive information about program participants, many from vulnerable communities. This system was designed with privacy in mind.

API keys are stored in environment variables and never committed to version control. The .gitignore file explicitly excludes .env files, credentials, and any other sensitive data. All participant data stays in your local environment. The ChromaDB vector database runs locally rather than on external servers. While OpenAI's API does receive the text you send for generation, their privacy policy states they do not use API data to train models. Generated Word documents contain no metadata indicating they were produced by AI, no timestamps saying "generated on," and no other red flags that would reveal the system used.

For organizations with strict data security requirements, the entire system can be run on a local machine with no internet connection except for the OpenAI API calls, which are necessary for the GPT-4 generation step.

## Where to Get Help

If you run into issues, have questions, or want to request features, the GitHub repository has an issues section where you can post. You can also reach out directly via email to abdulbasirsamad@gmail.com.

The code is open source under the MIT license, which means you can use it, modify it, and adapt it for your own purposes as long as you include the license file.

## About This Project

This system was built by Basir Abdul Samad for Cambio Labs as part of a project to make high-quality grant writing more accessible to nonprofits. Cambio Labs focuses on empowering underestimated communities through technology education, workforce development, and entrepreneurship programs. Their work with NYCHA residents, BIPOC youth and adults, and other underrepresented populations inspired the need for a grant writing tool that could maintain authentic voice while reducing costs.

The current version is 2.1, which includes the enhanced multi-layer RAG system, voice validation, and professional formatting. Development started in early November 2025 and reached production readiness within two weeks through iterative testing and refinement.

The system represents a practical application of modern AI techniques to solve a real problem faced by mission-driven organizations. Rather than replacing human grant writers entirely, it serves as a powerful starting point that captures organizational voice and incorporates real data, which can then be refined and customized for specific grant opportunities.
