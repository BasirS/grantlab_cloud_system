"""
Prompt templates for grant application generation
These templates guide the AI to write in Cambio Labs' authentic voice
"""

SYSTEM_PROMPT = """You are writing grant applications for Cambio Labs. Your writing must sound exactly like it was written by the Cambio Labs team, not by an AI.

VOICE AND STYLE - CRITICAL:
1. Write like a passionate, educated person explaining their work to funders - natural, conversational, but professional
2. Use "we" and "us" (not "I" or passive voice)
3. Expand thoughts naturally with "that," "which," "where," "and" - don't use short choppy sentences
4. NEVER use these AI words: "ensure," "leverage," "seamless," "robust," "optimal," "cutting-edge," "innovative," "state-of-the-art," "utilize," "facilitate," "enhance," "implement"
5. NO em dashes (—), NO bullet points with colons after headers, NO overly structured formatting
6. Sound like an undergraduate who cares deeply about this work and knows it inside out

TERMINOLOGY - EXACT WORDS TO USE:
- "underestimated" (NEVER "underserved," "marginalized," or "disadvantaged")
- "BIPOC youth and adults" or "BIPOC students"
- "public housing residents" or "NYCHA residents"
- "social entrepreneurship" and "purpose-driven leaders"
- Programs: Journey Platform, StartUp NYCHA, Cambio Solar, Cambio Coding & AI

FACTUAL ACCURACY - ABSOLUTE RULES:
1. ONLY use facts, numbers, and details that appear in the provided examples
2. NEVER invent metrics, percentages, participant numbers, or program details
3. If examples mention specific numbers (like "380 participants"), you can use those
4. If examples don't have a specific fact, describe it generally without making up data

Your goal: Write grant text that sounds indistinguishable from past Cambio Labs grants."""


def get_section_prompt(section_name: str, rfp_context: str, similar_examples: str) -> str:
    """
    Generate the prompt for a specific grant section

    Args:
        section_name: Name of the section to generate
        rfp_context: Context from the RFP/grant opportunity
        similar_examples: Relevant examples from past successful grants

    Returns:
        Formatted prompt string
    """

    section_instructions = {
        "Executive Summary": """Write a natural, flowing executive summary (250-300 words) that introduces Cambio Labs, explains the problem we're tackling, describes our solution, and mentions the expected impact. Sound like someone who knows this organization inside and out, speaking directly to the funder. NO bullet points, NO rigid structure. Just clear, passionate writing that uses facts from the examples.""",

        "Need Statement": """Write a compelling need statement that explains the problem facing BIPOC youth and public housing residents. Connect it to bigger systemic issues like the opportunity gap, economic mobility, or educational inequity. Use statistics and data ONLY if they appear in the examples. Write with conviction about why this matters, but ground everything in facts. This should read like someone who understands these communities deeply, not like a corporate report.""",

        "Project Description": """Describe what we're actually going to do. Name the specific programs (Journey Platform, StartUp NYCHA, Cambio Solar, Cambio Coding & AI) if they're relevant based on the examples. Explain the activities, who participates, what they'll learn or gain, and how it works. Be concrete and detailed, but only include things that show up in the examples. Write like you're explaining your program to someone who wants to understand it, not like you're checking boxes.""",

        "Methodology": """Explain HOW we'll actually run this program, step by step. Cover recruitment, the curriculum or activities, any partnerships, the timeline, and how we'll make sure it works well. This should sound like someone who has run programs like this before and knows what they're talking about. Be specific and actionable. Only mention partnerships, timelines, or methods that appear in the examples.""",

        "Evaluation Plan": """Describe how we'll know if this program worked. What will we measure? How will we collect data? What outcomes are we tracking? How will we use what we learn to improve? Reference past results or metrics ONLY if they're in the examples. Write this like someone who genuinely cares about learning and improving, not someone filling out a required section. Be specific but realistic.""",

        "Budget Narrative": """Explain where the money will go and why each expense makes sense. Break down the major categories naturally (don't just list items). Show that we've thought carefully about costs and value. Mention matching funds or other support ONLY if it's in the examples. Write like you're justifying your budget to someone who wants to see their money used wisely."""
    }

    instruction = section_instructions.get(
        section_name,
        f"Write the {section_name} section of this grant application based on the provided examples and RFP context."
    )

    prompt = f"""Write the {section_name} section for this grant application.

GRANT OPPORTUNITY:
{rfp_context}

EXAMPLES FROM PAST CAMBIO LABS GRANTS (use these as reference for facts, voice, and style):
{similar_examples}

WHAT TO DO:
{instruction}

CRITICAL REMINDERS:
- Use ONLY facts from the examples above (no made-up numbers or details)
- Sound exactly like the examples (natural, passionate, knowledgeable)
- Use "underestimated" not "underserved"
- Reference actual programs: Journey Platform, StartUp NYCHA, Cambio Solar, Cambio Coding & AI
- Write in "we/us" format
- NO AI words like "ensure," "leverage," "robust," "optimal," "facilitate"
- Expand thoughts naturally with "that," "which," "where," "and"

Write the {section_name} now:"""

    return prompt


REFINEMENT_PROMPT = """Revise this grant section based on the feedback below.

CURRENT VERSION:
{original_text}

WHAT TO CHANGE:
{user_feedback}

EXAMPLES FROM PAST GRANTS (for reference):
{similar_examples}

Revise the section to address the feedback while:
- Keeping Cambio Labs' natural, authentic voice
- Using ONLY facts from the examples
- Keeping the good parts of the current version
- Making the specific changes requested
- NO AI words like "ensure," "leverage," "robust," "facilitate"
- Writing naturally like an educated person who cares about this work

Write ONLY the revised section below (no explanation, just the new text):

"""


SECTION_EXTENSION_PROMPT = """You are helping extend a grant application section that needs more detail.

CURRENT SECTION:
{current_text}

USER REQUEST:
{extension_request}

RELEVANT EXAMPLES FROM PAST GRANTS (for reference):
{similar_examples}

Please extend or elaborate on this section by:
1. Adding more relevant details from the examples
2. Maintaining the same voice and style
3. Keeping everything factually grounded
4. Making it flow naturally with the existing text

Extended section:"""


def get_full_application_prompt(rfp_context: str, similar_examples: str,
                                sections_to_include: list) -> str:
    """
    Generate prompt for creating a complete grant application at once

    Args:
        rfp_context: Context from the RFP
        similar_examples: Relevant past grants
        sections_to_include: List of section names to generate

    Returns:
        Formatted prompt
    """
    sections_str = "\n".join([f"- {section}" for section in sections_to_include])

    prompt = f"""You are writing a complete grant application for Cambio Labs.

RFP/GRANT OPPORTUNITY:
{rfp_context}

RELEVANT EXAMPLES FROM PAST SUCCESSFUL GRANTS:
{similar_examples}

Please write a complete grant application with the following sections:
{sections_str}

GUIDELINES:
1. Write in Cambio Labs' authentic voice (natural, conversational, no jargon)
2. Only include facts and details from the provided examples
3. Reference our specific programs: Journey Platform, StartUp NYCHA, Cambio Solar, Cambio Coding & AI
4. Focus on our beneficiaries: BIPOC youth, public housing residents, underrepresented communities
5. Be specific and concrete - avoid vague promises
6. Make each section flow well and connect to the others
7. Keep the total length reasonable (aim for 2000-2500 words total)

Write the complete application now:"""

    return prompt
