# StockFlow Coding Conventions

## 1. General Principles

StockFlow follows these principles:

- Prefer simple and maintainable solutions.
- Keep responsibilities separated.
- Avoid premature abstraction and over-engineering.
- Prefer explicit code over clever code.
- Validate data at system boundaries.
- Keep business logic independent from framework-specific code where practical.
- Do not duplicate business rules across frontend and backend.
- Security-sensitive logic must always be enforced on the backend.

---

## 2. Backend

### 2.1 Technology

The backend uses:

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic / Pydantic Settings
- PostgreSQL
- Ruff
- pytest

### 2.2 Naming Conventions

Use `snake_case` for:

- Variables
- Functions
- Methods
- Modules
- Database columns

Example:

```python
inventory_item
get_inventory()
calculate_stock_balance()
```

Use `PascalCase` for:

- Classes
- Pydantic schemas
- SQLAlchemy models

Example:

```python
InventoryItem
InventoryItemCreate
InventoryItemResponse
```

Use `UPPER_SNAKE_CASE` for constants.

Example:

```python
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100
```

### 2.3 Type Hints

Use type hints for function parameters and return values.

Example:

```python
def get_inventory(item_id: int) -> InventoryItem:
    ...
```

Avoid unnecessary use of `Any`.

Avoid:

```python
def process_data(data: Any) -> Any:
    ...
```

Prefer a specific type whenever practical.

### 2.4 API Layer

API routes are responsible for:

- Receiving HTTP requests
- Validating request data
- Calling application/service logic
- Returning HTTP responses

API routes should not contain large amounts of business logic.

Avoid:

```python
@router.post("/inventory")
def create_inventory(...):
    # validation
    # business rules
    # calculations
    # database operations
    # response transformation
```

Prefer:

```text
API Router
    ↓
Service
    ↓
Database
```

### 2.5 Services

Services contain application and business logic.

Examples:

```text
inventory_service.py
transaction_service.py
forecast_service.py
```

Services should not depend on HTTP-specific concepts unless necessary.

Business rules should be implemented in one place whenever possible.

### 2.6 Database

SQLAlchemy models represent database entities.

Database models should not be returned directly as public API contracts.

Use separate Pydantic schemas for API input and output.

The general flow is:

```text
SQLAlchemy Model
        ↓
Service
        ↓
Pydantic Schema
        ↓
API Response
```

Database schema changes must be managed through Alembic migrations.

Never modify the production database structure manually without a corresponding migration.

### 2.7 Configuration

Application configuration must be managed through environment variables and Pydantic Settings.

Secrets must never be committed to Git.

Examples:

```text
DATABASE_URL
JWT_SECRET
POSTGRES_PASSWORD
```

Never hard-code secrets in source code.

---

## 3. Frontend

### 3.1 Technology

The frontend uses:

- Next.js
- TypeScript
- React
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zustand

### 3.2 Naming Conventions

Use `camelCase` for:

- Variables
- Functions
- Hooks

Examples:

```typescript
inventoryItems
fetchInventory()
useInventory()
```

Use `PascalCase` for:

- React components
- Types
- Interfaces

Examples:

```typescript
InventoryTable
InventoryItem
InventoryResponse
```

Use `UPPER_SNAKE_CASE` for constants when they represent fixed configuration values.

Example:

```typescript
DEFAULT_PAGE_SIZE
MAX_PAGE_SIZE
```

### 3.3 React Components

Components should have a clear responsibility.

Prefer smaller, focused components such as:

```text
InventoryTable
InventoryFilters
InventoryPagination
```

over one large component containing the entire page.

Page-level components should coordinate smaller components rather than contain every UI detail themselves.

### 3.4 Data Fetching

Server communication should not be scattered throughout UI components.

Prefer:

```text
Component
    ↓
TanStack Query Hook
    ↓
API Client
    ↓
Backend API
```

API-related logic should be reusable and centralized.

### 3.5 State Management

Use the simplest appropriate state mechanism.

Use:

- React state for local component state.
- TanStack Query for server state.
- Zustand for shared client state.

Do not put server data into Zustand unless there is a specific reason.

### 3.6 TypeScript

TypeScript strict mode must remain enabled.

```json
{
  "strict": true
}
```

Avoid:

```typescript
const data: any = ...
```

Prefer explicit types or inferred types.

Do not disable TypeScript checks merely to make a build pass.

---

## 4. Project Structure

StockFlow follows a modular monolith architecture.

### 4.1 Backend Structure

```text
apps/backend/
├── migrations/
├── src/
│   └── app/
│       ├── api/
│       ├── db/
│       ├── models/
│       ├── schemas/
│       └── services/
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

### 4.2 Frontend Structure

```text
apps/frontend/
├── src/
│   └── app/
├── public/
├── Dockerfile
├── package.json
└── package-lock.json
```

### 4.3 Adding New Directories

New directories should only be introduced when there is a clear responsibility for them.

Avoid creating generic directories such as:

```text
utils/
helpers/
common/
misc/
```

unless their responsibility is clearly defined.

---

## 5. API and Service Separation

The backend follows this general flow:

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

The frontend follows:

```text
UI Component
     ↓
TanStack Query
     ↓
API Client
     ↓
REST API
```

Responsibilities should remain separated.

A component should not contain raw SQL.

An API router should not contain complex business calculations.

A database model should not contain HTTP response logic.

---

## 6. Database and Inventory Rules

Inventory-related operations must preserve business consistency.

Stock changes should be represented through explicit transactions.

Examples include:

```text
Import
Export
Borrow
Return
Adjustment
Transfer
```

Inventory calculations must be performed consistently from transaction data.

Avoid directly changing stock balances in multiple unrelated places.

Critical inventory rules must be enforced by the backend and database where appropriate.

---

## 7. Error Handling

API errors should use appropriate HTTP status codes.

Common examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
500 Internal Server Error
```

Do not expose internal implementation details, database errors, stack traces, or secrets to API clients.

Errors should be logged on the backend while returning safe messages to clients.

---

## 8. Formatting and Linting

### 8.1 Backend

Ruff is the source of truth for Python linting and formatting.

Run:

```powershell
uv run ruff check .
uv run ruff format --check .
```

To automatically fix supported issues:

```powershell
uv run ruff check . --fix
uv run ruff format .
```

### 8.2 Frontend

ESLint is the source of truth for frontend linting.

Run:

```powershell
npm run lint
```

TypeScript must be checked with:

```powershell
npx tsc --noEmit
```

Do not introduce an additional formatter unless there is a clear project requirement.

---

## 9. Testing

Backend tests use pytest.

Tests should focus on:

- Business rules
- API behavior
- Database behavior
- Edge cases
- Regression prevention

Frontend tests should focus on:

- Component behavior
- User interactions
- Important UI states
- Data-fetching behavior

Not every function requires a test.

Prioritize testing business-critical behavior.

---

## 10. Git Commit Convention

StockFlow follows Conventional Commits.

Common prefixes:

```text
feat:
fix:
refactor:
test:
docs:
chore:
```

Examples:

```text
feat: add inventory transaction API
fix: prevent negative stock balance
refactor: simplify inventory service
test: add inventory service tests
docs: update API documentation
chore: update backend dependencies
```

Commits should represent meaningful changes.

Avoid vague commit messages such as:

```text
update
fix
test
changes
final
final2
final-final
```

---

## 11. Environment and Secrets

Local environment variables are stored in `.env`.

`.env` must never be committed.

`.env.example` contains variable names and safe example or default values.

Frontend local environment variables are stored in:

```text
apps/frontend/.env.local
```

Only variables intended for browser exposure may use:

```text
NEXT_PUBLIC_*
```

Never expose sensitive values through `NEXT_PUBLIC_*`.

Sensitive examples include:

```text
JWT_SECRET
POSTGRES_PASSWORD
DATABASE_URL
```

Production secrets will be managed outside Git and local `.env` files.

---

## 12. Code Review Checklist

Before committing code, verify:

- [ ] Code follows naming conventions.
- [ ] Business logic is placed in the appropriate layer.
- [ ] No secrets are committed.
- [ ] No unnecessary abstraction was introduced.
- [ ] Backend Ruff passes.
- [ ] Frontend ESLint passes.
- [ ] TypeScript check passes.
- [ ] Relevant tests pass.
- [ ] Database changes have an Alembic migration.
- [ ] API behavior is documented when necessary.

---

## 13. Guiding Principle

StockFlow is a learning and portfolio project intended to demonstrate practical software engineering.

The project should favor:

```text
Simple
    ↓
Correct
    ↓
Maintainable
    ↓
Testable
    ↓
Scalable when necessary
```

Architecture should evolve according to actual requirements rather than anticipated complexity.