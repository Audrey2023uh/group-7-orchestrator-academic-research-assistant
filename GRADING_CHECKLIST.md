# Grading Checklist

Maps assignment rubric items to implementation evidence. Does not claim a guaranteed grade.

| Requirement | Pts | Implementation location | Test / evidence | Output file | Status |
|-------------|-----|-------------------------|-----------------|-------------|--------|
| Failure demo video (individual) | 20 | Failure scripts in each `student_*/test_failure.py` | Run pytest with guardrail off/on | Recorded MP4 **not in repo** — must be filmed manually | PARTIAL |
| Guardrail code (code-based) | 20 | `main_system.py` + `agents/guardrails.py` + `student_*/snippet.py` | `pytest` 20 passed | snippets | DONE |
| Quantitative metrics | 15 | `student_*/metrics.md` written by tests | Measured before/after tables | `student_*/metrics.md` | DONE |
| Interview story (~150 words) | 15 | `student_*/interview_story.md` + `INTERVIEW_STORIES.md` | Word-count ~150 technical stories | those files | DONE |
| Frozen shared contract | 10 | `contract.py` | Imported by all nodes | `contract.py` | DONE |
| Integrated multi-agent graph | 15 | Coordinator + 4 workers in `main_system.py` | `python main_system.py` → 20 reviews, validated, terminated | `outputs/*` | DONE |
| Design docs | 5 | `DESIGN_DOCS.md` (6 modes + 19 risks + tradeoffs) | Document review | `DESIGN_DOCS.md` | DONE |
| Dynamic routing / retries / termination | — | `coordinator_node`, conditional edges | Graph smoke tests | `tests/test_graph.py` | DONE |
| Mock dangerous actions | — | `tools/tool_runtime.py` | Rogue tool tests | metrics student_3 | DONE |
| Free/local stack only | — | `requirements.txt`, Ollama optional | No paid API required | README | DONE |
| 20 isolated reviewers | — | `reviewer_node` loop | 20 markdown files | `outputs/reviews/reviewer_01..20.md` | DONE |
| Meta-analysis after validation | — | `reporter_node` | File exists post-run | `outputs/meta_analysis.md` | DONE |

## Team demo video (5 min)

Not produced in this environment. Script outline: show architecture → disable one guardrail → show failure metrics → enable guardrail → show recovery → show 20 reviews + meta-analysis.
