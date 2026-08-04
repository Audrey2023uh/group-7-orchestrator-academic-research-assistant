# Grading Checklist

**Group 7 · Single-author submission · Audrey Rah**

Maps assignment rubric items to implementation evidence. Folder names `student_*` are required failure-mode package labels completed by the same author. Does not claim a guaranteed grade.

| Requirement | Pts | Implementation location | Test / evidence | Output file | Status |
|-------------|-----|-------------------------|-----------------|-------------|--------|
| Failure demo video | 20 | Failure scripts in each `student_*/test_failure.py` | Run pytest with guardrail off/on | ✅ Individual videos completed (`Final_student1..6_video.mp4` in each `student_*` folder; ~2 minutes each) | PRESENT |
| Guardrail code (code-based) | 20 | `main_system.py` + `agents/guardrails.py` + all six `student_*/snippet.py` | `pytest` suite | snippets | PRESENT |
| Quantitative metrics | 15 | All six `student_*/metrics.md` written by tests | Measured before/after tables | `student_*/metrics.md` | PRESENT |
| Interview story (~150 words) | 15 | All six `student_*/interview_story.md` + `INTERVIEW_STORIES.md` | First-person technical stories by Audrey Rah | those files | PRESENT |
| Frozen shared contract | 10 | `contract.py` | Imported by all nodes; first git commit | `contract.py` | PRESENT |
| Integrated multi-agent graph | 15 | Coordinator + 4 workers in `main_system.py`; all six guardrails wired | `python main_system.py` → 20 reviews, validated, terminated | `outputs/*` | PRESENT |
| Design docs | 5 | `DESIGN_DOCS.md` (6 modes + 19 risks + tradeoffs) | Document review | `DESIGN_DOCS.md` | PRESENT |
| Dynamic routing / retries / termination | — | `coordinator_node`, conditional edges | Graph smoke tests | `tests/test_graph.py` | PRESENT |
| Mock dangerous actions | — | `tools/tool_runtime.py` | Rogue tool tests | `student_3_rogue/metrics.md` | PRESENT |
| Free/local stack only | — | `requirements.txt`, Ollama optional | No paid API required | README | PRESENT |
| 20 isolated reviewers | — | `reviewer_node` loop | 20 markdown files | `outputs/reviews/reviewer_01..20.md` | PRESENT |
| Meta-analysis after validation | — | `reporter_node` | File exists post-run | `outputs/meta_analysis.md` | PRESENT |
| Single-author consistency | — | README / DESIGN / stories / checklist | Explicit Group 7 · Audrey Rah authorship | docs | PRESENT |

## Demo video (author-recorded)

✅ Individual videos completed. All six approximately two-minute failure/success demonstration videos are included in the corresponding `student_*` folders (`Final_student1_video.mp4` … `Final_student6_video.mp4`).

Team integrated 5-minute demo video: not yet in the repository (record separately if still outstanding).
