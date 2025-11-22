from fastapi import APIRouter
from backend.research_engine import research_company
from backend.ai_engine import ask_ai
from backend.account_plan_engine import generate_account_plan
from backend.plan_state import update_section, get_sections
from backend.chat_agent import handle_user_message
from backend.conflict_detector import detect_conflicts
from backend.agent_memory import memory, clear_memory
from backend.plan_state import update_section, get_sections, save_last_company, get_last_company

# Debug
print("ROUTES FILE LOADED")

router = APIRouter()

# ------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------
@router.get("/health")
def health_check():
    return {"status": "ok", "message": "Health endpoint working"}


# ------------------------------------------------------
# RESEARCH ENDPOINT
# ------------------------------------------------------
@router.get("/research")
def research(company: str):
    print("RESEARCH ENDPOINT HIT")

    result = research_company(company)
    raw_data = result["data"]
    conflicts = result["conflicts"]

    print("STEP 1: URLs found:", list(raw_data.keys()))

    condensed_data = {url: text[:500] for url, text in raw_data.items()}
    print("STEP 2: Condensed data prepared")

    summary_prompt = f"""
    Summarize the company '{company}' using the following data:

    {condensed_data}

    Provide a structured output with:
    - Overview
    - Products / Services
    - Business Model
    - Financial Highlights
    - Challenges
    - Opportunities
    - Competitors
    """

    print("STEP 3: Sending prompt to AI...")
    summary = ask_ai(summary_prompt)
    print("STEP 4: AI summary received")

    return {
        "company": company,
        "sources": list(raw_data.keys()),
        "summary": summary,
        "conflicts": conflicts
    }


# ------------------------------------------------------
# ACCOUNT PLAN GENERATION
# ------------------------------------------------------
@router.get("/generate-plan")
def generate_plan(company: str):
    print("GENERATING ACCOUNT PLAN")

    raw_data = research_company(company)
    condensed_data = {url: text[:500] for url, text in raw_data.items()}

    summary_prompt = f"""
You are an expert company analyst.

Write a concise structured summary of '{company}' 
using ONLY the following text snippets:

{list(condensed_data.values())}

Required sections:
- Overview
- Products / Services
- Business Model
- Challenges
- Opportunities
- Competitors

Keep the entire answer under 20 lines.
"""


    research_summary = ask_ai(summary_prompt)

    plan = generate_account_plan(company, research_summary)

    return {
        "company": company,
        "account_plan": plan
    }
@router.post("/update-section")
def update_plan_section(section: str, text: str):
    print("Updating section:", section)
    ok = update_section(section, text)
    if not ok:
        return {"error": "Invalid section name"}

    return {"message": f"Section '{section}' updated successfully."}

@router.get("/plan-sections")
def get_plan_sections():
    return get_sections()

@router.post("/chat")
def chat(message: str):
    reply = handle_user_message(message)
    return {"reply": reply}

@router.get("/detect-conflicts")
def detect_conflicts_endpoint(company: str):
    result = research_company(company)
    return {
        "company": company,
        "conflicts": result["conflicts"]
    }

@router.get("/memory")
def get_memory():
    return memory


@router.post("/clear-memory")
def reset_memory():
    clear_memory()
    return {"message": "Memory cleared"}
