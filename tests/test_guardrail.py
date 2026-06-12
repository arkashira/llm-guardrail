from guardrail import Guardrail, Alert
import pytest
from datetime import datetime, timedelta

def test_check_failure_rate():
    alert = Alert("guardrail_failure_rate_high", 5, 15, 30)
    guardrail = Guardrail(alert)
    assert guardrail.check_failure_rate(100, 6) == True
    assert guardrail.check_failure_rate(100, 4) == False

def test_send_alert():
    alert = Alert("guardrail_failure_rate_high", 5, 15, 30)
    guardrail = Guardrail(alert)
    guardrail.check_failure_rate(100, 6)
    guardrail.send_alert()

def test_silence_alert():
    alert = Alert("guardrail_failure_rate_high", 5, 15, 30)
    guardrail = Guardrail(alert)
    guardrail.check_failure_rate(100, 6)
    guardrail.violations = [datetime.now() - timedelta(minutes=31)]
    guardrail.silence_alert()
    assert guardrail.violations == []

def test_main():
    import sys
    sys.argv = ["guardrail.py", "--total-calls", "100", "--blocked-calls", "6"]
    from guardrail import main
    main()

def test_main_silence():
    import sys
    sys.argv = ["guardrail.py", "--total-calls", "100", "--blocked-calls", "4"]
    from guardrail import main
    main()
