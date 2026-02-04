# Migration Strategy

MachWork uses forward-only, transactional migrations. Each migration file is numbered and immutable once deployed.

## Principles

- **No destructive changes without data migration plan.**
- **Transactional DDL** for safety (PostgreSQL).
- **Backward compatibility** for APIs during rolling deployments.
- **Audit-first changes**: new tables/columns add before removing old ones.

## Workflow

1. Create a new migration file in `db/migrations/` with the next sequential number.
2. Run migrations in CI/CD before application deploy.
3. Validate schema with `SELECT` checks or migration verification scripts.

## Example

- `001_init.sql` establishes initial enums, tables, constraints, and indices.

## Rollback Policy

Rollbacks are performed by applying compensating migrations (never edit or delete previously applied migrations).
