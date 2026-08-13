"""Persistent research memory for the Academic Research Assistant.

Short-term memory: conversational turns scoped to the current session.
Long-term memory: papers, findings, decisions, and agent outputs across sessions.

The store is a SQLite database (server-side), isolated per user. Secrets are
redacted and never persisted. This package is additive: the LangGraph CLI path
keeps working if memory is unavailable.
"""

from memory.service import (
    approve_decision,
    clear_user_memory,
    delete_memory_item,
    delete_session,
    get_or_create_session,
    list_memory,
    list_sessions,
    load_session_messages,
    memory_brief_for_user,
    persist_research_run,
    pin_finding,
    save_message,
)

__all__ = [
    "approve_decision",
    "clear_user_memory",
    "delete_memory_item",
    "delete_session",
    "get_or_create_session",
    "list_memory",
    "list_sessions",
    "load_session_messages",
    "memory_brief_for_user",
    "persist_research_run",
    "pin_finding",
    "save_message",
]
