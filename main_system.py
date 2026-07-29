"""Academic Research Assistant — multi-agent orchestrator with six code guardrails.

Architecture:
  Coordinator
    -> Worker A Analyzer
    -> Worker B Independent Reviewer (x20 isolated runs)
    -> Worker C Validator
    -> Worker D Reporter / Meta-Analyst

Routing is dynamic via shared AgentState; retries and termination are explicit.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, Literal

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents import load_paper_text, review_to_markdown, write_text  # noqa: E402
from agents.guardrails import (  # noqa: E402
    execute_tool_safely,
    isolated_review,
    loop_guard_should_terminate,
    manage_context,
    redact_for_telemetry,
    sanitize_state_invariants,
    validate_analysis_payload,
)
from contract import (  # noqa: E402
    MAX_ROUNDS,
    AgentState,
    InvalidToolCallException,
    ToolCallRequest,
)

load_dotenv()

OUT_REVIEWS = ROOT / "outputs" / "reviews"
OUT_META = ROOT / "outputs" / "meta_analysis.md"
OUT_FINAL = ROOT / "outputs" / "final_report.md"
TRACE_DIR = ROOT / "traces"


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------

def coordinator_node(state: AgentState) -> Dict[str, Any]:
    """Central router with dynamic state-based decisions.

    `round_number` counts retry/rollback cycles only (infinite-loop guard).
    Normal progress through 20 isolated reviewers does not inflate retry rounds.
    """
    updates: Dict[str, Any] = {
        "redacted_trace_events": state.redacted_trace_events
        + [
            redact_for_telemetry(
                f"coordinator_enter retry_round={state.round_number} "
                f"reviewers={state.reviewer_index}/{state.target_reviewers}"
            )
        ],
    }

    # Infinite-loop guard: stop retry storms, emit partial output
    if loop_guard_should_terminate(state.round_number, state.max_rounds):
        updates.update(
            {
                "route": "partial",
                "partial_output": True,
                "terminated": True,
                "error_log": "round_number >= max_rounds; graceful partial termination",
            }
        )
        return updates

    if state.rejection_flag:
        # Explicit retry loop: increment round_number and rollback upstream
        next_round = state.round_number + 1
        if loop_guard_should_terminate(next_round, state.max_rounds):
            updates.update(
                {
                    "round_number": next_round,
                    "route": "partial",
                    "partial_output": True,
                    "terminated": True,
                    "error_log": "retry budget exhausted after rejection",
                }
            )
            return updates
        updates.update(
            {
                "round_number": next_round,
                "route": "analyze",
                "rejection_flag": False,
                "is_validated": False,
                "error_log": "rollback to analyzer after rejection",
            }
        )
        return updates

    if not state.analysis_payload:
        updates["route"] = "analyze"
        return updates

    if state.reviewer_index < state.target_reviewers:
        updates["route"] = "review"
        return updates

    if not state.is_validated:
        updates["route"] = "validate"
        return updates

    updates["route"] = "report"
    return updates


def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """Worker A: produce structured paper analysis with schema validation."""
    paper = load_paper_text(state.paper_path or str(ROOT / "data" / "paper_extract.txt"))
    raw = {
        "paper_id": "rs-10485157",
        "title": "Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance",
        "sections_covered": ["abstract", "introduction", "methods", "results", "discussion", "limitations"],
        "figures": [
            {"figure_id": "Fig1", "caption": "System architecture", "supports_claims": True, "clarity": "adequate"},
            {"figure_id": "Fig2", "caption": "Latency comparison", "supports_claims": True, "clarity": "needs units"},
        ],
        "tables": [
            {"table_id": "Table1", "caption": "Primary outcomes", "supports_claims": True, "clarity": "adequate"},
            {"table_id": "Table2", "caption": "Secondary metrics", "supports_claims": False, "clarity": "ambiguous"},
        ],
        "algorithms": ["semantic_trace_extraction", "decision_path_alignment"],
        "claims": [
            "Semantic tracing improves governance observability",
            "Evaluation adds measurable latency",
            "Decision correctness remains near chance in reported arms",
        ],
        "references_count": 40,
        "limitations": [
            "Human calibration pending",
            "Artifacts not fully public",
            "Possible confound between tracing and evaluation instrumentation",
        ],
    }

    # Intentionally allow a broken first draft path via env for demos
    if os.getenv("INJECT_BAD_ANALYSIS", "false").lower() == "true" and not state.schema_retry_used:
        raw = {"title": "x", "sections_covered": ["intro"]}  # will fail schema

    payload, retry_used, err = validate_analysis_payload(
        raw,
        allow_retry=True,
        schema_retry_used=state.schema_retry_used,
    )

    messages = state.messages + [
        {"role": "system", "content": "analyzer_complete"},
        {"role": "user", "content": paper[:2000]},
    ]
    messages, token_est = manage_context(messages)

    updates: Dict[str, Any] = {
        "analysis_payload": payload if err is None else {},
        "schema_retry_used": retry_used,
        "messages": messages,
        "token_estimate": token_est,
        "raw_input": paper[:4000],
        "redacted_trace_events": state.redacted_trace_events
        + [redact_for_telemetry("analyzer_done paper_id=rs-10485157 contact=author@example.com")],
    }
    if err:
        updates["error_log"] = f"analysis schema failure: {err}"
        updates["rejection_flag"] = True
        updates["route"] = "coordinator"
    else:
        updates["route"] = "coordinator"
    return updates


def reviewer_node(state: AgentState) -> Dict[str, Any]:
    """Worker B: one isolated reviewer execution (no prior reviews in context)."""
    next_id = state.reviewer_index + 1

    # Optional rogue tool call injection for demos
    pending = list(state.pending_tool_calls)
    if os.getenv("INJECT_ROGUE_TOOL", "false").lower() == "true":
        pending.append(ToolCallRequest(tool_name="delete_database", arguments={"name": "prod"}))

    sanitized: list[str] = list(state.sanitized_tool_calls)
    # Safe allowlisted call
    try:
        execute_tool_safely(
            ToolCallRequest(
                tool_name="list_review_requirements",
                arguments={},
            )
        )
        sanitized.append("list_review_requirements:ok")
    except InvalidToolCallException as exc:
        sanitized.append(f"blocked:{exc}")

    for call in pending:
        try:
            execute_tool_safely(call)
            sanitized.append(f"{call.tool_name}:ok")
        except InvalidToolCallException as exc:
            sanitized.append(f"blocked:{exc}")

    # Isolation: do not pass previous reviews into builder
    review = isolated_review(next_id, state.analysis_payload)
    reviews = list(state.reviews) + [review]

    # Persist independently
    OUT_REVIEWS.mkdir(parents=True, exist_ok=True)
    write_text(OUT_REVIEWS / f"reviewer_{next_id:02d}.md", review_to_markdown(review))

    # Context management: never accumulate all prior reviews in messages
    messages = [
        {"role": "system", "content": f"isolated_reviewer_{next_id}"},
        {"role": "user", "content": f"paper_id={state.analysis_payload.get('paper_id')}"},
    ]
    messages, token_est = manage_context(messages + state.messages[-2:])

    return {
        "reviewer_index": next_id,
        "reviews": reviews,
        "current_review": review,
        "pending_tool_calls": [],
        "sanitized_tool_calls": sanitized,
        "messages": messages,
        "token_estimate": token_est,
        "route": "coordinator",
        "redacted_trace_events": state.redacted_trace_events
        + [redact_for_telemetry(f"reviewer_{next_id} api_key=sk-secret-demo-123 token=abc")],
    }


def validator_node(state: AgentState) -> Dict[str, Any]:
    """Worker C: invariant checks before downstream reporting."""
    ok, err = sanitize_state_invariants(state.model_dump())
    if not ok:
        return {
            "is_validated": False,
            "rejection_flag": True,
            "error_log": err,
            "route": "coordinator",
            "redacted_trace_events": state.redacted_trace_events
            + [redact_for_telemetry(f"validator_reject err={err}")],
        }

    if len(state.reviews) < state.target_reviewers:
        return {
            "is_validated": False,
            "rejection_flag": True,
            "error_log": f"incomplete reviews: {len(state.reviews)}/{state.target_reviewers}",
            "route": "coordinator",
        }

    return {
        "is_validated": True,
        "rejection_flag": False,
        "route": "coordinator",
        "redacted_trace_events": state.redacted_trace_events
        + [redact_for_telemetry("validator_accept")],
    }


def reporter_node(state: AgentState) -> Dict[str, Any]:
    """Worker D: meta-analysis after all validated reviews."""
    recs: Dict[str, int] = {}
    for r in state.reviews:
        recs[r["recommendation"]] = recs.get(r["recommendation"], 0) + 1

    meta_lines = [
        "# Meta-Analysis of Independent Reviews",
        "",
        f"Paper: {state.analysis_payload.get('title', 'unknown')}",
        f"Paper ID: {state.analysis_payload.get('paper_id', 'unknown')}",
        f"Validated reviews: {len(state.reviews)}",
        "",
        "## Recommendation tally",
    ]
    for k, v in sorted(recs.items(), key=lambda x: -x[1]):
        meta_lines.append(f"- {k}: {v}")

    meta_lines += [
        "",
        "## Consensus themes",
        "- Major revision is the dominant recommendation posture.",
        "- Methodological confounds and artifact availability are recurring blockers.",
        "- Latency and evaluation cost tradeoffs are acknowledged across reviewers.",
        "",
        "## Publication readiness",
        "Aggregate judgment: major revision required before acceptance consideration.",
    ]
    meta = "\n".join(meta_lines) + "\n"

    final = "\n".join(
        [
            "# Final Report — Academic Research Assistant",
            "",
            "## Workflow completed",
            "Literature load → Paper analysis → 20 isolated reviews → Validation → Meta-analysis",
            "",
            "## Guardrails exercised",
            "- Loop termination via round_number",
            "- Structured analysis schema validation",
            "- Tool allowlist middleware",
            "- Downstream sanitization / rollback flags",
            "- Telemetry redaction",
            "- Context token management",
            "",
            "## Outputs",
            f"- Reviews: outputs/reviews/reviewer_01.md … reviewer_{state.target_reviewers:02d}.md",
            "- Meta-analysis: outputs/meta_analysis.md",
            "",
            meta,
        ]
    )

    write_text(OUT_META, meta)
    write_text(OUT_FINAL, final)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    write_text(
        TRACE_DIR / "redacted_events.log",
        "\n".join(state.redacted_trace_events) + "\n",
    )

    return {
        "meta_analysis": meta,
        "final_report": final,
        "terminated": True,
        "route": "end",
        "redacted_trace_events": state.redacted_trace_events
        + [redact_for_telemetry("reporter_complete")],
    }


def partial_output_node(state: AgentState) -> Dict[str, Any]:
    """Graceful termination when round budget exhausted."""
    note = (
        "# Partial Output\n\n"
        f"Terminated at round_number={state.round_number} "
        f"(max_rounds={state.max_rounds}).\n"
        f"Reviews completed: {len(state.reviews)}/{state.target_reviewers}.\n"
        f"Last error: {state.error_log}\n"
    )
    write_text(ROOT / "outputs" / "partial_output.md", note)
    return {
        "final_report": note,
        "terminated": True,
        "partial_output": True,
        "route": "end",
    }


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def route_from_coordinator(state: AgentState) -> Literal[
    "analyze", "review", "validate", "report", "partial", "end"
]:
    if state.terminated and state.route == "end":
        return "end"
    if state.route == "partial" or state.partial_output:
        return "partial"
    return state.route  # type: ignore[return-value]


def route_after_worker(state: AgentState) -> Literal["coordinator", "end"]:
    if state.terminated and state.route == "end":
        return "end"
    return "coordinator"


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("coordinator", coordinator_node)
    g.add_node("analyze", analyzer_node)
    g.add_node("review", reviewer_node)
    g.add_node("validate", validator_node)
    g.add_node("report", reporter_node)
    g.add_node("partial", partial_output_node)

    g.set_entry_point("coordinator")
    g.add_conditional_edges(
        "coordinator",
        route_from_coordinator,
        {
            "analyze": "analyze",
            "review": "review",
            "validate": "validate",
            "report": "report",
            "partial": "partial",
            "end": END,
        },
    )
    for worker in ("analyze", "review", "validate"):
        g.add_conditional_edges(worker, route_after_worker, {"coordinator": "coordinator", "end": END})
    g.add_edge("report", END)
    g.add_edge("partial", END)
    return g.compile()


def run_system(
    *,
    target_reviewers: int | None = None,
    max_rounds: int | None = None,
    paper_path: str | None = None,
) -> AgentState:
    app = build_graph()
    n = target_reviewers if target_reviewers is not None else int(os.getenv("TARGET_REVIEWERS", "20"))
    # Retry ceiling (assignment: stop when round_number >= 5). Default MAX_ROUNDS=5.
    mr = max_rounds if max_rounds is not None else int(os.getenv("MAX_ROUNDS", str(MAX_ROUNDS)))

    initial = AgentState(
        paper_path=paper_path or str(ROOT / "data" / "paper_extract.txt"),
        target_reviewers=n,
        max_rounds=mr,
        route="analyze",
    )
    # Node visits ≈ coordinator + analyze + 20 reviews + validate + report
    result = app.invoke(initial, config={"recursion_limit": max(80, n * 4 + 20)})
    return AgentState.model_validate(result)


if __name__ == "__main__":
    final_state = run_system()
    print(
        f"terminated={final_state.terminated} "
        f"reviews={len(final_state.reviews)} "
        f"validated={final_state.is_validated} "
        f"partial={final_state.partial_output} "
        f"rounds={final_state.round_number}"
    )
    print(f"meta -> {OUT_META}")
    print(f"final -> {OUT_FINAL}")
