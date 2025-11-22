# Advanced memory system for the agent

memory = {
    "last_company": None,
    "conversation_summary": "",
    "plan_sections_edited": [],
    "pending_questions": [],
    "context_history": []
}


def remember(key, value):
    memory[key] = value


def append_memory(key, value):
    if key not in memory:
        memory[key] = []
    memory[key].append(value)


def recall(key):
    return memory.get(key, None)


def add_context(role, content):
    memory["context_history"].append({"role": role, "content": content})


def get_context():
    return memory["context_history"]


def clear_memory():
    memory["last_company"] = None
    memory["conversation_summary"] = ""
    memory["plan_sections_edited"] = []
    memory["pending_questions"] = []
    memory["context_history"] = []
