from dataclasses import dataclass
from typing import Dict

@dataclass
class Metric:
    module: str
    policy: str
    severity: str
    value: int

class LLMGuardrail:
    def __init__(self):
        self.metrics = {
            'llm_guardrail_blocked_total': [],
            'llm_guardrail_corrected_total': []
        }

    def increment_blocked(self, module: str, policy: str, severity: str):
        metric = Metric(module, policy, severity, 1)
        self.metrics['llm_guardrail_blocked_total'].append(metric)

    def increment_corrected(self, module: str, policy: str, severity: str):
        metric = Metric(module, policy, severity, 1)
        self.metrics['llm_guardrail_corrected_total'].append(metric)

    def get_metrics(self) -> Dict[str, list]:
        return self.metrics

    def expose_metrics(self) -> str:
        metrics = self.get_metrics()
        output = ''
        for metric_name, metric_values in metrics.items():
            for metric in metric_values:
                output += f'{metric_name}{{module="{metric.module}", policy="{metric.policy}", severity="{metric.severity}"}} {metric.value}\n'
        return output
