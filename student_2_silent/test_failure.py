"""Reproduce silent structural / hallucination failure via schema validation."""
from pathlib import Path

from student_2_silent.snippet import validate_with_one_retry


def test_invalid_payload_detected():
    bad = {"title": "x", "sections_covered": ["intro"]}
    ok, _, retry_used, missing = validate_with_one_retry(bad, schema_retry_used=True)
    assert ok is False
    assert missing >= 1


def test_one_automated_correction():
    bad = {"title": "x", "sections_covered": ["intro"]}
    ok, payload, retry_used, missing = validate_with_one_retry(bad, schema_retry_used=False)
    assert ok is True
    assert retry_used is True
    assert "methods" in [s.lower() for s in payload["sections_covered"]]


def test_write_metrics():
    samples = [
        {"title": "x", "sections_covered": ["intro"]},
        {"paper_id": "rs-1", "title": "ok title here", "sections_covered": ["abstract"]},
        {
            "paper_id": "rs-10485157",
            "title": "Semantic Tracing Paper Title Long Enough",
            "sections_covered": ["abstract", "methods", "results", "limitations"],
        },
        {"title": "short", "sections_covered": []},
        {"paper_id": "ab", "title": "abcdef", "sections_covered": ["methods", "results"]},
    ]
    invalid = 0
    missing_total = 0
    corrected = 0
    for s in samples:
        ok0, _, _, m0 = validate_with_one_retry(s, schema_retry_used=True)
        if not ok0:
            invalid += 1
            missing_total += m0
        ok1, _, ru, _ = validate_with_one_retry(s, schema_retry_used=False)
        if (not ok0) and ok1 and ru:
            corrected += 1

    rate = invalid / len(samples)
    success = corrected / invalid if invalid else 0.0
    path = Path(__file__).resolve().parent / "metrics.md"
    path.write_text(
        f"""# Metrics — Silent Hallucination / Structural Guardrail

Measured by `test_failure.py` over {len(samples)} synthetic analyzer payloads.

| Metric | Value |
|--------|-------|
| invalid payload rate (no retry) | {rate:.2%} ({invalid}/{len(samples)}) |
| missing-field / error count (sum) | {missing_total} |
| correction success rate (one retry) | {success:.2%} ({corrected}/{invalid}) |
| schema retries allowed | 1 |

Before: invalid structured payloads could proceed silently.
After: Pydantic rejects incomplete section coverage and paper identifiers; one automated correction retry is permitted.
""",
        encoding="utf-8",
    )
    assert path.exists()
    assert invalid >= 1
