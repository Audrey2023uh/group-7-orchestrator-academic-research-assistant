"""Guardrail snippet: deterministic round_number termination (Student 1)."""
from contract import MAX_ROUNDS


def should_stop_retry_loop(round_number: int, max_rounds: int = MAX_ROUNDS) -> bool:
    """If round_number >= max_rounds, stop retrying and emit partial output."""
    return round_number >= max_rounds


def coordinator_route(round_number: int, rejection_flag: bool, max_rounds: int = MAX_ROUNDS) -> str:
    if should_stop_retry_loop(round_number, max_rounds):
        return "partial"
    if rejection_flag:
        return "retry"
    return "continue"
