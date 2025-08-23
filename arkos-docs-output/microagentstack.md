# MicroAgentStack — Cooperative Work Pods

## Definition

A **MicroAgentStack** is a deployable cluster of cooperative agents assembled to accomplish a bounded objective.  Think of it as a project team spun up on demand: each stack has its own **CommandChiefAgent** (the stack master), a set of specialised Operators, Adapters and Guards, and a dedicated workspace.  Stacks can be created, scaled and destroyed rapidly, making them the primary execution units within ark‑os‑noa.

## Composition

* **CommandChiefAgent (Stack Master):** Orchestrates the stack, decomposes tasks, assigns work to subordinate agents, monitors progress, resolves conflicts and enforces SLAs.
* **Operators:** Specialised agents that perform specific functions.  Examples include code runners (execute code), data wranglers (transform data), doc generators (produce reports), testers (run unit/integration tests) and packagers (build zips, PDFs).
* **Adapters:** Connectors to external systems (repos, CRMs, APIs) and publishers to internal services (registry, MinIO, Postgres).  Adapters abstract away details like auth and rate‑limits.
* **Guards:** Policy enforcement points—security scanners, licence checkers, quality gates.  They ensure the stack adheres to policies defined by NOA and the Board Agents.

## Goals

1. **Deliver end‑to‑end outcomes:** A stack should own the entire life cycle of its objective—from cloning a repo to producing a digest report, from running tests to publishing a package.
2. **Scale horizontally:** Multiple stacks can be spun up concurrently when tasks are independent or parallelisable.  This enables large scale operations like digesting hundreds of repos simultaneously.
3. **Clean teardown:** After completion, a stack cleans up its resources (containers, temporary volumes) and archives logs, SBOMs and artefacts with proper retention policies.

## Lifecycle

1. **Bootstrap:**  Given inputs (e.g. repo URL, CRM base URL, model list), the CommandChiefAgent creates a **WorkPlan**, prepares the environment and mounts necessary sidecars.  It avoids Docker‑in‑Docker by using **Capsule** sidecars to talk to the outer BuildKit/containerd environment【43537238352704†L1068-L1088】.
2. **Execute:**  The stack runs its Operators in parallel where possible.  Retrying tasks with exponential backoff ensures resilience; failures trigger controlled retries or escalation to the Board Agent.
3. **Validate:**  Once tasks finish, Guards run acceptance tests (e.g. unit tests, SBOM scans, licence checks) and produce human‑readable summaries.  If acceptance criteria fail, the stack either retries or fails the WorkPlan.
4. **Package:**  On success, the stack assembles outputs into deliverables (zip file, compiled PDF, JSON indices).  It updates internal registries (OCI images, Postgres metadata, vector DB) and publishes logs and traces.
5. **Archive:**  The stack removes its runtime environment and persists all logs, SBOMs, run IDs, and checksums.  Retention policies decide how long to keep each artefact.

## One‑liners & Conventions

* Stacks are named by timestamps or descriptive identifiers (e.g. `stack‑20250822‑103045`).
* They maintain their own directory structure (`in/`, `work/`, `out/`, `logs/`) for clarity and reproducibility.
* Each stack produces a unique run ID and attaches it to all outputs and logs for traceability.

## Relationship to Other Components

* **Board Agents:** Create and oversee stacks.  Each stack reports to its Board Agent.  Board Agents can run multiple stacks in parallel.
* **ModelSelectorAgents:** When a stack requires AI processing, the CommandChiefAgent requests a ModelSelector to choose the appropriate model and logs the rationale.
* **Digest Agent:** Often uses MicroAgentStacks to perform large‑scale digestions across many repos or datasets.  Each stack digests one or more sources and returns results to the Digest Agent.

MicroAgentStacks bring structure, scalability and reliability to ark‑os‑noa’s execution model.  By isolating work into bounded pods, the system can handle complex, parallel workflows without turning into a monolith.
