# Peer Review — Reviewer 04

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**DOI:** 10.21203/rs.3.rs-10485157/v1  
**Author:** Audrey Rah / Rahimi  

---

## 1. Summary of the paper

The paper introduces semantic tracing: a measurement and control viewpoint in which multi-agent natural-language handoffs are treated as carriers of goals, constraint sets, evidence commitments, and escalation obligations. It specifies a handoff packet, a seven-class failure taxonomy (F1–F7), and a metric suite (SPS, AHF, IDR, TCS, TUA, GCR, HPR, HEP, WRS) with formulas (1)–(9). Empirically, a LangGraph-orchestrated LangChain agent pipeline with optional LangSmith spans is compared against a no-evaluation LLM condition inside a finished 450-run matrix. Reported aggregates include TCS 0.624 vs 0.912, latency ~126.2 s vs ~101.7 s, non-significant semantic-metric contrasts, and decision-family correctness 57/160 vs 59/160. SHADOWAI-RISK supplies the application context; human calibration of weights and labels is pending.

## 2. Major strengths

Formalizing the handoff as an explicit schema (Figure 3 / Figure 9) is the right abstraction boundary: fields for constraints, evidence identifiers, residual risk, permitted tools, and escalation state are closer to verifiable state than free-text chat logs. Distinguishing observability predicates (LangSmith spans) from semantic predicates (evaluation layer) and from decision predicates (Human Review Gate) is philosophically sound and uncommon. Equation-level attempts for SPS, IDR, HPR, and TCS show intent to move beyond slogan-level “guardrails.” Integrity rules in the Methodology section (no fabricated participant statistics; synthetic vs private traces labeled) indicate awareness of specification hygiene.

## 3. Major weaknesses

The work does not provide invariants, refinement relations, or completeness arguments for the failure taxonomy. F1–F7 are named and mapped loosely onto IDR/HPR/TUA/AHF/HEP, but there is no proof obligation of the form: every violation of sender intent or policy is detected by at least one metric, nor a counterexample suite establishing residual blind spots (e.g., paraphrastic constraint weakening that preserves set overlap, or temporally inconsistent evidence commitments).

Metric definitions are underspecified as mathematical objects. In (1), `Sim`, `EvidSupport`, and the weights α, β, γ are not given domains, computable instances, or calibration constraints beyond α+β+γ=1. In (3), `ScopeExpansion(Ih)` is undefined as a function. In (7), HPR’s denominator “unsupported claims introduced” lacks an identification procedure that is robust to duplicate claims and partial reuse. WRS (9) applies an unspecified `normalize` and unsettled weights—including “expert” weights never exhibited.

Without those precise definitions, empirical claims that SPS/AHF/IDR/TUA/GCR/HPR/HEP are “not significant” do not have a stable meaning, and governance mappings in Table 10 cannot be sound triggers.

## 4. Methodological concerns

**Specification versus implementation gap.** Section 9 presents continuous set-theoretic style metrics; the controlled prototype later encodes several quantities with ad hoc max/Boolean rules. A formal-methods reading treats this as two different systems. Which specification does the 160-run evaluator refine?

**Trace completeness as a coverage property.** TCS (4) is a set-cardinality ratio over `RequiredSpans`. The paper never axiomatizes `RequiredSpans` as a function of workflow type, nor states monotonicity/invariance properties under adding an evaluation subscriber. The observed TCS drop under evaluation strongly suggests the required set is not invariant to the treatment—i.e., the measurand is ill-typed as a comparative effectiveness endpoint.

**Failure-mode completeness.** Annotation guidance in Appendix F uses 0–2 rubrics for five dimensions, which do not biject with F1–F7. Escalation suppression (F7) versus contradiction (F6) need distinct observable predicates on packet sequences; those predicates are not written as temporal logic over hops h=0…H.

**Human gate.** Figure 17’s escalate/freeze/resume pathway is operationally described but not modeled (no state machine invariants such as “no terminal approve while unresolved mandatory escalation flag is true”). Table 6’s scenario outcomes hint such rules exist in code; they should be specified.

## 5. Statistical concerns

Statistics inherit definitional instability. Holm-corrected Mann–Whitney tests on n=160 cannot validate a metric that lacks a fixed interpretation function. Non-significance of SPS/IDR/HPR may indicate true absence of effect, coarse detectors, or weight settings that crush variance—undecidable pending calibration. Ablation SPS Cliff δ ≈ 0.5–0.625 on n=8 is not a substitute for metamorphic tests (constraint deletion must decrease SPS; unsupported claim reuse must increase HPR). Decision correctness 59/160 vs 57/160 is a separate property from semantic invariants; conflating transparency benefits with correctness is a category error the Discussion mostly avoids but the contribution list sometimes blurs.

## 6. Novelty assessment

Relative to classical multi-agent verification and recent LLM-agent failure taxonomies, the novelty lies in binding handoff packets to governance controls under NIST-style vocabulary. That is an applied specification contribution, not a verification contribution, until invariants and machine-checkable predicates appear. LangChain/LangGraph/LangSmith integration, while useful, is not formal novelty.

## 7. Technical correctness

Architectural claims separating LangSmith from scoring/decisions appear correct. Completeness of the 450/450 matrix is an execution claim, not a semantic correctness claim; the paper sometimes juxtaposes them too closely in abstracts. Example private trace IDs document existence of spans, not satisfaction of any invariant. Governance alignments (Figure 29) are correctly labeled interpretive; that honesty should extend to metric soundness claims.

Suspected incorrectness: treating uncalibrated WRS movements as reliability evidence; treating TCS differences as semantic-tracing success/failure without a treatment-invariant coverage spec; asserting seven failure classes “guide” metrics without a coverage lemma.

## 8. Reproducibility assessment

Formal reproducibility requires executable specs: packet grammar, predicates for F1–F7, metric reference implementation with fixed weights seed, and a conformance test suite. Those are not publicly available. Appendix C points to supplementary stubs and states weights are uncalibrated—appropriate disclosure, but it means numerical Table 5 cells are not reference-reproducible in the verification sense. Private LangSmith dependence further blocks independent checking of span predicates used by TCS.

## 9. Clarity and organization

Definitions are spread across Section 5.1, 5.3, Section 9, Appendix C, Appendix F, and prototype paragraphs near Table 6. A formal reader needs a single “Specification” section: syntax of packets, small-step workflow relation, observable predicates, metrics as functions of traces, and claimed properties (even if only conjectures). Figures 16 and 21 help conceptually but do not replace precise definitions. Equation typesetting and symbol glossaries should introduce every function before first use.

## 10. Suggested revisions

1. Provide a formal grammar for `LLMHandoffPacket` and a state machine for the Human Review Gate with explicit invariants.  
2. Define `Sim`, `EvidSupport`, `ScopeExpansion`, unsupported-claim identity, and `RequiredSpans` with algorithmic pseudocode and complexity notes.  
3. Publish fixed default weights for exploratory mode and separate “uncalibrated” labeling from any inferential headline.  
4. Prove or empirically stress-test taxonomy coverage: construct adversarial handoffs for each F-class and show metric response directionality (metamorphic relations).  
5. Re-specify TCS so required spans are identical across eval/no-eval arms; re-estimate Table 5 afterward.  
6. Align Appendix F rubrics with F1–F7 via an explicit encoding table.  
7. Move contribution language from “framework effectiveness” to “specification + uncalibrated instrumentation study” until Stage F completes.  
8. Add a limitations subsection on incompleteness of F1–F7 relative to prompt-injection and covert channel attacks mentioned only as future work.

## 11. Publication recommendation

Major Revision

## 12. Confidence score

0.84
