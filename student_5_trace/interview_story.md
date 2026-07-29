# Interview Story — Telemetry Privacy Guardrail

**Author: Audrey Rah (Group 7) · Failure-mode package: `student_5_trace`**

Trace events in the orchestrator originally echoed emails, API key material, local filesystem paths, and personal names. That is unacceptable for coursework demos and for any environment that may export spans to a tracing backend. I added a centralized redaction interceptor that scrubs secrets, emails, names, and path prefixes before events are written. On a fixed set of synthetic events, sensitive-value detections equaled the pre-redaction leak count; after interception, leaked values fell to zero, yielding full measured redaction accuracy on that suite. The before/after table in `metrics.md` is reproducible via `test_failure.py`, demonstrating that privacy controls belong in code at the telemetry boundary rather than in informal logging discipline.
