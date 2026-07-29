"""Shared frozen state contract for the Academic Research Orchestrator.

All graph nodes must read/write through these schemas.
"""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FigureNote(BaseModel):
    figure_id: str
    caption: str = ""
    supports_claims: bool = True
    clarity: str = "adequate"
    missing_info: str = ""


class TableNote(BaseModel):
    table_id: str
    caption: str = ""
    supports_claims: bool = True
    clarity: str = "adequate"
    missing_info: str = ""


class AnalysisPayload(BaseModel):
    """Structured Analyzer output (Worker A)."""

    paper_id: str = Field(..., min_length=3)
    title: str = Field(..., min_length=5)
    sections_covered: List[str] = Field(default_factory=list)
    figures: List[FigureNote] = Field(default_factory=list)
    tables: List[TableNote] = Field(default_factory=list)
    algorithms: List[str] = Field(default_factory=list)
    claims: List[str] = Field(default_factory=list)
    references_count: int = 0
    limitations: List[str] = Field(default_factory=list)

    @field_validator("sections_covered")
    @classmethod
    def require_core_sections(cls, v: List[str]) -> List[str]:
        required = {"abstract", "methods", "results", "limitations"}
        lowered = {s.lower() for s in v}
        missing = required - lowered
        if missing:
            raise ValueError(f"missing required sections: {sorted(missing)}")
        return v


class ReviewSchema(BaseModel):
    """Schema every independent reviewer must satisfy."""

    reviewer_id: int = Field(..., ge=1, le=20)
    expertise: str
    evaluation_strategy: str
    section_by_section: str
    figure_by_figure: str
    table_by_table: str
    algorithm_equation_analysis: str
    strengths: List[str]
    weaknesses: List[str]
    novelty: str
    technical_correctness: str
    methodological_rigor: str
    evidence_quality: str
    clarity: str
    missing_references: List[str]
    unsupported_claims: List[str]
    proposed_revisions: List[str]
    publication_readiness: str
    recommendation: Literal["Accept", "Minor revision", "Major revision", "Reject"]
    confidence: float = Field(..., ge=0.0, le=1.0)


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)


class AgentState(BaseModel):
    """Universal graph state contract."""

    task_domain: str = "academic_research_assistant"
    raw_input: str = ""
    paper_path: str = ""
    round_number: int = 0
    max_rounds: int = 5
    is_validated: bool = False
    rejection_flag: bool = False
    schema_retry_used: bool = False
    error_log: Optional[str] = None
    analysis_payload: Dict[str, Any] = Field(default_factory=dict)
    sanitized_tool_calls: List[str] = Field(default_factory=list)
    pending_tool_calls: List[ToolCallRequest] = Field(default_factory=list)
    reviewer_index: int = 0
    target_reviewers: int = 20
    reviews: List[Dict[str, Any]] = Field(default_factory=list)
    current_review: Dict[str, Any] = Field(default_factory=dict)
    messages: List[Dict[str, str]] = Field(default_factory=list)
    token_estimate: int = 0
    redacted_trace_events: List[str] = Field(default_factory=list)
    route: str = "analyze"
    terminated: bool = False
    partial_output: bool = False
    meta_analysis: str = ""
    final_report: str = ""
    metrics: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


# Hardcoded tool allowlist for Worker B middleware
ALLOWED_TOOLS: Dict[str, Dict[str, Any]] = {
    "load_paper_extract": {"required_args": ["path"]},
    "list_review_requirements": {"required_args": []},
    "mock_web_lookup": {"required_args": ["query"]},
}


class InvalidToolCallException(Exception):
    """Raised when a tool call violates the allowlist or argument policy."""


MAX_ROUNDS = 5
TOKEN_SOFT_LIMIT = 2500
SCHEMA_RETRY_LIMIT = 1
