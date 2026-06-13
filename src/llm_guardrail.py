import re
from dataclasses import dataclass
from typing import List

BANNED_WORDS = ["badword", "forbidden"]

@dataclass
class GuardrailResult:
    """Result of a guardrail check."""
    safe_response: str
    violations: List[str]

def guardrail(prompt: str, module_name: str) -> GuardrailResult:
    """Checks a prompt for banned words and returns a sanitized response."""
    violations = []
    safe_response = prompt
    for word in BANNED_WORDS:
        if word.lower() in prompt.lower():
            safe_response = re.sub(word, "*" * len(word), safe_response, flags=re.IGNORECASE)
            violations.append(word)
            print(f"[llm_guardrail] Policy violation in '{module_name}': '{word}'")
    return GuardrailResult(safe_response, violations)

def get_safe_response(prompt: str, module_name: str) -> str:
    """Returns a sanitized response for a given prompt."""
    result = guardrail(prompt, module_name)
    return result.safe_response
