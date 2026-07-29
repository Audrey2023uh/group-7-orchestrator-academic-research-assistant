# Interview Story — Silent Structural Failure Guardrail

**Author: Audrey Rah (Group 7) · Failure-mode package: `student_2_silent`**

The analyzer worker occasionally returned plausible JSON that omitted mandatory domain fields such as methods or limitations coverage. Without schema enforcement those payloads looked successful in logs while poisoning downstream reviewers. I instrumented Pydantic `AnalysisPayload` validation and measured an elevated invalid-payload rate on synthetic malformed drafts, along with a non-zero missing-field error count. Enabling a single automated correction retry recovered a large fraction of repairable cases; a second failure still rejects the payload rather than silently continuing. `test_failure.py` records invalid-payload rate, missing-field totals, and correction success rate. This code-level contract check closes the silent-hallucination gap that prompt wording alone cannot guarantee in a multi-agent pipeline.
