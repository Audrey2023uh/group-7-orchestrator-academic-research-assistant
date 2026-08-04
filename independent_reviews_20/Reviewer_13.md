# Peer Review — Reviewer 13

**Persona:** Multi-agent systems architect
**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance (Research Square rs-10485157/v1)

---

## 1. Summary

This paper attacks a real systems problem: LLM multi-agent workflows lose constraint and evidence commitments across natural-language hops, and conventional tracing does not score that loss in governance-relevant terms. The authors propose semantic tracing, implement a four-role LangGraph pipeline (Inventory → Evidence → Governance → Human Review) with LangChain tool/prompt/JSON-repair machinery, optionally emit LangSmith spans, and score handoffs with a rule-based evaluation layer. I read this primarily as a multi-agent systems architecture paper with an evaluation appendix, not as a finished metrology or compliance contribution.

The empirical story is mixed but usefully non-heroic. The 450/450 matrix completed with no terminal failures. Relative to llm_no_eval, the llm_langsmith_semantic_eval condition lowered TCS (0.624 vs. 0.912; Holm p < 0.001; medium Cliff’s δ), raised latency (~126.2 s vs. ~101.7 s; large Cliff’s δ), slightly worsened WRS, left most semantic metrics nonsignificant, and did not change decision-family correctness (57/160 vs. 59/160). Human calibration remains pending. As an architect, I find the systems decomposition credible and the negative-leaning results scientifically healthy; the manuscript needs tightening around metric interpretation and a few architectural ambiguities, but it is closer to publishable systems work than the strongest rejection cases in this area.

## 2. Strengths

Figure 5 and Figure 8 give a clean executable story: orchestrator, agents/tools, trace capture, evaluation, human gate, final decision. Table 3 is unusually responsible for ecosystem papers—it ties LangChain, LangGraph, and LangSmith to concrete modules (`llm_client.py`, `graph_langgraph.py`, `tracing.py`) and explicitly states what LangSmith does not do. Pydantic-validated `LLMHandoffPacket` objects as the unit of hop semantics (Figure 9) are the right systems abstraction; many multi-agent demos still pass free-text strings and then wonder why drift is unmeasurable. Preserving an unmodified deterministic baseline beside genuine LLM agents (Figure 11; Figure 22) is good experimental hygiene. Figure 20’s schema-validation emphasis matches what production MAS teams actually need. Completing variability and ablation cells rather than stopping at a demo trace shows engineering seriousness. The discussion’s conclusion that transparency/auditability—not decision accuracy—was the principal demonstrated benefit matches the data and matches my experience with agent wrappers around deterministic cores.

## 3. Weaknesses

Architectural sympathy does not erase several issues. First, the evaluation layer’s interaction with tracing appears to harm TCS. If enabling semantic evaluation drops required-span completeness from 0.912 to 0.624, either the required-span definition is unstable across conditions, instrumentation is inconsistently applied, or evaluation side-effects disrupt span emission. That is a first-order systems bug or definition bug and cannot be narrated away as a governance insight without root-cause analysis. Second, decision-family correctness near 36% suggests either very hard scenarios, weak judges, or agents that are not yet competent for the governance task; architects need error analysis by scenario family (Figure 23’s perturbation types) rather than only aggregate Fisher tests. Third, remediate remains proposed (Figure 8) while approve/restrict/monitor/escalate are shown; the control surface is incomplete for enterprise closure loops. Fourth, local Ollama-via-OpenAI-compatible routing is fine for a lab, but the paper should discuss how nondeterminism, tool timeouts, and repair-chain retries interact with LangGraph state and human-gate freezes under load. Fifth, pending human calibration means SPS/IDR/HPR cannot yet drive routing policies despite Equations (1)–(7); the architecture diagram should mark metric-triggered edges as future work more aggressively than Figure 17 currently does.

## 4. Methodological

Figure 13’s experimental loop and Figure 19’s three-condition split are methodologically sound for a systems paper: deterministic baseline, LLM without evaluation, LLM with LangSmith + evaluation. Keeping the production Vercel app unchanged avoids the common failure mode of “research” that silently mutates the live system. The ~30 scenario set covering clean evidence, drift, missing evidence, Shadow AI escalation, contradictions, and severity levels is a reasonable first generator, though I would prefer a published scenario schema and seeds. Checkpointing and resume-safe skips (Stage D) are practical and should be described with enough detail for other labs to copy. The main methodological gap for MAS readers is insufficient reporting of orchestration failure modes: schema repair frequency, tool retry counts, conditional-edge hit rates to human_review, and how often the gate’s freeze/resume path (Figure 17) was exercised in the 160+160 primary runs—not only in the n=5 Table 6 vignette.

## 5. Statistical

For an architecture audience, the statistics are adequate to support a cautious systems claim and inadequate to support a “semantic evaluation improves agent governance quality” claim. Holm-corrected Mann–Whitney tests with Cliff’s δ are appropriate for skewed latency/metric distributions. The large latency effect is believable for an added evaluation pass. Non-significant SPS/AHF/IDR/TUA/GCR/HPR/HEP results should push the authors to treat the evaluation layer as a diagnostic prototype, not as a proven control plane. Ablations with n=8 and large SPS Cliff’s δ are suggestive of packet-field sensitivity—useful for API design—but too weak for architectural mandates. Please report per-condition distributions or violin plots beyond Figure 14/18’s summary comparison, and break decision correctness down by scenario class.

## 6. Novelty

Relative to MetaGPT-style role pipelines and AgentOps taxonomies, the novelty is the governance-oriented handoff packet plus an explicit six-way separation of concerns (Section 5.7) inside a risk-intelligence case. That is incremental but real. LangGraph+LangChain+LangSmith compositions are no longer novel by themselves; what is still relatively scarce is a completed multi-hundred-run matrix that admits when evaluation fails to move decision quality. I would cite this as engineering knowledge contribution if the TCS regression is explained and the packet schema is positioned against prior structured agent-message formats more carefully.

## 7. Technical correctness

Implementation claims in Table 8 look coherent: agents implemented, live NVD retrieval observed, private LangSmith root trace documented, unit tests passed, production untouched. Technical concerns: (1) TCS decline with evaluation needs causal explanation; (2) WRS depends on uncalibrated weights yet is interpreted as reliability; (3) Table 6 expected outputs differ by condition (e.g., Monitor vs Proceed on clean evidence), which is acceptable only if condition-specific oracles are justified—otherwise “PASS” means “matched its own policy,” not “matched a shared governance truth”; (4) Figure 15 is wisely labeled conceptual—keep it that way. None of these fatally invalidate the systems artifact, but they limit the strength of correctness claims about governance outcomes.

## 8. Reproducibility

Architects will want the experimental repo, `requirements.txt` pins, graph definition, prompt templates (Appendix D / S3), scenario JSON, and scripts that regenerate Table 5. “Upon reasonable request” is a weak posture for a paper whose contribution is an implemented pipeline. Private LangSmith project details help authenticity but block replication of cloud spans; local JSON traces (`outputs/local_traces/`) should be sampled in the supplement. If those artifacts are released, reproducibility looks achievable because the architecture is concrete.

## 9. Clarity

For systems readers, Figures 6–8 and 20 are clear; the paper is long and sometimes repeats the same 450/450 and pending-calibration sentences. Condensing duplicated limitations language would help. Table 5 is the right results table; keep numerical WRS values rather than NR. Explain the TCS drop near Figure 14 with a span-inventory diff between conditions.

## 10. Revisions

1. Root-cause the TCS drop (0.912 → 0.624): publish required-span checklists per condition and show whether evaluation disables, renames, or delays spans.
2. Add orchestration telemetry: repair rates, tool failures, human-gate trigger counts across the 320 primary LLM runs.
3. Provide scenario-level decision-correctness breakdown aligned to Figure 23 perturbation families.
4. Mark metric-triggered policy edges in Figure 17 as pending calibration; do not imply closed-loop control from uncalibrated SPS/IDR.
5. Release or deposit the experimental codebase and a minimal trace/metric reproduction script.
6. Justify condition-specific expected decisions in Table 6 or adopt a shared oracle where scientifically appropriate.
7. Minor edit pass to reduce repetition and fill NR cells in Table 5.

These are fixable within a revision cycle. I do not see a fundamental architectural dead end.

## 11. Recommendation

**Minor Revision**

## 12. Confidence

**0.74**

I am fairly confident the systems contribution is real and that Minor Revision is appropriate if the TCS regression is explained rather than hand-waved. If the authors cannot explain TCS degradation or refuse to release reproduction materials, I would escalate to Major Revision on resubmission review.
