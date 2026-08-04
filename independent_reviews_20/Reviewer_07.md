# Peer Review — Reviewer 07

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**Persona lens:** Human–computer interaction; human oversight, calibration, and operator load

---

## 1 Summary

The paper argues that multi-agent LLM workflows need measurable preservation of goals, constraints, and evidence commitments across natural-language handoffs, and it operationalizes that idea in a local Inventory → Evidence → Governance → Human Review Gate pipeline. I evaluate the contribution from an HCI and human-oversight perspective: Does the Human Review Gate support calibrated, accountable intervention, or does it merely insert a mandatory node that shifts unresolved uncertainty onto operators? Figure 17’s escalation loop (trigger, freeze, evidence package, human decision, resume/terminate) and Figure 26’s human-escalation path correctly position oversight as a first-class design object, which is welcome relative to agent demos that bury humans in a footnote. Yet human calibration, inter-rater agreement, and surveys remain pending throughout (abstract; Stage E; Table 9), while HEP—the metric most directly about escalation quality—shows no significant eval-versus-no-eval difference in the primary contrast. Decision-family correctness sits near 57–59 of 160 in both LLM arms. The manuscript therefore documents a technically wired gate more convincingly than it documents usable, reliable human governance under cognitive load.

---

## 2 Major strengths

Mandatory routing to human review in the LangGraph StateGraph (Table 3; Figure 8) avoids the common failure mode where “human-in-the-loop” is optional theater. The handoff packet schema (Figures 3 and 9) gives reviewers structured fields—constraints, residual risk, escalation state—rather than a raw chat dump, which is a prerequisite for reducing search cost during oversight. Appendix F’s coding rubric (constraint preservation, evidence support, tool appropriateness, contradiction absence, escalation appropriateness on 0–2 scales, with third-coder adjudication) is a sensible plan for aligning machine scores with human judgment once annotation begins. The discussion’s own conclusion—that transparency and auditability, not superior final accuracy, are the demonstrated benefits—matches what an oversight researcher would expect and resists overselling automation.

---

## 3 Major weaknesses

Operator cognitive load is almost entirely unmeasured. Mean workflow latency rises from about 101.7 s to 126.2 s when evaluation is enabled (Table 5; Figure 18), yet there is no human-subjects study of how long an analyst needs to consume the evidence package, how many screens or spans they inspect (Figure 10’s hierarchy is complex), or whether freeze-and-resume interrupts create mode errors. HEP is defined (Equation 8) but not validated against expert warrants; without calibration, “precision of escalations” is a computational label, not a human-factors outcome. Figure 21 explicitly separates computationally applied metrics from pending human calibration—honest, but it leaves the central HCI claim undersupported: that semantic-tracing signals help people intervene better. Pending surveys (Supplementary File S2; Table 9) mean we lack even self-report measures of trust, workload (e.g., NASA-TLX), or appropriate reliance.

---

## 4 Methodological concerns

Mixed-methods Stages A–E culminate in a completed computational matrix while Stage F/G human data are deferred (Figure 12). For an oversight paper, that sequencing inverts priorities: the interface and escalation policy should be stress-tested with people before claiming governance relevance. The gate’s decision vocabulary (approve/restrict/monitor/escalate; remediate still proposed in Figure 8) is not accompanied by a decision-support design—highlighting, progressive disclosure, or explanation of which metric triggered freeze. Scenario-level Table 6 shows the multi-agent condition producing Hold/Reject outcomes where the deterministic baseline often Monitors or Escalates under different expected mappings; without a think-aloud or agreement study, it is unclear whether humans would endorse those gate outcomes or merely rubber-stamp them. Temperature variability and ablations expand machine conditions but do not expand human protocol conditions (time pressure, partial information, conflicting metric alerts).

---

## 5 Statistical concerns

Non-significant HEP, SPS, AHF, IDR, TUA, GCR, and HPR between primary LLM conditions (Table 5) undercuts the narrative that the evaluation layer currently improves the signals humans would use. Significant reductions in TCS and WRS with evaluation, plus large latency effects, suggest the eval arm may worsen the operator’s information environment (less complete traces, slower cycles) while leaving decision-family correctness unchanged (Fisher/χ² n.s., p ≈ 0.91). Ablations with n=8 are correctly flagged as low power; similarly, human agreement studies will need pre-specified κ/ICC targets and sample sizes—Appendix F describes adjudication but not power. Until calibrated weights exist for Equation 1 and Equation 9, presenting WRS “expert weights” as significantly lower with eval risks implying expert disagreement with the system when “expert” may mean an unvalidated weighting heuristic.

---

## 6 Novelty

Relative to Amershi et al.’s human–AI interaction guidelines (cited) and EU AI Act human-oversight expectations, the novelty is the concrete gate plus packetized handoffs inside an AI-risk inventory workflow. That applied packaging is useful. Conceptually, the work does not yet advance theories of calibrated trust, automation bias in multi-agent traces, or shared mental models across Inventory/Evidence/Governance roles. Novelty will increase substantially once the planned annotation and survey strands exist; at present, novelty is stronger on systems integration than on HCI knowledge claims.

---

## 7 Technical correctness

Implementation evidence for the `human_review` node and Shadow AI / escalation triggering (Table 8) appears consistent and appropriately scoped as local-only. Prototype HEP rules in Section 10.3 (1 when required escalations are handled or non-escalations correctly left alone) are logically coherent for a lab stub but are not the same as human-warranted escalation quality—mixing them in reader-facing tables without persistent caveats could mislead. Figure 15’s warning not to treat nested-run diagrams as empirical screenshots is good practice and should be echoed wherever conceptual escalation figures might be mistaken for validated UX.

---

## 8 Reproducibility

Prompts and rubric stubs are pointed to Supplementary File S3 and Appendix F, which helps future human-subjects replication. Missing pieces for HCI reproducibility include: task instructions for reviewers, UI wireframes of the evidence package, timing protocols, and exclusion criteria for operators. Code upon request and private LangSmith projects hinder labs that want to recreate the exact freeze metadata humans would see. Local JSON traces could support offline replay studies if released with a codebook linking spans to gate states.

---

## 9 Clarity/organization

Human-oversight content is distributed across Figures 8, 17, and 26, Equation 8, Appendix F, and limitations text. A single “Human Review Gate design and evaluation” subsection would improve scanability for HCI readers. The paper’s repeated reminders that calibration is pending are clear; less clear is how operators should act when SPS/IDR/HPR are non-significant while TCS drops—actionable guidance for threshold setting is thin despite Table 10’s interpretive mappings (HEP monitoring to tune human-gate thresholds).

---

## 10 Suggested revisions

1. Run a modest human-subjects study: inter-rater agreement on Appendix F labels; HEP against expert warrants; workload and time-on-task at the gate.  
2. Redesign the evidence package for cognitive economy—prioritize trigger rationale, changed constraints, and missing evidence over full span trees by default.  
3. Report how often the gate fires, false-alarm and miss rates from the human’s perspective, and whether latency growth predicts abandoned reviews.  
4. Keep remediate-as-proposed clearly separated in all UX claims; avoid implying a full oversight workbench.  
5. Pre-register annotation sample size and agreement metrics before claiming calibrated SPS/WRS.  
6. Discuss automation bias: high AHF/completeness displays may encourage over-trust even when decision accuracy is mediocre (~0.36 decision-family correctness).  
7. Soften enterprise oversight recommendations until survey and calibration pending items in Table 9 are addressed.

---

## 11 Recommendation

**Major Revision**

The Human Review Gate is a promising control point, but the manuscript currently validates wiring more than human oversight quality. Add empirical human calibration, agreement, and workload evidence—or reframe claims strictly as systems architecture without governance-effectiveness language.

---

## 12 Confidence

**0.74**
