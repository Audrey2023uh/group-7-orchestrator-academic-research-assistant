# Summary Metrics — Six Guardrails

**Author: Audrey Rah (Group 7)**  
Source: measured values from each `student_*/metrics.md` (no invented or rounded figures).

| Guardrail | Failure Mode | Before | After | Improvement |
|-----------|--------------|--------|-------|-------------|
| G1 Infinite-loop stop | Infinite Graph Loop | iterations 100; round_number at stop 100; approx tokens burned 12000; latency (ms) 0.003 | iterations 6; round_number at stop 5; approx tokens burned 720; latency (ms) 0.001 | tokens saved 11280; latency reduced (ms) 0.002 |
| G2 Silent/structural | Silent Hallucination / Structural | invalid payload rate (no retry) 80.00% (4/5); missing-field / error count (sum) 8 | correction success rate (one retry) 100.00% (4/4); schema retries allowed 1 | correction success rate (one retry) 100.00% (4/4) |
| G3 Rogue tools | Rogue Tool Execution | unsafe execution attempts before (unguarded path) 2 | unsafe executions after (guardrail ON) 0; blocked unauthorized calls 2; malformed requests rejected 1 | unsafe executions after (guardrail ON) 0 |
| G4 Cascade | Downstream Cascade | downstream crashes before 20/20 | downstream crashes after 0/20 | rollback success rate 100% |
| G5 Privacy | Telemetry Privacy Redaction | sensitive values detected (before) 6; leaked values before 6 | leaked values after 0 | redaction accuracy 100% |
| G6 Tokens | Context Window / Token Burn | approx token count 12574; latency (ms, concatenate context) 0.020; messages retained 41 | approx token count 655; latency (ms, concatenate context) 0.016; messages retained 4 | percentage reduction 94.8% |

Per-guardrail detail: `student_1_loop/metrics.md` … `student_6_tokens/metrics.md`.
