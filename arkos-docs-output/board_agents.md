# Board Agents — Executive Team of ark‑os‑noa

## Definition & Role

The **Board Agents** sit at the top of the **ark‑os‑noa** organisation just below NOA.  They are analogous to an executive board in a company: each agent owns a domain (strategy, operations, finance, legal, security, partnerships, research) and has authority to commission **MicroAgentStacks** to execute work.  By design they are *few in number* but *broad in scope*—their purpose is to translate NOA’s vision into specific missions, ensure alignment with ElementArk/DeFlex’s business model, and provide governance across all stacks and agents.

## Roster & Responsibilities

- **Strategy/CTO Agent** – Sets technical direction: system architecture, Capsule (Full‑Illusion) adoption, environment policies (no Docker‑in‑Docker), cohesion across services.
- **COO Agent** – Owns operational runbooks, SLAs, scheduling and change management.  Coordinates delivery timelines and resource utilisation.
- **CFO/FinOps Agent** – Manages budgets and spend telemetry.  Optimises cost across compute, storage and model usage.
- **Legal/Compliance Agent** – Ensures licence compliance, data governance, export controls and regulatory adherence.  Maintains policy frameworks.
- **Security Agent** – Enforces secrets management, supply‑chain security, SBOM attestation and vulnerability thresholds.  Gatekeeper for risk.
- **Growth/Partnerships Agent** – Curates ingestion roadmaps for repos, APIs and CRMs; drives ecosystem strategy and partnership integrations.
- **Digest Agent (R&D)** – Sits on the board as the research arm.  Its role is to *digest everything* (code, data, SaaS, models) and surface insights.  See `digest_agent.md` for details.

## Operating Rules

1. **Delegation:** Board Agents can spin up one or more **MicroAgentStacks** to accomplish tasks.  Each stack has its own **CommandChiefAgent** orchestrating the details, leaving the Board Agent to focus on strategy and oversight.
2. **Specialisation:** When a task requires sophisticated model selection, a Board Agent requests a **ModelSelectorAgent** to choose the most appropriate AI model or tool.  This ensures tasks are executed with the right balance of cost, latency and accuracy.
3. **Governance:** Board Agents enforce policies across stacks—licensing, vulnerability gates, security posture, and budget limits.  They maintain decision logs and risk registers for audit.
4. **Parallelism:** Multiple stacks can run concurrently.  Board Agents schedule tasks to maximise throughput while respecting resource constraints.

## Capabilities

* **Multi‑project scheduling:** assign and monitor numerous tasks across different domains and stacks; handle dependencies and deadlines.
* **Cross‑repo initiatives:** coordinate wide‑sweep digest operations (e.g., SBOM/security posture across all repos) by commissioning multiple stacks.
* **Program governance:** maintain an overarching view of risks, mitigations, budget spend, and deliverable quality.
* **Policy enforcement:** integrate security scanners, licence gates, and compliance checks into the workflow.

## Tools & Signals

Board Agents interact with the system through:

- **Research & analysis tools:** for web search, code parsing and data exploration within the current year’s context.
- **Change control & telemetry:** CI/CD gates, policy engines (e.g. OPA), vulnerability scanners and cost dashboards.
- **Observability feeds:** real‑time traces, metrics and logs aggregated from MicroAgentStacks and sidecars.  These signals inform decisions on scaling up/down stacks or raising alerts.

## Relationship to Other Components

* **NOA:** Board Agents receive missions from NOA and report status back.  They provide domain expertise and enforce governance while letting NOA handle high‑level planning and cross‑domain coordination.
* **MicroAgentStacks:** Board Agents are the owners of stacks.  They commission stacks to achieve defined objectives and decommission them when tasks complete.  Each stack operates autonomously but reports progress to its Board Agent.
* **ModelSelectorAgents:** When tasks require AI model inference, Board Agents request a ModelSelector to choose among local or hosted models.  The selection is recorded in the trace for audit.
* **Digest Agent:** The Digest Agent is part of the Board but behaves like an R&D lab—collecting raw information, synthesising knowledge graphs and summarising findings for the board to act on.

By keeping the Board Agents separate from execution details yet close enough to enforce policy, ark‑os‑noa achieves a balance between **strategic oversight** and **operational agility**.
