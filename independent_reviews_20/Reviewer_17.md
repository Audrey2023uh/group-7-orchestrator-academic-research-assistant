# Independent Peer Review — Reviewer 17

**Persona:** Clarity and scientific-writing editor (ESL-aware)  
**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems… (Research Square rs-10485157/v1)  
**Source:** `data/paper_extract.txt`

## 1. Summary of the paper

This preprint argues that observability traces alone do not answer the enterprise governance question of whether multi-agent LLM workflows preserved goals, constraints, and evidence commitments across hops. It introduces a semantic-tracing framing, a handoff-packet schema, a metric suite (SPS, AHF, IDR, TCS, TUA, GCR, HPR, HEP, WRS), and a mixed-methods staged plan (Stages A–G). Empirically, the author reports a finished 450-run matrix contrasting deterministic agents with LLM agents without evaluation and LLM agents with LangSmith plus a rule-based semantic evaluator. Numerically, evaluation-enabled runs show lower TCS (0.624 vs 0.912), higher mean latency (~126.2 s vs ~101.7 s), nonsignificant differences on most semantic metrics, and similar decision-family correctness (~36%). A live SHADOWAI-RISK site anchors the case narrative; the multi-agent extension remains local and non-integrated. Human annotation, surveys, and production integration are still pending. The conclusion wisely stresses transparency over decision superiority—language that should be mirrored everywhere else in the manuscript.

## 2. Major strengths

From an editorial standpoint, the author often self-corrects in ways many submissions do not: Figure 15 is labeled conceptual (not a screenshot); Figure 29 separates authoritative requirements from interpretive mappings; Section 13 inventories threats to validity honestly. ESL-related surface noise (broken hyphenation, “?” glyph substitutions for en-dashes and Greek letters in the extract) does not obscure the scientific story when the story is told once. The layered figures that *do* work—especially Figure 5’s pipeline and Figure 8’s approve/restrict/monitor/escalate branches with remediate marked proposed—help non-specialist readers. Table 2’s research questions give the paper a spine that editors can use to demand answerability.

## 3. Major weaknesses

Figure overload is the dominant clarity failure. The extract references Figures 1 through 29 plus Appendix Figure J1—far beyond what a single article can teach. Many panels restate the same architecture (Figures 2, 5, 6, 7, 11, 19, 20, 22, 27) with slight redraws. Readers cannot hold a stable mental model when every section re-introduces the stack. Equally damaging is contradictory status language: abstract and Section 5.4 celebrate `complete:true` and “aggregate numerical… results,” while Table 8 says semantic metrics are “Pending semantic validation / Not calculated from annotated corpora,” and Table 9 lists controlled experiments as “Partially collected (functional)” with “semantic metrics still pending.” A careful ESL reader will ask which sentence to trust. Broken cross-references (“Table ??” appears at least twice) communicate unfinished manuscript hygiene. Contribution bullets C1–C8 sound finished; Stage F/G language sounds unfinished. That contradiction is editorial, not merely statistical.

## 4. Methodological concerns

Method prose is staged (A–G) but the reader is not given a single status ledger table that lists each stage as done / partial / pending with one verb tense throughout. Figure 12’s mixed-methods diagram promises qualitative–quantitative joining “at validation,” yet validation strands (IRR, surveys) are pending—so the figure currently overpromises process completion. Scenario vocabulary drifts among “~30 controlled scenarios,” five laboratory scenarios in Section 10.3, and Appendix K’s S1–S4 list plus a note that additional large-scale scenarios “remain pending,” which collides with 450/450 completeness wording. For clarity, methods must freeze a glossary: scenario set size, repetition rule, and what “complete” means (run execution vs metric calibration).

## 5. Statistical concerns

Editors need parallel structure in results tables. Table 5 reports TCS with means, Holm p, Cliff’s δ, and interpretation, then reports WRS as “NR” while still saying “Significant… Small.” That is unreadable and looks like placeholder residue. Figure 14 and Figure 18 both visualize “primary outcomes” with overlapping messages (TCS/latency vs decision correctness); pick one primary results figure and demote the other. Decision-family correctness 57/160 vs 59/160 should be written once with a clear definition of “family,” not restated with swapped order (abstract vs body) without explanation. Ablation caveats are present but buried; move them beside any ablation claim in the same paragraph.

## 6. Novelty assessment

Conceptually, “semantic tracing” as a named construct is communicable and potentially memorable. Relative to AgentOps and existing tracing docs, the novelty for readers is the governance binding and handoff packet—not the twenty-ninth architecture diagram. Novelty will land only if the writing stops repeating framework brand names in titles, keywords, and every section heading and instead foregrounds the measurand and the evidence limits.

## 7. Technical correctness

I flag correctness issues that are also clarity issues. Prototype metric rules after Table 6 redefine SPS/IDR in drift-flag form that does not obviously equal Equations (1) and (3). Readers cannot know which definition produced Table 5. TCS interpretation text says higher is better, yet the evaluation arm is lower—explain mechanism in one plain paragraph. “Decision accuracy 1.0” in Table 7 versus ~0.36 decision-family correctness in Table 5 will be read as an error unless the different denominators and label ontologies are taught explicitly.

## 8. Reproducibility assessment

Clarity of availability statements matters. “Upon reasonable request,” private project names, and a machine-local Windows path in Section 5.4 are not reproducible communication. Supplementary Files S1–S5 are named; the extract does not show them. Tell readers exactly what they can download today versus what is author-held. Figure 10’s real private trace ID is useful documentation but not a substitute for a redacted public example.

## 9. Clarity and organization

Recommended structure for revision: (1) Problem and gap (short); (2) Construct and metrics (one figure); (3) System and what is implemented vs proposed (one figure + one table); (4) Experimental design (one figure); (5) Results (Table 5 + one plot); (6) Micro-case optional; (7) Limitations; (8) Interpretive governance map. Merge duplicate architecture figures. Normalize tense: completed runs vs pending calibration. Fix OCR/export artifacts (?, missing letters in “Tracing,” broken formulas in the text extract) before camera-ready. Soften title: the triple framework branding in the title forces product-adjacent reading; a measurand-first title would serve international audiences better. Avoid synonym churn (“semantic preservation,” “meaning preservation,” “handoff fidelity,” “process transparency”) without a one-time glossary.

## 10. Suggested revisions

1. Cut figure count aggressively; retain Fig. 1 (logic), one architecture, Fig. 13 or 19 (design), Fig. 14 or 18 (results), Fig. 21 (calibration boundary), Fig. 29 (interpretive map).  
2. Insert a one-page Status Ledger replacing contradictory complete/pending sentences.  
3. Repair all “Table ??” references; unify abstract vs Table 5 ordering of 57/160 and 59/160.  
4. Add a glossary box for SPS/IDR/HPR/TCS and for decision-family labels.  
5. Move repeated 450/450 boilerplate to a single Methods subsection; cite it elsewhere.  
6. ESL polish pass for article use, parallel headings, and consistent capitalization of metric names.  
7. Align conclusion language with abstract: transparency benefit, latency cost, no decision superiority, calibration pending.

## 11. Publication recommendation

**Major Revision**

## 12. Confidence score

0.84
