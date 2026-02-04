# API Endpoints (REST v1)

All endpoints are versioned under `/api/v1` and require JWT access tokens unless explicitly noted.

## Auth & Security
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout`
- `POST /auth/refresh`
- `POST /auth/verify-email`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `POST /auth/mfa/enable`
- `POST /auth/mfa/verify`
- `POST /auth/mfa/disable`
- `GET /auth/sessions`
- `DELETE /auth/sessions/{sessionId}`

## Users & Profiles
- `GET /users/me`
- `PATCH /users/me`
- `GET /users/{userId}` (admin scoped)
- `GET /users/{userId}/memberships`
- `POST /users/{userId}/memberships`
- `DELETE /users/{userId}/memberships/{membershipId}`

## Companies
- `POST /companies`
- `GET /companies/{companyId}`
- `PATCH /companies/{companyId}`
- `GET /companies/{companyId}/members`
- `POST /companies/{companyId}/members`
- `PATCH /companies/{companyId}/members/{membershipId}`
- `DELETE /companies/{companyId}/members/{membershipId}`

## Projects
- `POST /companies/{companyId}/projects`
- `GET /companies/{companyId}/projects`
- `GET /companies/{companyId}/projects/{projectId}`
- `PATCH /companies/{companyId}/projects/{projectId}`
- `POST /companies/{companyId}/projects/{projectId}/locations`
- `POST /companies/{companyId}/projects/{projectId}/milestones`
- `PATCH /companies/{companyId}/projects/{projectId}/milestones/{milestoneId}`
- `POST /companies/{companyId}/projects/{projectId}/assignments`
- `DELETE /companies/{companyId}/projects/{projectId}/assignments/{assignmentId}`

## Job Marketplace
- `POST /companies/{companyId}/jobs`
- `GET /companies/{companyId}/jobs`
- `GET /companies/{companyId}/jobs/{jobId}`
- `PATCH /companies/{companyId}/jobs/{jobId}`
- `POST /jobs/{jobId}/applications`
- `GET /jobs/{jobId}/applications`
- `PATCH /jobs/{jobId}/applications/{applicationId}`
- `GET /workers/me/profile`
- `POST /workers/me/profile`
- `PATCH /workers/me/profile`
- `POST /workers/me/skills`
- `POST /workers/me/certifications`

## CRM
- `POST /companies/{companyId}/clients`
- `GET /companies/{companyId}/clients`
- `GET /companies/{companyId}/clients/{clientId}`
- `PATCH /companies/{companyId}/clients/{clientId}`
- `GET /companies/{companyId}/clients/{clientId}/history`
- `POST /companies/{companyId}/leads`
- `GET /companies/{companyId}/leads`
- `PATCH /companies/{companyId}/leads/{leadId}`
- `POST /companies/{companyId}/leads/{leadId}/notes`
- `POST /companies/{companyId}/communications`

## Invoicing
- `POST /companies/{companyId}/invoices`
- `GET /companies/{companyId}/invoices`
- `GET /companies/{companyId}/invoices/{invoiceId}`
- `PATCH /companies/{companyId}/invoices/{invoiceId}`
- `POST /companies/{companyId}/invoices/{invoiceId}/line-items`
- `POST /companies/{companyId}/invoices/{invoiceId}/payments`
- `POST /companies/{companyId}/invoices/{invoiceId}/bank-proofs`
- `POST /companies/{companyId}/invoices/{invoiceId}/mark-overdue`
- `GET /companies/{companyId}/invoices/{invoiceId}/pdf`

## Analytics
- `GET /companies/{companyId}/analytics/dashboard`
- `GET /companies/{companyId}/analytics/financials`
- `GET /companies/{companyId}/analytics/projects`
- `GET /companies/{companyId}/analytics/workers`
- `GET /companies/{companyId}/analytics/exports`

## Admin Panel
- `GET /admin/users`
- `GET /admin/companies`
- `PATCH /admin/companies/{companyId}`
- `GET /admin/subscriptions`
- `PATCH /admin/subscriptions/{subscriptionId}`
- `GET /admin/audit-logs`
- `GET /admin/system-config`
- `PATCH /admin/system-config`
- `POST /admin/manual-payments/verify`
- `POST /admin/abuse-reports`
