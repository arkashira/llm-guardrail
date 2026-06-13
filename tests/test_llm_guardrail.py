import re
from llm_guardrail import LLMGuardrail, Policy


def test_guardrail_corrects_violation():
    policy = Policy(
        name="no-personal-data",
        pattern=r"\b\d{3}-\d{2}-\d{4}\b",
        url="https://example.com/policies/no-personal-data",
    )
    guardrail = LLMGuardrail([policy])

    response = "My SSN is 123-45-6789."
    corrected = guardrail.check_and_correct(response)

    assert corrected != response
    assert "Policy violation: no-personal-data" in corrected
    assert "https://example.com/policies/no-personal-data" in corrected

    corrections = guardrail.get_corrections()
    assert len(corrections) == 1
    corr = corrections[0]
    assert re.match(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        corr.correction_id,
        re.I,
    )
    assert corr.original == response
    assert corr.corrected == corrected
    assert corr.policy_name == "no-personal-data"


def test_guardrail_passes_when_no_violation():
    policy = Policy(
        name="no-personal-data",
        pattern=r"\b\d{3}-\d{2}-\d{4}\b",
        url="https://example.com/policies/no-personal-data",
    )
    guardrail = LLMGuardrail([policy])

    response = "Everything looks fine."
    corrected = guardrail.check_and_correct(response)

    assert corrected == response
    assert guardrail.get_corrections() == []
