# Peer Review — Reviewer 02

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**DOI:** 10.21203/rs.3.rs-10485157/v1  
**Author:** Audrey Rah / Rahimi  

---

## 1. Summary of the paper

The author describes a laboratory comparison of LLM multi-agent governance workflows with and without a semantic-evaluation overlay, plus a deterministic SHADOWAI-RISK-derived baseline. Instrumentation relies on LangChain/LangGraph execution and optional LangSmith spans. Outcomes include Trace Completeness Score, Workflow Reliability Score variants, a battery of semantic/governance rates (SPS, AHF, IDR, TUA, GCR, HPR, HEP), latency, tokens, cost, and decision-family correctness. The headline matrix is 450 completed runs. The abstract and Table 5 emphasize Holm-adjusted Mann–Whitney contrasts on n=160 per primary LLM arm: TCS 0.624 versus 0.912; latency about 126.2 s versus 101.7 s; decision correctness 57/160 versus 59/160 with Fisher/χ² non-significance; several semantic metrics non-significant; human annotation still pending.

## 2. Major strengths

Reporting of null decision-correctness findings alongside significant process metrics is scientifically preferable to selective emphasis on architecture diagrams alone. Use of Cliff’s δ with directional interpretation for TCS and latency is more informative than p-values in isolation. The manuscript acknowledges low power for ablations (n=8) and states that human calibration has not occurred—statements that, if enforced in the interpretation, would prevent overclaiming.

## 3. Major weaknesses

This manuscript does not meet a serious experimental-design bar for confirmatory inference. The design confounds the evaluation layer with tracing configuration, scenario perturbation structure, and stochastic LLM behavior without an adequately pre-specified estimand. “Complete:true” for 450/450 runs is an engineering completion metric, not evidence of statistical adequacy, balance, or unbiased missingness handling.

Most critically, the metrics that supposedly justify the paper’s title—semantic preservation and drift—are uncalibrated against human judgments, while the statistically strongest effects (TCS ↓, latency ↑) are operational/process endpoints that may be mechanically induced by how “required spans” are defined when evaluation is enabled. Decision-family correctness—arguably the clinically relevant analogue for governance—shows no difference. Publishing a governance-effectiveness narrative on that pattern would be premature.

## 4. Methodological concerns

**Unit of analysis and dependence.** Workflows sharing scenarios, prompts, and model checkpoints are unlikely to be independent Bernoulli or continuous observations. Treating 160+160 runs as independent Mann–Whitney samples without clustering by scenario, seed group, or temperature cell inflates Type I error. Figure 13’s experimental loop mentions repetitions and variability, but the primary analysis description does not present mixed models, GEE, or scenario-stratified tests.

**Condition construction.** Deterministic 32, llm_no_eval 160, llm_langsmith_semantic_eval 160, variability 50, and ablations 48 are heterogeneous buckets. Pooling rhetoric around “450/450” obscures that inferential claims rest on a subset. The deterministic arm is not integrated into the primary inferential contrast in Table 5, so baseline comparative effectiveness remains largely descriptive (Tables 6–7, n=5 scenarios).

**Outcome multiplicity without a locked primary endpoint.** SPS, AHF, IDR, TUA, GCR, HPR, HEP, two WRS weightings, TCS, latency, tokens, and correctness constitute a large family. Holm adjustment is mentioned for primary eval versus no-eval contrasts, yet the abstract still foregrounds a favorite significant pattern (TCS) while listing a string of non-significant semantic metrics. That is compatible with selective spotlighting.

**Ablations.** n=8 with Cliff’s δ of 0.5–0.625 for SPS drops after removing constraints/evidence identifiers is anecdotal. No confidence intervals, no power calculation, no multiple-comparison control specific to the ablation family.

## 5. Statistical concerns

1. **No a priori power analysis** for detecting differences in decision correctness. With ~36% correctness in both arms (59/160 vs 57/160), the study is underpowered for modest absolute improvements; p≈0.91 is unsurprising and should not be spun as “equivalence.” Equivalence testing (TOST) was not performed.

2. **Mann–Whitney + Holm** on many endpoints does not replace reporting of medians/IQRs, exact δ confidence intervals, or robustness checks under scenario clustering.

3. **WRS “significant, small effect” with NR point estimates** in Table 5 is unacceptable for a results table. Effects without magnitudes invite interpretation shopping.

4. **TCS 0.912 vs 0.624** needs a measurement model: if evaluation injects additional required fields/spans, lower TCS can be a definitional artifact. Construct confounding of the endpoint with the treatment is a fatal design flaw unless disproved.

5. **Temperature variability (50 runs)** and stochastic LLM error structures are mentioned but not modeled; variance components are absent.

6. **Fisher/χ² for correctness** should state whether the decision-family taxonomy was pre-registered and whether expected labels differ by condition (Table 6 suggests condition-specific expected mappings in the toy scenarios—dangerous if carried into the large matrix).

7. Pending human calibration means the semantic endpoints have **unknown reliability**; inferential statements about SPS/IDR/HPR nullity are not scientifically interpretable as absence of semantic effect.

## 6. Novelty assessment

As an applied systems write-up, the LangChain/LangGraph/LangSmith integration around SHADOWAI-RISK is not empty. As a statistical contribution to evaluating multi-agent governance, novelty is thin: the paper does not introduce a validated measurement instrument, a causal identification strategy, or a benchmark with human gold labels. Novelty claims hinging on “first integrated framework” are overstated while Stage F data remain absent.

## 7. Technical correctness

Arithmetic presentation of 59/160 and 57/160 as ~0.369 and ~0.356 is fine. Holm-adjusted p<0.001 for TCS is not independently verifiable without raw vectors. Conceptual risk of incorrect causal attribution (evaluation “causes” lower completeness) is high. Prototype metric rules adjacent to Table 6 (binary HPR/GCR-style encodings) appear inconsistent with continuous equations (1)–(8); if those rules leaked into any aggregate, technical correctness of Section 10 is compromised.

## 8. Reproducibility assessment

Without public microdata, analysis scripts, random seeds, and a SAP (statistical analysis plan), the inferential results are not reproducible. Private LangSmith project identifiers do not substitute for analysis datasets. Supplementary metric stubs (S3) are not a substitute for the locked code that produced Table 5.

## 9. Clarity and organization

Empirically relevant material is scattered across Section 8, Section 10.3, Table 5, Figure 14, Figure 18, and a separate n=5 walkthrough. A biostatistical reader must hunt for the analysis set, exclusion rules, and multiplicity plan. The paper would be clearer if it contained a CONSORT-like diagram for runs, a single primary endpoint declaration, and a dedicated statistical methods subsection with software, tests, and multiplicity controls.

## 10. Suggested revisions

1. Write and adhere to a statistical analysis plan: primary endpoint, secondary endpoints, clustering level, multiplicity procedure, and missing-data rules.  
2. Re-analyze with scenario-level hierarchical models; report ICC and cluster-robust inferences.  
3. Provide full descriptive tables (median, IQR, mean, SD) and Cliff’s δ CIs for all primary endpoints; fill NR WRS cells.  
4. Test whether TCS definitions differ by arm; if so, redefine TCS to be treatment-invariant or drop it as a causal endpoint.  
5. Conduct equivalence or superiority tests for decision correctness with justified margins; stop implying practical parity from p≈0.91 alone.  
6. Defer confirmatory claims on SPS/IDR/HPR/WRS until annotated corpora and reliability (κ/ICC) exist; move uncalibrated scores to exploratory.  
7. Power the ablation study or remove effect-size language for n=8.  
8. Release anonymized run-level CSV and analysis code.

## 11. Publication recommendation

Reject

## 12. Confidence score

0.92
