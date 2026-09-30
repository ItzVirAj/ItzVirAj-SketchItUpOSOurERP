# SketchItUp Owner OS — Bugs & Fixes

> Bug history, hardening record, known issues and verification guidance for the current repository.
>
> Last reviewed: 30 September 2026
>
> Repository: https://github.com/ItzVirAj/ItzVirAj-SketchItUpOSOurERP

## 1. Purpose

This document has two separate responsibilities:

1. record important bugs/issues that have already been fixed
2. record known remaining defects, risks and engineering debt

Do not confuse an incomplete feature with a runtime bug.

- **BUG** = something behaves incorrectly, crashes, violates an invariant, or allows an invalid state.
- **GAP** = required functionality does not exist yet.
- **HARDENING** = functionality exists but requires stronger validation/security/operational guarantees.
- **RISK** = a known architectural or deployment concern that may become a defect under certain conditions.

---

# 2. Recently Fixed Bugs / Hardening

The following fixes are evidenced by recent commits in the repository history.

## FIX-001 — Marketing campaign attribution metrics

**Status:** FIXED

Campaign attribution/KPI calculations were corrected so marketing attribution could be calculated against the connected CRM/sales data.

Commit:
`1719ef6f74b45ce8b38e00647f0309112b3ccc8d`

---

## FIX-002 — Communications member lookup

**Status:** FIXED

A communications membership lookup issue was corrected.

Commit:
`992310a75892834c1347ffafff831988a8dee7af`

---

## FIX-003 — Scheduler advisory-lock execution

**Status:** FIXED

The overdue-notification scheduler's advisory-lock execution path was corrected to avoid unsafe/incorrect concurrent execution.

Commit:
`94eceba5fe964cdf0bce0caa4cbe84f7aebaa387`

---

## FIX-004 — Finance schema validator indentation

**Status:** FIXED

A finance Pydantic/schema validation indentation defect was corrected.

Commit:
`d8ac5fb48054ea88d61a9e01ec796920344b47d5`

---

## FIX-005 — CRM bootstrap indentation

**Status:** FIXED

CRM bootstrap/setup logic had an indentation defect that was corrected.

Commit:
`abe17a8d2d1b8724db321821185908f115df2dad`

---

## FIX-006 — Audit timestamp type import

**Status:** FIXED

An audit-related timestamp type/import issue was corrected.

Commit:
`1aabdf0b0b3d4c06c8e5034435e6b1c03a006f98`

---

## FIX-007 — Email validation dependency

**Status:** FIXED

The backend dependency required for email validation was added.

Commit:
`567a5980f0a8324cbec815ea1a204db9b271cff0`

---

## FIX-008 — Project client organization validation

**Status:** FIXED

Project creation/update paths were hardened so referenced clients are validated against the current organization.

Commit:
`de46883cedc1dede4afbda85f26428bfbfd5fb2a`

This is important for tenant isolation.

---

## FIX-009 — CRM lead contact and temperature validation

**Status:** FIXED

CRM lead validation was hardened around:

- contact ownership/relationship
- allowed lead temperature values

Commit:
`019fd5fbd1f780f962304de813d2662fb8a91f6e`

---

## FIX-010 — Dashboard CRM metrics

**Status:** FIXED

CRM-related dashboard calculations were hardened.

Commit:
`833a297ad3f4aeca9a00753db910bc412951f798`

---

## FIX-011 — Finance payment lifecycle

**Status:** FIXED / HARDENED

Finance payment handling was hardened so payment recording is tied to an invoice lifecycle in which the invoice is already in a payment-eligible status.

Commit:
`1962a3662b7b45f4f3f04d96bd95408f10a7e929`

---

## FIX-012 — Proposal acceptance validation

**Status:** FIXED / HARDENED

Proposal acceptance was hardened to:

- prevent more than one contract being created for the same proposal
- validate the client through the proper organization-aware lookup

Commit:
`148e78968f69384d5bf4e857a66437b79f7e6b61`

---

## FIX-013 — Redis realtime reconnect handling

**Status:** FIXED / HARDENED

Realtime Redis reconnect behavior was hardened.

Commit:
`a951eff817f0629285a7288ed65e21cd1a64179c`

---

## FIX-014 — Archived channel message access

**Status:** FIXED / HARDENED

Archived communication channels were hardened so message access does not continue to behave like access to an active channel.

Commit:
`9ae38a62b9f9727152c4251dde90f04cb29b8f28`

---

## FIX-015 — Marketing content, gig and bid validation

**Status:** FIXED / HARDENED

The marketing module was hardened to reject invalid states including:

- invalid content workflow status
- scheduled/published content without publish time
- invalid content owner on update
- negative gig counters
- invalid bid status
- negative bid amount
- negative connects used

Commit:
`76358a14834d2620800727cdbcf7680175769949`

---

## FIX-016 — Marketing CSV import safety

**Status:** FIXED / HARDENED

Marketing CSV import handling was expanded with:

- validation
- idempotency behavior
- per-row savepoints
- safer row-level processing
- corrected import/metric handling

Relevant commits:

- `6976a820cbd3ae07536d33fbca0c8b32838bc8b0`
- `f0412986375ce7d5caad4743353f52bb32726f6e`
- `fe1bbf5da5326f2938e622846ceb834f7172e77b`

---

# 3. Known Remaining Bugs / Risks

These are not claimed as fixed. They should be verified during future implementation and testing.

## BUG/RISK-001 — Frontend is not connected to most backend modules

**Status:** OPEN

The current `src/App.tsx` is primarily a shell.

The navigation changes local state, while most module pages display placeholder/empty-state content.

The frontend currently demonstrates a backend health check, but not complete authenticated CRUD workflows for the operational modules.

### Impact

A large portion of the actual backend capability is inaccessible through the product UI.

### Fix

Create a real frontend API/client layer and connect each module page to its existing FastAPI endpoints.

---

## BUG/RISK-002 — Frontend authentication flow is incomplete

**Status:** OPEN

The current tracked frontend does not demonstrate the complete production authentication lifecycle.

### Fix

Implement:

- login page
- access-token handling
- refresh flow
- logout
- current-user bootstrap
- protected routes
- 401 recovery
- permission-aware navigation

The backend remains the authority for authentication/authorization.

---

## BUG/RISK-003 — Global search UI is currently non-functional

**Status:** OPEN

The shell contains a search field, but the current App implementation does not connect it to a global search backend.

### Fix

Implement authenticated global search across permitted entities and enforce organization/object visibility server-side.

---

## BUG/RISK-004 — WebSocket token transport risk

**Status:** OPEN RISK

The current communications WebSocket endpoint accepts the access token in the connection query string.

### Risk

Query-string credentials may be exposed in logs, monitoring systems, proxies or infrastructure traces depending on deployment.

### Fix

Evaluate a safer authentication mechanism for WebSockets, such as an appropriate secure handshake/token exchange pattern compatible with the deployment architecture.

Do not simply weaken authentication to remove the warning.

---

## BUG/RISK-005 — Document storage depends on deployment configuration

**Status:** OPEN RISK

The document module supports S3-compatible storage, but file operations depend on valid storage configuration.

### Possible failure

Upload/download functionality can be unavailable when the required storage environment variables are not configured.

### Fix

Add:

- deployment configuration validation
- clear readiness reporting
- safe operator diagnostics
- frontend error states
- storage connectivity checks

Do not expose storage credentials to the browser.

---

## BUG/RISK-006 — Inconsistent documentation locations

**Status:** OPEN

The repository currently contains:

- root `Architecture.md`
- `docs/architecture.md`

These files contain different levels of architectural documentation.

### Risk

Different AI/developers may read different architecture baselines.

### Fix

Use `docs/` as the canonical documentation area and either:

- consolidate the files later, or
- clearly define the root file as the top-level architecture entry point.

Do not maintain conflicting architectural rules.

---

## BUG/RISK-007 — Placeholder module directories

**Status:** OPEN ENGINEERING DEBT

Current backend tree includes directories such as:

- `people`
- `proposals`
- `files`
- `messaging`

with little/no implementation in the current snapshot, while related functionality is located in modules such as sales, documents and communications.

### Risk

Developers or AI systems may incorrectly create duplicate implementations.

### Fix

Before adding a module, search the repository and define the canonical implementation location.

Do not create a second People/HR, proposal, file or messaging system without an explicit architecture decision.

---

## BUG/RISK-008 — Incomplete tenant-isolation test coverage

**Status:** OPEN HIGH PRIORITY

The application has organization-aware backend lookups, but repository-level coverage needs systematic verification.

### Required tests

For each module:

- read another organization's record
- update another organization's record
- delete another organization's record
- use another organization's foreign-key ID
- access another organization's files
- access another organization's communication channel
- access another organization's invoice/client/project

### Expected result

Cross-organization operations must never succeed.

---

## BUG/RISK-009 — Authorization coverage needs a full endpoint matrix

**Status:** OPEN HIGH PRIORITY

Permission dependencies exist, but every endpoint still needs systematic verification.

### Audit

For every route verify:

```
Authentication
    ↓
Permission
    ↓
Organization scope
    ↓
Object authorization
    ↓
State-transition authorization
    ↓
Audit
```

Do not assume a route is safe merely because it has an authentication dependency.

---

## BUG/RISK-010 — Dashboard performance may degrade with data volume

**Status:** OPEN PERFORMANCE RISK

Dashboard endpoints aggregate data across several business areas.

As data grows, aggregation queries should be checked for:

- N+1 behavior
- repeated subqueries
- missing indexes
- unnecessary full-table scans
- excessive frontend refetching

### Fix

Benchmark realistic production-like volumes and optimize based on query plans rather than guessing.

---

## BUG/RISK-011 — Missing complete financial immutability controls

**Status:** OPEN

Finance currently has foundational lifecycle validation, but mature accounting controls still need implementation.

### Required

- issued-invoice edit lock
- credit-note corrections
- payment reversal/correction
- audit trail
- controlled status transitions
- line-item integrity

Do not solve accounting corrections by deleting historical records.

---

## BUG/RISK-012 — Proposal/contract workflow remains incomplete

**Status:** OPEN

A number of acceptance validations exist, but the complete lifecycle is not implemented.

### Required

- revision handling
- reject/expire states
- contract numbering
- signed document linkage
- e-sign integration
- complete approval workflow
- frontend lifecycle UI

---

## BUG/RISK-013 — Communications frontend/realtime verification is incomplete

**Status:** OPEN

The backend has REST and WebSocket infrastructure, but the complete frontend realtime experience still needs verification.

### Required tests

- connect
- authenticate
- join/subscribe
- receive message
- send message
- edit message
- unread state
- mark read
- archive behavior
- reconnect behavior
- authorization after reconnect

---

## BUG/RISK-014 — Background scheduler needs production observability

**Status:** OPEN

The overdue notification loop exists and has advisory-lock hardening.

It still requires operational verification for:

- failures
- retries
- duplicate notifications
- missed executions
- process restarts
- timezone behavior
- observability

### Fix

Move toward a centralized job system with:

- job IDs
- retry policy
- execution status
- idempotency
- structured logs
- failure visibility

---

## BUG/RISK-015 — Migration state can be misunderstood

**Status:** OPEN PROCESS RISK

A migration existing in Git does not prove it has been applied to production.

This is particularly important for:

`db/migrations/019_marketing_outreach.sql`

### Rule

Production migration state must be verified against the production database.

Documentation should distinguish:

- file exists
- migration prepared
- temporary branch verified
- production applied
- production verified

---

# 4. Recurring Bug Classes To Prevent

## 4.1 Cross-tenant references

Never trust UUIDs supplied by the frontend.

Bad:

```
db.get(Client, client_id)
```

without organization validation.

Correct pattern:

```
client_id + current organization
```

must be validated together.

---

## 4.2 Invalid state transitions

Do not allow arbitrary status strings from the frontend.

Every stateful entity should have:

- defined allowed states
- allowed transitions
- transition validation
- audit event

---

## 4.3 Duplicate side effects

Operations such as:

- proposal acceptance
- payment recording
- lead conversion
- invoice generation
- notifications
- automation jobs

must be idempotent where retries are possible.

---

## 4.4 Historical-record deletion

Financial, audit and operational history should not be "corrected" by deleting records when a controlled reversal/correction is required.

---

## 4.5 Frontend/backend contract drift

The frontend must not invent field names or status values that differ from FastAPI schemas.

Use a centralized API client and shared TypeScript types where practical.

---

## 4.6 Permission drift

A UI may hide a button, but the server must independently reject unauthorized requests.

Every new endpoint must be included in the permission matrix.

---

## 4.7 Database/application mismatch

ORM models and migrations must agree.

After schema changes verify:

- table exists
- columns exist
- foreign keys exist
- indexes exist
- constraints exist
- RLS/policies exist where applicable

---

## 4.8 Realtime race conditions

Realtime state must tolerate:

- reconnects
- duplicate delivery
- delayed delivery
- out-of-order UI events
- stale subscriptions
- archived entities

---

# 5. Bug Verification Checklist

Before declaring a bug fixed:

### Reproduce

Write down:

- endpoint/page
- input
- expected result
- actual result
- affected user/role

### Fix

Change the smallest correct layer.

Do not patch frontend symptoms when the actual defect is backend validation.

### Test

Test:

- normal case
- invalid case
- unauthorized case
- cross-tenant case
- boundary case
- retry/repeat case where relevant

### Verify persistence

Confirm the database contains exactly the expected state.

### Verify audit

Confirm the expected audit event exists for important mutations.

### Verify frontend

Confirm:

- success state
- loading state
- empty state
- error state
- retry state
- permission behavior

### Verify integration

For cross-module bugs, test the complete workflow rather than the isolated endpoint.

---

# 6. Golden Regression Suite

The following regression flow should become the primary business test:

```
Create Lead
   ↓
Assign Owner
   ↓
Schedule Follow-up
   ↓
Move to Qualified / Won
   ↓
Create Client
   ↓
Create Proposal
   ↓
Accept Proposal
   ↓
Create Contract
   ↓
Create Project
   ↓
Create Task
   ↓
Create Meeting
   ↓
Attach Document
   ↓
Approve Milestone
   ↓
Issue Invoice
   ↓
Record Payment
   ↓
Dashboard / Revenue / Timeline
```

At each step verify:

- organization ID
- permissions
- foreign keys
- audit
- notifications
- duplicate protection
- state transitions

---

# 7. AI Bug-Fixing Rules

An AI developer must follow these rules when fixing defects:

1. Reproduce or identify the defect from actual repository behavior before changing code.
2. Inspect the current implementation and recent commit history.
3. Do not create a second implementation to work around the bug.
4. Fix the root cause rather than masking the symptom.
5. Preserve existing working workflows.
6. Do not weaken authorization to make an endpoint work.
7. Do not bypass tenant checks.
8. Do not delete historical data as a shortcut for correction.
9. Add regression coverage for every important bug fix.
10. If a database change is required, create a migration.
11. Verify migration state separately from Git state.
12. For frontend defects, verify the backend contract before changing UI assumptions.
13. For realtime defects, test disconnect/reconnect behavior.
14. For scheduler defects, test duplicate execution and restart behavior.
15. Document the fix and its verification result here.

---

# 8. Bug Status Format

Use this format when adding new entries:

```
## BUG-XXX — <Title>

Status: OPEN / FIXED / VERIFIED / RISK / WONT-FIX

Area: <module>

Severity: CRITICAL / HIGH / MEDIUM / LOW

Symptom:
<what is wrong>

Root cause:
<why it happens>

Fix:
<what was changed>

Regression test:
<what test protects it>

Verification:
<how it was verified>

Commit:
<commit SHA>
```

---

# 9. Current Priority

The next defect-prevention work should focus on:

1. tenant-isolation tests
2. complete authorization matrix
3. frontend/backend contract tests
4. golden-path end-to-end tests
5. financial state/integrity tests
6. realtime reconnect tests
7. scheduler/job observability
8. document storage integration tests
9. dashboard performance testing
10. production migration verification

---

# 10. Final Rule

**A bug fix is not complete when the code compiles.**

It is complete when the defect is reproduced, corrected at the correct layer, regression-tested, security-checked, persisted correctly, audited where required, and verified through the affected user workflow.
