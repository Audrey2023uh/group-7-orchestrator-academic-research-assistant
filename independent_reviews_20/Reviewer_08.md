# Peer Review — Reviewer 08

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**Persona lens:** Causal inference; experimental identification and A/B design

---

## 1 Summary

I review this preprint as a design-and-analysis problem: what causal contrast is actually identified by the completed 450/450 matrix, and do the reported Holm-corrected Mann–Whitney and Fisher tests support the interpretive claims? The abstract and Section 8 advertise primary eval versus no-eval contrasts (n=160 each) with lower TCS under evaluation, lower WRS variants, large latency effects, and null results for most semantic metrics and decision-family correctness. Figure 19 asserts a three-condition separation—deterministic baseline; LLM without semantic evaluation; LLM with LangSmith tracing and semantic evaluation—expressly to avoid attributing evaluation effects to LangSmith alone. That verbal commitment is undermined by the operational fact that the third arm bundles private LangSmith instrumentation with the semantic evaluation layer. Figure 14 and Table 5 therefore compare a compound treatment to a control that lacks both pieces. Under standard identification assumptions, the estimand is the joint effect of (tracing + evaluation + whatever else differs in that configuration), not the effect of “semantic evaluation” or of “LangSmith.” Given that bundle, plus pending human calibration of the very metrics used as outcomes, I do not find the causal story publishable in its current form.

---

## 2 Major strengths

The author repeatedly warns against overclaiming production validation and notes that metrics are computationally applied rather than construct-validated (Figure 21). Reporting nulls for SPS/AHF/IDR/TUA/GCR/HPR/HEP and for decision correctness is scientifically healthier than p-hacking a success narrative. Completing a large matrix with checkpointing (Figure 13) and stating 0 terminal failures provides a clear accounting of sample realization. Cliff’s δ alongside Holm-adjusted p-values is preferable to p-values alone. The deterministic baseline’s inclusion, even if under-powered relative to LLM arms (32 vs 160), shows awareness that LLM stochasticity needs a stable reference pathway.

---

## 3 Major weaknesses

The central identification failure is the LangSmith–evaluation confound. Figure 19’s schematic cannot repair a design that never crosses the two factors. A 2×2 (LangSmith on/off × evaluation on/off), or at least an LLM+LangSmith-without-eval arm and an LLM+eval-without-LangSmith arm, is the minimum for the claims the discussion wants to make about observability versus evaluation. Second, multiple endpoints are tested (TCS, two WRS versions, a battery of semantic metrics, latency, tokens, decision correctness) with Holm correction mentioned for some contrasts; the full family of tests, ordering, and whether latency/tokens were primary or secondary are not pre-specified in a protocol. Third, decision-family correctness near 36% raises questions about the outcome definition and base rates; a null between arms is not informative if both arms are poor against ground truth. Fourth, ablations at n=8 with large Cliff’s δ on SPS are correctly labeled low power yet still appear in the results narrative—classic over-interpretation risk.

---

## 4 Methodological concerns

Assignment mechanism is unclear: are the 160+160 runs independent replications on a fixed scenario bank with shared seeds logged, or a mixture of scenarios and temperatures that induces dependence across observations? Mann–Whitney assumes independent samples; repeated measures nested in scenarios (Figure 15’s nested-run schema is “conceptual only”) would require hierarchical models or scenario-level paired contrasts. Figure 13 includes annotation in the loop, but annotation did not occur—so metric computation for SPS-like quantities in the large matrix must rely on rule-based detectors (`semantic_detector.py`) whose error process may itself be affected by the evaluation flag (post-treatment measurement bias). The small five-scenario prototype (Tables 6–7) uses condition-specific expected outcomes, which means “accuracy” is not transportable to the 160-run arms without a unified label map. Temperature variability (50 runs) and ablations (48) are described as part of the matrix but are not integrated into a single pre-registered analysis plan that protects the primary contrast from optional stopping or selective emphasis.

---

## 5 Statistical concerns

Table 5’s headline TCS decline (0.912 → 0.624, Cliff’s δ ≈ −0.33) under the bundled treatment is difficult to interpret causally: evaluation might strip or omit spans, tracing might change instrumentation, or completeness scoring might treat cloud-exported fields differently. Latency’s large effect (δ ≈ 0.67) is plausible as a cost of extra work but is not mediated/moderated formally. Non-significant token differences with significant wall-clock differences suggest waiting, I/O, or evaluation overhead rather than generation cost—interesting, but again descriptive of a bundle. Fisher/χ² on 59/160 vs 57/160 (p ≈ 0.91) is appropriately null; presenting it beside dramatic TCS effects invites readers to construct a “transparency without accuracy” story that still depends on an unidentified mechanism. WRS “expert” weights without validated experts are not estimands of scientific interest. Confidence intervals for proportions and for Cliff’s δ are not systematically reported in the extract’s summary tables. Multiple-comparison control across the semantic battery may explain many nulls; that is fine if the primary endpoint was predeclared—otherwise nulls and positives alike are hard to trust.

---

## 6 Novelty

Methodologically, combining LangGraph agents with a metric suite is incremental relative to AgentOps and multi-agent failure papers cited (e.g., Cemri et al.). The causal-design novelty is negative: the paper does not introduce a cleaner identification strategy than typical demo-style A/B conflations. The governance mapping (Table 10, Figure 29) is interpretive and not an empirical contribution. I would rate scientific novelty as modest and currently blocked by design ambiguity.

---

## 7 Technical correctness

Equations (1)–(9) are internally consistent as definitions; they are not validated measurement models. Calling the matrix “complete:true” is fine as engineering status, not as statistical adequacy. The manuscript’s own integrity rules (no invented participant statistics; synthetic traces labeled) are followed in spirit, which I appreciate. Technical incorrectness arises when prose attributes effects to “semantic evaluation” or to “LangSmith tracing” separately while the contrast identifies only their combination (see also Figure 27’s conceptual separation of trace capture and evaluation—conceptually right, experimentally untested).

---

## 8 Reproducibility

Without public code, run-level microdata, random seeds, and a pre-registered analysis script, independent re-estimation of Table 5 is impossible. Supplementary File S3 is mentioned, but Code Availability is request-gated. For causal credibility, the community needs a DAG of intended interventions, an analysis notebook that reproduces Holm adjustments, and a table of scenario IDs per run. Private LangSmith dependency further obstructs exact replication of TCS if TCS depends on cloud-visible spans.

---

## 9 Clarity/organization

Figure 19 and Figure 27 communicate the intended logical separation well; the results text sometimes re-blurs it. Figure 14’s visual emphasis on TCS versus decision correctness is clear but rhetorically powerful relative to the weak identification. The paper is long enough that a short “Estimands and assumptions” subsection would help methodologists more than additional architecture diagrams.

---

## 10 Suggested revisions

1. Re-run or re-analyze with a factorial design that crosses LangSmith and evaluation, or explicitly redefine all claims as effects of the bundled treatment.  
2. Pre-register primary and secondary endpoints, the exact multiple-testing procedure, and exclusion rules.  
3. Move from unpaired Mann–Whitney on pooled runs to scenario-paired or multilevel models; report ICC by scenario.  
4. Provide run-level data and scripts for Table 5.  
5. Demote n=8 ablation effect sizes to appendix exploratory status.  
6. Clarify decision-family ground truth and discuss absolute performance, not only arm differences.  
7. Until human calibration exists, remove causal language about “semantic preservation effectiveness.”

---

## 11 Recommendation

**Reject**

(or **Major Revision** only if the venue explicitly accepts non-identified systems demos with a complete rewrite of claims). As an empirical governance-evaluation paper, the LangSmith+eval confound and unregistered multi-endpoint testing are fatal. A resubmission needs factorial identification, locked estimands, and shareable microdata.

---

## 12 Confidence

**0.86**
