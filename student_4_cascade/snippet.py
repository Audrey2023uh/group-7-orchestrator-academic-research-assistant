"""Guardrail snippet: sanitization node preventing cascade (Student 4)."""
from typing import Any, Dict, Tuple

from agents.guardrails import sanitize_state_invariants


def sanitize_or_reject(state: Dict[str, Any]) -> Tuple[bool, str | None]:
    return sanitize_state_invariants(state)


def downstream_reporter(state: Dict[str, Any], *, guardrail_enabled: bool) -> str:
    """Simulates reporter crash on malformed upstream when unguarded."""
    if guardrail_enabled:
        ok, err = sanitize_or_reject(state)
        if not ok:
            return f"ROLLBACK:{err}"
    # Unguarded / passed: access nested fields that crash if missing
    return state["analysis_payload"]["paper_id"] + "::" + str(len(state["reviews"]))
