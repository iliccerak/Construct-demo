# Payment & Invoice Workflows

MachWork supports **only** bank transfer and cash payments. All confirmations are manual and audited.

## Invoice Lifecycle

1. **Draft Creation** (optional in UI) → stored as `pending` once issued.
2. **Issue Invoice** → assigns the next sequential number for the company.
3. **Pending** → invoice awaits payment.
4. **Paid (Bank)** → requires bank transfer proof upload and reviewer confirmation.
5. **Paid (Cash)** → requires cash receiver identification.
6. **Overdue** → set manually or via scheduled job after due date.

## Sequential Numbering
- Each company has its own sequence (e.g., `MW-2025-0001`).
- Stored in `invoices.invoice_number` with a company unique constraint.

## Bank Transfer Workflow

1. Record payment intent with method `bank_transfer`.
2. Upload bank transfer proof (`bank_transfer_proofs`).
3. Authorized staff manually verifies proof.
4. Invoice status set to `paid_bank`.
5. Audit log entry recorded.

## Cash Workflow

1. Record payment with method `cash`.
2. Provide cash receiver name (`cash_received_by`).
3. Invoice status set to `paid_cash`.
4. Audit log entry recorded.

## Restrictions

- No automatic payment confirmations.
- No card or online payment gateways.
- Payments cannot exceed invoice total; partials require explicit line tracking.
