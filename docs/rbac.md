# RBAC Permission Matrix

RBAC is enforced at the API layer using stored permissions. Every request is validated against the caller's role within the target company.

## Roles
- Super Admin (platform owner)
- Company Owner
- Company Admin
- Manager
- Worker
- Client

## Permissions
| Permission | Super Admin | Company Owner | Company Admin | Manager | Worker | Client |
| --- | --- | --- | --- | --- | --- | --- |
| platform.manage | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| company.create | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| company.update | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| company.members.manage | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| project.create | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| project.update | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| project.assignments.manage | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| job.post | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| job.apply | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| crm.clients.manage | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| crm.leads.manage | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| invoices.create | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| invoices.update | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| invoices.payments.record | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| reports.view | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| worker.profile.manage | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| client.portal.view | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |

## Enforcement Notes
- Membership role is resolved from `company_memberships`.
- Super Admin bypasses company scoping but all actions are still audited.
- Any request lacking a valid membership is rejected with 403.
