# Digest Agent — R&D Engine for ark‑os‑noa

## Role & Position

The **Digest Agent** operates as the research and development arm of the Board Agents.  Its primary mission is to *“digest everything”*—code repositories, datasets, documents, APIs, SaaS systems (including live CRMs) and even AI models.  By analysing these sources, the Digest Agent extracts structured knowledge, builds semantic indices, and surfaces insights that inform strategic decisions.  Though part of the Board, it behaves like a self‑contained lab, spinning up **MicroAgentStacks** to perform large‑scale digestions.

## Pipeline

1. **Discover:** Identify sources to digest.  This includes scanning internal GitHub repos, listing connected APIs/CRMs, and reading the current model ingestion list.  Discovery may rely on board directives or scheduled tasks.
2. **Fetch:** Clone or synchronise the source material.  For code repos, perform a shallow clone and gather dependency lock files.  For CRMs or APIs, pull metadata and sample records while respecting rate limits.  Handle authentication using secure tokens from the secrets manager.
3. **Parse:** Use language‑specific parsers (Python AST, ts‑morph for JS/TS, go/ast, Rust syn, JavaParser) to analyse code and extract modules, functions, classes and call graphs.  For API schemas, parse OpenAPI/GraphQL definitions.  Build an **SBOM** to capture all packages and versions.
4. **Analyze:** Generate embeddings for code, documentation and data using models selected via the **ModelSelectorAgent**.  Build a **knowledge graph** linking functions, data structures, APIs and entities.  Identify external API calls, config surfaces and extension points.  Apply entity linking to unify references across sources.
5. **Summarize:** Produce layered summaries: per file, per module, per repository and across repositories.  Summaries highlight the system’s purpose, architecture, dependencies, risks and extension points.  The Digest Agent uses LLMs to craft human‑readable reports and cross‑links to original sources.
6. **Surface:** Publish outputs as markdown dossiers, dashboards and vector DB upserts.  Persist `profile.json`, `system_card.md`, `kg.json`, and embeddings.  Offer search and retrieval APIs for downstream agents.
7. **Secure:** Scan for secrets and vulnerabilities using tools like Trivy, Grype and Gitleaks.  Classify findings by severity and quarantine sensitive information.  Tag licences and export‑control flags【43537238352704†L1068-L1088】.

## Tools

* **Web research:** limited to current‑year sources, retrieving official documentation and examples.
* **Language parsers & AST tools:** Python’s `ast`, TS’s `ts‑morph`, Go’s `go/ast`, Rust’s `syn`, Java’s `JavaParser`.
* **Security scanners:** Syft to produce SBOMs; Grype and Trivy to scan for vulnerabilities; Gitleaks to detect secrets; Semgrep for static analysis.
* **Embeddings & vector DB:** Sentence transformers or llama.cpp embedding models; pgvector or Qdrant to store vectors and link them to original files.
* **Visualization & reports:** Graph builders, markdown generators and PDF compilers.

## Outputs

The Digest Agent delivers:

* **Digest reports:** Markdown documents (e.g. `2025‑08‑22_digest_report.md`) summarising findings.
* **Structured indices:** JSONL files representing the knowledge graph, call graph and embedding metadata.  These feed search and retrieval APIs.
* **SBOM & security reports:** Comprehensive lists of dependencies and vulnerabilities.
* **Vector store entries:** Embeddings upserted to the chosen vector DB for semantic search.

## Relationship to Other Components

* **Board Agents:** Commission digestion tasks and consume the Digest Agent’s findings when making strategic decisions.
* **MicroAgentStacks:** Used to parallelise large digests—each stack handles a set of sources and feeds results back to the Digest Agent.
* **ModelSelectorAgents:** Select embedding models and summarisation LLMs appropriate for each source type.  For example, code summarisation may use a codex model, while plain text summarisation uses a general LLM.
* **Data & Storage layer:** Stores artefacts and indices in MinIO, Postgres and the vector store.  The Digest Agent ensures proper metadata tagging and retention policies.

By systematically consuming and analysing every relevant piece of information, the Digest Agent turns unstructured data into actionable knowledge for ark‑os‑noa’s decision makers.
