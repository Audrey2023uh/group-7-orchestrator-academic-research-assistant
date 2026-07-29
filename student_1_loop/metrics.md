# Metrics — Infinite Graph Loop Guardrail

Measured by `test_failure.py` on this machine (deterministic simulation).

| Metric | Before (guardrail OFF) | After (guardrail ON) |
|--------|------------------------|----------------------|
| iterations | 100 | 6 |
| round_number at stop | 100 | 5 |
| approx tokens burned | 12000 | 720 |
| latency (ms) | 0.004 | 0.001 |
| tokens saved | — | 11280 |
| latency reduced (ms) | — | 0.002 |

Notes:
- Unguarded path is hard-capped at 100 iterations for safety (would otherwise not terminate).
- Guarded path stops when `round_number >= 5` and routes to partial output.
