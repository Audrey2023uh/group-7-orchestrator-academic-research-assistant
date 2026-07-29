# Design Documentation — Academic Research Orchestrator

**Group 7 · Author: Audrey Rah (single-author submission)**

One developer owned the full lifecycle: frozen shared contract, six code-based guardrails, coordinator-driven LangGraph integration, quantitative metrics, and interview narratives. Assignment folder names `student_1_*` … `student_6_*` label failure-mode packages only; they do not imply multiple contributors.

## Architecture diagram

One unified multi-agent system matching `main_system.py` (Group 7 · Audrey Rah). The `student_*` folders are failure-mode evidence packages for the six guardrails inside this single graph—not six separate systems.

```mermaid
flowchart TB
  subgraph UNIFIED["Unified Multi-Agent System — main_system.py"]
    direction TB

    subgraph GLOBAL["Global Cross-Cutting Guardrails"]
      direction LR
      PRIV["G5 Privacy Redaction<br/>redact_for_telemetry()"]
      CTX["G6 Context / Token Management<br/>manage_context()"]
    end

    C["Central Coordinator<br/>dynamic state routing"]

    C -->|"route=analyze<br/>missing analysis_payload"| A
    C -->|"route=review<br/>reviewer_index < 20"| B
    C -->|"route=validate<br/>reviews complete"| V
    C -->|"route=report<br/>is_validated"| R
    C -->|"round_number >= max_rounds<br/>G1 loop termination"| P

    A["Worker A: Analyzer<br/>G2 schema validate + 1 correction retry"]
    B["Worker B: Actor / Independent Reviewer<br/>x20 isolated runs · G3 tool allowlist"]
    V["Worker C: Validator<br/>G4 sanitization / invariants"]
    R["Worker D: Reporter / Meta-Analyst"]
    P["Partial Output Node<br/>graceful max-round stop"]

    A -->|"return to coordinator<br/>+ redact + manage_context"| C
    B -->|"return to coordinator<br/>+ redact + manage_context"| C
    V -->|"accept → coordinator"| C
    V -->|"rejection_flag<br/>validation failure"| RB

    RB["Rollback / Retry Path<br/>round_number++ · re-route to Analyzer"]
    RB -->|"self-correction retry<br/>if round_number < max_rounds"| C
    RB -->|"retry budget exhausted"| P

    R --> ENDN(["END"])
    P --> ENDN
  end

  SHARED["Shared Contract: contract.py · AgentState"]
  SHARED -.-> C
  GLOBAL -.-> A
  GLOBAL -.-> B
  GLOBAL -.-> V
  GLOBAL -.-> R
  GLOBAL -.-> C
```

Rendered image: [`architecture_diagram.png`](architecture_diagram.png) · Mermaid source: [`docs/architecture_diagram.mmd`](docs/architecture_diagram.mmd)

**Diagram coverage checklist (aligned with class instructions):**

| Required element | Shown |
|------------------|-------|
| One central Coordinator | Yes |
| Worker A Analyzer | Yes |
| Worker B Actor | Yes |
| Worker C Validator | Yes |
| Worker D Reporter | Yes |
| Dynamic conditional routing | Yes (`route=…` edges) |
| Retry / self-correction path | Yes (Rollback → Coordinator / Analyzer) |
| Validation failure rollback | Yes (`rejection_flag`) |
| Maximum-round termination | Yes (`round_number >= max_rounds` → Partial) |
| Global privacy redaction layer | Yes (G5) |
| Global context/token management | Yes (G6) |
| All six guardrails in one system | Yes (G1–G6) |

## State-routing explanation

Routing decisions are derived only from `AgentState`:

- Missing `analysis_payload` → Analyzer
- `reviewer_index < target_reviewers` → Reviewer (isolated; prior reviews excluded from Worker B context)
- Reviews complete and not validated → Validator
- `is_validated` → Reporter
- `rejection_flag` → increment `round_number`, rollback to Analyzer
- `round_number >= max_rounds` (default 5) → Partial Output termination

This yields conditional transitions, retry loops, and explicit termination without a fixed linear pipeline.

## Contract-first design

`contract.py` freezes:

- `AgentState` — universal graph state
- `AnalysisPayload` / `ReviewSchema` — structured I/O
- `ALLOWED_TOOLS` — capability boundary
- `InvalidToolCallException` — policy violation type
- Constants: `MAX_ROUNDS`, `TOKEN_SOFT_LIMIT`, `SCHEMA_RETRY_LIMIT`

All workers import these schemas; nodes must not invent parallel ad-hoc dictionaries for core fields. The same author committed the contract before implementing the six guardrail packages and the integrated graph.

## Six implemented failure modes

| # | Failure-mode package | Failure | Guardrail | Integration |
|---|----------------------|---------|-----------|-------------|
| 1 | `student_1_loop` | Infinite retry loops | `round_number >= 5` → partial | `main_system.coordinator_node` |
| 2 | `student_2_silent` | Silent structural failure | Pydantic + 1 retry | `validate_analysis_payload` |
| 3 | `student_3_rogue` | Rogue tool calls | Allowlist middleware | `tools.tool_runtime` |
| 4 | `student_4_cascade` | Downstream cascade | Sanitization + rollback | `sanitize_state_invariants` |
| 5 | `student_5_trace` | Privacy leak in traces | Redaction interceptor | `redact_for_telemetry` |
| 6 | `student_6_tokens` | Token / context explosion | Prune + summarize | `manage_context` |

Every package includes `snippet.py`, `test_failure.py`, `metrics.md`, and `interview_story.md` authored by Audrey Rah.

## Nineteen additional failure risks considered

1. Prompt injection via paper text  
2. Cross-reviewer contamination (information leakage between personas)  
3. Non-termination from LangGraph recursion limits alone  
4. Partial file writes leaving corrupt review artifacts  
5. Clock skew in latency metrics  
6. Schema drift between contract versions  
7. Over-redaction destroying debug utility  
8. Under-redaction of novel secret formats  
9. Tool argument type confusion (string vs path traversal)  
10. Replay attacks on cached tool results  
11. Model refusal loops under Ollama  
12. Duplicate reviewer IDs under concurrent runs  
13. Disk exhaustion from unbounded trace logs  
14. Unicode normalization mismatches in paper IDs  
15. False-positive cascade rejects starving the reporter  
16. Metrics fabrication if tests are skipped  
17. Environment variable leakage into child processes  
18. Dependency supply-chain risk in pip packages  
19. Human operators accepting all cookies on publisher sites  

## Alternative mitigations

| Risk | Alternatives |
|------|----------------|
| Loops | External watchdog process; circuit breaker library |
| Schema | JSON Schema validators; OpenAPI contracts |
| Tools | OS sandbox; separate tool microservice |
| Cascade | Saga pattern with compensating transactions |
| Privacy | Dedicated PII vault; field-level encryption |
| Tokens | Sliding window embeddings; remote summarization service |

## Design tradeoffs

- **Deterministic builders vs live LLM**: default offline path maximizes reproducibility and avoids paid APIs; live Ollama improves linguistic variety but reduces determinism.
- **Retry round vs workflow step counting**: `round_number` tracks rejection retries only so twenty reviewer executions remain possible under a retry ceiling of five.
- **Hardcoded allowlist vs dynamic discovery**: prefer explicit safety over flexible plugins for the coursework threat model.
- **Solo ownership**: one author kept contract, guardrails, and integration consistent, avoiding multi-contributor schema drift.

## Safety constraints

- Mock all destructive tools  
- Never execute real trades or deletes  
- Never commit `.env` secrets  
- Necessary/Essential cookies only for any browser interaction  
- No assistant-product branding in repository text  
