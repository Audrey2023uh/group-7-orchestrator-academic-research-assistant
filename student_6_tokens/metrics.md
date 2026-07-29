# Metrics — Context Window / Token Burn Guardrail

Measured by `test_failure.py` simulating 20 reviewer message accumulations.

| Metric | Before | After |
|--------|--------|-------|
| approx token count | 12574 | 655 |
| percentage reduction | — | 94.8% |
| latency (ms, concatenate context) | 0.043 | 0.017 |
| messages retained | 41 | 4 |

Before: full tool outputs and prior reviews accumulated in message history.
After: context-management node summarizes older messages and preserves critical structured state.
