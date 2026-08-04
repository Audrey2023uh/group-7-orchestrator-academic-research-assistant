# Peer Review — Reviewer 11

**Persona:** Bibliometrics / related-work completeness
**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance (Research Square rs-10485157/v1)

---

## 1. Summary

This preprint proposes “semantic tracing” as a first-class construct for measuring meaning preservation across natural-language handoffs in LLM-based multi-agent systems, implemented with LangChain, LangGraph, and LangSmith and anchored in the SHADOWAI-RISK governance prototype. The experimental matrix is reported as complete at 450/450 runs (deterministic 32, llm_no_eval 160, llm_langsmith_semantic_eval 160, variability 50, ablations 48) with zero terminal failures. Primary contrasts show lower Trace Completeness Score under evaluation (TCS 0.624 vs. 0.912; Holm-adjusted p < 0.001; Cliff’s δ ≈ −0.33), higher mean latency (~126.2 s vs. ~101.7 s; Cliff’s δ ≈ 0.67), significantly lower WRS under equal and expert weights (small effects), non-significant differences on SPS/AHF/IDR/TUA/GCR/HPR/HEP, and non-significant decision-family correctness (59/160 vs. 57/160). Human calibration, inter-rater agreement, surveys, and production integration remain pending.

From a bibliometric and related-work standpoint, the paper’s gap claim in Table 1 is ambitious: it asserts that no integrated framework treats meaning preservation as a measurand, binds it to LangSmith-style traces, maps failures to governance controls, and demonstrates the approach in an enterprise AI-risk context. That claim cannot be sustained without a more exhaustive, reproducible literature matrix than Section 4 and Appendix A currently provide. The empirical honesty about TCS drops, latency costs, and nonsignificant decision correctness is commendable, but the literature foundation is too thin relative to the novelty rhetoric.

## 2. Strengths

The manuscript is unusually transparent about what has and has not been validated. Table 8 and Table 9 correctly separate functionally verified components from pending semantic calibration and survey collection. Figure 21’s distinction between computational scores and pending human calibration is bibliographically useful as a claim-boundary device. The primary results in Table 5 and Figure 14/Figure 18 do not oversell decision accuracy: decision-family correctness is near chance and statistically indistinguishable across LLM conditions. Completing a 450/450 matrix with Holm-corrected Mann–Whitney reporting and Cliff’s δ effect sizes is more rigorous than many agent-system preprints that report only cherry-picked traces. The related-work structure in Table 1 at least attempts a strand-based synthesis (LLM multi-agent surveys, hallucination surveys, AgentOps/LangSmith, NIST/ISACA/EU/ENISA), which is preferable to an undifferentiated citation dump.

## 3. Weaknesses

The related-work section is the manuscript’s weakest scholarly pillar. Section 4 cites surveys (Guo et al.; Li et al.; Wang et al.), CAMEL, MetaGPT, AgentBench, Lost-in-the-Middle, Ji et al. on hallucination, Xia et al. on AgentOps, and a cluster of standards documents, yet the coverage of adjacent literatures is incomplete for a paper that claims a precise gap. Missing or under-engaged strands include: (i) conversation-state and dialogue-state tracking metrics from spoken dialogue systems and task-oriented dialogue; (ii) formal semantic fidelity / meaning-preservation measures from semantic communication and information theory beyond a passing framing; (iii) multi-agent communication protocols and ACL/FIPA-style commitment logics from classical MAS (beyond Wooldridge); (iv) LLM evaluation harnesses for agent trajectories (ToolBench, AgentBoard, GAIA, WebArena-style benchmarks, and failure taxonomies beyond Cemri et al. 2025); (v) MLOps/observability and distributed-tracing literature (OpenTelemetry semantic conventions, span-quality metrics) that already treat completeness of required spans—directly relevant to TCS Equation (4); (vi) Shadow IT / Shadow AI scholarship beyond Silic & Back (2014), including more recent empirical studies of unsanctioned generative-AI use; and (vii) assurance mapping papers that already attempt NIST AI RMF operationalization, which compete with the interpretive mapping in Table 10 and Figure 29.

Table 1’s “Unresolved for this study” column reads as advocacy rather than bibliometric synthesis. Declaring that AgentOps/LangSmith lack “semantic preservation scoring for governance” may be true for LangSmith specifically, but the claim that the intersection is empty requires systematic search evidence. Appendix A describes inclusion criteria and points to Supplementary File S1, yet the main text does not report PRISMA-style counts, years covered, databases queried beyond a short list, or inter-coder reliability for the literature matrix. Self-citation to the author’s other Research Square preprint (Ref. 22) and to the SHADOWAI-RISK artifact (Ref. 20) is fine if balanced; here it risks circular gap construction.

## 4. Methodological

Methodologically, Stages A–E (Section 7) are clear, and Figure 12’s mixed-methods diagram is intelligible. The three-condition separation in Figure 19 is methodologically important so that evaluation effects are not attributed to LangSmith alone. However, the literature-review methodology is underspecified relative to the rest of the paper’s procedural detail. Appendix A’s queries (“multi-agent LLM, agent observability, hallucination, AI risk management, AI Act, and NVD”) are too coarse to support the gap statement. There is no reported snowballing from Cemri et al., Xia et al., or AgentBench, no citation-network analysis, and no explicit exclusion log for borderline papers on agent evaluation metrics. For a bibliometrics-sensitive venue, Supplementary File S1 must be promoted into the main narrative with coverage statistics; otherwise the gap claim remains unfalsifiable.

## 5. Statistical

The statistical reporting of the completed matrix is comparatively careful: Holm correction, Mann–Whitney tests, Cliff’s δ, Fisher/χ² for decision-family correctness, and acknowledgment that ablations (n=8) are low-powered. The TCS drop (0.624 vs. 0.912) and latency increase (~126.2 s vs. ~101.7 s) are credible primary findings. Non-significance on the semantic suite and on decision correctness (59/160 vs. 57/160) correctly constrains causal claims about governance benefit. What is missing bibliometrically is comparison against prior reported effect sizes in agent-evaluation papers: without situating Cliff’s δ ≈ −0.33 (TCS) and ≈ 0.67 (latency) relative to published agent-ops benchmarks, readers cannot judge whether these magnitudes are novel or expected instrumentation artifacts. WRS numerical values are listed as NR in Table 5 despite significance claims—this is a reporting gap that also weakens meta-analytic reuse.

## 6. Novelty

The handoff-packet schema (Figure 3 / Figure 9) and the explicit binding of semantic metrics to enterprise AI-risk workflows are potentially novel as an integration package. Individually, however, multi-agent LLM surveys, hallucination-propagation concerns, LangSmith tracing, and NIST-aligned governance checklists are well-trodden. Novelty therefore hinges on the integrated claim in Table 1. Until the related-work matrix demonstrates that no prior system jointly (a) defines meaning-preservation measurands across hops, (b) instruments LangSmith-style traces, (c) maps metric failures to controls, and (d) evaluates them in an enterprise risk prototype with a completed quantitative matrix, the contribution should be framed as engineering synthesis plus provisional measurement, not as filling a uniquely empty niche. The pending human calibration further softens novelty: computational application of Equations (1)–(9) without annotated corpora is closer to a metric proposal than a validated measurement contribution.

## 7. Technical correctness

Reported numerical contrasts appear internally consistent across the abstract, Section 8, Table 5, and the discussion: TCS lower with eval, latency higher, decision correctness nonsignificant, 450/450 complete. The paper correctly states that LangSmith does not compute SPS/GCR (Figure 4, Figure 27, Table 3). Technical correctness issues relevant to literature claims include over-precise gap language, occasional broken cross-references (“Table ??”), and the risk that “semantic tracing” is used both as a conceptual contribution and as a brand for a LangChain-ecosystem case study. Shadow AI is treated as a motivating construct and as a scenario class; that dual use is fine if definitions cite contemporary literature more carefully than a single 2014 Shadow IT paper plus ENISA threat landscapes.

## 8. Reproducibility

Code availability “upon reasonable request,” private LangSmith project `semantic-tracing-shadowai`, and Supplementary Files S1–S4 are noted, but independent bibliometric reproduction of the gap claim is not currently possible from the main text alone. The literature matrix (S1) must be publicly inspectable with DOIs, inclusion/exclusion codes, and search dates. Experimental reproducibility of the 450/450 matrix is a separate issue: without released prompts, scenario JSON, and metric scripts, neither the empirical nor the bibliographic claims can be audited. Table 3’s code-path evidence is helpful for implementation claims but does not substitute for an open reproducibility package.

## 9. Clarity

The writing is generally clear and unusually candid about pending work. Figures 1, 6, 11, and 28 communicate research logic and contribution status well. Clarity suffers where related-work strands are summarized in Table 1 without citing the specific works that supposedly leave each cell unresolved. Readers cannot tell which “agent surveys” were judged insufficient or which “hallucination surveys” failed to address hop-wise propagation. Expanding Table 1 into a citation-backed coverage matrix would fix this.

## 10. Revisions

1. Expand Section 4 into a systematic related-work review with searchable databases, date ranges, hit counts, and inclusion/exclusion tallies; move the essential content of Supplementary File S1 into the main paper or an archival deposit with a persistent identifier.
2. Soften or qualify the Table 1 gap claim until coverage of dialogue-state tracking, OpenTelemetry/MLOps span metrics, agent trajectory benchmarks (beyond AgentBench), and recent Shadow AI empirical studies is demonstrated.
3. Add a bibliometric positioning paragraph that situates TCS and latency effect sizes against prior agent-observability evaluations.
4. Report WRS point estimates (currently NR in Table 5) and confidence intervals for all primary metrics to support future meta-analysis.
5. Reduce self-citation circularity; cite independent operationalizations of NIST AI RMF Measure/Govern when discussing Table 10 and Figure 29.
6. Fix broken table cross-references and ensure every “unresolved” cell in Table 1 names exemplar citations that were reviewed and judged insufficient.
7. Retain the honest reporting of nonsignificant decision correctness and pending human calibration; do not expand governance claims until the literature and calibration gaps are closed.

## 11. Recommendation

**Major Revision**

## 12. Confidence

**0.78**

The recommendation reflects high confidence that related-work incompleteness and an overstated gap claim are material defects, combined with moderate confidence in the empirical reporting of the 450/450 matrix based on the extract’s internal consistency. I am less certain about Supplementary File S1’s actual depth because it was not inspectable in the review package; if S1 already contains a rigorous coded matrix, the related-work critique may partially soften, but the main text would still need to surface that evidence.
