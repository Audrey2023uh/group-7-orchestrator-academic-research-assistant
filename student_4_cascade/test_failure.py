"""Reproduce downstream cascade from malformed upstream state."""
from pathlib import Path

import pytest

from student_4_cascade.snippet import downstream_reporter


def _bad_state():
    return {"analysis_payload": {}, "reviews": []}


def _good_state():
    return {
        "analysis_payload": {
            "paper_id": "rs-10485157",
            "title": "Semantic Tracing Title Long Enough",
            "sections_covered": ["abstract", "methods", "results", "limitations"],
        },
        "reviews": [],
    }


def test_unguarded_crashes():
    with pytest.raises(KeyError):
        downstream_reporter(_bad_state(), guardrail_enabled=False)


def test_guarded_rollbacks():
    out = downstream_reporter(_bad_state(), guardrail_enabled=True)
    assert out.startswith("ROLLBACK:")


def test_guarded_allows_valid():
    out = downstream_reporter(_good_state(), guardrail_enabled=True)
    assert out.startswith("rs-10485157")


def test_write_metrics():
    crashes_before = 0
    crashes_after = 0
    rollbacks = 0
    trials = 20
    for _ in range(trials):
        try:
            downstream_reporter(_bad_state(), guardrail_enabled=False)
        except Exception:
            crashes_before += 1
        out = downstream_reporter(_bad_state(), guardrail_enabled=True)
        if out.startswith("ROLLBACK:"):
            rollbacks += 1
        else:
            crashes_after += 1

    path = Path(__file__).resolve().parent / "metrics.md"
    path.write_text(
        f"""# Metrics — Downstream Cascade Guardrail

Measured by `test_failure.py` over {trials} malformed-state trials.

| Metric | Value |
|--------|-------|
| downstream crashes before | {crashes_before}/{trials} |
| downstream crashes after | {crashes_after}/{trials} |
| rollback success rate | {rollbacks / trials:.0%} |

Before: missing `paper_id` caused KeyError in reporter.
After: sanitization node sets rejection/rollback path before downstream execution.
""",
        encoding="utf-8",
    )
    assert crashes_before == trials
    assert crashes_after == 0
    assert rollbacks == trials
