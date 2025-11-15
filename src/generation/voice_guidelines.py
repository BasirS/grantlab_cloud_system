"""
Cambio Labs Voice Guidelines and Authenticity System
This module contains comprehensive voice rules, signature phrases, and validation tools
to achieve 95-98% alignment with authentic Cambio Labs writing
"""

# ============================================================================
# CAMBIO LABS SIGNATURE PHRASES (extracted from 53 historical grants)
# ============================================================================

SIGNATURE_PHRASES = {
    "mission_statements": [
        "We firmly believe that those who are closest to the issues are also best equipped to solve them.",
        "When people gain access to tools, training, and community, they generate the solutions their neighborhoods need most.",
        "Entrepreneurship is more than a business path—it's a tool for reclaiming agency and reshaping local economies.",
        "We champion a new generation of entrepreneurs who prioritize and uplift their neighborhoods.",
        "We create transformative educational programs, technology, and cross-sectoral partnerships that equip program participants with the skills and networks to become founders of organizations driven by social and environmental missions.",
    ],

    "community_empowerment": [
        "For thousands of New Yorkers living in public housing, entrepreneurship is one of the few viable paths to income and ownership.",
        "More than 80% of 2024 participants reported they would not have pursued their venture without this program.",
        "By embedding our accelerator in trusted community spaces, employing NYCHA alumni as instructors, and by providing access to tech and coaching, we create a culturally responsive, high-impact accelerator.",
        "We invite and integrate the feedback of our community members, who we center as experts.",
        "With your support, we will continue to scale a model that transforms untapped potential into community-powered prosperity.",
    ],

    "codesign_language": [
        "co-designed with NYCHA residents and tenant leaders",
        "co-created with community partners",
        "Our approach is based on user-centered design, where we test our assumptions about community needs and engage in two-way dialogues to cultivate empathy before we design.",
        "We center community voices in every aspect of program development.",
        "designed in partnership with those who will benefit most",
    ],

    "program_descriptions": {
        "journey": [
            "Our Journey platform is a gamified learning experience where participants access multimedia lessons, project-based challenges, and live feedback.",
            "Learners earn gemstones they can cash in for prizes, mentorship sessions, and workshops.",
            "All participants gain lifetime access to our alumni community, curriculum, and career opportunities.",
            "Our platform allows us to meet our learners where they are, provide live feedback, and provide an engaging and gamified learning experience.",
        ],
        "startup_nycha": [
            "Six-month business accelerator co-designed with NYCHA residents and tenant leaders",
            "At our Fulton Houses pilot, we had 60+ signups in the first week",
            "95% of participants were women of color",
            "Culminates in a public pitch competition with seed funding opportunities",
            "Creates community-powered prosperity",
        ],
        "cambio_solar": [
            "Green workforce training leading to industry-recognized certifications like OSHA and GPRO",
            "Community-owned solar businesses and cooperatives",
            "Addresses both environmental and economic justice",
        ],
    },

    "impact_language": [
        "community-powered prosperity",
        "untapped potential",
        "purpose-driven leaders",
        "social entrepreneurs who solve local challenges",
        "durable skills for 21st century careers",
        "pathways to economic empowerment",
        "generational wealth creation",
    ],
}

# ============================================================================
# AI BUZZWORDS TO AVOID (these scream "AI-generated")
# ============================================================================

AI_BUZZWORDS_FORBIDDEN = [
    # Overused corporate speak
    "catalyze", "leverage", "optimize", "seamless", "seamlessly",
    "robust", "state-of-the-art", "cutting-edge", "innovative",
    "transformative", "groundbreaking", "revolutionary",

    # AI writing patterns
    "at the heart of what we do", "at the core of our mission",
    "bridge to empowerment", "pathway that challenges",
    "challenge and change", "deeply rooted in", "far more than",
    "the chasm between", "rectifying the", "not just... but...",

    # Generic corporate phrases
    "ensure", "facilitate", "enhance", "utilize", "implement",
    "strategic deployment", "carefully crafted", "testament to",
    "commitment to excellence", "proven track record",
    "we are proud to", "we are excited to", "we are committed to",
    "we are dedicated to", "we are deeply committed", "we recognize",
    "we understand that", "we believe in the power",

    # Melodramatic phrases
    "transformative movement", "pathways that challenge",
    "dedicated to creating", "driven by a mission to",
    "catalyze significant positive change",

    # RED FLAGS - NEVER USE THESE
    "generated", "AI-generated", "created by AI", "produced by",
    "this application was", "this proposal was created",
]

# Words to use sparingly and only with specific context
CAUTION_WORDS = {
    "innovative": "Only use with specific examples of what makes it innovative",
    "transformative": "Use sparingly, prefer 'transformational programs' with concrete outcomes",
    "robust": "Only in 'robust curriculum' or 'robust network' with specifics",
    "ensure": "Replace with 'we will' or 'participants gain'",
    "leverage": "Replace with 'use' or 'build on'",
}

# ============================================================================
# REQUIRED LANGUAGE PATTERNS
# ============================================================================

REQUIRED_PATTERNS = {
    "underestimated": {
        "use": "underestimated communities",
        "never": ["underserved", "disadvantaged alone", "marginalized"],
        "context": "Always pair with strength: 'underestimated communities with untapped potential'"
    },

    "bipoc": {
        "use": "BIPOC youth and adults",
        "also_ok": ["BIPOC students", "BIPOC communities", "BIPOC founders"],
        "never": ["minority", "people of color alone without BIPOC"]
    },

    "codesign": {
        "required_in": ["methodology", "project_description"],
        "phrases": [
            "co-designed with NYCHA residents and tenant leaders",
            "co-created with community partners",
            "designed in partnership with those closest to the issues"
        ]
    },
}

# ============================================================================
# TONE AND PACING RULES
# ============================================================================

TONE_RULES = {
    "sentence_length": {
        "avg_words": 18-25,
        "mix": "Blend of short (10-15 words) and medium (20-30 words) sentences",
        "avoid": "Excessively long (40+) or choppy (under 8) sentences"
    },

    "paragraph_length": {
        "ideal": "4-7 sentences per paragraph",
        "avoid": "Single sentence paragraphs or 10+ sentence blocks"
    },

    "emotional_register": {
        "use": "Confident, matter-of-fact, passionate but grounded",
        "avoid": "Melodramatic, overly inspirational, preachy",
        "example_good": "For thousands of New Yorkers living in public housing, entrepreneurship is one of the few viable paths to income and ownership.",
        "example_bad": "We are driven by a mission to challenge and change the systemic barriers that have long hindered equal opportunities."
    },

    "voice": {
        "first_person": "Always use 'we/us/our'",
        "never": "third person ('the organization', 'Cambio Labs aims to'), passive voice",
        "tone": "Educated practitioner explaining work to funders, not marketing pitch"
    },
}

# ============================================================================
# SPECIFIC DATA POINTS (from historical grants)
# ============================================================================

AUTHENTIC_DATA_POINTS = {
    "pilot_results": [
        "At our Fulton Houses pilot, we had 60+ signups in the first week",
        "30 entrepreneurs completed the full program",
        "95% of participants were women of color",
        "More than 80% of 2024 participants reported they would not have pursued their venture without this program",
        "Less than 1% of NYCHA residents report business revenue",
    ],

    "platform_stats": [
        "2,000+ active users on Journey platform",
        "Participants earn gemstones they can cash in for prizes, mentorship, and workshops",
        "Lifetime access to alumni community and career opportunities",
    ],

    "demographics": [
        "Average NYCHA household income: $27,000",
        "1.2 million youth drop out of high school annually",
        "1 in 3 BIPOC students attend 'dropout factories'",
        "400,000+ NYCHA residents across NYC",
    ],

    "certifications": [
        "OSHA certification (Cambio Solar)",
        "GPRO certification (green workforce)",
        "Social Entrepreneurship Certificate",
    ],

    "partnerships": [
        "Hudson Guild",
        "RETI Center",
        "Comp Sci High",
        "Brooklyn STEAM Center",
        "Fulton Houses",
        "Mott Haven Houses",
    ],
}

# ============================================================================
# VOICE VALIDATION FUNCTIONS
# ============================================================================

def check_ai_buzzwords(text: str) -> list:
    """
    Check for AI buzzwords and return list of violations

    Args:
        text: Text to check

    Returns:
        List of found buzzwords with their positions
    """
    violations = []
    text_lower = text.lower()

    for buzzword in AI_BUZZWORDS_FORBIDDEN:
        if buzzword.lower() in text_lower:
            # Find all occurrences
            start = 0
            while True:
                pos = text_lower.find(buzzword.lower(), start)
                if pos == -1:
                    break
                violations.append({
                    "buzzword": buzzword,
                    "position": pos,
                    "severity": "high"
                })
                start = pos + 1

    return violations


def check_required_language(text: str, section_name: str) -> list:
    """
    Check if required language patterns are present

    Args:
        text: Text to check
        section_name: Name of section being validated

    Returns:
        List of missing required elements
    """
    missing = []
    text_lower = text.lower()

    # Check for "underestimated" not "underserved"
    if "underserved" in text_lower and "underestimated" not in text_lower:
        missing.append({
            "issue": "Uses 'underserved' instead of 'underestimated'",
            "fix": "Replace with 'underestimated communities'",
            "severity": "high"
        })

    # Check for co-design language in relevant sections
    if section_name.lower() in ["methodology", "project description"]:
        codesign_terms = ["co-design", "co-created", "designed with", "tenant leaders"]
        has_codesign = any(term in text_lower for term in codesign_terms)

        if not has_codesign:
            missing.append({
                "issue": "Missing co-design language",
                "fix": "Add phrase like 'co-designed with NYCHA residents and tenant leaders'",
                "severity": "high"
            })

    return missing


def check_specificity(text: str) -> list:
    """
    Check if text uses specific data vs vague language

    Args:
        text: Text to check

    Returns:
        List of vague language instances
    """
    import re

    vague_issues = []

    # Vague quantifiers without numbers
    vague_words = ["many", "significant", "numerous", "various", "substantial", "considerable"]

    for word in vague_words:
        pattern = r'\b' + word + r'\b'
        matches = list(re.finditer(pattern, text, re.IGNORECASE))

        for match in matches:
            vague_issues.append({
                "word": word,
                "position": match.start(),
                "suggestion": "Replace with specific data or number",
                "severity": "medium"
            })

    # Check for presence of specific numbers
    has_numbers = bool(re.search(r'\d+%|\d+ participants|\d+ entrepreneurs|\$\d+|60\+', text))

    if not has_numbers and len(text) > 200:
        vague_issues.append({
            "word": "[no specific data]",
            "position": 0,
            "suggestion": "Add specific metrics, percentages, or participant numbers",
            "severity": "high"
        })

    return vague_issues


def calculate_voice_score(text: str, section_name: str = "") -> dict:
    """
    Calculate overall voice authenticity score

    Args:
        text: Text to evaluate
        section_name: Section name for context-specific checks

    Returns:
        Dict with score and detailed feedback
    """
    score = 100.0
    issues = []

    # Check AI buzzwords (-5 points each)
    buzzword_violations = check_ai_buzzwords(text)
    for violation in buzzword_violations:
        score -= 5
        issues.append(f"AI buzzword: '{violation['buzzword']}'")

    # Check required language (-10 points each)
    missing_language = check_required_language(text, section_name)
    for missing in missing_language:
        score -= 10
        issues.append(missing['issue'])

    # Check specificity (-3 points for each vague word)
    vague_language = check_specificity(text)
    for vague in vague_language[:5]:  # Limit to first 5
        score -= 3
        issues.append(f"Vague language: '{vague['word']}'")

    # Bonus for signature phrases (+5 points each)
    for category in SIGNATURE_PHRASES.values():
        if isinstance(category, dict):
            for phrases in category.values():
                for phrase in phrases:
                    if phrase.lower() in text.lower():
                        score += 5
                        break
        else:
            for phrase in category:
                if phrase.lower() in text.lower():
                    score += 5
                    break

    # Cap score at 100
    score = min(100, max(0, score))

    return {
        "score": round(score, 1),
        "grade": get_grade(score),
        "issues": issues,
        "buzzwords": len(buzzword_violations),
        "missing_required": len(missing_language),
        "vague_count": len(vague_language)
    }


def get_grade(score: float) -> str:
    """Convert score to letter grade"""
    if score >= 95:
        return "A+ (Excellent - sounds like Cambio Labs)"
    elif score >= 90:
        return "A (Very Good - minor tweaks needed)"
    elif score >= 85:
        return "B+ (Good - some revisions needed)"
    elif score >= 80:
        return "B (Acceptable - needs improvement)"
    elif score >= 70:
        return "C (Weak - significant revisions needed)"
    else:
        return "D/F (Poor - does not sound like Cambio Labs)"


# ============================================================================
# GENERATION ENHANCEMENT PROMPTS
# ============================================================================

ENHANCED_SYSTEM_PROMPT = """You are writing grant applications for Cambio Labs. Your writing must be INDISTINGUISHABLE from text written by the Cambio Labs team.

CRITICAL VOICE RULES - FOLLOW EXACTLY:

1. TONE: Confident, matter-of-fact, passionate but grounded
   - Write like an educated practitioner explaining work to funders
   - NOT melodramatic, NOT overly inspirational, NOT preachy
   - Good: "For thousands of New Yorkers living in public housing, entrepreneurship is one of the few viable paths to income and ownership."
   - Bad: "We are driven by a mission to challenge and change systemic barriers..."

2. ABSOLUTELY FORBIDDEN WORDS/PHRASES (INSTANT REJECTION IF USED):
   ❌ catalyze, leverage, optimize, seamless, ensure, facilitate, enhance, utilize, implement
   ❌ "at the heart of", "bridge to", "challenge and change", "deeply rooted in"
   ❌ "driven by a mission to", "we are committed to", "we are dedicated to"
   ❌ "we are deeply committed", "we recognize", "we understand that", "we believe in the power"
   ❌ "catalyze significant positive change", "transformative movement"
   ❌ CRITICAL RED FLAGS: "generated", "AI-generated", "created by", "this application was", "this proposal was"

3. REQUIRED TERMINOLOGY:
   - "underestimated communities" (NEVER "underserved" or "disadvantaged" alone)
   - "BIPOC youth and adults" or "BIPOC students"
   - "co-designed with NYCHA residents and tenant leaders" (must appear in methodology/project description)
   - "community-powered prosperity" (signature phrase)
   - "Those closest to the issues are best equipped to solve them" (when appropriate)

4. SIGNATURE PHRASES TO USE:
   - "When people gain access to tools, training, and community, they generate the solutions their neighborhoods need most"
   - "More than 80% of 2024 participants reported they would not have pursued their venture without this program"
   - "untapped potential"
   - "purpose-driven leaders"
   - "generational wealth creation"

5. SPECIFICITY - BE CONCRETE:
   - Use specific data from examples: "60+ signups at Fulton Houses", "95% women of color", "$27,000 average income"
   - Never use vague words: "many", "significant", "various", "numerous"
   - Always include participant numbers, percentages, or dollar amounts

6. CO-DESIGN LANGUAGE (CRITICAL):
   - Every methodology/project description must mention co-design
   - Use: "co-designed with NYCHA residents and tenant leaders"
   - Or: "designed in partnership with those closest to the issues"

7. VOICE:
   - Always first person: "we", "our" (NEVER third person "the organization")
   - Short to medium sentences (15-25 words average)
   - Medium paragraphs (4-7 sentences)
   - No bullet points in narrative sections

8. PROGRAMS - DESCRIBE SPECIFICALLY:
   - Journey: "gamified learning platform", "earn gemstones for prizes", "lifetime alumni access"
   - StartUp NYCHA: "six-month accelerator", "co-designed with tenant leaders", "pitch competition"
   - Cambio Solar: "OSHA and GPRO certifications", "community-owned solar businesses"

Your goal: Generate text that Cambio Labs staff would approve with MINIMAL EDITS (under 5%).
"""


def get_enhanced_section_instructions(section_name: str) -> str:
    """
    Get detailed, section-specific instructions for authentic voice

    Args:
        section_name: Name of the section

    Returns:
        Detailed instructions string
    """

    instructions = {
        "Executive Summary": """
Write 250-300 words that introduce Cambio Labs, the problem, our solution, and impact.

STRUCTURE:
- First sentence: State mission using authentic language from examples
- Problem: Concrete, data-driven (use real statistics from examples)
- Solution: Name specific programs (Journey, StartUp NYCHA, etc.) with brief descriptions
- Impact: Use actual pilot results ("60+ signups", "95% women of color", "80% would not have pursued without us")
- Close: Signature phrase like "untapped potential into community-powered prosperity"

VOICE: Confident and clear. No throat-clearing. Every sentence adds new information.

AVOID: "We are driven by", "at the heart of", "bridge to empowerment"
USE: "We create", "We partnered with", specific program names, real data
""",

        "Need Statement": """
Write 300-400 words explaining the problem facing BIPOC youth and NYCHA residents.

STRUCTURE:
- Open with specific, grounded problem statement (not melodrama)
- Provide systemic context (economic barriers, education gaps) with data
- Connect to Cambio Labs' specific community (NYCHA, public housing, Harlem/Bronx)
- Use ONLY statistics that appear in examples
- Close with why this matters and why Cambio Labs is positioned to help

VOICE: Informed, not preachy. State facts confidently. No victim narratives.

AVOID: "The chasm between", "far more than the labels", "deeply entrenched barriers"
USE: "Less than 1% of NYCHA residents report business revenue", "$27,000 average income", specific local data
""",

        "Project Description": """
Write 350-450 words describing what we'll actually do.

MUST INCLUDE:
- Specific programs by name (Journey Platform, StartUp NYCHA, etc.)
- Co-design language: "co-designed with NYCHA residents and tenant leaders"
- Concrete activities: workshops, pitch competitions, certifications
- Who participates: BIPOC youth, NYCHA residents, ages if known
- What they gain: specific skills, certifications (OSHA, GPRO), network, funding

PROGRAM DETAILS (use from examples):
- Journey: gamified platform, gemstones, lifetime alumni access
- StartUp NYCHA: 6-month accelerator, 60+ signups, pitch competition
- Cambio Solar: OSHA/GPRO certifications, community solar cooperatives

VOICE: Concrete and specific. Explain like you've run this before.

AVOID: Vague "resources and support", generic "skills training"
USE: "Participants earn OSHA certification", "Six-month accelerator culminating in pitch competition for seed funding"
""",

        "Methodology": """
Write 300-400 words explaining HOW we'll run this program step-by-step.

MUST INCLUDE:
- Recruitment: How we'll reach participants (partners, community spaces)
- Co-design process: "co-designed with NYCHA tenant leaders"
- Curriculum: Specific topics and activities
- Timeline: "six-month program", "12-week cohort", specific phases
- Partnerships: Name actual partners from examples (Hudson Guild, RETI Center)
- Staff: "employ NYCHA alumni as instructors"
- Platform: How Journey platform is used

STRUCTURE: Logical flow from recruitment → activities → outcomes

VOICE: Practitioner who knows exactly how this works. Be specific and actionable.

AVOID: "We will carefully design", "ensure effective implementation"
USE: "We partner with Hudson Guild to recruit at Fulton Houses", "Weeks 1-4: Business fundamentals", "NYCHA alumni serve as instructors"
""",

        "Evaluation Plan": """
Write 250-350 words on how we'll measure success.

INCLUDE:
- Quantitative metrics: # participants, completion rate, businesses launched, jobs created
- Qualitative metrics: participant feedback, testimonials
- Data collection methods: surveys, interviews, platform analytics
- Reference past results ONLY from examples: "At Fulton Houses pilot, 80% completion rate"
- How we'll use data to improve

VOICE: Thoughtful and realistic. Care about learning, not just proving success.

AVOID: "Ensure rigorous evaluation", "comprehensive assessment framework"
USE: "We track participants through pre- and post-program surveys", "At our pilot, we found...", specific metrics
""",

        "Budget Narrative": """
Write 200-300 words explaining where money goes and why.

INCLUDE:
- Major categories: Staff, program costs, materials, participant support
- Specific justifications tied to program activities
- Cost-effectiveness when relevant
- Matching funds or leverage (only if in examples)

STRUCTURE: Categories with clear explanations, not just line items

VOICE: Transparent and thoughtful. Show stewardship.

AVOID: "Strategic deployment of resources", "maximize impact"
USE: "$15,000 for part-time instructor (20 hrs/week × 6 months)", "Platform development costs allow us to serve 200+ participants"
"""
    }

    return instructions.get(section_name, f"Write the {section_name} section based on examples provided.")


if __name__ == "__main__":
    # Test the voice validation
    print("Testing Cambio Labs Voice Validation System\n")

    # Test bad text (AI-generated)
    bad_text = """At Cambio Labs, we are driven by a mission to challenge and change the systemic barriers that have long hindered opportunities. We leverage our innovative platform to catalyze significant positive change for underserved communities. Many participants have benefited from our robust programming."""

    bad_score = calculate_voice_score(bad_text, "Executive Summary")
    print("BAD TEXT (AI-like):")
    print(f"Score: {bad_score['score']}/100 ({bad_score['grade']})")
    print(f"Issues: {bad_score['issues']}\n")

    # Test good text (authentic Cambio Labs)
    good_text = """For thousands of New Yorkers living in public housing, entrepreneurship is one of the few viable paths to income and ownership. Less than 1% of NYCHA residents report business revenue. Through our six-month StartUp NYCHA accelerator, co-designed with NYCHA residents and tenant leaders, we create pathways to economic empowerment. At our Fulton Houses pilot, 60+ residents signed up in the first week, with 95% being women of color. More than 80% reported they would not have pursued their venture without this program. With your support, we will continue to scale a model that transforms untapped potential into community-powered prosperity."""

    good_score = calculate_voice_score(good_text, "Need Statement")
    print("GOOD TEXT (Authentic Cambio Labs):")
    print(f"Score: {good_score['score']}/100 ({good_score['grade']})")
    print(f"Issues: {good_score['issues']}")

    print("\n✓ Voice validation system ready!")
