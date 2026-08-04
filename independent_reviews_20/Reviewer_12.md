# Peer Review — Reviewer 12

**Persona:** AI ethics / accountability
**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance (Research Square rs-10485157/v1)

---

## 1. Summary

The paper develops a semantic-tracing framework intended to make LLM multi-agent handoffs auditable for enterprise AI governance, using LangChain/LangGraph/LangSmith instrumentation inside a SHADOWAI-RISK-related experimental extension. Ethically, the manuscript’s most important empirical signals are not the architectural diagrams but the completed 450/450 matrix outcomes: evaluation-enabled runs show substantially lower trace completeness (TCS 0.624 vs. 0.912), meaningfully higher latency (~126.2 s vs. ~101.7 s), small but significant WRS reductions, nonsignificant movement on semantic and governance metrics (SPS, AHF, IDR, TUA, GCR, HPR, HEP), and nonsignificant decision-family correctness (57/160 vs. 59/160). Human calibration, inter-rater agreement, surveys, and production integration remain pending.

As an ethics and accountability review, I treat those results as a warning against governance theater. A system that increases latency, reduces measured trace completeness, and fails to improve decision correctness while still marketing interpretive mappings to NIST, the EU AI Act, ISACA, OECD, ENISA, and IEEE (Table 10; Figure 29) risks creating a false sense of control—especially when “Shadow AI” is both a motivating harm narrative and a scenario label inside a local prototype that is explicitly not production-integrated.

## 2. Strengths

Accountability-positive design choices are real. Figure 17 and Figure 26 place a Human Review Gate on the critical path rather than treating oversight as a dashboard afterthought. Section 5.7 and Figure 27 correctly refuse to let LangSmith “decide” approve/restrict/escalate outcomes; separating orchestration, LLM reasoning, deterministic safeguards, tracing, evaluation, and human decision is an ethical architecture contribution even before metrics are calibrated. The authors repeatedly state that governance mappings are interpretive, not certification (Figure 29). Reporting nonsignificant decision correctness rather than burying it is ethically better than typical agent-demo papers. Table 8’s frank “Not integrated into production” and “Pending semantic validation” rows reduce the chance that readers will mistake a laboratory extension for deployed assurance. The dual-use surface is at least partially acknowledged through cybersecurity framing and ENISA citations, and the conclusion admits that deterministic baselines may remain preferable when only a final recommendation is needed.

## 3. Weaknesses

The ethics problems concentrate in claim–evidence mismatch around Shadow AI, dual-use, and governance mapping.

First, Shadow AI claims. The introduction and motivation sections cast unauthorized AI use as a central organizational harm. Yet the empirical artifact does not study Shadow AI in the wild; it injects “Shadow AI” as a controlled scenario class among ~30 laboratory scenarios and shows that a Human Review Gate can fire under protocol. That is not evidence that semantic tracing detects, deters, or governs unsanctioned enterprise AI adoption. Using Shadow AI as a keyword and risk story while measuring only in-sandbox multi-agent workflows risks conceptual bait-and-switch: readers may infer organizational visibility gains that the 450/450 matrix does not demonstrate.

Second, dual-use. A detailed failure taxonomy (F1–F7), handoff schemas (Figure 3), and evaluation-layer logic that flags constraint omission, scope expansion, and escalation suppression can help defenders—but the same instrumentation recipe can help adversaries craft stealthier agent pipelines that preserve schema validity while laundering unsupported claims. The paper’s cybersecurity discussion (Section 12) emphasizes inventory-to-NVD linkage and unsafe tool selection visibility; it does not adequately analyze how publishing metric thresholds, perturbation designs (Figure 23–24), and escalation triggers could be gamed. Dual-use discussion is thin relative to the operational detail disclosed.

Third, governance overclaim. Even with Figure 29’s disclaimer, Table 10 maps low SPS/high IDR to NIST Manage actions, high HPR to NIST AI 600-1 confabulation controls, low TCS to EU AI Act transparency/logging expectations, and HEP monitoring to OECD/IEEE accountability. Given that SPS/IDR/HPR/HEP differences were nonsignificant in the primary contrast, and that human calibration is pending (Figure 21), these mappings are currently rhetorical alignments of unvalidated signals to heavyweight regulatory concepts. Low TCS under the evaluation condition is especially troubling ethically: if “insufficiently auditable” is the governance reading of low TCS, then the evaluation-enabled condition looks worse on the paper’s own auditability proxy while costing ~24 seconds of additional latency on average—yet the narrative still presents semantic tracing as a path to accountable AI.

## 4. Methodological

From an accountability perspective, the methodology’s staged design (Figure 12; Stages A–E) is coherent, but Stage F/G—human annotation, inter-rater agreement, and surveys—are exactly the stages that would justify ethical claims about oversight quality, and they remain pending. Evaluating HEP (Human Escalation Precision) computationally without human adjudication of whether escalations were warranted is circular: the metric that supposedly supports accountability has not been calibrated by accountable humans. Figure 19’s separation of LangSmith from evaluation is methodologically good; ethically, however, packaging both under “LangSmith + semantic evaluation” in public summaries (including the abstract’s compressed phrasing) can still mislead non-expert readers into believing a commercial tracing product performs normative governance assessment.

## 5. Statistical

The statistics undermine rather than support strong accountability claims. Decision-family correctness near 36% with no significant eval-versus-no-eval difference means the governance-facing outcome that executives would care about—right decision family—was not improved. Significant TCS degradation and large latency effects are costs borne by the organization. Small WRS decreases with evaluation further suggest that composite “reliability” under current weights moved the wrong direction. Non-significance on HPR and GCR means the paper cannot claim reduced hallucination propagation or improved policy compliance from the evaluation layer in the primary contrast. Ablations associating constraint/evidence removal with large SPS drops are underpowered (n=8) and should not be used in ethics argumentation about control efficacy. Holm correction is appropriate; it does not rescue the interpretative leap from these results to EU AI Act or NIST operational compliance narratives.

## 6. Novelty

Ethically novel work would either (a) validate human-oversight quality gains with inter-rater and stakeholder studies, or (b) rigorously stress-test dual-use and gaming. This paper’s novelty is mostly systems integration plus an honest negative-leaning computational result set. That honesty could itself be a contribution if the discussion centered organizational risk of adopting uncalibrated semantic dashboards. Instead, Sections 11–12 still pivot toward “process-level semantic accountability” as a needed enterprise capability while the measured accountability-relevant outcomes remain weak or pending.

## 7. Technical correctness

Technically, the authors are careful in places: LangSmith observes; humans decide; production Vercel is unchanged; 450/450 is complete; calibration pending. The ethical incorrectness is not fabricated numbers but category errors—treating interpretive Table 10 cells as if they were operational control designs, and treating Shadow AI scenario PASS rows in Table 6/Table 7 as evidence about Shadow AI governance. Table 7’s perfect escalation precision/recall in a five-scenario micro-comparison is easy to over-read; those are protocol-compliance scores under labeled perturbations, not field accountability metrics. Figure 10’s real private trace ID documents instrumentation authenticity but says nothing about fairness, due process, or misuse potential.

## 8. Reproducibility

For ethics auditability, third parties need redacted traces, annotation guidelines, and decision logs that show how human gates changed outcomes. Code “upon request,” private LangSmith credentials, and pending surveys (Table 9) currently prevent independent accountability assessment. If organizations adopted this pattern based on the preprint alone, they would be unable to reproduce the claimed audit trail in their own assurance programs. That is an ethical reproducibility failure, not merely an engineering inconvenience.

## 9. Clarity

Figure 29’s separation of authoritative requirements from author mappings is clear and welcome. Clarity problems arise in keyword and abstract framing: “Shadow AI,” “AI governance,” “NIST AI RMF,” and “cybersecurity” sit beside results that primarily show a local multi-agent instrumentation cost/benefit profile. Non-specialist risk readers may not notice that human calibration is pending until late sections. The paper should lead with the accountability-relevant headline: evaluation increased latency, decreased TCS, and did not improve decision-family correctness.

## 10. Revisions

1. Reframe Shadow AI: distinguish empirical claims about unsanctioned AI use from laboratory scenario labels; remove or heavily qualify keyword-level implications that the study measured Shadow AI governance in organizations.
2. Add an explicit dual-use and adversarial-gaming subsection covering threshold gaming, schema-valid laundering of unsupported claims, and risks of publishing escalation logic.
3. Demote Table 10 from “control mapping” language to “hypothesized future control hypotheses,” and bar any mapping that depends on metrics lacking significant effects or human calibration.
4. Center the discussion on the ethical meaning of worse TCS and higher latency without decision-quality gains; discuss automation bias and false assurance risks.
5. Do not report HEP as an accountability metric until human adjudication exists; mark it provisional in Figure 21 and Table 4.
6. Provide a stakeholder-facing limitations box stating that the work is not a compliance assessment under the EU AI Act or NIST AI RMF.
7. Release redacted materials sufficient for an external ethics audit of human-gate behavior.

## 11. Recommendation

**Major Revision**

## 12. Confidence

**0.82**

I am confident that the accountability overclaim relative to pending human work and nonsignificant decision correctness is a central defect. Confidence is slightly reduced only because the authors already include many disclaimers; the issue is whether those disclaimers sufficiently counteract the governance framing for likely readers.
