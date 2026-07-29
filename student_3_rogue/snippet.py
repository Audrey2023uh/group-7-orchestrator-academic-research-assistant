"""Guardrail snippet: tool-call allowlist middleware (Student 3)."""
from contract import ToolCallRequest
from tools.tool_runtime import validate_and_execute


def guarded_tool_call(tool_name: str, arguments: dict | None = None):
    return validate_and_execute(
        ToolCallRequest(tool_name=tool_name, arguments=arguments or {}),
        guardrail_enabled=True,
    )


def unguarded_tool_call(tool_name: str, arguments: dict | None = None):
    """Guardrail disabled — still uses mocked dangerous implementations that raise."""
    return validate_and_execute(
        ToolCallRequest(tool_name=tool_name, arguments=arguments or {}),
        guardrail_enabled=False,
    )
