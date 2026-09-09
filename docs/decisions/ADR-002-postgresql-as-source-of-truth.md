# ADR-002: Use PostgreSQL as the Source of Truth

- **Status:** Accepted
- **Date:** 2026-09-09
- **Decision Type:** Database Architecture
- **Scope:** Backend / Data

---

## 1. Context

StockFlow is an Inventory Management Platform that manages transactional
inventory data.

The system needs to maintain reliable information about:

- Materials
- Warehouses
- Storage Locations
- Inventory quantities
- Stock transactions
- Stock transaction items
- Inventory checks
- Suppliers
- Customers
- Users

Inventory operations include:

```text
IN
OUT
TRANSFER
ADJUSTMENT
```

The system also needs historical transaction data that can later be used as
the foundation for demand forecasting.

The database therefore needs to act as the authoritative source for both
current inventory state and transactional history.

---

## 2. Decision

StockFlow will use **PostgreSQL as the authoritative source of transactional
and inventory data**.

PostgreSQL will be the primary persistent data store for the application.

The backend will access PostgreSQL through SQLAlchemy.

Database schema changes will be managed through Alembic migrations.

---

## 3. Data Architecture

The core data relationship is:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ├── Master Data
   ├── Inventory State
   ├── Stock Transactions
   ├── Inventory Checks
   └── Historical Data
```

The inventory architecture follows three related concepts:

```text
Inventory
    = Current State

Stock Movement
    = Immutable Operational History

Transactions
    = Source of Truth
      for how inventory changed
```

Current inventory represents the state of stock at a given point in time.

Transactions represent the operations that caused inventory to change.

Historical transaction data can later be used by the ML pipeline for demand
forecasting.

---

## 4. Reasons

### 4.1 Transactional Inventory Data

Inventory operations require reliable transactional behavior.

Operations such as stock in, stock out, transfer, and adjustment can affect
multiple records and therefore require consistent database operations.

PostgreSQL provides the relational database capabilities required by the
application.

### 4.2 Relational Data Model

StockFlow contains strongly related entities.

Examples include:

```text
Category
    ↓
Material
    ↓
Inventory
    ↓
Stock Transaction
    ↓
Stock Transaction Item
```

Other relationships include:

```text
Warehouse
    ↓
Storage Location
```

and:

```text
Supplier / Customer
    ↓
Stock Transactions
```

A relational database is appropriate for these relationships.

### 4.3 Historical Data

The future ML pipeline requires historical material demand extracted from
stock-out transactions.

Keeping transactional history in PostgreSQL provides a persistent data
foundation for future extraction, validation, preprocessing, and feature
engineering.

### 4.4 Production-Like Learning

PostgreSQL allows the project to practice realistic database engineering
concepts including:

- Relational schema design
- Constraints
- Transactions
- Indexing
- Query optimization
- Migrations
- Data integrity

These concepts are directly relevant to the project's learning goals.

---

## 5. Alternatives Considered

### 5.1 SQLite

**Not selected for the current architecture.**

SQLite could provide a simpler local database for a small application.

However, StockFlow is intentionally designed as a production-like learning
project using a client-server architecture with FastAPI and PostgreSQL.

PostgreSQL therefore better matches the intended architecture and learning
objectives.

### 5.2 Other Database Systems

Other relational database systems were not selected because PostgreSQL already
satisfies the current application requirements.

Introducing another database would add complexity without a demonstrated
benefit.

---

## 6. Consequences

### Positive Consequences

- Reliable relational data storage.
- Strong support for transactional operations.
- Suitable for inventory consistency.
- Suitable for historical data storage.
- Supports complex relational queries.
- Provides a strong foundation for future ML data extraction.
- Provides production-oriented database learning experience.

### Negative Consequences

- More infrastructure than an embedded database such as SQLite.
- Requires PostgreSQL configuration and management.
- Local development requires the PostgreSQL service or Docker container.

These costs are acceptable for the current project scope.

---

## 7. Database Migration Strategy

Database schema changes will be managed through Alembic.

The expected flow is:

```text
SQLAlchemy Model
       ↓
Alembic Migration
       ↓
PostgreSQL Schema
```

Database structure should not be changed manually without a corresponding
migration.

Migrations should be committed to Git so that the database schema can be
reproduced across development and deployment environments.

---

## 8. Data Integrity Principles

Inventory-related data must preserve business consistency.

The system should:

- Validate transaction input.
- Enforce appropriate database constraints.
- Use database transactions for atomic inventory operations.
- Preserve stock movement history.
- Avoid uncontrolled direct modification of inventory state.
- Keep historical operational data available for auditing and analysis.

The exact constraints and transaction implementation will be defined during
the backend and inventory phases.

---

## 9. ML Data Foundation

PostgreSQL will also provide the historical data foundation for the ML
pipeline.

The planned flow is:

```text
PostgreSQL
     ↓
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
Model Training
```

The ML pipeline should consume validated historical data rather than becoming
a second source of truth for transactional inventory data.

---

## 10. Related Decisions

This decision is related to:

- ADR-001: Use Modular Monolith Architecture
- ADR-003: Minimal Infrastructure

---

## 11. Review Criteria

This decision should be reconsidered only if a concrete requirement appears
that PostgreSQL cannot reasonably satisfy.

The project should not introduce another primary database solely for
technology experimentation or architectural complexity.

---

## 12. References

- StockFlow Blueprint v1.0
- `docs/architecture/system-architecture.md`
- `docs/decisions/ADR-001-modular-monolith.md`