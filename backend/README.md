# MachWork Backend

This backend is designed as a modular, layered, API-first system with strict separation of concerns across Domain, Application, Infrastructure, and Presentation layers.

## Folder Structure

```
src/
  domain/               # Domain entities, value objects, domain services
    auth/
    users/
    companies/
    projects/
    jobs/
    crm/
    invoicing/
    analytics/
    admin/
    shared/
  application/          # Use-cases, orchestration, policies, DTOs
    auth/
    users/
    companies/
    projects/
    jobs/
    crm/
    invoicing/
    analytics/
    admin/
    shared/
  infrastructure/       # External concerns (DB, email, storage, logging)
    persistence/
    security/
    email/
    storage/
    audit/
  presentation/         # API controllers, routing, middleware
    api/
      v1/
        routes/
        middlewares/
```

## Architectural Principles

- Stateless services for horizontal scaling.
- API-first with strict RBAC enforcement per request.
- Infrastructure adapters keep external dependencies isolated.
- Domain layer contains core business rules and invariants.

See `docs/` for schema, migrations, API design, and security requirements.

## Setup & Run (Development)

1. Create a virtual environment and install dependencies:
   - `python -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`
2. Ensure PostgreSQL is running and migrations are applied.
3. Export required environment variables (`DATABASE_URL`, SMTP settings, JWT keys).
4. Run the API:
   - `uvicorn src.main:app --host 0.0.0.0 --port 8080`

## Tests

- `pytest`
