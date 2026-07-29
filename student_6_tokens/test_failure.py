"""Reproduce context window explosion across many reviewer-like messages."""
import time
from pathlib import Path

from student_6_tokens.snippet import prune_messages


def build_bloated_history(n_reviews: int = 20) -> list:
    msgs = [{"role": "system", "content": "orchestrator"}]
    for i in range(1, n_reviews + 1):
        msgs.append(
            {
                "role": "assistant",
                "content": (
                    f"REVIEWER_{i}_FULL_OUTPUT " + ("semantic tracing evidence " * 80)
                ),
            }
        )
        msgs.append({"role": "tool", "content": "TOOL_OUTPUT " + ("x" * 400)})
    return msgs


def test_prune_reduces_tokens():
    msgs = build_bloated_history(20)
    before = sum(max(1, len(m["content"]) // 4) for m in msgs)
    pruned, after = prune_messages(msgs, soft_limit=2500)
    assert after < before
    assert len(pruned) < len(msgs)


def test_write_metrics():
    msgs = build_bloated_history(20)
    t0 = time.perf_counter()
    before = sum(max(1, len(m["content"]) // 4) for m in msgs)
    _ = "".join(m["content"] for m in msgs)  # simulate naive full context use
    latency_before = (time.perf_counter() - t0) * 1000

    t1 = time.perf_counter()
    pruned, after = prune_messages(msgs, soft_limit=2500)
    _ = "".join(m["content"] for m in pruned)
    latency_after = (time.perf_counter() - t1) * 1000
    reduction = (before - after) / before if before else 0.0

    path = Path(__file__).resolve().parent / "metrics.md"
    path.write_text(
        f"""# Metrics — Context Window / Token Burn Guardrail

Measured by `test_failure.py` simulating 20 reviewer message accumulations.

| Metric | Before | After |
|--------|--------|-------|
| approx token count | {before} | {after} |
| percentage reduction | — | {reduction:.1%} |
| latency (ms, concatenate context) | {latency_before:.3f} | {latency_after:.3f} |
| messages retained | {len(msgs)} | {len(pruned)} |

Before: full tool outputs and prior reviews accumulated in message history.
After: context-management node summarizes older messages and preserves critical structured state.
""",
        encoding="utf-8",
    )
    assert after < before
    assert reduction > 0.5
