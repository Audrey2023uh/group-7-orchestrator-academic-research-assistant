# Metrics — Downstream Cascade Guardrail

**Author: Audrey Rah (Group 7) · Single-author failure-mode package `student_4_cascade`**

Measured by `test_failure.py` over 20 malformed-state trials.

| Metric | Value |
|--------|-------|
| downstream crashes before | 20/20 |
| downstream crashes after | 0/20 |
| rollback success rate | 100% |

Before: missing `paper_id` caused KeyError in reporter.
After: sanitization node sets rejection/rollback path before downstream execution.
