# ADR-003: Adopt Minimal Infrastructure

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decision Type:** Infrastructure Architecture
- **Scope:** Development / Deployment / MLOps

---

## 1. Context

StockFlow is designed as a learning-first, production-like project.

The project aims to develop practical skills in:

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Machine Learning
- MLOps
- Docker
- GitHub Actions
- GCP

The project should demonstrate production-oriented engineering without
introducing infrastructure that does not solve a concrete requirement.

The initial application only requires:

```text
Frontend
Backend
PostgreSQL
```

Additional infrastructure may become useful as the ML and deployment
capabilities evolve.

---

## 2. Decision

StockFlow will adopt a **minimal infrastructure approach**.

Only infrastructure required by the current application or development phase
will be introduced.

The initial Docker Compose environment contains:

```text
Frontend
Backend
PostgreSQL
```

MLflow will be introduced after the ML pipeline exists.

Additional infrastructure such as Redis, Kafka, Kubernetes, or other
distributed infrastructure will not be introduced unless a concrete
requirement justifies it.

---

## 3. Current Infrastructure

The current local development environment is:

```text
┌─────────────────────┐
│ Frontend            │
│ Next.js             │
│ :3000               │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Backend             │
│ FastAPI             │
│ :8000               │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ PostgreSQL          │
│ :5432               │
└─────────────────────┘
```

The environment is managed using Docker Compose.

---

## 4. Reasons

### 4.1 Reduce Unnecessary Complexity

Every additional infrastructure component introduces operational concerns.

Examples include:

- Configuration
- Networking
- Monitoring
- Security
- Deployment
- Maintenance
- Troubleshooting

Infrastructure should therefore be introduced only when its value is
demonstrated.

### 4.2 Focus on Learning Objectives

The project is intended to develop depth in:

- Software engineering
- Backend development
- Database engineering
- Machine Learning
- MLOps

Adding infrastructure without a concrete requirement can distract from these
objectives.

### 4.3 Easier Local Development

A smaller development environment is easier to:

- Start
- Stop
- Debug
- Reproduce
- Explain
- Deploy

This is especially important for a learning and portfolio project.

### 4.4 Production-Like Without Being Production-Complex

The goal is not to reproduce the infrastructure of a large enterprise system.

The goal is to practice production-oriented engineering principles while
keeping the system understandable and maintainable.

---

## 5. Infrastructure Introduction Strategy

Infrastructure should be introduced progressively.

### Phase 0

Use:

```text
Docker Compose
├── Frontend
├── Backend
└── PostgreSQL
```

### ML Phase

Introduce MLflow when the ML pipeline is ready:

```text
PostgreSQL
     ↓
ML Pipeline
     ↓
MLflow
```

MLflow will be used for:

- Experiment tracking
- Parameters
- Metrics
- Model artifacts
- Model registry

### CI/CD Phase

Introduce GitHub Actions for:

```text
Git Push
    ↓
GitHub Actions
    ├── Lint
    ├── Unit Tests
    ├── Integration Tests
    └── Build
```

### Deployment Phase

Introduce GCP services after the local Docker architecture is stable.

The exact GCP services should be selected based on the requirements of the
application at that stage.

---

## 6. Alternatives Considered

### 6.1 Kubernetes

**Rejected for the initial version.**

Kubernetes would introduce substantial orchestration and operational
complexity that is not required by the current application.

It may be studied separately if there is a specific learning objective, but it
is not part of the initial StockFlow architecture.

### 6.2 Redis

**Not required initially.**

Redis may become useful for specific requirements such as caching or
distributed state.

It should only be introduced when a concrete requirement exists.

### 6.3 Kafka

**Not required initially.**

StockFlow does not currently require an event streaming platform.

Kafka should not be introduced merely to demonstrate event-driven
architecture.

### 6.4 Other Infrastructure

Other infrastructure components should be evaluated using the same principle:

> Introduce infrastructure because the system needs it, not because the
> technology exists.

---

## 7. Consequences

### Positive Consequences

- Simpler development environment.
- Easier debugging.
- Lower infrastructure overhead.
- Easier onboarding and reproduction.
- Clearer architecture.
- More focus on core engineering and ML objectives.
- Lower risk of premature architectural complexity.

### Negative Consequences

- Some advanced infrastructure patterns will not be available initially.
- The system may require architectural changes if future requirements
  introduce new scaling or reliability needs.
- Some production technologies will be learned later rather than immediately.

These trade-offs are intentional.

---

## 8. Decision Criteria for Adding Infrastructure

Before introducing a new infrastructure component, answer:

1. What concrete problem does it solve?
2. Can the current architecture solve the problem without it?
3. What operational complexity does it introduce?
4. Does it provide measurable value?
5. Is the requirement expected to persist?
6. Is the component appropriate for the current project phase?

If the problem can be solved simply without additional infrastructure, the
simpler solution should be preferred.

---

## 9. Related Decisions

This decision is related to:

- ADR-001: Use Modular Monolith Architecture
- ADR-002: Use PostgreSQL as the Source of Truth

---

## 10. Review Criteria

This decision should be reconsidered when a concrete requirement appears for
additional infrastructure.

Examples include:

- Demonstrated performance bottlenecks
- Caching requirements
- Event-driven processing
- Independent service scaling
- Production deployment requirements
- ML experiment tracking
- Automated model lifecycle management

The introduction of infrastructure should be driven by requirements rather
than technology popularity.

---

## 11. References

- StockFlow Blueprint v1.0
- `docs/architecture/system-architecture.md`
- `docs/decisions/ADR-001-modular-monolith.md`
- `docs/decisions/ADR-002-postgresql-as-source-of-truth.md`