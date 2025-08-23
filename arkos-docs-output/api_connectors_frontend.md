# API, Connectors & Front‑End of ark‑os‑noa

## Gateway API

The **Gateway API** is the central entry point for interacting with ark‑os‑noa’s backend services.  Implemented using FastAPI, it exposes endpoints for ingesting sources, spawning capsules, toggling CRM behaviours, ingesting models and administering the system.

### Key Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/digest` | POST | Submit a digest request.  The request includes sources (e.g. repo URL, API base URL), intent (integrate, analyse), and optional metadata.  It triggers the Intake Service and returns a job ID. |
| `/capsule/spawn` | POST | Spawn a new Capsule environment.  Returns Capsule identifiers and access tokens.  Used when custom stacks need to be run manually or via the front‑end. |
| `/crm/toggle` | POST | Toggle the CRM Strangler Proxy mode for a specific endpoint (e.g. enable write‑through for `/contacts`).  Allows incremental migration from external CRM to internal implementation. |
| `/models/ingest` | POST | Add a model to the local registry.  Accepts a model identifier (e.g. Hugging Face repo) and optional metadata.  The Model Serving service pulls the model and makes it available through the ModelSelector. |
| `/models/benchmark` | POST | Run evaluations on local or remote models.  Returns latency, cost and accuracy metrics that feed into the ModelSelector’s decision graph. |
| `/admin/*` | GET/POST | Administrative endpoints for tasks such as inspecting job statuses, viewing SBOMs, retrieving logs, enabling/disabling features (NATS, Supabase, vcluster) and rotating secrets.  Protected via authentication and authorisation. |

All endpoints accept and return JSON; error responses include descriptive messages and relevant codes.  The Gateway uses request identifiers and attaches trace IDs to facilitate debugging and correlation across services.

## Connectors & Integrations

ark‑os‑noa interacts with the outside world via **Adapters** and **Connectors**.  These modules encapsulate authentication, rate limiting, and protocol details, allowing the rest of the system to remain agnostic to third‑party specifics.

### Built‑in Connectors

- **GitHub Connector:** Uses the GitHub API to search, clone and pull repositories.  It supports scoping by organisation or repository and can read commit logs and PR metadata.
- **CRM Connector:** Provides read/write access to CRM systems (e.g. Salesforce, HubSpot).  Initially operates in shadow mode (read‑only) via the CRM Strangler Proxy; write‑through can be toggled per endpoint.  Handles pagination, rate limits and authentication.
- **Model Hub Connector:** Interfaces with external model repositories (e.g. Hugging Face).  Supports pulling models, downloading tokenizers and retrieving licences.  Works in conjunction with the Model Serving service.
- **Other API Connectors:** Additional connectors (e.g. for Slack, Notion, Jira) can be added by implementing the Adapter interface.  Each connector is packaged as its own microservice or plugin to preserve modularity.

### Internal Connectors

- **Registry & Object Store:** Adapters communicate with the private OCI registry and MinIO using signed URLs.  They ensure that images and artefacts are pushed/pulled securely and that content addressing is respected.
- **Database & Vector Store:** Adapters abstract database interactions.  They provide typed functions to query or insert metadata, run logs and embeddings without exposing SQL directly to the application logic.

## Front‑End (Admin Console)

The **Admin Console** is a web interface built with Next.js.  Its primary function is to give administrators and power users visibility and control over the system.  Major features include:

* **Jobs Dashboard:** Displays active and past digest jobs, their statuses, progress bars and any errors.  Users can drill down into individual jobs to view their `profile.json`, `system_card.md`, SBOMs and vulnerability reports.
* **Capacities & Capsules:** Shows currently running Capsules, their resource usage and health status.  Offers controls to spawn or destroy Capsules.
* **Artefacts Explorer:** Lists generated artefacts (zip files, PDFs, embeddings, SBOMs).  Allows downloading via signed URLs and cross‑referencing to their origins.
* **SBOM & Security:** Provides a dedicated section to review SBOMs, vulnerabilities, licences and risk scores.  Policies can be configured here (e.g. accepted licence list, vulnerability severity thresholds).
* **Model Registry & Selector:** Displays available models, their metadata, benchmarks and usage statistics.  Administrators can add models to the ingestion queue or deprecate existing ones.  The ModelSelector’s decisions and rationales are visible for transparency.
* **CRM Controls:** Allows toggling of CRM endpoint modes (shadow/write‑through), viewing recent calls, and measuring divergence between external CRM data and internal state.
* **Settings & Feature Flags:** Provides toggles for enabling/disabling optional services (NATS, Supabase, vcluster) and adjusting environment variables.  Also offers secret rotation and certificate management.

## Interaction Patterns

* **External Clients:** Use the Gateway API to submit work.  They receive job IDs and can query progress or results.  Authentication tokens limit access based on roles.
* **Internal Agents:** Call endpoints via Adapters.  For example, a CommandChiefAgent may call `/digest` to start digestion for a new source or `/models/ingest` to add an in‑house model.  Internal calls attach run IDs and context for traceability.
* **Front‑End Users:** Access the Admin Console to monitor and control the system.  When they trigger actions (e.g. toggling a CRM endpoint), the console issues calls to the Gateway API on their behalf.

By exposing a clear API and a rich front‑end, ark‑os‑noa ensures that humans and agents can seamlessly interact with the system, inspect its state and adapt its behaviour without compromising security or traceability.
