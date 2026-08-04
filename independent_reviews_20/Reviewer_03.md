# Peer Review — Reviewer 03

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**DOI:** 10.21203/rs.3.rs-10485157/v1  
**Author:** Audrey Rah / Rahimi  

---

## 1. Summary of the paper

From an artifact standpoint, this work packages a local multi-agent governance pipeline: Pydantic handoff packets, LangChain `ChatOpenAI` agents with tools (`nvd_cve_lookup`, `evidence_fixture_loader`), a LangGraph `StateGraph` (`inventory → evidence → governance → human_review`), optional `@traceable` LangSmith spans, and a separate rule-based evaluator (`semantic_detector.py`). SHADOWAI-RISK on Vercel is left unchanged; experiments live in a separate local tree. The author reports finishing 450 workflow executions across deterministic, LLM, variability, and ablation cells, contrasting eval vs no-eval LLM arms on TCS (0.624 vs 0.912), latency (~126.2 s vs ~101.7 s), and decision-family correctness (57/160 vs 59/160, n.s.), among other scores. Human calibration remains undone. Code availability is “upon reasonable request.”

## 2. Major strengths

The implementation boundary discipline is better than average for agent papers. Table 3’s mapping of packages to files, Figure 10’s refusal to fake a LangSmith screenshot, and Table 8’s explicit “not integrated into production” row reduce the usual vaporware risk. Separating orchestration (LangGraph), model calls (LangChain), tracing (LangSmith), and scoring (local rules) is the correct engineering decomposition; Section 5.7 states it plainly. Completing a resume-safe matrix with zero terminal failures suggests real harness engineering rather than a one-off notebook demo.

## 3. Major weaknesses

**Artifacts are not reviewable.** A systems paper whose contribution is an operable tracing/evaluation stack cannot gate the source, prompts, scenario fixtures, local JSON traces, and aggregate exporters behind email requests. Private LangSmith project `semantic-tracing-shadowai` and a single root trace id do not allow reviewers to replay spans, validate metadata tags (`agent_role`, `hop_index`, etc.), or audit how TCS numerators/denominators were computed.

**Reproducibility package claims exceed what reviewers can access.** Appendix L lists S3 `Reproducibility_Package/` and metric definition markdown, but the preprint channel does not make clear that these are publicly downloadable with the submission. Local absolute paths in Section 5.4 are useless to anyone else.

**Evaluation coupling to unavailable detectors.** If the headline empirical result is that enabling semantic evaluation lowers TCS and raises latency without improving decisions, reviewers must inspect the evaluator and the required-span schema. Those are precisely the artifacts withheld.

## 4. Methodological concerns

Smoke-test evidence (two unit tests passed; live CVE identifiers once) is far below what is needed to trust a 450-run campaign. There is no reported CI job, hermetic environment lockfile beyond a requirements mention, container image, or deterministic replay mode for LLM calls (local Ollama OpenAI-compatible endpoint is fine architecturally, but model digest, Modelfile, and sampling parameters must be pinned).

Scenario generation and perturbation injection (constraint omission, scope expansion, evidence inflation, etc.) are described narratively around Figure 23–24, yet without a versioned scenario manifest a third party cannot regenerate the matrix. Ablation cells (48) and variability cells (50) are especially opaque: what was deleted, in which hop, under which seed?

The dual metric story—continuous equations in Section 9 versus prototype Boolean-ish rules near the five-scenario study—smells like two code paths. Engineering rigor demands one metric library, golden tests, and a single schema version stamped into every output JSON.

## 5. Statistical concerns

I defer detailed multiplicity critique to statistical specialists, but from a measurement-pipeline view the statistics inherit whatever bugs exist in trace export and scoring. If evaluation adds spans or fields that TCS requires, the 0.624 vs 0.912 contrast may be an instrumentation bug misread as a finding. Latency +24.5 s mean difference with large Cliff’s δ is plausible for extra work, but without profiling traces (evaluator time vs model time vs LangSmith export) the number is not actionable. Decision correctness parity (≈36% either way) suggests either a hard task or a weak labeler; neither can be diagnosed without the scoring scripts.

## 6. Novelty assessment

Wiring LangChain + LangGraph + LangSmith to a governance workflow is incremental engineering. The more distinctive piece is the handoff-packet schema and failure taxonomy feeding enterprise controls. That novelty is unrealized for the community until the artifact is public. Right now the paper reads as a private lab notebook summary with extensive architecture figures (Figure 2, 5, 7, 8, 20).

## 7. Technical correctness

Claims that LangSmith does not compute SPS/GCR and does not choose approve/restrict/escalate match the described code roles and are believable. Functional Table 8 items (agents implemented locally; Human Review Gate triggers on Shadow AI/escalation; local traces under `outputs/local_traces/`) are credible as self-reports but unverified. Inconsistency risk remains between “semantic metrics pending annotated corpora” (Table 8/9) and extensive computational contrasts in Table 5—reviewers need to know which code produced the 160-run aggregates if annotation never happened. The paper’s answer (rule-based computational application without human calibration) must be reflected in method names and result headings to avoid implying validated semantic scores.

## 8. Reproducibility assessment

**Fail.** Code upon request; traces private; production integration absent; survey/annotation pending; no public DOI-attached archive of the experimental repository; Windows-specific local path published instead of a clone URL. Appendix E environment variables help configure LangSmith but do not reproduce results. I cannot re-run the 450/450 matrix, regenerate Table 5, or confirm Figure 18’s latency/correctness comparison. For an artifact-centric contribution, this is disqualifying under contemporary SE/empirical software engineering expectations.

## 9. Clarity and organization

The manuscript over-indexes on architecture diagrams and under-indexes on build/run instructions. A competent external engineer wants: repo layout, `make reproduce`, pinned models, scenario IDs, and a results schema. Instead, organization prioritizes governance essays and many near-duplicate workflow figures (Figure 8 vs 20 vs 22). Table 3 and Table 8 are the most useful artifacts sections and should lead the experimental write-up.

## 10. Suggested revisions

1. Publish a public repository (or anonymous archive for double-blind) containing `llm_agents/`, `workflow/`, scenarios, metric code, and scripts that emit Table 5.  
2. Ship redacted local JSON traces and a documented subset of LangSmith exports sufficient to validate TCS inputs.  
3. Pin model identity, temperature grid, retry policy, and dependency hashes; add a one-command reproduction path for a smoke subset and for full aggregates.  
4. Unify metric implementations; add unit tests that lock Equations (1)–(9) to fixtures; delete ambiguous prototype scoring forks or isolate them clearly.  
5. Profile latency to show where the ~126.2 s vs ~101.7 s gap arises.  
6. Replace “upon reasonable request” with a concrete artifact DOI before resubmission.  
7. Trim duplicate figures; keep Figure 5, Figure 10, Figure 19, and the results displays.

## 11. Publication recommendation

Reject

## 12. Confidence score

0.88
