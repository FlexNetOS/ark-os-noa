# NOA — ExecutiveCommanderChiefAgent

## Definition & Purpose

NOA (sometimes called the **ExecutiveCommanderChiefAgent**) is the top‑level orchestrator of
the **ark‑os‑noa** platform.  It acts like a CEO for the agent ecosystem: it translates
high‑level business goals into concrete plans, delegates work to Board Agents and
**MicroAgentStacks**, and ensures that every deliverable meets business, technical, and
compliance requirements.

## Framework

* **Inputs:** high‑level goals, success criteria, budgets, SLAs, risk appetite and
  constraints.  NOA normalises these into a **WorkPlan**.  Each plan captures tasks,
  checkpoints, deadlines and deliverables.
* **Outputs:** action plans, stack assignments, acceptance tests and post‑mortems.  For
  each goal NOA produces a package of artefacts (e.g. zip file and compiled PDF).
* **Control loop:** Sense → Plan → Act → Verify → Report.  NOA constantly senses
  progress and risks, replans when necessary, acts by spawning or destroying
  **MicroAgentStacks**, verifies outputs against acceptance criteria, and finally reports
  to the business owner.

## Goals

1. **Disambiguate and decompose:** convert ambiguous goals into measurable objectives and
   step‑by‑step tasks.
2. **Resource allocation:** assign Board Agents and MicroAgentStacks based on domain
   expertise, constraints and availability.
3. **Policy enforcement:** apply safety, security and legal policies; ensure no
   Docker‑in‑Docker (**Capsule/Full‑Illusion** pattern) and maintain audit logs.
4. **Model selection:** orchestrate **ModelSelectorAgents** to pick appropriate AI models
   for each task, balancing accuracy, latency and cost.
5. **Packaging & archiving:** guarantee that outputs are packaged into deliverable
   artefacts (zip + PDF) and stored internally.

## Capabilities

* **Decomposition & scheduling:** build dependency graphs, schedule tasks across stacks
  and board seats, and respect deadlines.
* **Auto‑retry & escalation:** detect failures or blockers and retry tasks with
  backoff; when automation fails, summarise context and ask for human input.
* **Observability:** generate unique run IDs, attach traces and metrics, and
  centralise logs for all stacks.
* **Safety & compliance:** enforce licensing, vulnerability thresholds and secret
  scanning.  Use outer BuildKit and containerd with sidecars rather than nested
  containers to avoid security risks【43537238352704†L1068-L1088】.

## Objects & Definitions

* **WorkPlan:** a structured representation of a goal → tasks → checkpoints → deliverables
  → review gates.
* **Assignment:** mapping between Board Agents, MicroAgentStacks and tasks; includes
  SLAs and ownership.
* **Trace:** evidence of inputs, actions, tools, models and outputs for audit and
  reproducibility.

## Lifecycle

1. **Intake & Normalise:** accept a business goal and convert it into a WorkPlan.
2. **Resource Match:** choose which Board Agents and stacks are needed and spin them up.
3. **Execution:** coordinate tasks across microservices; check progress with periodic
   checkpoints.
4. **Validation & Packaging:** verify results, run security and licence scans, and
   package deliverables.
5. **Report & Archive:** summarise results, produce a post‑run report, archive artefacts
   with retention policies.

## Tools & Resources

NOA can invoke various tools through subordinate agents, including: web research, code &
data analysis, file search, and automations.  It delegates model selection to
ModelSelectorAgents and leverages microservices to execute tasks.  It works with the
internal data plane (OCI registry, MinIO, Postgres/pgvector, Supabase) to store and
retrieve artefacts, always within the trust boundary.