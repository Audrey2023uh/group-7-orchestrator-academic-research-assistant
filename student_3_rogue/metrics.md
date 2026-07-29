# Metrics — Rogue Tool Execution Guardrail

Measured by `test_failure.py`. Dangerous tools are mocked and never perform real side effects.

| Metric | Value |
|--------|-------|
| blocked unauthorized calls | 2 |
| malformed requests rejected | 1 |
| unsafe execution attempts before (unguarded path) | 2 |
| unsafe executions after (guardrail ON) | 0 |

Before: unauthorized tool names could reach the runtime.
After: hardcoded allowlist + argument validation raises InvalidToolCallException prior to execution.
