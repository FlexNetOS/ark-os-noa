# ModelSelectorAgents — Choosing the Right Tool for the Job

## Purpose

A **ModelSelectorAgent** specialises in selecting the best AI model or tool for a given task.  In the context of ark‑os‑noa, tasks vary widely—from reasoning and planning, to code analysis, to data transformation.  Selecting the wrong model can waste resources or compromise privacy.  The ModelSelector provides an intelligent arbitration layer, helping Board Agents and **MicroAgentStacks** achieve high quality results while respecting cost, latency and privacy constraints.

## Framework

* **Inputs:** Each call to a ModelSelector includes a task description, input size (e.g. document length, number of files), the privacy tier (public, sensitive, confidential), latency budget, and a cost cap.  These parameters come from the requesting agent (often a Board Agent or CommandChiefAgent).
* **Decision Graph:** The ModelSelector applies a decision graph:
  1. **Task classification** – Is this reasoning/planning, bulk transformation, code/data manipulation, or something else?
  2. **Complexity estimation** – How large or intricate is the input?  This influences whether to use a bigger model or a lightweight one.
  3. **Model/Tool selection** – Choose from a catalogue of available models (remote APIs, local models served via llama.cpp/Ollama, code runners, data converters) using heuristics or learned policies.
  4. **Guardrails assertion** – Check licensing, privacy levels and security requirements.  For example, confidential data must stay on‑prem and use local models.
* **Outputs:** A plan specifying the chosen model or tool, the expected cost/latency, and a rationale.  The rationale becomes part of the execution **Trace**, enabling auditing and future optimisation.

## Default Policy

The default policy can be tuned, but common guidelines include:

1. **Reasoning / Planning tasks:** Use high‑quality generalist models (e.g. GPT‑5).  These tasks benefit from advanced reasoning and tolerance for slower latency when results matter.
2. **Bulk transforms / formatting:** Use fast, cost‑efficient models; they handle repetitive conversions without needing deep reasoning.
3. **Code & data tasks:** Prefer dedicated code analysis tools or local runtimes for safety.  Use sandboxed execution to evaluate code or parse data.  Employ smaller codex models when summarising code.
4. **Offline/local fallbacks:** If the privacy tier demands on‑prem processing or if network latency is unacceptable, use local models served via llama.cpp, vLLM or similar frameworks.  This reduces latency and eliminates external data exposure.

## Tools & Telemetry

- **Model catalogues:** The selector maintains metadata about available models—accuracy, context limits, token costs, latency benchmarks, licensing and hardware requirements.  It syncs with the local model server and remote provider APIs.
- **Cost/latency forecaster:** Predicts cost and latency using historical telemetry and dynamic system load.  This helps decide when to use a cheaper but slower model vs. a more expensive high‑performance one.
- **Performance feedback:** The selector ingests feedback after tasks complete (e.g. success, error rate, user satisfaction).  Over time it learns to better match tasks to models.

## Relationship to Other Components

- **Board Agents:** Request ModelSelector assistance when their tasks involve AI/ML.  They set budgets and specify privacy tiers.  The ModelSelector returns a plan and rationale.
- **MicroAgentStacks:** CommandChiefAgents invoke ModelSelectors inside their stacks when a task requires AI processing.  This ensures each stack uses consistent policies and optimal models.
- **NOA:** Maintains overarching policies for model selection (allowed licences, vulnerability gates, GPU quotas).  The ModelSelector enforces these policies and logs decisions back to NOA’s audit trail.

## Benefits

* **Efficiency:** Avoids blindly calling the largest or default model for every task, saving compute and cost.
* **Compliance:** Ensures tasks adhere to privacy and licensing requirements—confidential data stays internal.
* **Transparency:** Provides a clear rationale for each selection so decisions can be audited and improved.
* **Extensibility:** New models or tools can be added to the catalogue; the decision graph can be refined with new criteria or learned policies.

By delegating model/tool choice to a dedicated ModelSelectorAgent, ark‑os‑noa keeps business logic and AI expertise separate, resulting in better outcomes and traceable decisions.
