# Interview Story — Cascade Failure Guardrail

**Author: Audrey Rah (Group 7) · Failure-mode package: `student_4_cascade`**

Malformed upstream state—an empty analysis payload without `paper_id`—caused the reporter path to throw `KeyError` and abort the run. Across twenty deterministic trials the unguarded downstream path crashed every time. I inserted an explicit sanitization node that checks invariants before reporting, converting those crashes into rollback responses that set a rejection flag for coordinator-driven recovery. After the guardrail, downstream crashes dropped to zero and rollback success reached one hundred percent on the same malformed inputs. Capturing crash counts and rollback rate in `metrics.md` made the failure mode interview-ready: validation is a hard gate that prevents one bad worker payload from cascading through the graph.
