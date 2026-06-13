# LLM Guardrail

This project provides a simple implementation of a guardrail system for Large Language Models (LLMs). It exposes Prometheus metrics for blocked and corrected responses.

## Usage

1. Create an instance of the `LLMGuardrail` class.
2. Call the `increment_blocked` or `increment_corrected` methods to update the metrics.
3. Use the `expose_metrics` method to retrieve the metrics in Prometheus format.

## Testing

Run the tests using `pytest`:
