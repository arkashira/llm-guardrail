import re
import uuid
from typing import List


class Policy:
    def __init__(self, name: str, pattern: str, url: str):
        self.name = name
        self.pattern = pattern
        self.url = url


class Correction:
    def __init__(self, correction_id: str, original: str, corrected: str, policy_name: str):
        self.correction_id = correction_id
        self.original = original
        self.corrected = corrected
        self.policy_name = policy_name


class LLMGuardrail:
    def __init__(self, policies: List[Policy]):
        self.policies = policies
        self._corrections: List[Correction] = []

    def check_and_correct(self, response: str) -> str:
        for policy in self.policies:
            if re.search(policy.pattern, response, re.IGNORECASE):
                corrected = f"Policy violation: {policy.name}. See {policy.url}"
                correction_id = str(uuid.uuid4())
                self._corrections.append(
                    Correction(correction_id, response, corrected, policy.name)
                )
                return corrected
        return response

    def get_corrections(self) -> List[Correction]:
        return list(self._corrections)
