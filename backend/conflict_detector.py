import re

KEY_FACTS = [
    "revenue",
    "employees",
    "headquarters",
    "ceo",
    "founded",
    "market share"
]


def extract_facts(text):
    """
    Extract small factual snippets using simple regex patterns.
    This does NOT need to be perfect — just enough for assignment.
    """

    facts = {}

    for key in KEY_FACTS:
        pattern = rf"{key}[^.:\n]*[:\-]?\s*([A-Za-z0-9$.,% ]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            facts[key] = match.group(1).strip()

    return facts


def detect_conflicts(all_sources):
    """
    Compare extracted facts across multiple scraped pages.
    all_sources = {url: text, url: text, ...}
    """

    extracted = {}

    for url, text in all_sources.items():
        extracted[url] = extract_facts(text)

    # Consolidate fact-by-fact
    conflicts = {}

    for key in KEY_FACTS:
        values_seen = {}

        for url, facts in extracted.items():
            if key in facts:
                value = facts[key]
                if value not in values_seen:
                    values_seen[value] = []
                values_seen[value].append(url)

        # If more than one different value for same fact → conflict
        if len(values_seen) > 1:
            conflicts[key] = values_seen

    return conflicts
