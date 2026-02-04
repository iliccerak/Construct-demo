# MachWork

MachWork is a production-grade job & service marketplace, CRM, project management, and invoicing platform for the construction industry. It is designed for multi-company ownership, strict RBAC, and global compliance.

## Repository Structure

```
backend/            # Backend architecture layout (domain/application/infrastructure/presentation)
frontend/           # Frontend architecture layout (component-based)
db/                 # Database migrations
  migrations/       # Versioned SQL migrations
  schema.sql        # (Optional) schema mirror
/docs               # Product requirements, API, RBAC, security, deployments
```

## Required Outputs

All mandatory deliverables are stored in `docs/` and `db/`:

- Backend folder structure: `backend/README.md`
- Frontend folder structure: `frontend/README.md`
- Database schema + relationships: `docs/database.md` and `db/migrations/001_init.sql`
- Migration strategy: `docs/migrations.md`
- API endpoints list: `docs/api.md`
- RBAC permission matrix: `docs/rbac.md`
- Payment & invoice workflows: `docs/payments.md`
- Admin panel structure: `docs/admin-panel.md`
- Environment variables: `.env.example`
- Deployment instructions: `docs/deployment.md`
- Security considerations: `docs/security.md`

## Setup Steps

1. Provision PostgreSQL and apply migrations in `db/migrations/`.
2. Configure environment variables using `.env.example`.
3. Deploy the backend services with the layer architecture in `backend/`.
4. Deploy the frontend from `frontend/` as static assets.

## Notes

- Only bank transfer and cash payments are supported.
- All data access is scoped by company to prevent leakage.
- All actions are audited for compliance.
