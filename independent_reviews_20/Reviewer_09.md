# Peer Review — Reviewer 09

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**Persona lens:** Open science; FAIR data, preregistration, and artifact availability

---

## 1 Summary

This Research Square preprint describes a semantic-tracing construct, a metric suite, and a local multi-agent experiment linked to the SHADOWAI-RISK prototype, culminating in a claimed complete 450-run matrix and aggregate contrasts. My review focuses on whether readers can Find, Access, Interoperate, and Reuse the evidence behind those claims. Table 9 is unusually revealing: survey responses pending; redacted production LangSmith traces pending; semantic metric cohort statistics pending; controlled multi-agent experiments listed as only partially collected for functional aspects while the abstract simultaneously trumpets 450/450 completion. Code Availability states source code is available from the corresponding author upon reasonable request—not a DOI-minted archive, not a public commit hash, not a license-clear reproduction package mirrored with the preprint. Supplementary Files S1–S5 are enumerated in Appendix L, but the review package I am assessing does not demonstrate that those files are openly deposited with persistent identifiers. On open-science grounds, the manuscript currently asks the community to trust closed artifacts for its strongest quantitative statements.

---

## 2 Major strengths

The author articulates integrity rules against inventing participant statistics and against presenting conceptual diagrams as empirical screenshots (Figure 15’s explicit caveat). Distinguishing implemented, experimental, and proposed components across Figures 6–11 is aligned with transparent reporting. Listing verification items in Table 8 (unit tests passed: 2; production integration: not done; semantic metrics pending annotated corpora) models the kind of status table FAIR advocates want, even when the answers are disappointing. Citation hygiene claims (DOI/official-URL verification; References_Verification.xlsx mentioned in Appendix I) show awareness of bibliographic reproducibility. The Creative Commons license on the preprint is a positive default for the text itself.

---

## 3 Major weaknesses

Reasonable-request code access is incompatible with the paper’s reproducibility rhetoric and with Supplementary File S3’s implied promise of a Reproducibility_Package. Private LangSmith project `semantic-tracing-shadowai` and a concrete root trace ID appear in Figure 10 and Table 8, yet Table 9 still marks redacted production traces as pending—leaving the only celebrated cloud evidence non-reusable by readers. There is no preregistration (OSF/AsPredicted/Registered Report) of the 450-run design, primary endpoints, or Holm procedure despite RQ6 explicitly asking what evaluation protocol supports reproducible assessment prior to data collection. Machine-readable metric stubs are said to live in S3 (`metric_definitions.md`), but without a public deposit, Equations (1)–(9) remain prose. Local path references to a personal OneDrive experimental directory in Section 5.4 are anti-FAIR and non-portable. For a governance paper that tells organizations to require tracing and sampleable audit artifacts, failing to publish its own sampleable artifacts is a serious normative inconsistency.

---

## 4 Methodological concerns

Open methodology requires frozen scenario definitions, prompt templates, and scoring scripts at analysis time. Appendix K sketches S1–S4 and points to five controlled prototype scenarios, while Section 8 describes ≥30 scenarios and mild/moderate/severe drift—yet no public scenario bank with versioning is cited by DOI. Figure 12’s mixed-methods diagram includes survey and annotation strands that Table 9 marks pending; reporting “results” from Stages D/E while Stage F/G data do not exist should trigger a clearer “computational pilot only” banner in title/abstract. Ablation and variability subsets are counted in the 450 total, but without an open codebook mapping each run to condition tags (`deterministic`, `llm_no_eval`, `llm_langsmith_semantic_eval`, etc.), external auditors cannot verify the denominator. “Complete:true” is an internal engineering flag, not a community-verifiable checksum of released data.

---

## 5 Statistical concerns

From a reproducibility standpoint, Table 5’s inferential claims (Holm-adjusted p-values, Cliff’s δ, Fisher/χ²) are not auditable without run-level outcomes. NR (not separately reported) for WRS point estimates while still declaring significance is especially problematic for reuse: effect direction is stated without exportable sufficient statistics. Pending inter-rater agreement means any future SPS/IDR/HPR human labels cannot be compared to a locked computational baseline unless that baseline is archived now. I recommend treating all inferential language as provisional until a data package with analysis scripts passes a third-party reproduction.

---

## 6 Novelty

Open-science novelty is absent: the work does not contribute a public benchmark, a registered protocol, or a FAIR trace corpus for multi-agent governance. Substantive topical novelty (semantic preservation as measurand in an AI inventory risk tool) could be real, but novelty that cannot be inspected collapses to an unverifiable claim. Figure 28’s contribution-to-validation mapping would be more persuasive if each “output” cell linked to an archived artifact URL.

---

## 7 Technical correctness

I do not dispute that the author likely ran local experiments; Table 8’s functional checklist is internally coherent. Correctness in the scholarly sense—correspondence between claims and inspectable evidence—is weak. Example: abstract asserts full matrix completion and primary contrasts, while Table 9 still describes controlled experiments as partially collected and semantic cohort statistics as pending. That tension needs reconciliation, not more adjectives. Interpretive mappings in Figure 29 / Table 10 are appropriately caveated as non-certification; similar humility should apply to unreproducible p-values.

---

## 8 Reproducibility

This is the decisive axis for my review. Blockers include: (1) code upon request; (2) private traces without a redacted public subset; (3) no dataset DOI for the 450-run results; (4) no preregistration; (5) environment pinned only loosely via `requirements.txt` claims in Table 3 without a lockfile hash in the preprint; (6) live prototype URL for SHADOWAI-RISK does not substitute for the experimental extension’s source. Appendix L’s S1–S5 list is a promissory note. Until deposits exist, independent researchers cannot confirm TCS 0.624 vs 0.912, latency distributions, or even that 0 terminal failures is accurate.

---

## 9 Clarity/organization

Status fragmentation across abstract, Section 10.5, Table 8, and Table 9 forces readers to cross-examine the paper to learn what is actually shareable. A single “Data and code availability” subsection with persistent links—or explicit “not yet deposited” statements—would improve honesty and clarity. Otherwise the writing quality is adequate; the organization problem is evidentiary, not merely stylistic.

---

## 10 Suggested revisions

1. Deposit code, configs, prompts, and metric scripts in a public archive (Zenodo/Software Heritage) with DOI and license; cite commit hash in the manuscript.  
2. Release a redacted run-level dataset sufficient to reproduce Table 5 and Figure 14/18 summaries.  
3. Preregister any subsequent calibration/annotation study; retrospectively document the 450-run plan as exploratory if it was not preregistered.  
4. Replace OneDrive-local path citations with repository-relative paths.  
5. Align abstract and Table 9 so “pending” items cannot be mistaken for completed empirical validation.  
6. Publish Supplementary S1–S5 with the preprint or mark them unavailable.  
7. Add a reproducibility checklist (seeds, model versions, Ollama tags, hardware).  

Without (1)–(2) at minimum, I do not support acceptance-track outcomes.

---

## 11 Recommendation

**Reject**

The governance and metric ideas may deserve a future open release, but the present preprint’s quantitative claims are not FAIR-verifiable. Closed code, private traces, pending cohorts, and no preregistration are disqualifying for an evidence-based methods contribution. I would reconsider after public archival of code and run-level data with reconciled reporting.

---

## 12 Confidence

**0.88**
