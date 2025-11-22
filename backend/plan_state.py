from backend.db import SessionLocal
from backend.models import PlanSection, Metadata


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


# Save a plan section to the DB
def update_section(section_name, new_text):
    db = SessionLocal()

    # DB record exists?
    existing = db.query(PlanSection).filter_by(section_name=section_name).first()

    if existing:
        existing.content = new_text
    else:
        record = PlanSection(section_name=section_name, content=new_text)
        db.add(record)

    db.commit()
    db.close()

    # Update in-memory cache too
    plan_sections[section_name] = new_text
    return True


# Load plan sections from database
def get_sections():
    db = SessionLocal()
    db_sections = db.query(PlanSection).all()

    for sec in db_sections:
        plan_sections[sec.section_name] = sec.content

    db.close()
    return plan_sections


def save_last_company(company):
    db = SessionLocal()
    meta = db.query(Metadata).filter_by(key="last_company").first()

    if meta:
        meta.value = company
    else:
        db.add(Metadata(key="last_company", value=company))

    db.commit()
    db.close()


def get_last_company():
    db = SessionLocal()
    meta = db.query(Metadata).filter_by(key="last_company").first()

    db.close()
    if meta:
        return meta.value
    return None
