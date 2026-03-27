import re

def sanitize_idea(idea: str) -> str:
    idea = idea.strip()
    idea = re.sub(r'[<>{}]', '', idea)
    return idea

def validate_idea_length(idea: str) -> str:
    if len(idea) < 10:
        raise ValueError("Idea must be at least 10 characters.")
    if len(idea) > 1000:
        raise ValueError("Idea must be under 1000 characters.")
    return idea