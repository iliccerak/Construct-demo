# Deployment Instructions

MachWork is built to run as SaaS or self-hosted. The backend is stateless and horizontally scalable.

## Required Services
- PostgreSQL 14+
- Object storage for bank proofs and PDF exports
- SMTP provider for email verification and password reset
- Optional: Redis for rate limiting and session cache

## Environment Setup

1. Provision PostgreSQL and apply migrations from `db/migrations/`.
2. Configure environment variables from `.env.example`.
3. Deploy backend as containers behind a load balancer.
4. Deploy frontend as static assets (CDN + edge caching).

## Scaling

- Scale API nodes horizontally.
- Use read replicas for reporting workloads.
- Enable object storage lifecycle policies for compliance.

## Backups

- Daily database backups with 35-day retention.
- Point-in-time recovery enabled.
- Object storage versioning for uploaded proofs.
