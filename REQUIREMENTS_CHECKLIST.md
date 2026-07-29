# Requirements Checklist (Source of Truth: Instructiones)

**Group 7 · Single-author submission · Audrey Rah**

Derived from Instructiones PDFs. Folder names `student_1_*` … `student_6_*` are required failure-mode package labels completed by one developer—not six contributors.

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
| A8 | Single author owns all six guardrails + integration | done |

## Contract-first

| ID | Requirement | Status |
|----|-------------|--------|
| C1 | Commit `contract.py` BEFORE individual work packages | done |
| C2 | Frozen contract used by all nodes | done |

## Six failure-mode packages (same author)

| ID | Package | Status |
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
| D1–D8 | README, DESIGN_DOCS, INTERVIEW_STORIES, contract, main_system, six packages, real metrics | done |
| D9 | Demo video(s) | MISSING — author must record |

## Academic workflow

| ID | Requirement | Status |
|----|-------------|--------|
| W1–W3 | Paper load, 20 isolated reviews, meta + final report | done |
| W4 | Cookie: Necessary/Essential only | documented |

## Gaps (honest)

- Author-recorded failure/system demo video(s)
- GitHub remote push if course requires a URL (`gh` not installed at build time)
