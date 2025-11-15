"""
Professional Grant Proposal Formatter
Formats grant applications to industry standards without AI red flags
"""

from datetime import datetime
from typing import Dict, Any


class ProfessionalGrantFormatter:
    """
    Formats grant applications to professional nonprofit standards
    Removes all AI red flags and adds proper headers/formatting
    """

    def __init__(self, organization_name: str = "Cambio Labs"):
        self.organization_name = organization_name

    def generate_cover_page(self, grant_title: str, funding_opportunity: str,
                           amount_requested: str, contact_info: Dict[str, str]) -> str:
        """
        Generate professional cover page (NO "Generated" timestamp!)

        Args:
            grant_title: Title of the grant program
            funding_opportunity: RFP number or opportunity name
            amount_requested: Dollar amount requested
            contact_info: Dict with contact details

        Returns:
            Formatted cover page text
        """

        cover_page = f"""


{self.organization_name.upper()}

{contact_info.get('address_line1', 'Cambio Labs')}
{contact_info.get('address_line2', 'Queens County, New York, United States')}
{contact_info.get('phone', '(301) 717-9982')}
{contact_info.get('email', 'sebastian@cambiolabs.org')}
{contact_info.get('website', 'www.cambiolabs.org')}



GRANT PROPOSAL

{grant_title}

{funding_opportunity}

Amount Requested: {amount_requested}

Submitted: {datetime.now().strftime('%B %Y')}



Contact Person:
{contact_info.get('contact_name', 'Sebastián Martín')}
{contact_info.get('contact_title', 'Founder & CEO')}
{contact_info.get('contact_email', 'sebastian@cambiolabs.org')}
{contact_info.get('contact_phone', '(301) 717-9982')}
"""

        return cover_page

    def generate_professional_header(self, grant_title: str, funding_opportunity: str,
                                    page_number: int = None) -> str:
        """
        Generate header for each page (NO "Generated" language!)

        Args:
            grant_title: Grant program title
            funding_opportunity: RFP number
            page_number: Optional page number

        Returns:
            Header text
        """

        header = f"{self.organization_name} | {funding_opportunity}"
        if page_number:
            header += f" | Page {page_number}"

        return header

    def format_full_application(self, sections: Dict[str, str],
                               grant_info: Dict[str, Any],
                               include_cover_page: bool = True) -> str:
        """
        Format complete application professionally (NO AI red flags!)

        Args:
            sections: Dict mapping section names to content
            grant_info: Grant details (title, RFP, amount, etc.)
            include_cover_page: Whether to include cover page

        Returns:
            Professionally formatted application
        """

        output = []

        # Cover page (if requested)
        if include_cover_page:
            cover = self.generate_cover_page(
                grant_title=grant_info.get('grant_title', 'Grant Proposal'),
                funding_opportunity=grant_info.get('rfp_number', 'Funding Opportunity'),
                amount_requested=grant_info.get('amount_requested', '$100,000'),
                contact_info=grant_info.get('contact_info', {})
            )
            output.append(cover)
            output.append("\n\n" + "="*70 + "\n\n")

        # Table of Contents (optional for longer grants)
        if len(sections) > 4:
            output.append("TABLE OF CONTENTS\n")
            output.append("="*70 + "\n\n")
            for i, section_name in enumerate(sections.keys(), 1):
                output.append(f"{i}. {section_name}\n")
            output.append("\n" + "="*70 + "\n\n")

        # Main content sections
        for section_name, content in sections.items():
            # Section header
            output.append(f"{section_name.upper()}\n")
            output.append("="*70 + "\n\n")

            # Clean content (remove any AI red flags)
            cleaned_content = self.clean_ai_redflags(content)

            output.append(cleaned_content)
            output.append("\n\n")

        return "".join(output)

    def clean_ai_redflags(self, text: str) -> str:
        """
        Remove AI red flags and overly formal language

        Args:
            text: Original text

        Returns:
            Cleaned text
        """

        replacements = {
            # Remove AI tell-tale phrases
            "we are deeply committed to": "we work to",
            "we are committed to": "we",
            "we are dedicated to": "we",
            "we are excited to": "we",
            "we are proud to": "we",

            # Remove melodramatic phrases
            "catalyze significant positive change": "create meaningful impact",
            "transformative movement": "significant change",
            "revolutionary": "innovative",

            # Remove overly formal connectors
            "Moreover,": "Additionally,",
            "Furthermore,": "In addition,",
            "In conclusion,": "Finally,",

            # Remove throat-clearing
            "In our work at Cambio Labs, we've seen": "We've seen",
            "In our mission at Cambio Labs,": "At Cambio Labs,",

            # Remove redundant "we believe/recognize"
            "We recognize the critical need": "There is a critical need",
            "We understand that": "",
            "We believe in the power": "Social entrepreneurship has the power",
        }

        cleaned = text
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)

        return cleaned

    def add_page_numbers(self, text: str, start_page: int = 1) -> str:
        """
        Add page numbers to formatted text

        Args:
            text: Formatted application text
            start_page: Starting page number

        Returns:
            Text with page numbers
        """

        # Simple implementation: add page number every ~50 lines
        lines = text.split('\n')
        output = []
        page = start_page

        for i, line in enumerate(lines):
            if i > 0 and i % 50 == 0:
                output.append(f"\n{'_'*70}\nPage {page}\n{'_'*70}\n")
                page += 1
            output.append(line)

        return '\n'.join(output)

    def validate_professional_format(self, text: str) -> Dict[str, Any]:
        """
        Validate that text follows professional standards

        Args:
            text: Application text

        Returns:
            Dict with validation results
        """

        issues = []
        warnings = []

        # Check for AI red flags
        ai_redflags = [
            "generated",
            "AI-generated",
            "created by",
            "produced by",
            "this was written",
        ]

        for flag in ai_redflags:
            if flag.lower() in text.lower():
                issues.append(f"RED FLAG: Contains '{flag}' - remove immediately!")

        # Check for professional elements
        if "Table of Contents" not in text and len(text) > 5000:
            warnings.append("Consider adding Table of Contents for longer proposals")

        # Check for proper headers
        if self.organization_name not in text[:500]:
            warnings.append("Organization name should appear in header/title")

        # Check for overly AI language
        ai_phrases = [
            "we are committed to",
            "we are dedicated to",
            "catalyze significant",
            "transformative movement"
        ]

        ai_count = sum(1 for phrase in ai_phrases if phrase.lower() in text.lower())
        if ai_count > 3:
            issues.append(f"Too many AI phrases ({ai_count}) - sounds robotic")

        return {
            "is_professional": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "score": max(0, 100 - (len(issues) * 20) - (len(warnings) * 5))
        }


# Example usage and testing
if __name__ == "__main__":
    formatter = ProfessionalGrantFormatter("Cambio Labs")

    # Test cover page
    print("TESTING PROFESSIONAL COVER PAGE:")
    print("="*70)

    cover = formatter.generate_cover_page(
        grant_title="NYCHA Entrepreneurship Initiative 2025",
        funding_opportunity="RFP #2025-NYCHA-ENT",
        amount_requested="$100,000",
        contact_info={
            'address_line1': '123 Innovation Way',
            'address_line2': 'New York, NY 10027',
            'phone': '(212) 555-0100',
            'email': 'grants@cambiolabs.org',
            'website': 'www.cambiolabs.org',
            'contact_name': 'Sebastián Andino',
            'contact_title': 'Executive Director',
            'contact_email': 'sebastian@cambiolabs.org',
            'contact_phone': '(212) 555-0100'
        }
    )

    print(cover)

    # Test red flag cleaning
    print("\n\nTESTING AI RED FLAG REMOVAL:")
    print("="*70)

    test_text = """At Cambio Labs, we are deeply committed to breaking down systemic barriers.
    We are excited to catalyze significant positive change in our communities. Moreover,
    we recognize the critical need for innovative programming."""

    cleaned = formatter.clean_ai_redflags(test_text)
    print(f"BEFORE:\n{test_text}\n")
    print(f"AFTER:\n{cleaned}\n")

    # Test validation
    print("\n\nTESTING VALIDATION:")
    print("="*70)

    bad_text = "This grant application was generated on November 15, 2025 by our AI system."
    validation = formatter.validate_professional_format(bad_text)
    print(f"Bad Text Validation: {validation}\n")

    good_text = """Cambio Labs
    NYCHA Entrepreneurship Initiative 2025

    We create transformative educational programs that equip BIPOC youth with
    entrepreneurial skills."""
    validation_good = formatter.validate_professional_format(good_text)
    print(f"Good Text Validation: {validation_good}")

    print("\n✓ Professional formatter ready!")
