"""Guardrail snippet: context window / token management (Student 6)."""
from agents.guardrails import manage_context
from contract import TOKEN_SOFT_LIMIT


def prune_messages(messages, soft_limit: int = TOKEN_SOFT_LIMIT):
    return manage_context(messages, soft_limit=soft_limit)
