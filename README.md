# llm-guardrail

A tiny, pure‑Python library that records the last 100 LLM responses together with a
policy status (`passed` / `blocked`) and serves a very small live dashboard.

## Features

* **In‑memory store** – keeps only the most recent 100 entries.
* **HTML dashboard** – auto‑refreshes every 5 seconds, shows timestamp, module,
  prompt snippet and response snippet.
* **Zero runtime dependencies** – only the Python standard library.

## Quick start
