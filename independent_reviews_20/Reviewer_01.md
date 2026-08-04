# Peer Review — Reviewer 01

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**DOI:** 10.21203/rs.3.rs-10485157/v1  
**Author:** Audrey Rah / Rahimi  

---

## 1. Summary of the paper

This preprint proposes semantic tracing as a governance-oriented measurand for LLM multi-agent workflows: rather than treating observability as mere span logging, it asks whether goals, constraints, evidence commitments, and escalation cues survive agent-to-agent handoffs. The author situates the work in enterprise AI risk—Shadow AI visibility, NIST AI RMF Govern/Map/Measure/Manage expectations, and related assurance instruments—and anchors the narrative in SHADOWAI-RISK, a live academic prototype that links AI inventories to vulnerability intelligence and executive decision pathways.

Operationally, the study separates a preserved deterministic baseline from a local experimental extension that uses LangChain for genuine LLM invocation (prompts, tools, structured JSON parsing, retries), LangGraph for stateful Inventory → Evidence → Governance → Human Review orchestration, and optional private LangSmith instrumentation for span capture. A rule-based semantic evaluation layer sits outside LangSmith. The completed matrix is reported as 450/450 runs (deterministic 32; llm_no_eval 160; llm_langsmith_semantic_eval 160; variability 50; ablations 48) with zero terminal failures. Primary eval-versus-no-eval contrasts show lower Trace Completeness Score under evaluation (0.624 vs. 0.912), higher latency (~126.2 s vs. ~101.7 s), small but significant WRS reductions, non-significant differences for SPS/AHF/IDR/TUA/GCR/HPR/HEP, and decision-family correctness that does not differ (59/160 vs. 57/160). Human calibration, inter-rater agreement, surveys, and production integration are explicitly pending.

## 2. Major strengths

The governance framing is unusually careful for this literature. The manuscript repeatedly refuses to equate LangSmith tracing with semantic scoring or with approve/restrict/escalate decisions, which is the right institutional message for NIST/ISACA-oriented readers. Table 1’s gap synthesis and the interpretive mapping in Table 10 (with the certification disclaimer in Figure 29) show discipline about what standards require versus what the author is proposing as research interpretation.

Implementation honesty is another strength. Table 3 ties LangChain, LangGraph, and LangSmith to concrete file-level roles; Figure 5 and Figure 11 make clear that the experimental stack is local and not quietly folded into the Vercel deployment. Completing a 450-run matrix with checkpointing and reporting both favorable and unfavorable contrasts (lower TCS; similar correctness; latency cost) builds credibility with governance audiences who are tired of cherry-picked agent demos.

## 3. Major weaknesses

The central governance claim—that semantic preservation can be measured and mapped to controls—still rests on computationally applied, uncalibrated metrics. Equation (1)–(9) and Table 4 define an attractive suite, but Stage F annotation and Appendix F’s human rubric have not been executed. Until those exist, WRS movements and null SPS/IDR/HPR results are difficult to interpret as governance evidence.

Relatedly, the “benefit” story in the Discussion and Conclusion emphasizes transparency and auditability, yet the primary quantitative signal associated with the evaluation-enabled condition is degraded TCS and a large latency penalty, without a corresponding gain in decision-family correctness. For AI-governance readers, that pattern needs a sharper theory of when process visibility is worth operational cost.

Finally, code and traces remain available only upon request, and LangSmith evidence is private (project semantic-tracing-shadowai). That limits independent scrutiny of the governance artifact the paper advocates.

## 4. Methodological concerns

The mixed-methods staging (framework → prototype observation → local extension → matrix → pending calibration) is sound on paper, but Stage E aggregates arrive before Stage F construct validation. Figure 21 correctly distinguishes computational scores from pending calibration; the Results section should lean harder on that distinction when interpreting Table 5.

Condition labeling also needs tighter discipline in places. The evaluation-enabled arm bundles LangSmith tracing with the semantic evaluation layer. Figure 19 argues for separating agents, LangSmith, and evaluation; the primary contrast still risks attributing TCS drops to “evaluation” when instrumentation or required-span definitions may be confounded. A clearer factorial decomposition (LLM only / LLM+LangSmith / LLM+LangSmith+eval) would strengthen causal reading of the TCS and latency effects.

The small n=5 prototype scenarios in Table 6/Table 7 are useful process illustrations but should not be rhetorically adjacent to the n=160 inferential claims without stronger section boundaries.

## 5. Statistical concerns

Holm correction and Cliff’s δ reporting for the primary contrasts are welcome. The TCS effect (medium δ ≈ −0.33) and latency effect (large δ ≈ 0.67) are clearly communicated; the Fisher/χ² non-significance for decision correctness (p ≈ 0.91) appropriately dampens claims of superior governance outcomes.

Concerns remain. Ablations at n=8 are correctly flagged as low-power, yet large SPS Cliff estimates (≈0.5–0.625) are still narratively available to optimistic readers. Multiple correlated metrics (WRS composites plus component scores) raise family-wise questions beyond the Holm adjustments already applied to the primary suite. Exact WRS point estimates are marked NR in Table 5, which weakens appraisal of the “small but significant” reliability reductions. Pre-registration of the primary endpoint (TCS vs. decision correctness vs. SPS) would help future versions avoid appearance of outcome flexibility.

## 6. Novelty assessment

Relative to AgentOps taxonomies and LangSmith documentation, the novelty is the governance binding: handoff packets as units of analysis, failure classes F1–F7, and interpretive control mapping for enterprise AI risk. That intersection is real and publishable in applied AI-governance venues, though incremental relative to concurrent multi-agent failure benchmarks. The SHADOWAI-RISK anchoring differentiates the paper from generic agent-observability notes, provided implemented versus proposed components remain as carefully separated as in Figure 6–8.

## 7. Technical correctness

Within the manuscript’s own scope statements, technical claims are largely careful. LangSmith is not said to compute SPS/GCR; remediate remains proposed; production files are untouched. The reported matrix composition and primary contrasts are internally consistent across abstract, Section 8, Table 5, and Figure 14/18.

Residual technical unease concerns metric operationalization: prototype scoring rules near Table 6 (e.g., binary-ish HPR/GCR behaviors) may not match the continuous formulations in Section 9. Clarifying which definitions generated the n=160 aggregates versus the n=5 walkthrough would improve correctness of interpretation.

## 8. Reproducibility assessment

Supplementary Files S1–S4 and Appendix E’s environment variables are positive signals. However, “available upon reasonable request,” private spans, and a local Windows path for the experimental project are insufficient for independent replication of the 450/450 matrix. Reviewers cannot verify required-span definitions behind TCS 0.624 vs. 0.912, temperature/variability protocols, or semantic_detector.py rule logic. A public, redacted reproducibility package with seeds, scenario manifests, and aggregate CSVs should be a condition of acceptance-track revision.

## 9. Clarity and organization

The paper is ambitious and sometimes overloaded with figures (research logic, layered architecture, many pathway diagrams). Still, the separation of orchestration, reasoning, safeguards, tracing, evaluation, and human decision in Section 5.7 is lucid and should be foregrounded earlier. Abstract density is high but accurate. Occasional placeholder references (e.g., Table ??) and figure-number sprawl (Figure 1 versus later contribution figures) need cleanup before journal submission.

## 10. Suggested revisions

1. Complete or, at minimum, pilot human calibration (Appendix F) with inter-rater statistics before treating SPS/IDR/HPR/WRS as governance-ready signals.  
2. Publish redacted code, scenario JSON, metric definition files, and aggregate result tables sufficient to reproduce Table 5.  
3. Disentangle LangSmith-only effects from evaluation-layer effects on TCS and latency; revise Figure 19 into an executed factorial analysis if feasible.  
4. Report WRS point estimates, confidence intervals, and multiplicity plan explicitly; keep ablation claims in a clearly exploratory subsection.  
5. Sharpen the Discussion so transparency benefits are argued on auditability criteria, not implied decision-quality gains (given 59/160 vs. 57/160).  
6. Repair cross-reference placeholders and reduce redundant architecture figures that do not change the empirical argument.

## 11. Publication recommendation

Major Revision

## 12. Confidence score

0.78
