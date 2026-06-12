import pytest
from src.llm_guardrail import llm_guardrail_data_source

def test_llm_guardrail_data_source_happy_path():
    module_name = "test_module"
    prompt = "Hello, world!"
    response = llm_guardrail_data_source(module_name, prompt)
    assert response["safe_response"] == "Safe response generated."
    assert response["policy_violations"] == []

def test_llm_guardrail_data_source_policy_violation():
    module_name = "test_module"
    prompt = "This contains sensitive information."
    response = llm_guardrail_data_source(module_name, prompt)
    assert response["safe_response"] == "Policy violations detected. Please revise your prompt."
    assert response["policy_violations"] == ["Policy violation: sensitive information detected"]
