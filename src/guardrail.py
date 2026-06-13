import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class Call:
    timestamp: datetime
    success: bool

class Guardrail:
    def __init__(self, threshold: float, window_minutes: int, silence_minutes: int):
        self.threshold = threshold
        self.window_minutes = window_minutes
        self.silence_minutes = silence_minutes
        self.calls = []
        self.last_alert = None

    def add_call(self, call: Call):
        self.calls.append(call)
        self.check_alert()

    def check_alert(self):
        now = datetime.now()
        window_start = now - timedelta(minutes=self.window_minutes)
        window_calls = [call for call in self.calls if call.timestamp >= window_start]
        if not window_calls:
            return
        failure_rate = sum(1 for call in window_calls if not call.success) / len(window_calls)
        if failure_rate > self.threshold:
            if self.last_alert is None or self.last_alert + timedelta(minutes=self.silence_minutes) < now:
                self.trigger_alert(failure_rate)
                self.last_alert = now

    def trigger_alert(self, failure_rate: float):
        print(f"Alert: Failure rate {failure_rate:.2%} exceeds threshold {self.threshold:.2%}")
        print("Sending Slack message to ops channel...")
        # Simulate sending a Slack message
        print("https://example.com/dashboard")

    def silence_alert(self):
        self.last_alert = None
