# LLM Guardrail Terraform Integration Layer

This project provides a Terraform integration layer for the LLM Guardrail.
It exposes a `llm_guardrail` data source that accepts a prompt and returns a safe response.
The provider automatically injects the module name into the request context.
Terraform logs any policy violations to the console during `plan`.
