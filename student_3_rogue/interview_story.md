# Interview Story — Rogue Tool Guardrail

**Author: Audrey Rah (Group 7) · Failure-mode package: `student_3_rogue`**

While exercising the independent reviewer worker, I injected unauthorized tool names such as database deletion and trade execution, plus malformed allowlisted calls missing required arguments. With the middleware disabled, those names reached the tool runtime; dangerous implementations remain mocked so no real side effects occur, but the attempt path is still counted as an unsafe execution attempt. With the hardcoded allowlist I enabled, unauthorized tools raise `InvalidToolCallException` before dispatch, and incomplete argument sets are rejected as malformed. Metrics show blocked unauthorized calls, rejected malformed requests, and zero successful unsafe executions after the guardrail. This dynamic tool-call gate is the difference between a demo agent that can be socially engineered into harmful actions and a production worker with an enforceable capability boundary.
