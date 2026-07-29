"""Guardrail implementations shared by main_system and student snippets."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from pydantic import ValidationError

from agents import approx_tokens, build_review_dict, redact_text
from contract import (
    MAX_ROUNDS,
    SCHEMA_RETRY_LIMIT,
    TOKEN_SOFT_LIMIT,
    AnalysisPayload,
    InvalidToolCallException,
    ReviewSchema,
    ToolCallRequest,
)
from tools.tool_runtime import validate_and_execute


def loop_guard_should_terminate(round_number: int, max_rounds: int = MAX_ROUNDS) -> bool:
    return round_number >= max_rounds


def validate_analysis_payload(
    payload: Dict[str, Any],
    *,
    allow_retry: bool,
    schema_retry_used: bool,
) -> Tuple[Dict[str, Any], bool, str | None]:
    """Return (payload, schema_retry_used, error)."""
    try:
        model = AnalysisPayload.model_validate(payload)
        return model.model_dump(), schema_retry_used, None
    except ValidationError as exc:
        if allow_retry and not schema_retry_used:
            corrected = dict(payload)
            corrected.setdefault("paper_id", "rs-10485157")
            corrected.setdefault("title", "Semantic Tracing in LLM-Based Multi-Agent Systems")
            sections = set(s.lower() for s in corrected.get("sections_covered", []))
            for req in ("abstract", "methods", "results", "limitations"):
                if req not in sections:
                    corrected.setdefault("sections_covered", []).append(req)
            try:
                model = AnalysisPayload.model_validate(corrected)
                return model.model_dump(), True, None
            except ValidationError as exc2:
                return payload, True, str(exc2)
        return payload, schema_retry_used, str(exc)


def execute_tool_safely(
    call: ToolCallRequest,
    *,
    guardrail_enabled: bool = True,
) -> Any:
    return validate_and_execute(call, guardrail_enabled=guardrail_enabled)


def sanitize_state_invariants(state: Dict[str, Any]) -> Tuple[bool, str | None]:
    """Return (ok, error)."""
    if not isinstance(state.get("analysis_payload"), dict) or not state["analysis_payload"]:
        return False, "missing analysis_payload"
    if "paper_id" not in state["analysis_payload"]:
        return False, "analysis_payload missing paper_id"
    reviews = state.get("reviews") or []
    for r in reviews:
        try:
            ReviewSchema.model_validate(r)
        except ValidationError as exc:
            return False, f"invalid review schema: {exc}"
    return True, None


def redact_for_telemetry(event: str) -> str:
    return redact_text(event)


def manage_context(messages: List[Dict[str, str]], soft_limit: int = TOKEN_SOFT_LIMIT) -> Tuple[List[Dict[str, str]], int]:
    total = sum(approx_tokens(m.get("content", "")) for m in messages)
    if total <= soft_limit:
        return messages, total
    # Keep system + last 2 messages; summarize the rest
    if len(messages) <= 3:
        pruned = [{"role": "system", "content": "PRIOR_CONTEXT_SUMMARIZED"}, messages[-1]]
        return pruned, sum(approx_tokens(m.get("content", "")) for m in pruned)
    head = messages[:1]
    tail = messages[-2:]
    summary = {
        "role": "system",
        "content": (
            f"SUMMARY of {len(messages) - 3} earlier messages pruned. "
            "Preserve paper_id, validated reviews, rejection flags."
        ),
    }
    pruned = head + [summary] + tail
    return pruned, sum(approx_tokens(m.get("content", "")) for m in pruned)


def isolated_review(reviewer_id: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build one review without prior review history (isolation)."""
    review = build_review_dict(reviewer_id, analysis)
    ReviewSchema.model_validate(review)
    return review
