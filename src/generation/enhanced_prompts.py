"""
Enhanced Prompt Templates for 95-98% Voice Authenticity
Integrates voice guidelines, signature phrases, and multi-layer RAG context
"""

from typing import Dict, List

from src.generation.voice_guidelines import (
    ENHANCED_SYSTEM_PROMPT,
    get_enhanced_section_instructions,
    SIGNATURE_PHRASES,
    AUTHENTIC_DATA_POINTS
)


def get_enhanced_section_prompt(section_name: str, rfp_context: str,
                                 multi_layer_context: str) -> str:
    """
    Generate enhanced prompt with comprehensive voice guidance

    Args:
        section_name: Name of the section to generate
        rfp_context: Context from the RFP/grant opportunity
        multi_layer_context: Formatted context from multi-layer RAG retrieval

    Returns:
        Formatted prompt string with detailed instructions
    """

    # Get section-specific instructions
    section_instructions = get_enhanced_section_instructions(section_name)

    # Build comprehensive prompt
    prompt = f"""You are writing the {section_name} section for a Cambio Labs grant application.

{'='*70}
GRANT OPPORTUNITY / RFP CONTEXT:
{'='*70}
{rfp_context}

{'='*70}
RETRIEVED EXAMPLES AND AUTHENTIC CAMBIO LABS CONTENT:
{'='*70}
{multi_layer_context}

{'='*70}
SECTION-SPECIFIC INSTRUCTIONS:
{'='*70}
{section_instructions}

{'='*70}
CRITICAL VOICE REQUIREMENTS (NON-NEGOTIABLE):
{'='*70}

1. FORBIDDEN AI WORDS - NEVER USE:
   ❌ catalyze, leverage, optimize, ensure, facilitate, enhance
   ❌ "at the heart of", "driven by a mission to", "bridge to empowerment"
   ❌ "challenge and change", "deeply rooted in", "testament to"

2. REQUIRED TERMINOLOGY:
   ✓ "underestimated communities" (NEVER "underserved")
   ✓ "BIPOC youth and adults" or "BIPOC students"
   ✓ "co-designed with NYCHA residents and tenant leaders" (in methodology/project description)

3. SIGNATURE PHRASES TO USE:
   ✓ "community-powered prosperity"
   ✓ "untapped potential"
   ✓ "purpose-driven leaders"
   ✓ "Those closest to the issues are best equipped to solve them"

4. BE SPECIFIC WITH DATA:
   ✓ Use exact numbers from examples: "60+ signups", "95% women of color", "$27,000 average income"
   ✗ NEVER use vague words: "many", "significant", "various", "numerous"

5. VOICE & TONE:
   - Confident and matter-of-fact (not melodramatic or preachy)
   - First person: "we/our" (never third person "the organization")
   - Sentence length: 15-25 words average (mix of short and medium)
   - Paragraph length: 4-7 sentences

6. AUTHENTICITY CHECKLIST:
   □ Uses signature Cambio Labs phrases from examples
   □ Includes specific data points (numbers, percentages, names)
   □ Avoids ALL AI buzzwords
   □ Sounds like a passionate practitioner, not a marketer
   □ Every sentence adds NEW information (no fluff)

{'='*70}
NOW WRITE THE {section_name.upper()}:
{'='*70}

Write ONLY the section content below (no meta-commentary, no "Here is..." preamble).
Make it sound EXACTLY like Cambio Labs wrote it themselves.

"""

    return prompt


def get_refinement_prompt_enhanced(original_text: str, user_feedback: str,
                                   multi_layer_context: str,
                                   section_name: str = "") -> str:
    """
    Enhanced refinement prompt with voice validation

    Args:
        original_text: Original generated text
        user_feedback: User's feedback or revision instructions
        multi_layer_context: Context from multi-layer RAG
        section_name: Section name for context

    Returns:
        Refinement prompt
    """

    prompt = f"""Revise this grant section based on feedback while maintaining Cambio Labs' authentic voice.

{'='*70}
CURRENT VERSION (TO BE REVISED):
{'='*70}
{original_text}

{'='*70}
USER FEEDBACK / WHAT TO CHANGE:
{'='*70}
{user_feedback}

{'='*70}
AUTHENTIC CAMBIO LABS EXAMPLES (for reference):
{'='*70}
{multi_layer_context}

{'='*70}
REVISION GUIDELINES:
{'='*70}

1. Address the specific feedback above
2. Keep the good parts of the current version
3. Use signature Cambio Labs phrases from the examples
4. Include specific data points (not vague language)
5. Avoid ALL AI buzzwords: catalyze, leverage, ensure, facilitate, etc.
6. Sound natural and authentic (not corporate or melodramatic)

VOICE CHECKLIST:
□ First person "we/our"
□ Specific data, not vague words
□ Signature phrases used
□ No AI buzzwords
□ Sounds like Cambio Labs

{'='*70}
WRITE ONLY THE REVISED SECTION (no explanation):
{'='*70}

"""

    return prompt


def get_full_application_prompt_enhanced(rfp_context: str,
                                         all_retrieved_context: Dict[str, str],
                                         sections_to_include: List[str]) -> str:
    """
    Enhanced prompt for generating a complete application

    Args:
        rfp_context: RFP/grant opportunity description
        all_retrieved_context: Dict mapping section names to their multi-layer context
        sections_to_include: List of section names to generate

    Returns:
        Comprehensive prompt for full application
    """

    sections_str = "\n".join([f"   {i+1}. {section}" for i, section in enumerate(sections_to_include)])

    # Sample context from first section
    sample_context = list(all_retrieved_context.values())[0] if all_retrieved_context else "No examples available"

    prompt = f"""You are writing a COMPLETE grant application for Cambio Labs.

{'='*70}
GRANT OPPORTUNITY / RFP:
{'='*70}
{rfp_context}

{'='*70}
SECTIONS TO WRITE:
{'='*70}
{sections_str}

{'='*70}
AUTHENTIC CAMBIO LABS EXAMPLES (use for reference):
{'='*70}
{sample_context}

(Additional section-specific examples are provided for each section)

{'='*70}
COMPREHENSIVE VOICE GUIDELINES:
{'='*70}

FORBIDDEN AI WORDS (never use):
❌ catalyze, leverage, optimize, ensure, facilitate, enhance, utilize
❌ "at the heart of", "driven by a mission", "bridge to", "challenge and change"

REQUIRED TERMS:
✓ "underestimated communities" (not "underserved")
✓ "BIPOC youth and adults"
✓ "co-designed with NYCHA residents and tenant leaders"
✓ "community-powered prosperity"
✓ "purpose-driven leaders"

PROGRAMS (describe with specifics):
- Journey Platform: gamified platform, earn gemstones, lifetime alumni access
- StartUp NYCHA: 6-month accelerator, 60+ signups at Fulton, 95% women of color, pitch competition
- Cambio Solar: OSHA/GPRO certifications, community solar cooperatives

DATA TO USE (from real examples):
- "60+ signups at Fulton Houses pilot"
- "95% of participants were women of color"
- "80% would not have pursued venture without this program"
- "Less than 1% of NYCHA residents report business revenue"
- "$27,000 average NYCHA household income"

VOICE & STYLE:
- Confident, matter-of-fact tone (not melodramatic)
- First person "we/our" throughout
- Specific data, no vague words ("many", "significant")
- Sentences: 15-25 words average
- Paragraphs: 4-7 sentences

STRUCTURE FOR EACH SECTION:
1. Executive Summary (250-300 words): Mission, problem, solution, impact
2. Need Statement (300-400 words): Problem with data, systemic context, community connection
3. Project Description (350-450 words): What we'll do, programs, activities, who benefits
4. Methodology (300-400 words): How we'll do it, recruitment, timeline, partnerships
5. Evaluation Plan (250-350 words): What we'll measure, how we'll collect data, past results
6. Budget Narrative (200-300 words): Where money goes, justifications, cost-effectiveness

{'='*70}
WRITE THE COMPLETE APPLICATION NOW:
{'='*70}

Format each section clearly with headers. Write in Cambio Labs' authentic voice.
Make this application indistinguishable from one written by Cambio Labs staff.

"""

    return prompt


# ============================================================================
# SECTION-SPECIFIC ENHANCED PROMPTS
# ============================================================================

def get_executive_summary_prompt_enhanced(rfp_context: str, context: str) -> str:
    """Enhanced Executive Summary prompt"""

    return f"""Write the Executive Summary for this Cambio Labs grant application (250-300 words).

RFP/GRANT OPPORTUNITY:
{rfp_context}

EXAMPLES FROM SUCCESSFUL CAMBIO LABS GRANTS:
{context}

STRUCTURE (natural flow, not bullet points):
1. Opening: State mission clearly and authentically
   - Good: "We create transformative programs that equip BIPOC youth with skills to become purpose-driven entrepreneurs"
   - Bad: "We are driven by a mission to challenge and change systemic barriers"

2. Problem: Concrete and data-driven
   - Use real stats: "Less than 1% of NYCHA residents report business revenue"
   - Avoid vague: "Many underserved communities lack access"

3. Solution: Name specific programs
   - Journey Platform (gamified, gemstones, lifetime access)
   - StartUp NYCHA (6-month, co-designed, pitch competition)
   - Include pilot results: "60+ signups at Fulton Houses, 95% women of color"

4. Impact: Real outcomes
   - "80% reported they would not have pursued their venture without this program"
   - Future vision with specific numbers if known

5. Close: Signature phrase
   - "Transform untapped potential into community-powered prosperity"
   - Or similar authentic Cambio Labs language

CRITICAL RULES:
✗ NO: "catalyze change", "leverage resources", "at the heart of our mission"
✓ YES: "We create", "We partner with", specific program names, real data

Write the Executive Summary now (250-300 words):
"""


def get_need_statement_prompt_enhanced(rfp_context: str, context: str) -> str:
    """Enhanced Need Statement prompt"""

    return f"""Write the Need Statement for this Cambio Labs grant application (300-400 words).

RFP/GRANT OPPORTUNITY:
{rfp_context}

EXAMPLES AND DATA FROM SUCCESSFUL GRANTS:
{context}

STRUCTURE:
1. Opening: Specific, grounded problem (not melodrama)
   - Good: "For thousands of New Yorkers living in public housing, entrepreneurship is one of the few viable paths to income and ownership."
   - Bad: "The chasm between those with access and those without continues to widen..."

2. Data-driven context:
   - Specific stats: "$27,000 average NYCHA income", "Less than 1% report business revenue"
   - Educational gaps if relevant: "1 in 3 BIPOC students attend dropout factories"
   - Local/community-specific data

3. Systemic barriers (grounded, not preachy):
   - Economic mobility challenges
   - Access to technology and training
   - Lack of entrepreneurship models in community

4. Community strength (always balance problem with potential):
   - "untapped potential"
   - "talented and driven entrepreneurs"
   - Community assets and resilience

5. Why Cambio Labs is positioned to address this:
   - Embedded in community
   - Co-designed with residents
   - Track record (cite pilot results)

VOICE:
- Informed and confident (not preachy or condescending)
- Use "underestimated" not "underserved"
- First person: "We see", "We work with"
- Specific, never vague

Write the Need Statement now (300-400 words):
"""


# ============================================================================
# VALIDATION PROMPTS
# ============================================================================

def get_voice_validation_prompt(generated_text: str, section_name: str) -> str:
    """
    Prompt for AI to self-validate and improve voice authenticity

    Args:
        generated_text: Text to validate
        section_name: Section name

    Returns:
        Validation and improvement prompt
    """

    return f"""Review this {section_name} and identify any voice authenticity issues.

GENERATED TEXT:
{generated_text}

VOICE QUALITY CHECKLIST:

1. AI Buzzwords (should be ZERO):
   Check for: catalyze, leverage, ensure, facilitate, optimize, "at the heart of", "driven by a mission"
   Found: [list any found]

2. Required Language:
   ✓ Uses "underestimated" not "underserved": [yes/no]
   ✓ Uses "BIPOC youth and adults": [yes/no]
   ✓ Includes co-design language (if methodology/project description): [yes/no]

3. Specificity:
   ✓ Includes specific numbers/data: [yes/no - list examples]
   ✗ Uses vague words (many, significant, various): [yes/no - list if found]

4. Signature Phrases:
   Uses Cambio Labs signatures: [list any found: "community-powered prosperity", "untapped potential", etc.]

5. Overall Tone:
   Sounds like: [A) Cambio Labs staff, B) Generic nonprofit, C) AI-generated corporate speak]
   Why:

IMPROVEMENT RECOMMENDATIONS:
[Specific changes to make the text more authentic]

REVISED VERSION:
[Rewrite with improvements if needed]
"""


if __name__ == "__main__":
    print("Testing Enhanced Prompts System\n")

    # Test executive summary prompt
    test_rfp = "Seeking proposals for entrepreneurship programs serving BIPOC communities and public housing residents. Budget: $100,000."

    test_context = """
Example 1 (from BRL Catalyst 2024):
For thousands of New Yorkers living in public housing, entrepreneurship is one of the few viable paths to income and ownership. Less than 1% of NYCHA residents report business revenue. Through our six-month StartUp NYCHA accelerator, co-designed with NYCHA residents and tenant leaders, we create pathways to economic empowerment.

=== AUTHENTIC PHRASES ===
- community-powered prosperity
- untapped potential
- Those closest to the issues are best equipped to solve them

=== SPECIFIC DATA ===
- 60+ signups at Fulton Houses
- 95% women of color
- 80% would not have pursued without program
"""

    prompt = get_executive_summary_prompt_enhanced(test_rfp, test_context)

    print("="*70)
    print("ENHANCED EXECUTIVE SUMMARY PROMPT:")
    print("="*70)
    print(prompt)
    print("\n✓ Enhanced prompts system ready!")
