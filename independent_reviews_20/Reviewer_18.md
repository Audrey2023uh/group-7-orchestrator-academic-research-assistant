# Independent Peer Review — Reviewer 18

**Persona:** Algorithms and equations pedant / formal definitions  
**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems… (rs-10485157/v1)  
**Reviewed from:** local paper extract

## 1. Summary of the paper

The work defines semantic communication for multi-agent LLM workflows as transfer of goals, constraints, evidence commitments, uncertainty, and permitted actions such that downstream agents do not violate sender intent or policy. It operationalizes measurement via a handoff packet and a suite of scores, with Equations (1)–(9) purporting to formalize SPS, AHF, IDR, TCS, TUA, GCR, HPR, HEP, and WRS. Empirically, a 450-run matrix contrasts LLM workflows with and without a semantic evaluation layer (n=160 each), reporting TCS 0.624 vs 0.912 (Holm-adjusted p<0.001, Cliff’s δ≈−0.33), latency ~126.2 s vs ~101.7 s (large effect), nonsignificant SPS/AHF/IDR/TUA/GCR/HPR/HEP, and decision-family correctness 57/160 vs 59/160 (n.s.). Ablations (n=8) allegedly induce large SPS drops when constraints or evidence identifiers are removed. Human weight calibration remains pending; Appendix C states α, β, γ and WRS weights are not calibrated. I evaluate the paper primarily on whether the mathematics is well-defined, internally consistent, and faithfully connected to reported numbers.

## 2. Major strengths

Publishing explicit numerator/denominator style definitions for governance-oriented agent metrics is the right instinct. Table 4’s range and “higher/lower is better” polarity table is a useful orientation device. Figure 16’s intent-versus-hop comparison diagram correctly places Sim(I₀,Iₕ), constraint overlap, and unsupported-claim penalties in one visual pipeline before aggregation. Distinguishing LangSmith span capture from study-specific metric services (Section 5.2) is formally important: the observability substrate is not the measurand. The failure taxonomy F1–F7 mapped onto IDR/HPR/TUA/AHF/HEP shows an attempt at construct coverage rather than a single vague “quality” score.

## 3. Major weaknesses

The formal core is not publication-ready. Equation (1) for SPSₕ is typeset in the extract as a broken linear combination involving Sim(I₀,Iₕ), a constraint-set term written with an ambiguous operator on C(I₀) and C(Ih), and EvidSupport(Ih), with weights that “sum to one.” Missing are: the metric space and range of Sim; whether C(·) is a set and the term is Jaccard, precision, or set difference; the exact definition and range of EvidSupport; and whether SPSₕ is guaranteed in [0,1] after weighting. Equation (3) for IDR uses a clip_{[0,1]} around an average of terms that already mix complement-of-overlap with ScopeExpansion(Ih); ScopeExpansion is never formalized (signature, units, boundedness). Equation (4) for TCS is a set-cardinality ratio of ObservedRequiredSpans ∩ RequiredSpans over |RequiredSpans|, but the paper never specifies the RequiredSpans universe per condition—critical because TCS *falls* under the evaluation-enabled arm. Equation (7) for HPR is a ratio that is undefined when the denominator “# unsupported claims introduced” is zero; no convention is stated. After Table 6, “prototype scenario-level metric rules” redefine SPS as 1 or max(0,1−lost/|C₀|), IDR as lost/|C₀| or 0, HPR as a binary 0/1 flag—**different objects** from Equations (1), (3), and (7). Reporting Table 5 aggregates without stating which definition executed is a formal defect. WRS in Equation (9) subtracts IDR and HPR inside a normalize(·) whose domain and invertibility are unspecified; weights are uncalibrated yet WRS significance is claimed.

## 4. Methodological concerns

A metric paper must freeze an evaluation function M: Trace × PacketSequence → ℝ^k before runs. Here, Metric_Definitions_and_Calibration.md is cited but not inspectable in the extract; human annotation guidelines exist but IRR is pending; yet computational scores are already contrasted at n=160. That inverts the proper order: calibrate constructs, then estimate effects. Ablations that remove constraints and measure SPS drops are almost tautological if SPS *is defined* via constraint overlap—useful as a unit test of the implementation, weak as scientific evidence. Condition C changes both tracing metadata and evaluation logic; any TCS change is therefore not identifiable as “evaluation cost” versus “changed required span set.”

## 5. Statistical concerns

If SPS/IDR/HPR are mostly nonsignificant while TCS and latency move, the formal story may be that the evaluation layer primarily perturbs trace bookkeeping and runtime, not the semantic measurands named in the title. Cliff’s δ on TCS is medium; on latency large; on decision correctness negligible. Without CI and without a pre-registered primary endpoint, the abstract’s laundry list of metrics invites selective emphasis. Ablation δ in 0.5–0.625 on n=8 should be marked exploratory or removed from inferential claims. Holm correction needs an enumerated contrast list tied to Equations (1)–(9), not a verbal mention.

## 6. Novelty assessment

Formally, composite reliability indices (WRS) and handoff completeness scores resemble classical multi-criteria aggregation more than a new theorem. Novelty could arise from a proven relationship between packet invariants and governance error rates. That relationship is not established: semantic metrics n.s., decision correctness n.s. The naming of semantic tracing is fine; the mathematics does not yet earn a strong novelty claim.

## 7. Technical correctness

Concrete inconsistencies I require fixed:

- **SPS:** reconcile Equation (1) with post–Table-6 prototype rules; state α,β,γ numerical defaults used in the 450 runs or admit heuristic proxies.  
- **IDR:** define ScopeExpansion; prove IDR∈[0,1]; explain polarity versus SPS constraint term (they are algebraically related and may be near-collinear).  
- **HPR:** define “unsupported claim” detection algorithmically; handle zero denominators; reconcile binary prototype HPR with fractional Equation (7).  
- **TCS:** publish the RequiredSpans checklist for conditions B and C; explain the 0.912→0.624 drop as a change in observation, requirement set, or scorer bug.  
- **AHF:** Completeness×Validity product needs codomains {0,1} or [0,1] stated.  
- **TUA/GCR/HEP:** “correct,” “violation,” and “warranted” require decision procedures, not English glosses.  
- **Figure 16** should match the repaired equations symbol-for-symbol.

Until then, Table 5 cannot be treated as measuring the objects named in Section 9.

## 8. Reproducibility assessment

Appendix C points to machine-readable stubs in S3; code is “upon request.” For equation-centric work this is insufficient: I need a reference implementation that asserts SPS∈[0,1], unit tests for empty unsupported-claim sets, and a golden trace with hand-computed scores. Private LangSmith spans cannot be the sole ground truth for TCS if RequiredSpans depend on instrumentation flags.

## 9. Clarity and organization

Section 9 should be rewritten as Definition–Equation–Invariant–EdgeCases for each metric, then a single Implementation Note stating what the 450-run code actually computed. Move prototype rewrite rules next to the formal defs, not after a PASS table. Table 4 interpretations must match equation polarity (IDR/HPR lower-better vs others higher-better) in every results sentence.

## 10. Suggested revisions

1. Provide fully formal definitions for SPS, IDR, HPR, and TCS with domains, codomains, and undefined-case conventions.  
2. Eliminate dual operationalizations or label them Metric-Formal vs Metric-Prototype with separate result tables.  
3. Disclose numeric weights used for any reported WRS; if uncalibrated, do not claim inferential WRS results.  
4. Publish RequiredSpans and the TCS drop root-cause analysis.  
5. Add algebraic notes on dependence between SPS constraint terms and IDR.  
6. Supply reference pseudocode and three worked numerical examples aligned to Figure 16.  
7. Relegate tautological ablation SPS drops to appendix unit tests.

## 11. Publication recommendation

**Major Revision**

## 12. Confidence score

0.91
