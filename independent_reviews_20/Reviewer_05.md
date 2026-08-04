# Peer Review — Reviewer 05

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**DOI:** 10.21203/rs.3.rs-10485157/v1  
**Author:** Audrey Rah / Rahimi  

---

## 1. Summary of the paper

Rahimi proposes a measurement stack for meaning preservation in LLM multi-agent governance workflows, implemented with LangChain agents, LangGraph routing, and LangSmith traces, and exercised inside SHADOWAI-RISK-related scenarios. The evaluation story mixes (a) computational scores derived from handoff comparisons and (b) a still-promised human annotation study. On the completed 450-run matrix, the eval-enabled LLM condition shows substantially lower TCS (0.624 vs 0.912), higher mean latency (~126.2 s vs ~101.7 s), small significant WRS decreases, non-significant SPS/AHF/IDR/TUA/GCR/HPR/HEP contrasts, and no decision-family correctness gain (57/160 vs 59/160). The author is explicit that human calibration and inter-rater agreement remain pending.

## 2. Major strengths

The paper’s threat-to-validity section actually names construct validity concerns for semantic similarity proxies—rare candor. Figure 21’s split between computational scores and pending calibration is the correct epistemic posture. Keeping LangSmith as an observability substrate rather than a magic semantic judge avoids a common category mistake in industry evaluations. Scenario typology that deliberately injects drift, missing evidence, and escalation suppression (Figure 23–26) is a promising start toward a diagnostic benchmark rather than only leaderboard accuracy.

## 3. Major weaknesses

**Construct validity of the metric suite is not established.** SPS, IDR, HPR, AHF, HEP, GCR, TUA, TCS, and WRS are presented as if they measure distinct theoretically motivated constructs (preservation, drift, hallucination propagation, handoff fidelity, escalation precision, compliance, tool correctness, trace coverage, reliability). Absent human labels, correlation structure, and discriminant validity checks, they may be overlapping rule hits on the same packet fields. Non-significant differences on SPS/IDR/HPR in Table 5 therefore cannot be read as “semantic behavior unchanged”; they may indicate insensitive operationalizations.

**Human calibration pending is not a minor caveat—it is the missing core of an NLP evaluation paper.** Appendix F’s rubric exists on paper; κ, ICC, adjudication outcomes, and item-level confusion patterns do not. Weight calibration for Equation (1) and WRS (9) is deferred, yet WRS significance is already reported.

**TCS is doing the empirical heavy lifting while being the least “semantic” construct.** A completeness ratio over required spans is an instrumentation coverage measure. Leading with TCS 0.624 vs 0.912 in the abstract risks advertising an observability artifact as evidence for semantic tracing effectiveness.

## 4. Methodological concerns

**Gold labels and annotation protocol.** Who annotates? On what sampling frame of hops? Are raters blinded to condition (eval vs no-eval)? Is the unit a hop, a packet field, or a full workflow? The mixed-methods diagram (Figure 12) places validation at the confluence of strands, but Stage F has not occurred while Stage E results are written in confirmatory language.

**Operationalization mismatch.** Section 9’s SPS mixes similarity, constraint overlap, and evidence support. Similarity on governance instructions is notoriously brittle (paraphrase vs constraint deletion). Constraint-set overlap misses severity of deleted constraints. Evidence support needs a groundedness protocol against NVD/tool returns; none is validated. HPR requires reliable detection of “unsupported claims introduced,” a hallucination evaluation problem the literature treats as hard—even with human judges.

**Baseline task difficulty.** Decision-family correctness near 36% in both LLM arms suggests either an ill-posed label taxonomy or a very hard decision family. Without confusion matrices or label definitions, construct validity of “correctness” itself is opaque. The n=5 walkthrough in Table 6 uses condition-specific expected outcomes (Monitor vs Proceed vs Hold vs Reject), which is fine for process QA but dangerous if similar remapping sneaks into the large-N correctness metric.

**Comparators.** The interesting NLP evaluation contrast would include strong single-agent baselines, alternative drift detectors, and human-only judgment upper bounds. Deterministic SHADOWAI-RISK logic is a systems baseline, not a semantic-measurement baseline.

## 5. Statistical concerns

From an evaluation-methodology angle, multiplicity across semantically related metrics is not only a Type I error issue; it is a construct fragmentation issue. If IDR and SPS are algebraic transforms of overlapping constraint features, joint non-significance is redundant information. Cliff’s δ for TCS and latency are fine for those operational endpoints. For decision correctness, reporting p≈0.91 without reliability-adjusted effective sample size or label noise model overstates the informativeness of the null. Ablation SPS effects at n=8 should not enter the main interpretive chain. Pending inter-rater agreement means any future human-correlated analysis will need pre-registered reliability thresholds before correlating automatic SPS with human scores.

## 6. Novelty assessment

Positioning semantic handoff fidelity as a first-class evaluation target for enterprise agent workflows is timely relative to AgentBench-style task success metrics and hallucination surveys focused on single-turn generation. The novelty will stick only if the metrics become validated instruments. As currently evidenced, the paper’s novelty is primarily systems integration plus an unvalidated metric proposal, which is weaker for NLP evaluation venues than for governance-engineering venues.

## 7. Technical correctness

Within the computational-ops story, contrasts are coherently repeated across Figure 14, Figure 18, and Table 5. The claim that annotated-corpus SPS/AHF/IDR/HPR/WRS values are not reported (near Table 8) while computational versions are reported is easy to miss; headings should say “automatic rule-based scores (uncalibrated).” Interpreting lower TCS as a semantic-tracing result is not technically justified by Equation (4)’s definition. Local $0 cost and non-significant tokens are plausible under Ollama-local execution but orthogonal to semantic construct claims.

## 8. Reproducibility assessment

Annotation guidelines without released annotated samples prevent reproduction of the evaluation methodology. Automatic metric code and scenario seeds are not publicly attached in a reviewer-accessible way. Private LangSmith traces block audit of what “observed required spans” contained when TCS fell to 0.624. Supplementary S2 survey and S3 stubs foreshadow reproducibility but do not currently enable an external team to replicate measurement properties (bias, variance, agreement).

## 9. Clarity and organization

Metric pedagogy is actually one of the clearer parts once the reader reaches Section 9 and Table 4; the difficulty is that Results ask those metrics to carry interpretive weight they have not earned. Too many application screenshots/pathway figures dilute the evaluation argument. A reorganization that fronts: constructs → operationalizations → reliability plan → automatic exploratory results → limitations would better match NLP evaluation norms. Abstract sentence packing of Holm results is accurate but invites over-reading of TCS as the semantic headline.

## 10. Suggested revisions

1. Run a pilot annotation study (even small-N) reporting κ/ICC on Appendix F dimensions before any WRS significance claims.  
2. Rename and segregate automatic scores as `auto-SPS`, `auto-IDR`, etc., and forbid governance-effectiveness language until calibration.  
3. Validate constructs: show convergent/discriminant correlations among metrics; include human ratings as anchors.  
4. Provide a groundedness protocol for unsupported claims (HPR/GCR) tied to tool outputs, not only packet self-text.  
5. Demote TCS from semantic-tracing headline to instrumentation QA; retarget abstracts toward the intended semantic constructs—or change the title’s emphasis.  
6. Publish label guidelines, adjudicated examples, and confusion matrices for decision-family correctness.  
7. Add baselines that stress-test metric sensitivity (paraphrase-only edits vs true constraint deletion).  
8. Keep pending surveys out of the critical path of the measurement argument.

## 11. Publication recommendation

Major Revision

## 12. Confidence score

0.86
