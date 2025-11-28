# ark-os-noa

Agent-driven platform for autonomous software development and operations with integrated coding agents for accelerated development.

## Quick Start

### Prerequisites
- Python 3.11+ with pip
- Docker and Docker Compose
- Git

### Automated Setup (Recommended)
```bash
# Clone and setup development environment
git clone https://github.com/FlexNetOS/ark-os-noa.git
cd ark-os-noa
./scripts/setup-dev.sh
```

### Manual Setup
```bash
# 1. Setup Python environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Start infrastructure
docker-compose up -d

# 4. Verify setup
python -m pytest tests/
```

## Coding Agents 🤖

This platform includes automated coding agents to accelerate development:

### Agent CLI
```bash
# List available agents
python agent.py list-agents

# Generate a new microservice
python agent.py generate-service my-new-service

# Check environment health
python agent.py health-check

# Run a service
python agent.py run-service intake --port 8001
```

### Available Agents
- **Service Generator**: Auto-generate microservice boilerplate with FastAPI endpoints, tests, and Docker configuration
- **Quality Checker**: Automated code formatting, linting, and security scanning (coming soon)
- **Test Generator**: Auto-generate comprehensive test suites (coming soon)
- **Deployment Agent**: Automated service deployment and monitoring (coming soon)

## Documentation

- 📋 [Install Guide Review & Analysis](INSTALL_GUIDE_REVIEW.md) - Comprehensive setup analysis and recommendations
- 🏗️ [Data Architecture & Autonomous Intelligence](data_architecture_autonomous_intelligence.md)
- 🧠 [Expanded Explanation & Intelligence Playbook](arkos-expanded-explained.md)
- 📚 Additional component overviews live under `arkos-docs-output/`

## Infrastructure

The `docker-compose.yml` file provisions core internal services:

- **Private OCI Registry** (port 5000) - Container image storage
- **MinIO Object Storage** (ports 9000, 9001) - S3-compatible storage with web console
- **Postgres with pgvector** (port 5432) - Main database with vector search
- **Supabase** (port 5433) - Developer-friendly Postgres variant  
- **Redis Streams** (port 6379) - Event bus and caching
- **NATS** (port 4222) - Optional pub/sub messaging

### Service URLs
- MinIO Console: http://localhost:9001 (admin/minioadmin)
- Registry Catalog: http://localhost:5000/v2/_catalog
- Postgres: postgresql://noa:noa@localhost:5432/noa

## Services Architecture

Microservice stubs for the expanded digest pipeline:

```
services/
├── intake/          # Request ingestion and validation
├── classifier/      # Content type and language detection  
├── graph_extract/   # Code analysis and dependency graphs
├── embeddings/      # Vector generation and search
├── env_synthesis/   # Environment setup and configuration
├── safety/          # Security scanning and SBOM generation
├── runner/          # Task execution and testing
├── integrator/      # Result aggregation and assembly
└── registrar/       # Artifact registration and storage
```

Each service is a FastAPI application with:
- Health check endpoints
- Processing pipeline integration
- Docker containerization
- Automated test coverage

## Development Workflows

### Generate New Service
```bash
python agent.py generate-service my-service --endpoint /process --endpoint /analyze
```

### Run Services
```bash
# Single service
python agent.py run-service intake --port 8001

# All services (different terminals)
for service in intake classifier graph_extract; do
  python agent.py run-service $service --port $((8000 + $i)) &
  ((i++))
done
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Test specific service
python -m pytest tests/test_intake.py

# With coverage
python -m pytest tests/ --cov=services --cov-report=html
```

### Code Quality
```bash
# Format code (when quality agent is available)
black services/ coding-agents/

# Type checking
mypy services/ coding-agents/

# Security scan
bandit -r services/ coding-agents/
```

## Contributing

1. Use the setup script: `./scripts/setup-dev.sh`
2. Generate services with: `python agent.py generate-service <name>`
3. Follow established patterns in existing services
4. Add tests for new functionality
5. Run quality checks before submitting

## Architecture Goals

1. **Agent-Driven Development**: Coding agents automate repetitive tasks
2. **Microservices**: Loosely coupled, independently deployable services
3. **Event-Driven**: Redis Streams for decoupled communication
4. **Security-First**: No Docker-in-Docker, proper isolation via Capsule sidecars
5. **Observable**: Comprehensive logging, metrics, and tracing
6. **Scalable**: Horizontal scaling via MicroAgentStacks
