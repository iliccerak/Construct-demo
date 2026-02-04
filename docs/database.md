# Database Schema & Relationships (PostgreSQL)

MachWork uses PostgreSQL with strict referential integrity and enum types for workflow enforcement. The canonical migration lives in `db/migrations/001_init.sql`.

## Core Entities

### Identity & Access
- **users**: Authenticated users with MFA support and verification flags.
- **companies**: Legal entities with billing and compliance data.
- **company_memberships**: Many-to-many mapping between users and companies with role assignment.
- **roles / permissions / role_permissions**: Stored permission model used by RBAC enforcement.
- **refresh_tokens**: Rotating refresh tokens with replacement tracking and token IDs (`jti`).
- **audit_logs**: Immutable audit trail across all modules.
- **email_verification_tokens**: One-time tokens for email verification.
- **password_reset_tokens**: One-time tokens for password reset.
- **mfa_backup_codes**: Backup codes for MFA recovery.

### Project & Workforce
- **projects**: Company projects with lifecycle status, budget, and dates.
- **project_locations**: Geo-addresses per project.
- **project_milestones**: Deadlines and delivery checkpoints.
- **project_assignments**: User assignment per project with role context.

### Job Marketplace
- **worker_profiles**: Worker marketplace profiles.
- **worker_skills**: Skill inventory with proficiency.
- **worker_certifications**: External certifications.
- **job_postings**: Internal or external job listings.
- **job_applications**: Workflow-validated applications.

### CRM
- **clients**: Company client records.
- **client_history**: Immutable snapshots of client updates.
- **leads**: Lead pipeline with status tracking.
- **lead_notes**: Internal CRM notes.
- **communications**: Emails/meetings logs tied to client/project.

### Invoicing
- **invoices**: Sequential invoice numbers per company.
- **invoice_line_items**: Structured line items with tax rates.
- **invoice_payments**: Manual payment confirmation only.
- **bank_transfer_proofs**: Uploaded bank transfer evidence.

### Platform Admin
- **subscription_tiers**: SaaS tier definitions.
- **company_subscriptions**: Company subscription status.

## Relationship Highlights

- Users belong to multiple companies via **company_memberships** with per-company roles.
- All project, client, invoice, and job data is **scoped by company_id** to prevent cross-company leakage.
- **client_history** records immutable snapshots for compliance.
- **invoice_payments** require a user record of who confirmed the payment.

## Enforced Constraints

- Enum types enforce workflow state transitions.
- Unique constraints for invoice numbering per company.
- Audit logs are append-only.

For SQL definitions and indices, see `db/migrations/001_init.sql`.
