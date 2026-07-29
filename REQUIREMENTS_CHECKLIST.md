# Requirements Checklist (Source of Truth: Instructiones)

Derived from complete reading of all PDFs in `Instructiones/` before implementation.
Assignment wins over any conflicting informal instructions.

## Core learning / architecture

| ID | Requirement | Status |
|----|-------------|--------|
| A1 | ONE unified system: Coordinator + 4 Workers | done |
| A2 | Domain: Academic Research Assistant | done |
| A3 | Dynamic state-based routing, conditional transitions, retry loops, termination | done |
| A4 | Not a naive linear pipeline | done |
| A5 | Python + LangGraph + LangChain Core + Pydantic | done |
| A6 | LangSmith optional free-tier only; no paid APIs required | done |
| A7 | All external destructive actions mocked | done |

## Contract-first

| ID | Requirement | Status |
|----|-------------|--------|
| C1 | Commit `contract.py` BEFORE individual work | done |
| C2 | Frozen contract used by all nodes | done |

## Six failure modes + guardrails

| ID | Student | Status |
|----|---------|--------|
| F1 | student_1_loop | done |
| F2 | student_2_silent | done |
| F3 | student_3_rogue | done |
| F4 | student_4_cascade | done |
| F5 | student_5_trace | done |
| F6 | student_6_tokens | done |

## Deliverables

| ID | Path | Status |
|----|------|--------|
| D1–D8 | README, DESIGN_DOCS, INTERVIEW_STORIES, contract, main_system, students, real metrics | done |
| D9 | Videos | NOT AUTOMATABLE — human recording required |

## Academic workflow

| ID | Requirement | Status |
|----|-------------|--------|
| W1–W3 | Paper load, 20 isolated reviews, meta + final report | done |
| W4 | Cookie: Necessary/Essential only | documented |

## Gaps

- Individual 2-minute failure videos
- Team 5-minute demo video
- GitHub remote push requires `gh` install + auth
