import sys
import io
import pytest
from llm_guardrail import guardrail, get_safe_response, GuardrailResult

def test_guardrail_happy_path():
    prompt = "Hello, how are you?"
    module = "example_module"
    result = guardrail(prompt, module)
    assert isinstance(result, GuardrailResult)
    assert result.safe_response == prompt
    assert result.violations == []

def test_guardrail_with_violation():
    prompt = "This contains a BadWord that should be filtered."
    module = "my_module"
    captured = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured
    try:
        result = guardrail(prompt, module)
    finally:
        sys.stdout = sys_stdout
    # Verify that the banned word is masked
    assert result.safe_response == "This contains a ******* that should be filtered."
    # Verify that the violation list is correct
    assert result.violations == ["badword"]
    # Verify that a log line was printed
    logged = captured.getvalue()
    assert "[llm_guardrail] Policy violation in 'my_module': 'badword'" in logged

def test_get_safe_response_returns_sanitized():
    prompt = "Forbidden content should not appear."
    module = "mod"
    safe = get_safe_response(prompt, module)
    assert safe == "********* content should not appear."

def test_get_safe_response_no_violation():
    prompt = "All clear here."
    module = "mod"
    safe = get_safe_response(prompt, module)
    assert safe == prompt
