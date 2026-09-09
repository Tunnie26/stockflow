# ADR-001: Use Modular Monolith Architecture

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decision Type:** Architecture
- **Scope:** Backend

---

## 1. Context

StockFlow is an Inventory Management Platform designed as both a learning
project and a production-like portfolio project.

The backend needs to support multiple business modules, including:

- Materials
- Categories
- Warehouses
- Storage Locations
- Suppliers
- Customers
- Stock operations
- Inventory
- Inventory Checks
- Stock Movement History
- Authentication and authorization

The project also has a future Machine Learning capability for demand
forecasting.

The system should provide clear separation between business responsibilities
while remaining simple enough to support learning, development, testing, and
maintenance.

A microservices architecture would introduce additional infrastructure and
operational complexity that is not currently required by the project.

---

## 2. Decision

StockFlow will use a **Modular Monolith** architecture for the core business
backend.

The backend will be deployed and operated as a single application while
maintaining clear internal boundaries between modules and responsibilities.

The initial architecture will not use microservices.

The ML pipeline will remain a separate capability from the core transactional
business backend.

---

## 3. Architecture

The initial system follows:

```text
Frontend
   ↓
FastAPI Modular Monolith
   ├── Authentication
   ├── Master Data
   ├── Inventory
   ├── Stock Transactions
   ├── Inventory Check
   └── Reporting / Dashboard APIs
   ↓
PostgreSQL
```

The future ML workflow is separated from the core business backend:

```text
PostgreSQL
     ↓
Historical Inventory Data
     ↓
ML Pipeline
     ↓
Demand Forecasting
```

The exact internal module boundaries may evolve as the application grows.

---

## 4. Reasons

### 4.1 Simplicity

A modular monolith requires less infrastructure and operational management
than a microservices architecture.

This allows the project to focus on:

- Python
- FastAPI
- SQL
- PostgreSQL
- Software architecture
- Testing
- Machine Learning
- MLOps

rather than service orchestration.

### 4.2 Clear Separation

Although the backend is deployed as one application, business responsibilities
can still be separated into modules and services.

This provides architectural discipline without introducing unnecessary
distributed-system complexity.

### 4.3 Learning Value

The project is intended to develop practical engineering skills.

A modular monolith provides an opportunity to learn:

- API design
- Business logic separation
- Database design
- Transactions
- Authentication
- Authorization
- Testing
- Dependency management
- Deployment

before introducing distributed-system concerns.

### 4.4 Future Evolution

The architecture should remain capable of evolving if a concrete requirement
appears.

Microservices may be considered in the future if there is a demonstrated need
such as:

- Independent scaling requirements
- Strong service isolation requirements
- Independent deployment requirements
- Significant operational or organizational constraints

Such a change must be justified by an actual requirement rather than by
technology preference.

---

## 5. Alternatives Considered

### 5.1 Microservices

**Rejected for the initial version.**

Microservices would introduce additional complexity around:

- Service communication
- Deployment
- Monitoring
- Configuration
- Networking
- Failure handling
- Data ownership
- Distributed transactions

These concerns are not required by the current project scope.

### 5.2 Monolithic Application Without Internal Boundaries

**Rejected.**

A completely unstructured monolith could make business logic increasingly
coupled as the project grows.

The modular monolith approach provides clearer boundaries while retaining the
simplicity of a single application.

---

## 6. Consequences

### Positive Consequences

- Simpler local development.
- Simpler Docker environment.
- Easier debugging.
- Easier deployment.
- Lower infrastructure requirements.
- Clear internal separation of business responsibilities.
- Suitable for the current project scope.
- Allows the project to focus on learning and maintainability.

### Negative Consequences

- All backend modules share the same application deployment.
- A failure in the application can affect multiple modules.
- Independent scaling of individual modules is not available.
- Strong module boundaries must be maintained through code organization and
  development practices.

---

## 7. Related Decisions

This decision is related to:

- ADR-002: PostgreSQL as the Source of Truth
- ADR-003: Minimal Infrastructure

---

## 8. Review Criteria

The decision should be reconsidered if the project develops a concrete
requirement that cannot be reasonably addressed within the modular monolith
architecture.

The architecture should not be changed solely to increase the number of
technologies used in the project.

---

## 9. References

- StockFlow Blueprint v1.0
- `docs/architecture/system-architecture.md`