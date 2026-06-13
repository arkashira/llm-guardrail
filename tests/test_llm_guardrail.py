from llm_guardrail import LLMGuardrail
import pytest

def test_increment_blocked():
    guardrail = LLMGuardrail()
    guardrail.increment_blocked('module1', 'policy1', 'severity1')
    metrics = guardrail.get_metrics()
    assert len(metrics['llm_guardrail_blocked_total']) == 1
    assert metrics['llm_guardrail_blocked_total'][0].module == 'module1'
    assert metrics['llm_guardrail_blocked_total'][0].policy == 'policy1'
    assert metrics['llm_guardrail_blocked_total'][0].severity == 'severity1'
    assert metrics['llm_guardrail_blocked_total'][0].value == 1

def test_increment_corrected():
    guardrail = LLMGuardrail()
    guardrail.increment_corrected('module2', 'policy2', 'severity2')
    metrics = guardrail.get_metrics()
    assert len(metrics['llm_guardrail_corrected_total']) == 1
    assert metrics['llm_guardrail_corrected_total'][0].module == 'module2'
    assert metrics['llm_guardrail_corrected_total'][0].policy == 'policy2'
    assert metrics['llm_guardrail_corrected_total'][0].severity == 'severity2'
    assert metrics['llm_guardrail_corrected_total'][0].value == 1

def test_expose_metrics():
    guardrail = LLMGuardrail()
    guardrail.increment_blocked('module1', 'policy1', 'severity1')
    guardrail.increment_corrected('module2', 'policy2', 'severity2')
    metrics = guardrail.expose_metrics()
    assert 'llm_guardrail_blocked_total{module="module1", policy="policy1", severity="severity1"} 1' in metrics
    assert 'llm_guardrail_corrected_total{module="module2", policy="policy2", severity="severity2"} 1' in metrics

def test_empty_metrics():
    guardrail = LLMGuardrail()
    metrics = guardrail.get_metrics()
    assert len(metrics['llm_guardrail_blocked_total']) == 0
    assert len(metrics['llm_guardrail_corrected_total']) == 0
