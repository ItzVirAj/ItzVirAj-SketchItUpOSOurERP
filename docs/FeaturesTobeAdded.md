# SketchItUp Owner OS — Features To Be Added

> Future implementation backlog derived from the Owner OS PRD and the current repository state.
>
> Last reviewed: 30 September 2026
>
> This document describes what still needs to be added or completed. It is not a claim that every item is required immediately.
>
> PRD source: `SketchItUp Owner OS PRD v1.0`

## 1. How to Read This Document

Feature status is divided into:

- **MISSING** — no meaningful implementation exists yet.
- **PARTIAL** — some backend/data/API support exists, but the required workflow is incomplete.
- **FRONTEND GAP** — backend capability exists but the user-facing feature is not connected.
- **HARDENING** — basic implementation exists but needs production-grade validation, authorization, constraints, tests or operational robustness.
- **INTEGRATION GAP** — internal capability exists, but the required external or cross-module connection is missing.

The current repository is backend-heavy. Therefore, many items below are **not requests to recreate backend functionality**; they are requests to connect, complete or extend what already exists.

---

# 2. Platform / Admin

## 2.1 Organization & Workspace

### PARTIAL
Complete the workspace/organization management experience.

Add:

- organization profile/settings UI
- business/legal details
- timezone
- locale/currency
- default working hours
- organization-level configuration
- workspace preferences

## 2.2 Users & Roles

### PARTIAL
Core users/roles/permissions exist.

Add:

- complete user management UI
- invite user flow
- activation/deactivation
- role assignment UI
- role/permission matrix
- user profile management
- organization membership management
- permission-aware navigation/actions
- secure session management UI

## 2.3 Security Administration

### HARDENING
Add:

- 2FA support
- session/device management
- login/security event views
- stronger rate-limit administration
- security audit views
- account recovery/password reset workflow
- configurable security policies

## 2.4 Audit

### PARTIAL
Audit logging exists.

Add:

- searchable audit log UI
- filters by user/action/entity/date
- entity-level history
- export
- immutable audit semantics
- consistent audit coverage across all modules

---

# 3. Home / Command Center / Dashboard

## 3.1 Real Home Dashboard

### FRONTEND GAP
Connect the existing dashboard aggregation APIs to the frontend.

Add:

- real pipeline snapshot
- active projects
- receivables/finance summary
- tasks/follow-ups due today
- overdue attention
- upcoming meetings
- recent activity
- notifications
- quick actions
- role-aware dashboard content

## 3.2 Founder / Owner View

Add:

- business health snapshot
- sales pipeline
- cash/receivables
- project delivery status
- team workload
- marketing performance
- overdue operational items
- high-priority approvals
- exception/attention feed

---

# 4. Calendar & Meetings

## 4.1 Complete Calendar

### PARTIAL
Basic events exist.

Add:

- day/week/month views
- event creation/edit/delete UI
- event detail drawer
- project/client/lead linking
- attendee support
- reminders
- recurring events
- calendar filters
- calendar search

## 4.2 Google Calendar

### INTEGRATION GAP
Add:

- Google OAuth connection
- calendar selection
- two-way synchronization
- sync status
- conflict handling
- event ownership mapping
- disconnect/reconnect flow

## 4.3 Google Meet

### INTEGRATION GAP
Add:

- create Meet link
- attach Meet to event
- display meeting link
- meeting status
- meeting metadata

## 4.4 Meeting Notes

### MISSING
Add:

- structured meeting notes
- attendees
- decisions
- risks
- open questions
- action items
- follow-up date
- project/client/lead linkage

## 4.5 Meeting → Action

### MISSING
Approved meeting action items must be able to create:

- tasks
- calendar follow-ups
- project actions
- notifications

## 4.6 Meeting Intelligence

### PHASE 2
Add upload-based meeting intelligence first.

Requirements:

- upload audio/transcript
- process summary
- extract decisions
- extract action items
- identify participants where possible
- human review
- approval before operationalization
- store approved summary
- create linked tasks only after approval

Do not make AI output directly modify operational records without human approval.

---

# 5. CRM

## 5.1 Complete CRM Frontend

### FRONTEND GAP
Build real CRM pages for:

- Kanban
- list
- lead detail
- client detail
- contacts
- activities
- follow-ups

## 5.2 CRM Search & Filters

### PARTIAL
Backend already supports several filters.

Add:

- saved filters
- filter presets
- advanced filtering
- clear/reset
- shareable team filters where required

## 5.3 Duplicate Detection

### MISSING
Add duplicate detection for:

- leads
- clients
- contacts

Potential matching fields:

- email
- phone
- company
- domain/name combinations

Provide user review before merge/delete.

## 5.4 Lead Scoring

### MISSING
Add:

- configurable scoring fields
- score calculation
- score display
- score history
- optional rule-based scoring first
- AI scoring later

## 5.5 Multiple Pipelines

### PARTIAL
Core pipelines/stages exist.

Add:

- pipeline management UI
- stage management UI
- probabilities
- stage ordering
- closed-won/closed-lost configuration
- pipeline selection per workflow

## 5.6 Email Templates / Sequences

### MISSING
Add:

- templates
- reusable variables
- approval
- scheduled sends
- sequence steps
- pause/stop
- activity logging
- unsubscribe/compliance controls where applicable

## 5.7 CRM Automations

Add:

- unowned lead assignment
- overdue follow-up escalation
- stage-change notifications
- won lead automation
- lost reason enforcement
- lead-to-client conversion workflow

---

# 6. Sales

## 6.1 Proposal Builder

### MISSING
Build a complete proposal workflow.

Add:

- proposal editor
- client/lead selection
- project selection
- title
- scope
- deliverables
- line items
- quantities
- rates
- discounts
- taxes
- totals
- terms
- validity
- notes
- reusable templates
- preview
- PDF/export
- share/send workflow

## 6.2 Proposal Lifecycle

### PARTIAL
Add controlled states:

- draft
- internal review
- approved
- sent
- viewed
- accepted
- rejected
- expired
- revised

Every transition should be audited.

## 6.3 Contracts

### PARTIAL
Add:

- contract numbering
- version/revision handling
- signed document linkage
- start/end dates
- status constraints
- approval flow
- e-sign integration
- contract-to-project conversion

---

# 7. Client / Lead → Project Conversion

### MISSING / INTEGRATION GAP

Implement the end-to-end Won Lead workflow:

```
Won Lead
  ↓
Create / select Client
  ↓
Create Project Draft
  ↓
Create Kickoff Task
  ↓
Create Project Folder Tree
  ↓
Create Project Communication Channel
  ↓
Create Initial Invoice / Schedule
  ↓
Notify assigned users
```

This is one of the most important cross-module automations.

The system should not require users to manually recreate the same business information across modules.

---

# 8. Projects & Delivery

## 8.1 Project Board

### PARTIAL
Add:

- Kanban
- statuses
- filters
- owner
- priority
- due dates
- client visibility where applicable
- drag/drop state transitions

## 8.2 Project Detail

Add:

- project overview
- client
- team
- timeline
- tasks
- milestones
- files
- communication
- financial status
- activity timeline

## 8.3 Task Management

### PARTIAL
Expand tasks with:

- task detail drawer
- subtasks
- dependencies
- priorities
- status history
- comments
- attachments
- mentions
- reminders
- recurring tasks
- task templates

## 8.4 My Tasks

### MISSING / FRONTEND GAP

Add:

- assigned tasks
- today
- upcoming
- overdue
- completed
- filters
- quick status updates
- bulk actions

## 8.5 Milestones

### MISSING / PARTIAL

Add:

- milestone model/workflow
- due dates
- owners
- approvals
- completion criteria
- client-visible status where required
- milestone → invoice trigger

## 8.6 Time Tracking

### PHASE 2

Add:

- timer/manual entry
- task/project linkage
- billable/non-billable
- approvals
- weekly timesheets
- utilization reporting

## 8.7 Capacity / Resource Planning

### PHASE 2

Add:

- team capacity
- workload
- allocation
- bottleneck visibility
- utilization reports
- assignment guidance

---

# 9. Files / Documents

## 9.1 File Library Frontend

### FRONTEND GAP

Build:

- folder tree
- file grid/list
- search
- filters
- upload
- preview
- download
- version history
- metadata
- linked client/project context

## 9.2 Folder Management

### PARTIAL

Add:

- create folder
- rename
- move
- nested folders
- delete/restore
- folder permissions
- internal/client visibility

## 9.3 File Versioning

### PARTIAL

Add:

- upload new version
- version list
- version comparison metadata
- restore/promote version
- version audit

## 9.4 Client Visibility

### MISSING

Every document intended for clients must explicitly declare visibility.

Internal-only documents must never leak into client views.

---

# 10. Communications

## 10.1 Chat Frontend

### FRONTEND GAP

Connect the existing REST/WebSocket backend.

Add:

- channel list
- message list
- composer
- unread counts
- mark as read
- realtime messages
- edits
- archive UI

## 10.2 Direct Messages

### MISSING

Add:

- one-to-one conversations
- conversation list
- unread state
- search

## 10.3 Threads / Replies

### MISSING

Add:

- reply-to-message
- thread view
- reply counts
- thread notifications

## 10.4 Mentions

Add:

- @mentions
- mention notifications
- mention search

## 10.5 Attachments

Add:

- file attachments
- upload progress
- secure download
- permission-aware file access

## 10.6 Communication → Work

Add explicit linking from messages to:

- tasks
- projects
- leads
- clients
- invoices
- documents

---

# 11. Marketing

## 11.1 Marketing Frontend

### FRONTEND GAP

Build real pages for:

- channels
- campaigns
- content calendar
- gigs
- bids
- metrics
- brand assets
- outreach
- KPIs
- attribution

## 11.2 Content Workflow

### PARTIAL

Add UI for:

- idea
- draft
- review
- approved
- scheduled
- published
- rejected

Show publish time and owner.

## 11.3 Marketing Calendar

Add:

- content calendar
- campaigns by date
- publishing schedule
- approval status
- workload

## 11.4 External Marketing Integrations

### PHASE 2 / 3
Possible integrations named by the PRD include:

- Mailchimp
- Brevo
- LinkedIn
- Instagram
- marketplace/platform integrations
- WhatsApp

Implement adapters rather than embedding provider-specific logic into core modules.

## 11.5 Marketing → Revenue

Ensure:

```
Campaign
  ↓
Lead attribution
  ↓
Won lead
  ↓
Contract
  ↓
Invoice
  ↓
Collected revenue
```

The existing backend has campaign attribution/KPI foundations; the frontend needs to make the connection visible and usable.

---

# 12. Finance

## 12.1 Finance Frontend

Build:

- invoice list
- invoice detail
- payment history
- aging
- expense list
- financial dashboard
- project/client financial view

## 12.2 Invoice Line Items

### MISSING

Add:

- item/description
- quantity
- unit price
- discount
- tax rate
- line total

Totals must be calculated consistently server-side.

## 12.3 Invoice Lifecycle

Add controlled states:

- draft
- issued
- partially paid
- paid
- overdue
- cancelled/void where permitted

Issued financial records must not be freely editable.

## 12.4 Credit Notes

### MISSING

Add:

- credit note entity
- numbering
- reason
- amount
- invoice linkage
- approval
- audit

## 12.5 Payment Corrections

### MISSING

Add controlled payment correction/reversal instead of deleting historical payments.

## 12.6 GST / Tax

### PARTIAL

Client records already support GST number.

Add:

- tax configuration
- GST details
- CGST/SGST/IGST logic as required by the product
- invoice tax breakdown
- tax reporting/export

Do not hard-code tax logic only in React.

## 12.7 Expense Approval

### MISSING

Add:

- expense states
- submit
- approve
- reject
- approver
- approval history

## 12.8 Recurring Invoices

### PHASE 2

Add:

- recurring schedule
- automatic draft generation
- approval/issue rules
- notifications
- failure/retry handling

## 12.9 Cash Flow

### PHASE 2

Add:

- receivables forecast
- expected inflow
- recurring revenue
- overdue impact
- basic cash-flow projection

---

# 13. People / HR

## 13.1 Employee Master

### MISSING / IN PROGRESS AREA

Add an employee master based on organization users, while excluding platform-only/server/admin identities as required by business rules.

Employee profile should include:

- employee profile
- department
- designation
- joining date
- reporting manager
- employment status
- documents
- emergency contact

## 13.2 Employee Documents

Add:

- identity documents
- offer/appointment documents
- policy acknowledgements
- secure access
- expiry reminders where applicable

## 13.3 Onboarding

### PHASE 2

Employee creation should trigger:

- onboarding checklist
- tasks
- document requirements
- notifications

## 13.4 HR Lite

### PHASE 2

Add:

- leave/basic attendance
- probation tracking
- employee notes
- basic compensation metadata if required
- HR reporting

Do not turn this into a full payroll system unless the product scope is explicitly expanded.

---

# 14. Knowledge Base

### MISSING

Add:

- knowledge home
- categories
- wiki pages
- search
- tags
- ownership
- version history
- publish/draft/review
- internal visibility
- client-visible knowledge where required

Phase 3 may add semantic/AI search.

---

# 15. Client Portal

### MISSING — PHASE 2

Add a dedicated client experience for:

- project status
- tasks/milestones visible to client
- files
- invoices
- payment status
- meeting links
- communication
- approvals
- shared documents

Strict rule:

**internal data must remain invisible to clients unless explicitly marked client-visible.**

Portal authorization must be enforced server-side, not merely through frontend route hiding.

---

# 16. Reports

## 16.1 Standard Reports

Add:

- sales pipeline
- lead conversion
- follow-up compliance
- project status
- task completion
- timesheet/utilization
- invoice aging
- revenue
- expenses
- marketing performance
- campaign attribution

## 16.2 Report Filters

Add:

- date ranges
- owner
- client
- project
- pipeline
- campaign
- status
- export

## 16.3 Custom Reports

### PHASE 3

Add configurable report builder only after standard reports are stable.

---

# 17. Support / AMC

### PHASE 2

Add:

- support tickets
- priority
- status
- assignee
- client/project linkage
- SLA tracking
- comments
- attachments
- AMC contracts
- renewal tracking
- escalation

Renewals approaching expiry should feed notifications and the dashboard.

---

# 18. Automation Engine

### MISSING — HIGH PRIORITY

Create a reusable automation/job framework.

Initial automations should include:

- won lead → client/project draft
- unowned lead → assignment/notification
- overdue follow-up → owner/founder escalation
- overdue task → assignee/PM notification
- approved milestone → invoice draft
- overdue invoice → reminder sequence
- approved meeting summary → tasks/channel updates
- employee created → onboarding
- renewal due soon → owner/founder notification

### Architecture requirement

Automations should be:

- idempotent
- auditable
- retryable
- permission-aware
- observable
- safe against duplicate execution

Do not create a separate ad-hoc scheduler for every feature.

---

# 19. Universal Activity / Timeline

### MISSING — HIGH PRIORITY

Create a reusable timeline/activity system across:

- leads
- clients
- contacts
- proposals
- contracts
- projects
- tasks
- meetings
- documents
- invoices
- payments
- communications
- employees

A single entity timeline should show:

- who did what
- when
- what changed
- source/module
- links to related records

The current CRM lead activity model should eventually fit into or coexist cleanly with this broader activity architecture.

---

# 20. Domain Events

### MISSING — HIGH PRIORITY

Introduce internal domain events for important state changes.

Examples:

- lead.won
- lead.created
- followup.overdue
- proposal.accepted
- contract.signed
- project.created
- milestone.approved
- invoice.issued
- invoice.overdue
- payment.recorded
- meeting.approved
- employee.created
- renewal.approaching

Events should enable notifications, automations and timeline updates without coupling every module directly to every other module.

---

# 21. Frontend Application Architecture

### HIGH PRIORITY

The existing frontend needs to evolve from a single shell into a feature-oriented application.

Add:

- authenticated route handling
- page-level modules
- shared layout
- reusable data table
- reusable Kanban
- drawers/modals
- forms
- toast/notification system
- skeleton loading states
- error boundaries
- empty states
- permission-aware UI
- centralized API client
- shared query keys
- typed request/response models
- consistent mutation/refetch handling

Recommended conceptual structure:

```
src/
├── app/
├── components/
├── layouts/
├── lib/
├── api/
│   ├── auth
│   ├── crm
│   ├── projects
│   ├── calendar
│   ├── sales
│   ├── finance
│   ├── documents
│   ├── communications
│   ├── marketing
│   └── dashboard
├── features/
│   ├── crm/
│   ├── projects/
│   ├── calendar/
│   ├── sales/
│   ├── finance/
│   ├── files/
│   ├── communications/
│   ├── marketing/
│   └── people/
└── styles/
```

This is a recommended organization, not a demand to rewrite the entire frontend in one change.

---

# 22. API / Backend Completion

For every UI feature, ensure there is a complete backend contract:

```
Frontend page
  ↓
API client
  ↓
FastAPI route
  ↓
Pydantic request schema
  ↓
Permission
  ↓
Tenant/object validation
  ↓
Service/business logic
  ↓
Database transaction
  ↓
Audit/domain event
  ↓
Response schema
  ↓
Frontend state update
```

Before adding a new endpoint, check whether the existing backend already supports the operation.

---

# 23. Integration Requirements

## Google Workspace

Add:

- Calendar
- Meet
- Drive
- Gmail
- contacts
- SSO where applicable

## Communication / Messaging

Potential later integrations:

- WhatsApp
- Telegram
- email
- inbound email

## Payments

Add payment-gateway adapter(s) when selected.

## E-sign

Add provider adapter for contract signing.

## Accounting

Potential:

- Tally
- Zoho or equivalent

## Developer Tools

Phase 3:

- GitHub
- GitLab

---

# 24. Search

### MISSING / PARTIAL

Build global search across:

- leads
- clients
- contacts
- projects
- tasks
- proposals
- contracts
- invoices
- files
- messages
- employees
- knowledge

Search should enforce organization and object-level visibility.

Target:

**fast search without exposing data the user cannot access.**

---

# 25. Notifications & Digests

### PARTIAL

Expand notifications into:

- in-app notifications
- unread counts
- notification preferences
- email notifications
- daily/weekly digests
- reminders
- escalation
- deep links to source records

Later:

- founder digest
- operational exception digest

---

# 26. Approvals

### MISSING / PARTIAL

Create reusable approval patterns for:

- proposals
- expenses
- invoices where required
- meeting summaries
- content
- contracts
- milestone approval

Each approval needs:

- requestor
- approver
- state
- timestamp
- decision
- comment
- audit event

---

# 27. File / Storage Hardening

Before production:

- validate upload permissions
- validate download permissions
- enforce client visibility
- checksum validation
- size/type restrictions
- storage-key isolation
- safe presigned URL handling
- orphan cleanup
- version integrity
- audit file access

---

# 28. Testing

### HIGH PRIORITY

Add automated coverage for:

## Unit

- service logic
- validators
- state transitions
- calculations

## API integration

- auth
- RBAC
- CRUD
- validation
- cross-module references

## Security

- cross-organization access attempts
- unauthorized actions
- role/permission matrix
- client portal isolation

## Database

- foreign keys
- unique constraints
- status constraints
- migration behavior

## Frontend

- critical components
- forms
- data fetching
- permission-aware rendering

## End-to-end

At minimum, cover the golden path:

```
Lead
 ↓
Proposal
 ↓
Contract
 ↓
Client
 ↓
Project
 ↓
Task/Meeting/Document
 ↓
Milestone
 ↓
Invoice
 ↓
Payment
 ↓
Reporting
```

---

# 29. Performance / Scalability

Add verification for PRD targets such as:

- common views < 2 seconds
- search < 1 second
- large Kanban views < 2 seconds

Focus on:

- pagination
- proper indexes
- avoiding N+1 queries
- query batching
- dashboard aggregation efficiency
- WebSocket connection lifecycle
- background job isolation

---

# 30. Deployment / Operations

Add:

- CI pipeline
- lint/type checks
- backend test execution
- frontend build checks
- migration validation
- deployment checks
- structured logs
- monitoring
- error tracking
- backup verification
- restore testing
- health/readiness endpoints

Production readiness should include verification of the stated availability, backup, RTO and RPO targets.

---

# 31. Phase Order

## Phase A — Stabilize Foundation

Do first:

1. backend/frontend integration layer
2. authentication UI
3. complete RBAC enforcement audit
4. tenant-isolation tests
5. universal timeline/activity
6. domain events/job framework
7. automated tests
8. CI
9. production observability

## Phase B — Finish Core Product

Then:

1. Home/dashboard
2. CRM frontend
3. Projects/task frontend
4. Calendar frontend
5. Google Calendar/Meet
6. Meeting notes/actions
7. Sales proposal builder
8. Finance frontend
9. Finance line items/tax/locking
10. Files/documents frontend
11. Communications frontend
12. Marketing frontend
13. Reports

## Phase C — Connect the Business

Build the complete lifecycle:

```
Marketing
   ↓
Lead
   ↓
Proposal
   ↓
Contract
   ↓
Project
   ↓
Delivery
   ↓
Milestone
   ↓
Invoice
   ↓
Payment
   ↓
Revenue / Reporting
```

Add the automations, notifications, activity timeline and cross-module links around it.

## Phase D — Phase 2

Then add:

- client portal
- HR lite
- support/AMC
- knowledge base
- timesheets
- capacity planning
- recurring invoices/cash flow
- meeting intelligence
- founder digest
- advanced automation

## Phase E — Phase 3

Only after the core operating workflows are stable:

- own products
- AI knowledge search
- lead scoring
- Git integrations
- custom reports
- OKRs
- white-label portal
- WhatsApp / advanced marketing integrations
- multi-entity finance

---

# 32. Feature Completion Standard

A feature should not be marked **COMPLETE** because a database table or API endpoint exists.

Mark a feature complete only when relevant layers are present:

```
Requirement
  ↓
Database
  ↓
Migration
  ↓
Backend model
  ↓
Request/response schema
  ↓
API/service
  ↓
Authorization
  ↓
Audit/event
  ↓
Frontend API client
  ↓
Frontend UI
  ↓
Loading/empty/error states
  ↓
Tests
  ↓
End-to-end verification
```

For integration features, also verify the actual external connection.

---

# 33. Important Non-Goals

Do not introduce these prematurely:

- microservices
- duplicated business entities
- frontend-only data stores for canonical records
- ad-hoc production SQL
- AI automation without human approval where the workflow requires review
- provider-specific business logic embedded throughout modules
- large rewrites merely to change folder structure

---

# 34. AI Developer Guidance

Use this document together with:

- `Architecture.md`
- `docs/architecture.md`
- `docs/CurrentState.md`
- the Owner OS PRD

Before implementing any item:

1. inspect the current repository
2. inspect the current backend route/model/schema
3. inspect the existing database migration
4. inspect current frontend structure
5. determine whether the feature is missing, partial or only disconnected
6. reuse existing entities and APIs where appropriate
7. add migrations only when the data model actually requires them
8. implement backend contract before frontend integration when backend support is missing
9. connect frontend to the real API
10. add permissions, audit and tests
11. verify the complete workflow
12. update this document when the implementation status changes

### Critical rule

**Do not implement a feature twice.**

Before creating a new model, endpoint or frontend data flow, search the repository for the existing implementation.

### Cross-module feature rule

For any feature crossing modules, document:

**source entity → target entity → database relationship → event/automation → API → permission → frontend client → UI → audit/test**

### Production rule

Never state that a feature, migration or integration is complete unless it has been actually implemented and verified in the target environment.

---

# 35. Final Product Direction

The desired end state is not a collection of independent pages.

It is one connected Owner OS where:

**marketing creates leads → CRM qualifies them → sales closes them → projects deliver them → documents/communications support delivery → milestones trigger billing → finance records payment → reports show the business → timeline/audit records the operational history.**

Every new feature should strengthen this connected operating model rather than create another isolated subsystem.
