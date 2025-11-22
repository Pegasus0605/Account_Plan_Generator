# Simple in-memory storage for the current account plan sections

plan_sections = {
    "executive_summary": "",
    "company_overview": "",
    "products_services": "",
    "business_model": "",
    "financials": "",
    "competitors": "",
    "challenges": "",
    "opportunities": "",
    "gtm_strategy": "",
    "action_items": ""
}

def update_section(section_name, new_text):
    if section_name not in plan_sections:
        return False
    plan_sections[section_name] = new_text
    return True

def get_sections():
    return plan_sections
