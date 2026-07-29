"""Tool implementations — all potentially harmful actions are mocked."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from contract import ALLOWED_TOOLS, InvalidToolCallException, ToolCallRequest


def load_paper_extract(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return "MOCKED_EMPTY_PAPER"
    # Cap size to avoid token explosion at tool boundary
    text = p.read_text(encoding="utf-8", errors="replace")
    return text[:12000]


def list_review_requirements() -> Dict[str, Any]:
    return {
        "required_fields": [
            "expertise",
            "recommendation",
            "confidence",
            "section_by_section",
            "figure_by_figure",
            "table_by_table",
        ]
    }


def mock_web_lookup(query: str) -> str:
    return f"MOCKED_LOOKUP_RESULT for query={query[:80]}"


def mock_delete_database(name: str) -> str:
    raise InvalidToolCallException(f"blocked dangerous tool delete_database({name})")


def mock_execute_trade(symbol: str, qty: int) -> str:
    raise InvalidToolCallException(f"blocked dangerous tool execute_trade({symbol},{qty})")


TOOL_IMPL = {
    "load_paper_extract": load_paper_extract,
    "list_review_requirements": list_review_requirements,
    "mock_web_lookup": mock_web_lookup,
    # Dangerous names exist only to be blocked by middleware
    "delete_database": mock_delete_database,
    "execute_trade": mock_execute_trade,
}


def validate_and_execute(call: ToolCallRequest, *, guardrail_enabled: bool = True) -> Any:
    name = call.tool_name
    args = call.arguments or {}

    if guardrail_enabled:
        if name not in ALLOWED_TOOLS:
            raise InvalidToolCallException(f"unauthorized tool: {name}")
        required = ALLOWED_TOOLS[name]["required_args"]
        for key in required:
            if key not in args:
                raise InvalidToolCallException(f"missing required arg '{key}' for {name}")
        # Reject empty required strings
        for key in required:
            if isinstance(args.get(key), str) and not str(args[key]).strip():
                raise InvalidToolCallException(f"empty required arg '{key}' for {name}")

    if name not in TOOL_IMPL:
        raise InvalidToolCallException(f"unknown tool implementation: {name}")

    fn = TOOL_IMPL[name]
    return fn(**args) if args else fn()
