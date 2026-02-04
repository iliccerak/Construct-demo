# Security Considerations

## Authentication & Authorization
- Passwords stored with strong hashing (Argon2id or bcrypt with high work factor).
- Refresh token rotation with reuse detection.
- Optional TOTP-based MFA with secure backup codes.
- RBAC enforced on every request using stored permissions.

## Data Protection
- TLS 1.2+ for all traffic.
- Encryption at rest for database and object storage.
- Field-level encryption for sensitive data (tax IDs, legal docs).

## Audit & Compliance
- Append-only audit logs for security events.
- Client history snapshots are immutable.
- GDPR export and deletion workflows with approval.

## Infrastructure
- IP allowlists for admin panel.
- Rate limiting on auth endpoints.
- Security headers (CSP, HSTS, X-Frame-Options).

## Operational Controls
- Separate environments for dev/stage/prod.
- Regular dependency scanning and patching.
