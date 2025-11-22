from backend.chat_memory import add_message, get_history
from backend.ai_engine import ask_ai
from backend.research_engine import research_company
from backend.account_plan_engine import generate_account_plan

from backend.agent_memory import remember, recall, append_memory, add_context
from backend.plan_state import save_last_company   # <-- REQUIRED IMPORT


def extract_company_name(message):
    msg = message.lower()
    msg = msg.replace("tell me about", "")
    msg = msg.replace("research", "")
    msg = msg.replace("company info", "")
    msg = msg.strip()
    return msg.title()


def handle_user_message(user_message):

    # save user context
    add_message("user", user_message)
    add_context("user", user_message)

    lower_msg = user_message.lower()

    # -----------------------------------------------------------
    # RESEARCH INTENT
    # -----------------------------------------------------------
    if "tell me about" in lower_msg or "research" in lower_msg:
        company = extract_company_name(user_message)
        print("Detected research intent. Company:", company)

        remember("last_company", company)
        save_last_company(company)

        data = research_company(company)
        raw = data["data"]
        conflicts = data["conflicts"]

        text_list = list(raw.values())
        print("Scraped text:", text_list)

        # Conflict detection
        if conflicts:
            conflict_text = f"I found conflicting information about {company}:\n\n"
            for fact, versions in conflicts.items():
                conflict_text += f"- {fact.upper()}:\n"
                for value, urls in versions.items():
                    conflict_text += f"  • {value} (from: {urls})\n"
            conflict_text += "\nShould I dig deeper?"

            add_message("assistant", conflict_text)
            add_context("assistant", conflict_text)
            return conflict_text

        # Summary fallback
        if not any(text_list):
            summary = f"No research data found for {company}."
        else:
            summary = ask_ai(f"""
                Summarize the following company information in 10 lines.
                If the text is unrelated or empty, just give a general overview of {company}.

                {text_list}
            """)

        add_message("assistant", summary)
        add_context("assistant", summary)
        return summary

    # -----------------------------------------------------------
    # GENERATE PLAN INTENT
    # -----------------------------------------------------------
    if "generate plan" in lower_msg or "create plan" in lower_msg:
        company = extract_company_name(user_message)
        print("Detected plan intent. Company:", company)

        remember("last_company", company)
        save_last_company(company)
        append_memory("plan_sections_edited", "generated_plan")

        data = research_company(company)
        raw = data["data"]
        text_list = list(raw.values())

        if not any(text_list):
            research_summary = f"No research data found. Generating a generic plan for {company}."
        else:
            research_summary = ask_ai(f"Summarize company data: {text_list}")

        plan = generate_account_plan(company, research_summary)

        add_message("assistant", plan)
        add_context("assistant", plan)
        return plan

    # -----------------------------------------------------------
    # NORMAL CHAT RESPONSE
    # -----------------------------------------------------------
    response = ask_ai(user_message)
    add_message("assistant", response)
    add_context("assistant", response)

    return response
