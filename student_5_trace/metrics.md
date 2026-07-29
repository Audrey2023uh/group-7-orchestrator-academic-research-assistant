# Metrics — Telemetry Privacy Redaction Guardrail

Measured by `test_failure.py` over 4 synthetic trace events.

| Metric | Value |
|--------|-------|
| sensitive values detected (before) | 6 |
| leaked values before | 6 |
| leaked values after | 0 |
| redaction accuracy | 100% |

Before: emails, API keys, names, and local paths appeared in traces.
After: centralized interceptor scrubs secrets prior to telemetry write.
