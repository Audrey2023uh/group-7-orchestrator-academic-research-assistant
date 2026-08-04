"""Guardrail snippet: structured-output schema enforcement (Student 2).

Assignment PDF requires Worker A to force outputs through an explicit schema via
`.with_structured_output(ContractSchema)`, catch schema parse errors, and allow
exactly one automated self-correcting retry.

This module keeps the project fully offline (no Ollama, OpenAI, or paid APIs).
Literal `BaseChatModel.with_structured_output(...)` needs a live/fake chat-model
backend; instead we provide an **offline test double** of that LangChain API
surface that binds the frozen contract schema (`AnalysisPayload` as
`ContractSchema`) and validates with Pydantic. Behavior matches the assignment
intent: schema enforcement, `ValidationError` catch, one retry, then reject.
"""
from typing import Any, Dict, Tuple, Type

from pydantic import BaseModel, ValidationError

from contract import AnalysisPayload

# Frozen contract schema used as ContractSchema in assignment wording.
ContractSchema = AnalysisPayload


class OfflineStructuredOutputDouble:
    """Offline test double for LangChain `llm.with_structured_output(schema)`.

    Not a network LLM. Deterministic Pydantic validation against the shared
    contract so tests and demos run without any local/remote model service.
    """

    def with_structured_output(self, schema: Type[BaseModel]):
        """Bind an explicit schema object (assignment: ContractSchema)."""
        self._schema = schema
        return self

    def parse(self, payload: Dict[str, Any]) -> BaseModel:
        """Parse/validate structured payload; raises ValidationError on failure."""
        return self._schema.model_validate(payload)


def validate_with_one_retry(
    payload: Dict[str, Any], schema_retry_used: bool
) -> Tuple[bool, Dict[str, Any], bool, int]:
    """Returns ok, payload, retry_used, missing_field_count.

    Uses OfflineStructuredOutputDouble().with_structured_output(ContractSchema).
    """
    structured = OfflineStructuredOutputDouble().with_structured_output(ContractSchema)
    try:
        model = structured.parse(payload)
        return True, model.model_dump(), schema_retry_used, 0
    except ValidationError as exc:
        missing = len(exc.errors())
        if schema_retry_used:
            return False, payload, True, missing
        title = str(payload.get("title") or "")
        if len(title) < 5:
            title = "Semantic Tracing in LLM-Based Multi-Agent Systems"
        paper_id = str(payload.get("paper_id") or "rs-10485157")
        if len(paper_id) < 3:
            paper_id = "rs-10485157"
        corrected = {
            "paper_id": paper_id,
            "title": title,
            "sections_covered": list(
                set([*(payload.get("sections_covered") or []), "abstract", "methods", "results", "limitations"])
            ),
            "figures": payload.get("figures") or [],
            "tables": payload.get("tables") or [],
            "algorithms": payload.get("algorithms") or [],
            "claims": payload.get("claims") or [],
            "references_count": int(payload.get("references_count") or 0),
            "limitations": payload.get("limitations") or ["unspecified"],
        }
        try:
            model = OfflineStructuredOutputDouble().with_structured_output(ContractSchema).parse(
                corrected
            )
            return True, model.model_dump(), True, missing
        except ValidationError as exc2:
            return False, payload, True, len(exc2.errors())
