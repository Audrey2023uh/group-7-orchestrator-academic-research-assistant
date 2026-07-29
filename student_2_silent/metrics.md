# Metrics — Silent Hallucination / Structural Guardrail

**Author: Audrey Rah (Group 7) · Single-author failure-mode package `student_2_silent`**

Measured by `test_failure.py` over 5 synthetic analyzer payloads.

| Metric | Value |
|--------|-------|
| invalid payload rate (no retry) | 80.00% (4/5) |
| missing-field / error count (sum) | 8 |
| correction success rate (one retry) | 100.00% (4/4) |
| schema retries allowed | 1 |

Before: invalid structured payloads could proceed silently.
After: Pydantic rejects incomplete section coverage and paper identifiers; one automated correction retry is permitted.
