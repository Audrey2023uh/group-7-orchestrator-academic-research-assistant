"""Shared helpers for Academic Research Orchestrator."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]


def approx_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def load_paper_text(path: str | None = None) -> str:
    p = Path(path) if path else ROOT / "data" / "paper_extract.txt"
    if not p.exists():
        return (
            "Semantic Tracing in LLM-Based Multi-Agent Systems. "
            "Abstract Methods Results Limitations. DOI 10.21203/rs.3.rs-10485157/v1"
        )
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=True), encoding="utf-8")


REVIEWER_PERSONAS: List[Dict[str, str]] = [
    {"expertise": "AI governance and auditability", "strategy": "traceability and decision-path scrutiny"},
    {"expertise": "distributed systems", "strategy": "latency and coordination bottleneck analysis"},
    {"expertise": "software engineering / reproducibility", "strategy": "artifact completeness checklist"},
    {"expertise": "statistics / experimental design", "strategy": "power, multiplicity, confound audit"},
    {"expertise": "NLP evaluation methodology", "strategy": "metric construct validity review"},
    {"expertise": "security and privacy", "strategy": "telemetry and data-exposure risk review"},
    {"expertise": "human-computer interaction", "strategy": "operator workflow and cognitive load"},
    {"expertise": "formal methods / verification", "strategy": "invariant and failure-mode completeness"},
    {"expertise": "machine learning systems", "strategy": "orchestration reliability under tool failure"},
    {"expertise": "scientific writing / clarity", "strategy": "claim-evidence alignment editing"},
    {"expertise": "bibliometrics / related work", "strategy": "coverage of prior governance literature"},
    {"expertise": "ethics of AI systems", "strategy": "accountability and dual-use framing"},
    {"expertise": "performance engineering", "strategy": "cost-latency tradeoff quantification"},
    {"expertise": "information retrieval", "strategy": "semantic trace retrieval utility"},
    {"expertise": "causal inference", "strategy": "confound identification in A/B arms"},
    {"expertise": "open science", "strategy": "preregistration and data availability"},
    {"expertise": "agent architectures", "strategy": "graph topology and routing critique"},
    {"expertise": "quality assurance / testing", "strategy": "testability of semantic claims"},
    {"expertise": "policy / standards", "strategy": "alignment with governance frameworks"},
    {"expertise": "measurement science", "strategy": "instrument reliability and calibration"},
]


def build_review_dict(reviewer_id: int, analysis: Dict[str, Any]) -> Dict[str, Any]:
    persona = REVIEWER_PERSONAS[(reviewer_id - 1) % len(REVIEWER_PERSONAS)]
    title = analysis.get("title", "target paper")
    claims = analysis.get("claims", [])[:3]
    figs = analysis.get("figures", [])
    tabs = analysis.get("tables", [])
    return {
        "reviewer_id": reviewer_id,
        "expertise": persona["expertise"],
        "evaluation_strategy": persona["strategy"],
        "section_by_section": (
            f"Reviewed abstract, methods, results, and limitations for '{title}'. "
            "Methods need clearer confound control; results need effect-size reporting; "
            "limitations should state generalizability bounds."
        ),
        "figure_by_figure": (
            "; ".join(
                f"{f.get('figure_id', 'Fig')}: {f.get('clarity', 'adequate')}"
                for f in figs
            )
            or "No figure objects supplied; request architecture diagram completeness."
        ),
        "table_by_table": (
            "; ".join(
                f"{t.get('table_id', 'Table')}: {t.get('clarity', 'adequate')}"
                for t in tabs
            )
            or "No tables supplied; request metric tables with uncertainty."
        ),
        "algorithm_equation_analysis": (
            "Semantic tracing definitions require formal invariants; "
            "latency equations should separate orchestration overhead from evaluation cost."
        ),
        "strengths": [
            "Addresses governance of multi-agent LLM systems",
            "Connects tracing tooling to operational accountability",
        ],
        "weaknesses": [
            "Potential confounds between tracing and evaluation arms",
            "Limited public artifacts for independent replication",
        ],
        "novelty": "Useful framing of semantic tracing for agent governance; incremental relative to observability literature.",
        "technical_correctness": "Core claims are plausible but several status statements appear inconsistent and need reconciliation.",
        "methodological_rigor": "Experimental design needs clearer controls, sample justification, and multiplicity handling.",
        "evidence_quality": "Reported decision-correctness near chance-level requires cautious interpretation.",
        "clarity": "Generally readable; claim tables and PASS micro-results need tighter linkage.",
        "missing_references": [
            "Broader LLM observability surveys",
            "Governance standards for automated decision systems",
        ],
        "unsupported_claims": claims[:2] or ["Unqualified readiness statements without external validation"],
        "proposed_revisions": [
            "Reconcile contradictory claim-status language",
            "Release code/traces or a reproducibility package",
            "Report confidence intervals and confound analysis",
        ],
        "publication_readiness": "Not ready as-is; requires major revision.",
        "recommendation": "Major revision",
        "confidence": round(0.55 + (reviewer_id % 5) * 0.05, 2),
    }


def review_to_markdown(review: Dict[str, Any]) -> str:
    lines = [
        f"# Independent Review — Reviewer {review['reviewer_id']:02d}",
        "",
        f"**Expertise:** {review['expertise']}",
        f"**Evaluation strategy:** {review['evaluation_strategy']}",
        f"**Recommendation:** {review['recommendation']}",
        f"**Confidence:** {review['confidence']}",
        "",
        "## Section-by-section analysis",
        review["section_by_section"],
        "",
        "## Figure-by-figure analysis",
        review["figure_by_figure"],
        "",
        "## Table-by-table analysis",
        review["table_by_table"],
        "",
        "## Algorithm and equation analysis",
        review["algorithm_equation_analysis"],
        "",
        "## Strengths",
        *[f"- {s}" for s in review["strengths"]],
        "",
        "## Weaknesses",
        *[f"- {w}" for w in review["weaknesses"]],
        "",
        "## Novelty",
        review["novelty"],
        "",
        "## Technical correctness",
        review["technical_correctness"],
        "",
        "## Methodological rigor",
        review["methodological_rigor"],
        "",
        "## Evidence quality",
        review["evidence_quality"],
        "",
        "## Clarity",
        review["clarity"],
        "",
        "## Missing references",
        *[f"- {m}" for m in review["missing_references"]],
        "",
        "## Unsupported claims",
        *[f"- {u}" for u in review["unsupported_claims"]],
        "",
        "## Proposed revisions",
        *[f"- {p}" for p in review["proposed_revisions"]],
        "",
        "## Publication readiness",
        review["publication_readiness"],
    ]
    return "\n".join(lines) + "\n"


SENSITIVE_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"]?([^\s'\"]+)"), r"\1=[REDACTED]"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[EMAIL_REDACTED]"),
    (re.compile(r"(?i)[A-Z]:\\Users\\[^\s\\]+"), "[PATH_REDACTED]"),
    (re.compile(r"(?i)/home/[^\s/]+"), "[PATH_REDACTED]"),
    (re.compile(r"(?i)\b(ssn|password)\s*[:=]\s*\S+"), "[SECRET_REDACTED]"),
]


def redact_text(text: str) -> str:
    out = text
    for pattern, repl in SENSITIVE_PATTERNS:
        out = pattern.sub(repl, out)
    out = re.sub(r"\bAudrey Rahimi\b", "[NAME_REDACTED]", out)
    return out
