# Metrics — Context Window / Token Burn Guardrail

**Author: Audrey Rah (Group 7) · Single-author failure-mode package `student_6_tokens`**

Measured by `test_failure.py` simulating 20 reviewer message accumulations.

| Metric | Before | After |
|--------|--------|-------|
| approx token count | 12574 | 655 |
| percentage reduction | — | 94.8% |
| latency (ms, concatenate context) | 0.035 | 0.018 |
| messages retained | 41 | 4 |

Before: full tool outputs and prior reviews accumulated in message history.
After: context-management node summarizes older messages and preserves critical structured state.
