# ark-os-noa

Early scaffolding for the agent-driven ark-os-noa platform.

## Infrastructure

The `docker-compose.yml` file provisions core internal services:

- Private OCI registry
- MinIO object storage
- Postgres with pgvector
- Supabase (Postgres variant)
- Redis Streams and optional NATS event bus

Start the stack locally:

```bash
docker-compose up -d
```

## Services

Microservice stubs for the expanded digest pipeline live under `services/`:

- intake
- classifier
- graph_extract
- embeddings
- env_synthesis
- safety
- runner
- integrator
- registrar

Each service is a small FastAPI app exposing a root endpoint that returns its name.

## Development

Install dependencies and run tests:

```bash
pip install -r requirements.txt
pytest
```
