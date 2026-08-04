# Peer Review — Reviewer 15

**Persona:** Policy / standards (NIST AI RMF; EU AI Act)
**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance (Research Square rs-10485157/v1)

---

## 1. Summary

This preprint seeks to connect multi-agent observability to enterprise AI governance obligations by defining semantic-tracing signals and mapping them interpretively onto NIST AI RMF, the EU AI Act, ISACA assurance practices, OECD principles, ENISA cybersecurity guidance, and IEEE 7000 (Table 10; Figure 29; Section 12). The implementation side is a local LangChain/LangGraph/LangSmith extension beside SHADOWAI-RISK, with a completed 450/450 experimental matrix. Empirically, evaluation-on runs show lower TCS (0.624 vs. 0.912), higher latency (~126.2 s vs. ~101.7 s), small WRS reductions, nonsignificant semantic/governance metric shifts, and nonsignificant decision-family correctness (57/160 vs. 59/160). Human calibration, surveys, and production integration remain pending.

My review asks a policy question: does the governance mapping operate as an implementable control design, or does it remain rhetorical crosswalk prose? Figure 29 correctly labels mappings as non-certification interpretations. Table 10 nonetheless presents tracing signals as if they were actionable triggers for Manage functions, transparency duties, and audit tests. Given the empirical profile—especially unchanged decision correctness, degraded TCS, and pending human work—the operational content is thin. The paper is useful as a research probe but not yet as standards-aligned governance method.

## 2. Strengths

Policy-facing strengths exist. The authors cite primary instruments rather than only blogs: NIST AI RMF 1.0, NIST AI 600-1 Generative AI Profile, NIST CSF 2.0, Regulation (EU) 2024/1689, OECD AI Principles, ENISA reports, ISACA lifecycle guidance, IEEE 7000-2021, ISO/IEC 42001, and ISO/IEC 23894. Figure 29’s visual separation of authoritative requirements from author interpretations is the right epistemic posture for academic work near regulated domains. Human oversight is not optional in the architecture: Figures 17 and 26 encode freeze/evidence-package/human-decision paths consistent in spirit with EU AI Act human-oversight expectations, even though the paper cannot claim Act compliance. Explicit missing-data behavior (“Data Unavailable” / “Not refreshed”) in the live prototype observation (Section 10.1) aligns with good assurance hygiene. The completed matrix and frank nonsignificant decision-correctness result prevent a pure success narrative that would be dangerous if reused in board decks. Recommendations in Section 12 (inventory AI systems; bind to vulnerability intelligence; require tracing for multi-agent workflows; keep prototype distinct from production claims) are practically sensible.

## 3. Weaknesses

**Rhetorical vs. operational mapping.** Table 10 maps “Low SPS / high IDR” to “Pause autonomous handoff; revise prompts/policies” under NIST Manage / ISACA monitoring. Operational mapping would specify: threshold determination method, false-positive/false-negative tolerances, roles accountable for pause decisions, record-keeping retention, and appeal/override paths. None of that is present. Moreover, SPS/IDR were nonsignificant in the primary contrast and are pending human calibration (Figure 21), so the trigger condition is neither validated nor stable.

**EU AI Act transparency/logging.** Table 10 links low TCS to Act transparency/logging expectations. Two problems follow. First, TCS is an author-defined span-completeness ratio (Equation 4), not a logging obligation analysis under the Act’s articles on record-keeping, technical documentation, or transparency to deployers/users. Second, the evaluation-enabled condition—the condition that supposedly advances governance—produced worse TCS. A policy reader must conclude that the proposed “governance” arm weakened the paper’s own auditability proxy while adding ~24 s mean latency. That undercuts operational credibility.

**NIST AI RMF Govern–Map–Measure–Manage.** Semantic tracing is repeatedly said to support Measure/Govern needs. Measure in the RMF sense requires valid metrics and documented risk measurement processes. The manuscript’s own limitations state that semantic metrics are not human-calibrated and that no inter-rater study exists. Therefore RMF Measure support is aspirational. Govern requires policies, accountability structures, and workforce processes; a local experimental repo with a Human Review Gate node is a technical control fragment, not a governance system. Map and Manage receive interpretive mentions without organizational context artifacts (system cards, impact assessments, residual-risk acceptance).

**ISACA-style assurance.** Generating “sampleable artifacts” is necessary but not sufficient for assurance. Auditors need populations, sampling plans, exception handling, and evidence retention. Private LangSmith projects and code-upon-request do not yet constitute an assurance evidence regime.

**Shadow AI and risk narrative.** Policy sections use Shadow AI exposure to motivate controls, but empirical work does not measure organizational Shadow AI prevalence, detection rate in unmanaged channels, or residual risk after control adoption. The mapping from laboratory escalation scenarios (Table 6 mandatory human-escalation row) to enterprise Shadow AI policy is rhetorical.

## 4. Methodological

For standards-oriented methodology, the study should have included a conformance matrix with columns for instrument clause, required organizational evidence, implemented system evidence, gap, and residual risk—updated after the 450/450 runs. Instead, Appendix notes and Table 10 offer high-level alignments. Figure 12’s mixed-methods plan includes surveys (S2) that could have captured practitioner judgments about control usefulness; those data are pending (Table 9). Without them, policy claims lack even qualitative stakeholder validation. The three-condition design (Figure 19) is scientifically helpful, but policy evaluation also needs a “documentation-only / no-agent” control for cost–benefit of multi-agent complexity versus deterministic baselines—partially present in Table 7’s runtime contrast (0.0001 s vs. ~5.85 s in the micro-study; ~101–126 s in the full LLM conditions) yet not translated into a governance cost-effectiveness argument.

## 5. Statistical

Policy adoption thresholds cannot be set from these statistics. Decision-family correctness did not improve under evaluation (p ≈ 0.91). If a control does not improve decision quality and worsens completeness and latency, a risk committee following RMF Manage would demand a clear compensating benefit. Process transparency is the authors’ answer (Section 11); that benefit is qualitatively plausible but not quantified (e.g., auditor time saved, incident detection lead time, oversight error rates). Significant TCS degradation should be treated as a control deficiency candidate, not as incidental. Small WRS decreases with evaluation are likewise adverse signals under current scoring. Nonsignificant HPR/GCR results mean the paper cannot claim measurable reduction in hallucination propagation or policy violations—both highly salient to NIST AI 600-1 and assurance testing.

## 6. Novelty

Crosswalking agent metrics to NIST/EU language is not new as a genre; many white papers do it. What would be novel is an operational playbook: clause-level evidence, calibrated thresholds, human-oversight procedures tested with inter-rater reliability, and production logging that satisfies stated regulatory functions. The present combination of a real multi-agent prototype plus interpretive Table 10 is only partially novel. The empirical candor about nonsignificant decision correctness is more novel—and more valuable to policymakers—than the mapping table itself.

## 7. Technical correctness

The paper is technically careful when it says mappings are interpretive and that no legal compliance claim is made (limitations; Figure 29). Technical incorrectness arises when operational verbs (“pause,” “trigger policy exception workflow,” “treat decision as insufficiently auditable”) appear without operational definitions, inviting over-reading by compliance teams. Table 5’s results are internally consistent with the abstract. The standards citations appear to point at real instruments. ISO/IEC 42001 and 23894 are named in related work but scarcely operationalized later; either deepen those alignments or remove them from the implication chain to avoid citation padding.

## 8. Reproducibility

Regulatory science and assurance demand reproducible evidence packs. Supplementary Files S1–S4 and private traces are a start, but policy reproducibility requires: redacted decision logs, human-gate rationales, retention schedules, and a publicly reviewable mapping spreadsheet with article/clause IDs. “Upon reasonable request” code availability is poorly matched to transparency themes the paper associates with the EU AI Act. Production integration pending (Table 8) means there is not yet a deployer-side evidence trail.

## 9. Clarity

Figure 29 and the limitations section are clear. Less clear is the abstract’s keyword stack (Shadow AI, NIST AI RMF, cybersecurity) beside results that a standards officer would summarize as: “local multi-agent evaluation increased latency, reduced trace completeness, and did not change decision correctness; human validation pending.” That plain-language summary should appear early for policy readers. Table 10 should be retitled “Hypothesized future control linkages (non-operational)” to prevent misuse.

## 10. Revisions

1. Convert Table 10 into a clause-level operational matrix (instrument → clause/function → required evidence → current system evidence → status: implemented/experimental/proposed → empirical support from the 450/450 matrix).
2. Explicitly analyze why lower TCS under evaluation is compatible—or incompatible—with claimed support for transparency/logging expectations.
3. Tie any retained NIST Measure claims to a completed calibration roadmap with acceptance criteria; until then, restrict Measure language to “proposed metrics.”
4. Quantify the transparency benefit (even via small expert review study) if decision correctness remains nonsignificant; otherwise weaken Manage recommendations.
5. Add a “how not to use this paper” box for compliance officers: not a conformity assessment, not an EU AI Act readiness claim, not a Shadow AI control validation.
6. Either operationalize ISO/IEC 42001/23894 mappings or remove them from the governance implications narrative.
7. Deposit an assurance-oriented evidence pack (redacted traces, gate logs, mapping spreadsheet).

With those revisions, the work could become a credible standards-informed systems paper. Without them, the governance chapter remains rhetorical.

## 11. Recommendation

**Major Revision**

## 12. Confidence

**0.80**

I am confident that the governance mapping is not yet operational at NIST/EU rigor, and that the empirical pattern (TCS down, latency up, decision correctness unchanged, human calibration pending) blocks strong policy claims. Confidence is not higher only because the authors’ disclaimers are genuine; the revision burden is to make the paper’s structure match those disclaimers.
