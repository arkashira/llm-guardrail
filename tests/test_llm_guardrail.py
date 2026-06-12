from src.llm_guardrail import LLMGuardrail, PolicyViolation

def test_invoke_safe_prompt():
    guardrail = LLMGuardrail("test_module")
    response = guardrail.invoke("safe prompt")
    assert response["response"] == "Safe response"

def test_invoke_unsafe_prompt():
    guardrail = LLMGuardrail("test_module")
    response = guardrail.invoke("unsafe prompt")
    assert response["response"] == "Policy violation"
    assert len(response["violations"]) == 1
    assert response["violations"][0] == "Unsafe prompt detected"

def test_log_violations():
    guardrail = LLMGuardrail("test_module")
    violations = ["Violation 1", "Violation 2"]
    guardrail.log_violations(violations)
    # Check that the violations are printed to the console
    # This test will not actually check the output, but it will ensure that the log_violations method does not throw any errors
