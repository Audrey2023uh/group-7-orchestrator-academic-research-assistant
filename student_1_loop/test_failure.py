"""Deterministic reproduction of infinite retry-loop failure (guardrail off/on)."""
from __future__ import annotations

import time
from pathlib import Path

import pytest

from student_1_loop.snippet import coordinator_route, should_stop_retry_loop


def simulate_loop(*, guardrail_enabled: bool, hard_cap: int = 100) -> dict:
    """Simulate coordinator retry storm. Always hard-capped for safety."""
    round_number = 0
    iterations = 0
    t0 = time.perf_counter()
    tokens_per_iter = 120  # synthetic budget cost per retry
    while True:
        iterations += 1
        rejection_flag = True  # perpetual rejection without guardrail
        if guardrail_enabled:
            route = coordinator_route(round_number, rejection_flag, max_rounds=5)
            if route == "partial":
                break
            round_number += 1
        else:
            # Unguarded: would loop forever — hard_cap only for safe measurement
            round_number += 1
            if iterations >= hard_cap:
                break
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return {
        "iterations": iterations,
        "round_number": round_number,
        "elapsed_ms": elapsed_ms,
        "tokens": iterations * tokens_per_iter,
        "stopped_by_guardrail": guardrail_enabled and should_stop_retry_loop(round_number, 5),
    }


def test_unguarded_hits_hard_cap():
    before = simulate_loop(guardrail_enabled=False, hard_cap=100)
    assert before["iterations"] == 100
    assert before["tokens"] == 12000


def test_guarded_stops_at_five():
    after = simulate_loop(guardrail_enabled=True)
    assert after["round_number"] == 5
    assert after["iterations"] == 6  # enter with 0..5 then stop at >=5 check before increment path
    assert after["tokens"] < 12000


def test_write_metrics(tmp_path: Path = None):
    before = simulate_loop(guardrail_enabled=False, hard_cap=100)
    after = simulate_loop(guardrail_enabled=True)
    metrics_path = Path(__file__).resolve().parent / "metrics.md"
    body = f"""# Metrics — Infinite Graph Loop Guardrail

Measured by `test_failure.py` on this machine (deterministic simulation).

| Metric | Before (guardrail OFF) | After (guardrail ON) |
|--------|------------------------|----------------------|
| iterations | {before['iterations']} | {after['iterations']} |
| round_number at stop | {before['round_number']} | {after['round_number']} |
| approx tokens burned | {before['tokens']} | {after['tokens']} |
| latency (ms) | {before['elapsed_ms']:.3f} | {after['elapsed_ms']:.3f} |
| tokens saved | — | {before['tokens'] - after['tokens']} |
| latency reduced (ms) | — | {before['elapsed_ms'] - after['elapsed_ms']:.3f} |

Notes:
- Unguarded path is hard-capped at 100 iterations for safety (would otherwise not terminate).
- Guarded path stops when `round_number >= 5` and routes to partial output.
"""
    metrics_path.write_text(body, encoding="utf-8")
    assert metrics_path.exists()
