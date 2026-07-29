"""Guardrail snippet: telemetry redaction interceptor (Student 5)."""
from agents.guardrails import redact_for_telemetry


def intercept(event: str) -> str:
    return redact_for_telemetry(event)
