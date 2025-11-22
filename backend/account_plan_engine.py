import pathlib
from backend.ai_engine import ask_ai
from backend.plan_state import plan_sections

TEMPLATE_PATH = pathlib.Path("backend/account_plan_template.txt")


def load_template():
    return TEMPLATE_PATH.read_text()


def generate_plan_sections(company, research_summary):
    prompt = f"""
    Generate detailed sections for an account plan for the company '{company}'.
    Use this research summary:

    {research_summary}

    Return clear, detailed sections for:
    - Executive Summary
    - Company Overview
    - Products & Services
    - Business Model
    - Financial Highlights
    - Competitors
    - Challenges
    - Opportunities
    - GTM Strategy
    - Action Items
    """

    result = ask_ai(prompt)

    return result

from backend.plan_state import plan_sections

def generate_account_plan(company, research_summary):
    template = load_template()

    # First, let AI generate all details
    sections_text = generate_plan_sections(company, research_summary)

    # Fill template with current section values (user-editable)
    filled = template.format(
        company=company,
        executive_summary=plan_sections["executive_summary"],
        company_overview=plan_sections["company_overview"],
        products_services=plan_sections["products_services"],
        business_model=plan_sections["business_model"],
        financials=plan_sections["financials"],
        competitors=plan_sections["competitors"],
        challenges=plan_sections["challenges"],
        opportunities=plan_sections["opportunities"],
        gtm_strategy=plan_sections["gtm_strategy"],
        action_items=plan_sections["action_items"]
    )

    # Attach AI research output for reference
    final_output = filled + "\n\n# AI Generated Details\n\n" + sections_text

    return final_output

