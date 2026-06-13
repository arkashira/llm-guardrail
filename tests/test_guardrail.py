import pytest
from datetime import datetime
from guardrail import Call, Guardrail

def test_guardrail_failure_rate_high():
    guardrail = Guardrail(threshold=0.05, window_minutes=15, silence_minutes=30)
    for i in range(100):
        guardrail.add_call(Call(timestamp=datetime.now(), success=True))
    for i in range(6):
        guardrail.add_call(Call(timestamp=datetime.now(), success=False))
    assert guardrail.last_alert is not None

def test_guardrail_failure_rate_low():
    guardrail = Guardrail(threshold=0.05, window_minutes=15, silence_minutes=30)
    for i in range(100):
        guardrail.add_call(Call(timestamp=datetime.now(), success=True))
    for i in range(4):
        guardrail.add_call(Call(timestamp=datetime.now(), success=False))
    assert guardrail.last_alert is None

def test_guardrail_silence_alert():
    guardrail = Guardrail(threshold=0.05, window_minutes=15, silence_minutes=30)
    for i in range(100):
        guardrail.add_call(Call(timestamp=datetime.now(), success=True))
    for i in range(6):
        guardrail.add_call(Call(timestamp=datetime.now(), success=False))
    assert guardrail.last_alert is not None
    guardrail.silence_alert()
    assert guardrail.last_alert is None
