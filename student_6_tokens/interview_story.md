# Interview Story — Token Burn Guardrail

**Author: Audrey Rah (Group 7) · Failure-mode package: `student_6_tokens`**

Running twenty isolated reviewers naively accumulates every prior review and tool dump into a shared message list, exploding approximate token counts and slowing context assembly. I simulated twenty full reviewer outputs plus tool payloads and measured several thousand approximate tokens with higher concatenation latency. I then added a context-management node that counts tokens, summarizes older messages, prunes redundant tool output, and preserves critical structured identifiers. After pruning, token counts dropped by well over half and latency for assembling the active context declined, while reviewer isolation still keeps each Worker B run free of peer reviews. Those measured reductions are checked into `metrics.md`, turning an abstract context-window risk into an operational budget control for long multi-agent jobs.
