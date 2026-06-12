import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse

@dataclass
class Alert:
    name: str
    threshold: float
    window: int
    silence_time: int

class Guardrail:
    def __init__(self, alert: Alert):
        self.alert = alert
        self.violations = []

    def check_failure_rate(self, total_calls: int, blocked_calls: int):
        failure_rate = (blocked_calls / total_calls) * 100 if total_calls > 0 else 0
        if failure_rate > self.alert.threshold:
            self.violations.append(datetime.now())
            return True
        return False

    def send_alert(self):
        if self.violations:
            print(f"Sending alert: {self.alert.name}")
            print(f"Slack message: Failure rate exceeded {self.alert.threshold}%")
            print(f"Link to dashboard: https://example.com/dashboard")

    def silence_alert(self):
        if self.violations and (datetime.now() - self.violations[-1]) > timedelta(minutes=self.alert.silence_time):
            self.violations = []
            print(f"Silencing alert: {self.alert.name}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--total-calls", type=int, help="Total number of calls")
    parser.add_argument("--blocked-calls", type=int, help="Number of blocked calls")
    args = parser.parse_args()

    alert = Alert("guardrail_failure_rate_high", 5, 15, 30)
    guardrail = Guardrail(alert)

    if guardrail.check_failure_rate(args.total_calls, args.blocked_calls):
        guardrail.send_alert()
    guardrail.silence_alert()

if __name__ == "__main__":
    main()
