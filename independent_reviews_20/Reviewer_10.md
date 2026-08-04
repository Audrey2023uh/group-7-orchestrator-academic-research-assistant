# Peer Review — Reviewer 10

**Manuscript:** Semantic Tracing in LLM-Based Multi-Agent Systems Using LangChain, LangGraph, and LangSmith for AI Governance  
**Persona lens:** Performance engineering; latency, token cost, and production scalability

---

## 1 Summary

I assessed the manuscript as a systems-performance review: what does semantic tracing cost in wall-clock time, tokens, and architectural complexity, and can those costs scale beyond a local Ollama lab? The author’s own aggregates are the right starting point. Table 5 and Figure 18 show mean workflow latency rising from roughly 101.7 s without evaluation to roughly 126.2 s with LangSmith tracing plus semantic evaluation (Cliff’s δ ≈ 0.67, large), while token usage does not differ significantly and local monetary cost is $0 because models run locally. Decision-family correctness remains statistically indistinguishable (59/160 vs 57/160). In the smaller process comparison, Table 7 reports average runtime of ~0.0001 s for the deterministic baseline versus ~5.85 s for multi-agent-with-LangSmith on five scenarios—orders-of-magnitude slowdown before the larger LLM matrix latencies. Figure 11 clarifies that the experimental stack is not integrated into production. Taken together, the paper successfully surfaces a classic performance tradeoff—more observability and evaluation overhead without improving the decision KPI—but it does not characterize tail latency, concurrency, caching, batch evaluation, or capacity planning needed for enterprise deployment.

---

## 2 Major strengths

Logging latency, tokens, and cost as operational complements (Section 9) rather than pretending they are semantic fidelity measures is the correct performance-engineering posture. Completing 450 runs with resume-safe checkpointing (Figure 13) suggests the harness can survive long jobs—an underrated reliability property for expensive agent workflows. Separating LangGraph orchestration from LangChain calls and from rule-based evaluation (Figure 5) creates natural places to insert profilers and circuit breakers. The conclusion’s frank statement that multi-agent benefits come with higher latency and complexity, while deterministic SHADOWAI-RISK may suffice when only a final recommendation is required, matches how platform teams actually choose architectures.

---

## 3 Major weaknesses

Two-minute-class mean latencies for governance workflows are already problematic for interactive executive review; the paper reports means without p50/p95/p99, saturation curves, or per-node timing breakdowns (inventory vs evidence vs governance vs evaluation vs trace export). Non-significant token differences alongside +24 s mean latency imply the evaluation path spends time outside token generation—CPU-bound rule evaluation, synchronous LangSmith upload, JSON repair retries, or tool I/O—yet Figure 27 and related text never profile those components. Scalability to production is out of scope by admission (Table 8: not integrated; Vercel unchanged), but the governance implications section still recommends requiring tracing for multi-agent workflows without SLO guidance. Local $0 cost hides the true production cost model: hosted LLM APIs, LangSmith ingestion/retention pricing, NVD lookup rate limits, and human-gate wait time (Figure 17), none of which are modeled. Ablation and variability cells add matrix volume but little performance insight (no cost–quality Pareto frontier).

---

## 4 Methodological concerns

The experimental loop in Figure 13 prioritizes repetitions and statistical testing over performance counters. A performance methodology would fix scenario mix, warm up caches, pin model versions, measure span durations from Figure 10’s hierarchy, and report open-loop versus closed-loop (human gate) latency separately—human freeze time should not be conflated with machine latency if the gate blocks. Table 6’s multi-agent runtimes (~5–6.5 s) on short prototype scenarios are not reconciled with ~100 s means in the large matrix; readers need an explanation (model size, hop count, retries, live NVD, evaluation depth, tracing). Without that reconciliation, external validity of latency claims is shaky. There is no load test: 160 sequential runs ≠ concurrent tenants. Temperature variability experiments address output stochasticity, not throughput.

---

## 5 Statistical concerns

Cliff’s δ for latency is large and significant; that is useful. Absence of interval estimates and distributional plots for latency/tokens limits capacity planning. Pooling all scenarios may mask heavy-tailed scenarios (mandatory escalation, conflicting recommendations) that dominate SLOs—Figure 23’s perturbation set is ideal for stratified latency reporting but is not used that way in the extract. Claiming non-significant token differences requires power analysis: with high run-to-run variance, a true token burn from evaluation might be missed. WRS and TCS movements under the slower arm should be discussed as potential quality–cost tradeoffs, not only as semantic findings; lower TCS at higher latency is a particularly worrying operating point (pay more, observe less complete traces).

---

## 6 Novelty

Performance-wise, the paper does not introduce new scheduling, speculative execution, incremental evaluation, or trace sampling strategies. Its novelty is applied measurement in a governance agent pipeline. Relative to generic LangSmith usage notes, documenting a large latency penalty with flat decision accuracy is a practical contribution for engineers deciding whether to enable eval layers—if the measurement methodology were fuller. As-is, novelty is moderate and empirical rather than architectural.

---

## 7 Technical correctness

Using a local OpenAI-compatible Ollama endpoint (Section 10.2.1) correctly explains $0 API spend; readers must not generalize that to production budgets. Retry/repair chains via LangChain can amplify latency variance; the paper notes retries exist but does not quantify retry incidence—an important correctness gap for performance claims. Trace completeness falling under the eval-enabled arm (Table 5) may indicate dropped spans under load or scoring definitions sensitive to timing; either interpretation matters for reliability engineering and is underexplored. Deterministic baseline near-instant runtimes in Table 7 are believable for pure rule logic and correctly set the opportunity cost of agentification.

---

## 8 Reproducibility

Performance reproduction needs hardware specs, Ollama model tags, concurrent thread counts, whether LangSmith was reachable on every eval run, and raw latency vectors. Those are not in the preprint body. Figure 18’s summary graphic is not a substitute for releasing timing CSVs. Private tracing further complicates replication of any network-induced latency component. A public benchmark harness with one-command timing would do more for adoption than additional architecture figures.

---

## 9 Clarity/organization

Operational results are split across Table 5, Figure 18, Tables 6–7, and discussion paragraphs; a dedicated “Performance and cost” results subsection would help practitioners. Figure 5’s pipeline is clear enough to annotate with expected milliseconds per stage—doing so would improve engineering readability. Some tension remains between lab $0 cost and enterprise recommendation language elsewhere.

---

## 10 Suggested revisions

1. Report full latency distributions (p50/p95/p99) and per-node/per-span timings aligned to Figure 10.  
2. Break out evaluation-layer time, LangSmith export time, tool I/O, and LLM decode time; explain the ~100 s vs ~6 s regime gap.  
3. Add a production cost model (API tokens, tracing egress, storage retention, human-gate FTEs) even if lab cash cost is zero.  
4. Provide concurrency/load tests and failure behavior under LangSmith or NVD slowdowns.  
5. Plot accuracy/latency and TCS/latency tradeoffs; consider sampling or asynchronous evaluation to reclaim SLO headroom.  
6. Quantify `.with_retry` and repair-chain frequency as drivers of tail latency.  
7. Soften “require tracing” recommendations with explicit SLO classes (batch audit vs interactive review).

---

## 11 Recommendation

**Major Revision**

The latency–accuracy pattern is important and directionally credible, but production-relevant performance engineering is incomplete: missing tails, component attribution, cost modeling, and load behavior. Strengthen measurement and temper scalability claims; then the paper becomes useful to platform teams.

---

## 12 Confidence

**0.80**
