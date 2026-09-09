# StockFlow System Architecture

## 1. Overview

StockFlow is an Inventory Management Platform designed as a learning-first,
production-like project.

The system is designed to demonstrate practical software engineering,
database management, machine learning, MLOps, and deployment practices.

The initial architecture prioritizes simplicity, maintainability, and clear
separation of responsibilities.

---

## 2. Architecture Style

StockFlow uses a **Modular Monolith** architecture for the core business
backend.

The system does not use microservices in the initial version.

The architecture should evolve only when there is a demonstrated technical
or business requirement for additional infrastructure or service separation.

The ML pipeline is treated as a separate capability from the core business
backend.

---

## 3. High-Level Architecture

The current system consists of three primary runtime components:

```text
┌──────────────────────────┐
│       Next.js            │
│      Frontend / UI       │
│         :3000            │
└────────────┬─────────────┘
             │
             │ REST / JSON
             ▼
┌──────────────────────────┐
│        FastAPI           │
│     Modular Backend      │
│         :8000            │
└────────────┬─────────────┘
             │
             │ SQLAlchemy
             ▼
┌──────────────────────────┐
│       PostgreSQL         │
│      Source of Truth     │
│         :5432            │
└──────────────────────────┘
```

The ML pipeline is introduced as a separate workflow after the transactional
and historical inventory data foundation is stable.

```text
PostgreSQL
     │
     │ Historical Data
     ▼
┌──────────────────────────┐
│       ML Pipeline        │
│    Train / Evaluate      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│    Demand Forecasting    │
│        7 / 30 days       │
└──────────────────────────┘
```

---

## 4. Frontend

### Technology

The frontend uses:

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zustand

### Responsibilities

The frontend is responsible for:

- User interface
- User interaction
- Form input
- Client-side validation where appropriate
- Displaying API data
- Managing server-state caching through TanStack Query
- Managing lightweight client/UI state through Zustand

The frontend is not a security boundary.

Authorization must always be enforced by the backend.

### Rendering Strategy

The frontend uses the Next.js App Router.

Server Components should be preferred where interactivity is not required.

Client Components should be introduced only where client-side interaction or
browser-specific behavior requires them.

---

## 5. Backend

### Technology

The backend uses:

- Python 3.13
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT

### Responsibilities

The backend is responsible for:

- REST API
- Request validation
- Authentication
- Authorization
- Business rules
- Inventory operations
- Transaction processing
- Database access
- API error handling

The backend is the primary security boundary of the application.

### Internal Flow

The general backend flow is:

```text
HTTP Request
     ↓
API Router
     ↓
Service
     ↓
SQLAlchemy
     ↓
PostgreSQL
```

API routers should remain focused on HTTP concerns.

Business logic should be implemented in services or appropriate domain
components rather than directly inside route handlers.

---

## 6. Database

PostgreSQL is the authoritative source of transactional and inventory data.

The database stores:

- Users
- Categories
- Materials
- Warehouses
- Storage Locations
- Suppliers
- Customers
- Inventory
- Stock Transactions
- Stock Transaction Items
- Inventory Checks

The core inventory principle is:

```text
Inventory = Current State

Stock Movement = Immutable Operational History

Transactions = Source of Truth
               for how inventory changed
```

Database schema changes are managed through Alembic migrations.

---

## 7. Inventory Architecture

Inventory operations are represented as explicit stock transactions.

Core operations include:

```text
IN
OUT
TRANSFER
ADJUSTMENT
```

The conceptual flows are:

### Stock In

```text
Supplier
    ↓
Stock IN
    ↓
Warehouse
    ↓
Storage Location
    ↓
Inventory + Quantity
```

### Stock Out

```text
Inventory
    ↓
Stock OUT
    ↓
Customer / Department
    ↓
Inventory - Quantity
```

### Transfer

```text
Location A
    │
    │ Transfer
    ▼
Location B

Location A: quantity - X
Location B: quantity + X
```

### Adjustment

```text
Physical Count
      ↓
Compare with System Quantity
      ↓
Difference
      ↓
Adjustment Transaction
      ↓
Corrected Inventory
```

---

## 8. Authentication and Authorization

The authentication flow is:

```text
Next.js Login
     ↓
POST /api/v1/auth/login
     ↓
FastAPI
     ├── Verify Credentials
     ├── Verify User
     └── Issue JWT
             ↓
        Access Token
             ↓
      Protected API
```

The initial roles are:

```text
ADMIN
VIEWER
```

### ADMIN

ADMIN has full read/write access across the system.

### VIEWER

VIEWER has read-only access.

Authorization is enforced by the backend.

Frontend visibility controls are considered UX behavior only and must not be
treated as a security mechanism.

JWT token handling should remain extensible so that refresh-token patterns can
be introduced later if required.

---

## 9. API Architecture

The API uses REST and JSON.

API versioning starts at:

```text
/api/v1
```

Core endpoints include:

```text
/api/v1/auth/login
/api/v1/auth/me

/api/v1/materials
/api/v1/categories
/api/v1/warehouses
/api/v1/locations
/api/v1/suppliers
/api/v1/customers

/api/v1/stock/in
/api/v1/stock/out
/api/v1/stock/transfer
/api/v1/stock/adjustment

/api/v1/inventory
/api/v1/inventory/{material_id}

/api/v1/inventory-checks
/api/v1/movements

/api/v1/forecasting
```

FastAPI provides OpenAPI / Swagger documentation for the API.

---

## 10. Docker Architecture

The local development environment uses Docker Compose.

Current services:

```text
┌─────────────────────┐
│ Frontend            │
│ Next.js             │
│ localhost:3000      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Backend             │
│ FastAPI             │
│ localhost:8000      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ PostgreSQL          │
│ localhost:5432      │
└─────────────────────┘
```

The current Docker Compose environment intentionally contains only the
infrastructure required by the current application foundation.

MLflow will be introduced in a later phase after the ML pipeline exists.

Infrastructure such as Redis, Kafka, or Kubernetes is not included unless a
concrete requirement appears.

---

## 11. Machine Learning Architecture

The initial ML problem is demand forecasting.

The primary input is historical material demand extracted from stock-out
transactions.

The planned workflow is:

```text
Historical Stock OUT
        ↓
Data Extraction
        ↓
Data Validation
        ↓
Preprocessing
        ↓
Feature Engineering
        ↓
Baseline
        ↓
Model Training
        ↓
Evaluation
        ↓
MLflow Tracking
        ↓
Best Model
        ↓
7-day / 30-day Forecast
```

The ML pipeline remains separate from the transactional business backend.

The forecasting capability is introduced after sufficient historical data and
a stable inventory data foundation are available.

---

## 12. MLOps Architecture

The planned MLOps workflow is:

```text
PostgreSQL
     ↓
Extract
     ↓
Validate
     ↓
Transform
     ↓
Feature Engineering
     ↓
Training
     ↓
Evaluation
     ↓
MLflow Experiment Tracking
     ↓
Model Registry
     ↓
Forecast Service
     ↓
FastAPI
     ↓
Next.js
```

MLflow is used to track:

- Experiments
- Parameters
- Metrics
- Model artifacts

The purpose is to support reproducibility and model comparison.

Continuous Training will be introduced only after the forecasting pipeline is
stable.

---

## 13. Dashboard Architecture

The dashboard is a consumer of validated business data.

It should not become the starting point for business logic.

Planned dashboard information includes:

- Total materials
- Low-stock materials
- Total inventory quantity
- Inventory value where applicable
- Stock movement trends
- Top-used materials
- Forecast alerts after ML capability becomes available

The dashboard should consume data from established backend APIs and services.

---

## 14. Deployment Direction

The long-term deployment direction is:

```text
GitHub
    ↓
GitHub Actions
    ↓
Docker
    ↓
GCP
```

The planned cloud environment will contain:

- Frontend
- FastAPI Backend
- PostgreSQL
- ML / model workflow

Exact GCP services will be selected after the local Docker architecture and
application foundation are stable.

---

## 15. Architecture Principles

StockFlow follows these principles:

1. Prefer simple architecture that can evolve.
2. Separate current inventory state from transaction history.
3. Keep business logic out of API route handlers where practical.
4. Validate inputs at the API boundary.
5. Enforce business rules in services or domain logic.
6. Treat backend authorization as the security boundary.
7. Avoid infrastructure that does not solve a demonstrated problem.
8. Measure ML improvements against a baseline.
9. Make experiments reproducible.
10. Every major phase should produce a working increment.
11. Optimize for learning depth and maintainability rather than technology
    count.

---

## 16. Current Architecture Status

The current implementation represents the foundation stage of StockFlow.

Implemented foundation:

```text
Next.js
   ↓
FastAPI
   ↓
PostgreSQL
```

Development infrastructure:

```text
Docker Compose
├── Frontend
├── Backend
└── PostgreSQL
```

The following capabilities belong to later phases:

```text
Authentication / RBAC
        ↓
Master Data
        ↓
Inventory Core
        ↓
Inventory Check
        ↓
Testing
        ↓
ML Forecasting
        ↓
MLflow
        ↓
CI/CD
        ↓
Continuous Training
        ↓
GCP Deployment
```

Architecture decisions should evolve together with these implementation
phases rather than being finalized prematurely.