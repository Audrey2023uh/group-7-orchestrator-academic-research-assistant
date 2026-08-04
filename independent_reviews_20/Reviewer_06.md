# Peer Review — Reviewer 06

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**Persona lens:** Security & privacy; telemetry and PII exposure risk

---

## 1 Summary

This manuscript proposes “semantic tracing” as a governance measurand for LLM multi-agent handoffs, tying structured packets and rule-based scores to a LangChain/LangGraph prototype and optional LangSmith observability, demonstrated against the SHADOWAI-RISK academic risk workflow. The author reports a completed 450-run matrix and contrasts LLM runs with versus without an evaluation layer. From a security and privacy standpoint, the contribution is less the metric algebra than the decision to route operational traces—including agent roles, policy identifiers, evidence sources, and hop indices—through a third-party cloud tracing service. Appendix E explicitly configures `LANGSMITH_API_KEY` and a named private project; Figure 10 documents a live root span identifier. Those choices place proprietary governance context, vulnerability-linked inventory signals, and potentially organization-identifying scenario content on an external observability plane. The paper acknowledges privacy-oriented redaction in Appendix I but does not treat cloud telemetry as a first-order threat model. I therefore read the work as an observability design paper that under-specifies confidentiality, residency, retention, and leakage paths for the very audit artifacts it asks enterprises to generate.

---

## 2 Major strengths

The manuscript is unusually candid that LangSmith does not compute SPS, GCR, or governance decisions; Table 3 and the surrounding text keep orchestration, reasoning, safeguards, tracing, evaluation, and human decision as separate responsibilities. That separation reduces a common vendor-conflation risk and helps security reviewers locate trust boundaries. The failure taxonomy (F1–F7) and handoff packet fields give concrete hooks for detecting unauthorized scope expansion and escalation suppression—failure modes that matter for Shadow AI and policy bypass. Table 8’s insistence that production Vercel assets were untouched is also a positive operational hygiene signal: the experiment did not silently enlarge the live attack surface of the deployed prototype.

---

## 3 Major weaknesses

Cloud tracing is treated primarily as an engineering convenience rather than a data-exfiltration channel. Figure 10 presents a verified private LangSmith pattern plus local JSON export, yet the security discussion never answers who can read spans, how long they persist, whether prompt contents and tool returns are stored verbatim, or how cross-tenant isolation is verified. Recommended metadata tags (`agent_role`, `hop_index`, `policy_id`, `tool_name`, `evidence_source`, `human_gate`) are useful for governance and simultaneously constitute a high-signal dossier if leaked. Appendix I advises avoiding secrets in traces and publishing only redacted examples, but the main results sections celebrate private cloud spans (including an example root trace ID) without a threat model, DPIA-style inventory of fields, or a local-only default architecture. For a paper that markets itself toward NIST/ENISA-aligned AI risk practice, this is a material omission: governance telemetry that leaks PII, CVE-linked asset context, or internal policy identifiers can create more risk than the Shadow AI problem it aims to illuminate.

---

## 4 Methodological concerns

Instrumentation methodology couples “optional private LangSmith” with the evaluation-enabled condition in ways that make it hard to separate observability side effects from evaluation logic—relevant not only for causal claims but for security testing, because enabling tracing changes what leaves the host. The pipeline in Figure 4 ends in governance alerting; if alerts and span payloads share the same cloud path, compromise of the tracing project becomes a control-plane failure. There is no adversarial evaluation of prompt injection into handoffs that could cause agents to embed credentials or customer identifiers into logged fields (future work mentions injection only briefly). Live NVD lookups in the Evidence agent expand the external dependency set; the paper does not discuss whether request logs or returned CVE payloads are mirrored into LangSmith spans. A security-minded methods section should specify field-level allow/deny lists for export, encryption at rest expectations, and a local span sink that never leaves the organizational boundary.

---

## 5 Statistical concerns

I am not primarily evaluating inferential design, but the privacy posture interacts with statistics: Table 5 reports TCS dropping from 0.912 to 0.624 under the evaluation-enabled (LangSmith-linked) condition. If completeness scoring depends on cloud-observed required spans, then network, credential, or export failures become confounded with “semantic evaluation” effects, and organizations may be pressured to keep cloud tracing always-on to protect metric validity—an unhealthy incentive from a data-minimization perspective. Decision-family correctness near 36% with non-significant differences does not justify expanding the blast radius of stored traces. Latency inflation (~101.7 s to ~126.2 s) is reported; the security cost of that extra dwell time for sensitive payloads in transit and at rest is not discussed.

---

## 6 Novelty

Binding meaning-preservation metrics to enterprise AI inventory/risk workflows is a plausible niche relative to generic AgentOps surveys. However, novelty on the security axis is limited: using LangSmith for spans, exporting JSON locally, and asserting private projects does not advance confidential observability, confidential computing for traces, or privacy-preserving audit logs. The interpretive Table 10 mapping (e.g., low TCS to EU AI Act transparency expectations) risks implying that more logging equals better compliance, without reconciling GDPR/data-minimization tensions inherent in rich multi-agent telemetry.

---

## 7 Technical correctness

Within stated bounds, the architectural claims about who decides what appear carefully worded and consistent with Table 3. The example trace ID and project name in Figure 10 / Table 8 are presented as real private instrumentation rather than mocked screenshots, which is ethically preferable to fabricating UI evidence. Correctness gaps appear in the security narrative: calling traces “private” is not equivalent to demonstrating non-exfiltration, key rotation, least-privilege API keys, or deletion SLAs. Appendix E’s environment-variable recipe is operationally accurate for enabling LangSmith and simultaneously a ready-made misconfiguration guide if copied into production without secret management. Code availability “upon reasonable request” further weakens independent verification of redaction and tracing wrappers in `workflow/tracing.py`.

---

## 8 Reproducibility

A third party cannot reproduce the cloud-trace claims without the author’s LangSmith credentials and project. Local JSON traces are said to exist under `outputs/local_traces/`, but the manuscript does not ship a public, redacted corpus with a documented schema and PII scrubbing report. Supplementary File S3 is referenced for configs, yet the Code Availability statement keeps the experimental repository gated. For security replication, reviewers need at minimum: (i) a local OpenTelemetry-style sink option; (ii) a published redaction policy with before/after examples; (iii) a data-flow diagram showing which fields never leave localhost. Those artifacts are not part of the reviewable package.

---

## 9 Clarity/organization

The paper is long and figure-heavy; security-relevant material is scattered across Appendix E, Appendix I, Table 9 (pending redacted production traces), and Figure 10. A dedicated “Telemetry threat model” subsection in the main text would help practitioners. Distinguishing proposed versus implemented components (Figures 6–7) is generally clear. Occasional tension remains between celebrating completed cloud spans and listing production redacted traces as pending in Table 9.

---

## 10 Suggested revisions

1. Add an explicit threat model for LangSmith and local exports: confidentiality, integrity, availability, insider access, and supply-chain risk of the tracing vendor.  
2. Default the architecture to local-only span capture; treat cloud export as an opt-in with DLP controls, field allowlists, and retention limits.  
3. Publish a redaction specification and a scrubbed sample of both JSON traces and any cloud-exportable metadata; remove or further de-identify live trace IDs if they could aid account correlation.  
4. Document whether prompts, tool outputs, organization profile fields, and CVE-linked inventory strings are stored in spans; if yes, justify necessity under data minimization.  
5. Separate security evaluation (attempted secret leakage, injection into logged fields) from semantic metric evaluation.  
6. Replace “upon reasonable request” code access with a public repository for tracing wrappers and evaluation code, even if scenario data remain synthetic.  
7. Soften compliance-adjacent language in Table 10 so that richer logging is not read as a substitute for privacy engineering.

---

## 11 Recommendation

**Major Revision**

The governance motivation and role separation are useful, but a paper that centers LangSmith cloud tracing for enterprise AI risk cannot treat privacy and telemetry leakage as appendix afterthoughts. Address the threat model, data minimization, and local-default observability before the work is suitable as governance guidance.

---

## 12 Confidence

**0.78**
