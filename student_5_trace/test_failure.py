"""Reproduce privacy leak through telemetry; measure redaction."""
from pathlib import Path

from student_5_trace.snippet import intercept


SAMPLES = [
    "user=Audrey Rahimi email=author@example.com api_key=sk-secret-demo-123",
    "path=C:\\Users\\audre\\secrets\\token.txt password=hunter2",
    "contact=reviewer@univ.edu token=abcDEF",
    "safe event: validator_accept paper_id=rs-10485157",
]


def count_leaks(text: str) -> int:
    needles = [
        "Audrey Rahimi",
        "author@example.com",
        "sk-secret-demo-123",
        "hunter2",
        "reviewer@univ.edu",
        "C:\\Users\\audre",
    ]
    return sum(1 for n in needles if n in text)


def test_redaction_removes_sensitive():
    raw = SAMPLES[0]
    scrubbed = intercept(raw)
    assert "sk-secret-demo-123" not in scrubbed
    assert "author@example.com" not in scrubbed
    assert "Audrey Rahimi" not in scrubbed


def test_write_metrics():
    before_join = "\n".join(SAMPLES)
    after_join = "\n".join(intercept(s) for s in SAMPLES)
    leaked_before = count_leaks(before_join)
    leaked_after = count_leaks(after_join)
    detected = leaked_before
    accuracy = 1.0 - (leaked_after / leaked_before if leaked_before else 0.0)

    path = Path(__file__).resolve().parent / "metrics.md"
    path.write_text(
        f"""# Metrics — Telemetry Privacy Redaction Guardrail

**Author: Audrey Rah (Group 7) · Single-author failure-mode package `student_5_trace`**

Measured by `test_failure.py` over {len(SAMPLES)} synthetic trace events.

| Metric | Value |
|--------|-------|
| sensitive values detected (before) | {detected} |
| leaked values before | {leaked_before} |
| leaked values after | {leaked_after} |
| redaction accuracy | {accuracy:.0%} |

Before: emails, API keys, names, and local paths appeared in traces.
After: centralized interceptor scrubs secrets prior to telemetry write.
""",
        encoding="utf-8",
    )
    assert leaked_before > 0
    assert leaked_after == 0
