# Peer Review — Reviewer 14

**Persona:** Measurement science / metrology
**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance (Research Square rs-10485157/v1)

---

## 1. Summary

The manuscript asserts that meaning preservation across multi-agent hops can be treated as a first-class measurand and operationalized through a suite of scores (SPS, AHF, IDR, TCS, TUA, GCR, HPR, HEP, WRS) computed from LangSmith-oriented traces and structured handoff packets. A 450/450 experimental matrix is complete. The headline computational contrasts are a large, significant drop in Trace Completeness Score under the evaluation condition (0.624 vs. 0.912; Holm-adjusted p < 0.001; Cliff’s δ ≈ −0.33), a large latency increase (~126.2 s vs. ~101.7 s; Cliff’s δ ≈ 0.67), small significant decreases in WRS, nonsignificant differences for the remaining semantic/governance metrics, and nonsignificant decision-family correctness (59/160 vs. 57/160). Critically, the authors state that human calibration, inter-rater agreement, and annotated-corpus evaluation remain pending (Figure 21; Table 8; Table 9; Appendix C).

From a metrology standpoint, this is a proposal for quantities without a completed measurement model. Equations (1)–(9) are formalisms; they are not yet validated measurement procedures. Reporting inferential statistics on uncalibrated, human-pending semantic metrics while branding them as governance measurands is a category error. I regard the TCS and latency contrasts as potentially meaningful operational observations about instrumentation overhead, and the semantic suite as premature quantification.

## 2. Strengths

The paper occasionally uses measurement language carefully. Figure 21 explicitly distinguishes computational scores from pending human calibration—an essential honesty many metric papers omit. Table 4 lists ranges and intended interpretations. Missing-data rules and WRS weight-sensitivity plans are mentioned via `Metric_Definitions_and_Calibration.md`. The authors refuse to invent participant statistics or fabricated inter-rater coefficients (Section 7 integrity rules). Completing 450 runs with Holm correction and Cliff’s δ, rather than presenting only Table 6’s five-scenario PASS theater, shows some quantitative seriousness. TCS Equation (4) is at least closer to an observable ratio of required spans than SPS’s similarity-weighted blend. Acknowledging that weights α, β, γ and WRS weights require future annotated corpora (Appendix C) is correct metrological hygiene—if only the rest of the paper’s rhetoric obeyed that constraint.

## 3. Weaknesses

The central weakness is undefined or under-defined measurands coupled with statistical theater.

**Measurand definition.** What is the true quantity intended by “semantic preservation”? Equation (1) mixes `Sim(I0, Ih)`, constraint-set overlap, and `EvidSupport(Ih)` with unspecified weights summing to one. Without a reference measurement procedure, reference materials (annotated handoffs), and a documented uncertainty budget, SPS is a heuristic index, not a measurand. The same applies to IDR, HPR, and HEP: numerators such as “unsupported claims reused downstream” and “warranted escalations” are human concepts awaiting operationalization, yet Table 5 reports “not significant” as if the constructs were already stably measured.

**Pending human calibration.** The paper repeatedly says calibration and inter-rater agreement are pending, then still prints primary eval vs. no-eval contrasts for semantic metrics and composites. You cannot both declare Stage F pending and treat SPS/AHF/IDR/HPR/HEP/WRS differences as scientific results about meaning preservation. At most, you may report software-output distributions of rule-based detectors with a clear label: “uncalibrated detector scores.”

**Trace Completeness Score paradox.** TCS falls sharply when evaluation is enabled. Either the measurand “required spans present” changes definition across arms, or the measurement process is disturbed by the evaluation apparatus (observer effect). Until a metrological investigation of that discontinuity appears—repeatability, span checklist stability, intermediate precision—the TCS contrast is not interpretable as a property of semantic governance; it may be an artifact of the measuring system.

**Decision correctness.** The only externally meaningful outcome-like quantity in the primary contrast—decision-family correctness—does not differ (Fisher/χ² n.s.). Near-36% correctness also raises questions about the quality of the reference decisions used as a “true value.”

**WRS.** Equation (9) normalizes a signed weighted combination of uncalibrated inputs. Significance on WRS with NR point estimates in Table 5 is unacceptable reporting practice.

## 4. Methodological

Measurement methodology would require: (i) a documented concept analysis of each quantity; (ii) annotation guidelines with examples and edge cases; (iii) pilot annotation; (iv) inter-rater reliability (κ, α, or ICC as appropriate) with confidence intervals; (v) calibration of weights against human labels; (vi) uncertainty propagation into SPS/WRS; (vii) then, and only then, confirmatory comparisons across conditions. The manuscript inverts this order. Figure 16’s hop-comparison cartoon and Figure 15’s nested-run schema do not substitute for a calibration design. Table 7’s prototype rules (SPS = 1 if no drift else max(0, 1 − lost/|C0|), etc.) reveal that early metric logic was scenario-scripted—fine for software tests, fatal if silently generalized to the 450-run “metric suite.” The authors must state whether the 320 primary LLM runs used the same simplified rules, the Equation (1)–(9) forms, or another detector in `semantic_detector.py`, and how those map to the annotated-corpus plan.

## 5. Statistical

Statistically significant differences on ill-defined quantities are not scientific findings about the target constructs; they are differences in algorithm outputs. Holm correction controls family-wise error among tests; it does not create construct validity. Cliff’s δ on TCS and latency may be retained if TCS is redefined strictly as an instrumentation completeness ratio with a fixed span inventory. Cliff’s δ on WRS should be withdrawn until weights are calibrated and uncertainty is reported. Non-significance on SPS/AHF/IDR/TUA/GCR/HPR/HEP should not be narrated as “no meaningful effect established” about semantic phenomena; the correct statement is that uncalibrated detector outputs did not differ detectably under the chosen test. Ablations with n=8 are underpowered and should not be used to claim large SPS sensitivity. Please report standard uncertainties, not only p-values and ordinal effect sizes.

## 6. Novelty

Novel measurement contributions require either a new validated quantity with demonstrated reliability/validity or a significant improvement in uncertainty for an existing quantity. This paper offers a named suite and equations. Relative to existing overlap, entailment, faithfulness, and trajectory-evaluation metrics, the novelty of SPS/IDR/HPR as measurement instruments is not established. The systems integration may be novel engineering; it is not yet novel metrology. Figure 28’s contribution map should downgrade C2 from a “formal metric suite” deliverable to a “metric proposal pending calibration.”

## 7. Technical correctness

Computational reproducibility of a score is not the same as metrological correctness. It may be technically true that the matrix is 450/450 complete and that Mann–Whitney tests were applied. It is not technically correct to interpret those tests as measuring semantic preservation effectiveness, which the discussion sometimes approaches and sometimes denies. Internal contradictions appear where Table 8 says semantic metrics are “Not calculated from annotated corpora” while Table 5 lists SPS and related metrics as “Computed” with significance outcomes. Both can be true only if “Computed” means rule-based detector output—language that must be forced into every results sentence. Latency and $0 local cost are comparatively well-defined operational quantities and are the most trustworthy rows in Table 5.

## 8. Reproducibility

A metrological package would include raw annotations, coder IDs, adjudication records, weight-fitting scripts, and validation splits. Those are pending by the authors’ admission (Table 9). Without them, independent laboratories cannot assess bias, repeatability, or reproducibility (ISO 5725 sense) of SPS or HPR. Local JSON traces and private LangSmith spans reproduce the tracing substrate, not the semantic measurement. Code upon request is insufficient for measurement claims.

## 9. Clarity

Ironically, the paper is clear enough about pending calibration that the residual overclaim stands out. Figure 21 should govern the entire Results section; currently Results still reads like a completed metric evaluation. Replace “semantic and governance metrics” language with “uncalibrated automatic scores.” Clarify the TCS denominator’s span inventory in Equation (4) with a normative table. Resolve NR cells for WRS.

## 10. Revisions

1. Withdraw confirmatory claims about SPS/AHF/IDR/HPR/HEP/GCR/WRS until human calibration and inter-rater studies are completed; move those contrasts to an appendix labeled “uncalibrated detector outputs.”
2. Provide full measurand definitions, reference procedures, and uncertainty budgets for any quantity retained in the main results—likely TCS (fixed span checklist), latency, tokens, and decision-family correctness against a validated oracle.
3. Investigate and report the measurement-system cause of the TCS drop under evaluation.
4. Do not use WRS significance with undisclosed/NR values; publish weights, sensitivity analyses, and uncertainties together.
5. Separate software verification (Table 8) from measurement validation in the narrative and in Figure 28.
6. If annotated studies cannot be completed for this version, retitle and reframe the paper as an architecture/instrumentation preprint, not a measurement contribution.

Absent those changes, the semantic-measurand claim is not scientifically tenable.

## 11. Recommendation

**Reject**

## 12. Confidence

**0.88**

Confidence is high that pending human calibration of the semantic suite, combined with statistical reporting as if constructs were measured, is a fatal flaw for any reading of this work as measurement science. A resubmission reframed as systems instrumentation with only well-defined operational quantities could be reconsidered; as currently positioned, rejection is warranted.
