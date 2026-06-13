# Guardrail
A Python project for monitoring and alerting on failure rates.

## Usage
1. Create a `Guardrail` instance with the desired threshold, window minutes, and silence minutes.
2. Add calls to the `Guardrail` instance using the `add_call` method.
3. The `Guardrail` instance will trigger an alert when the failure rate exceeds the threshold.
