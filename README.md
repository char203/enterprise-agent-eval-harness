# Enterprise LLM Evaluation Harness

A reproducible evaluation harness for testing enterprise AI agent behavior using **Inspect AI**, **Ollama**, and **Qwen3**.

The project evaluates whether an LLM can make policy-grounded customer support decisions across security, billing, access, privacy, and product-support scenarios.

## Results

| Version | Evaluation | Accuracy | Total Tokens | Runtime |
|---|---|---:|---:|---:|
| V1 | 3-case constrained baseline | 100% | 1,824 | 37s |
| V2 | 24-case expanded benchmark | 54.2% | 27,466 | 20m 19s |
| V3 | 24-case + policy grounding | **75.0%** | 42,392 | 36m 34s |

Expanding the benchmark from 3 to 24 cases exposed a generalization failure that was hidden by the initial small test set.

Adding explicit policy grounding improved exact-match decision accuracy from **54.2% to 75.0% (+20.8 percentage points)** on the same 24-case benchmark.

The experiment also exposed an accuracy/efficiency tradeoff: richer policy context improved decision quality while increasing token usage and inference latency.

## What the Harness Evaluates

Each support ticket must be classified into exactly one action:

- `RESOLVE` — the agent has sufficient grounded information to resolve the request.
- `REQUEST_INFO` — additional information or verified context is required.
- `ESCALATE` — the request requires human intervention due to security, privacy, permissions, policy, or approval requirements.

The benchmark includes cases involving:

- Unauthorized access and security incidents
- Account and permission changes
- Billing and refunds
- Privacy and data deletion
- SSO configuration
- Product capability questions
- Service-status questions
- Password and account recovery

## Failure Analysis

The expanded benchmark revealed a systematic **over-resolution failure mode**.

The model sometimes selected `RESOLVE` for requests where it lacked sufficient evidence, including:

- unverified product capabilities,
- current service status,
- sensitive account changes,
- access verification.

This demonstrated that correct enterprise-agent behavior requires more than generating a plausible answer: decisions must be grounded in explicit policy and available context.

## Policy-Grounded Evaluation

To address these failures, the harness introduces a support policy defining when the agent should resolve, request information, or escalate.

The policy includes a core grounding constraint:

> Never assume that a product feature, account state, service status, permission, or company policy is true when it is not explicitly available in the provided context.

Running the same 24-case benchmark with this policy increased accuracy from **54.2% to 75.0%**.

## Architecture

```text
Support Ticket
      |
      v
  Inspect AI
      |
      v
Support Policy
      |
      v
   Qwen3 4B
      |
      v
Decision
      |
      +---- RESOLVE
      +---- REQUEST_INFO
      +---- ESCALATE
      |
      v
Exact-Match Scorer
      |
      v
Ground-Truth Dataset
