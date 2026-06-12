import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class PolicyViolation:
    message: str

class LLMGuardrail:
    def __init__(self, module_name: str):
        self.module_name = module_name

    def invoke(self, prompt: str) -> Dict:
        # Simulate policy checking
        if "unsafe" in prompt:
            return {"response": "Policy violation", "violations": [PolicyViolation("Unsafe prompt detected").message]}
        else:
            return {"response": "Safe response"}

    def log_violations(self, violations: list):
        for violation in violations:
            print(f"Policy violation: {violation}")
