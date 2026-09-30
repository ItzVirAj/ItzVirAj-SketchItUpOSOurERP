# SketchItUp Owner OS — Architecture

> Living architecture reference for `ItzVirAj/ItzVirAj-SketchItUpOSOurERP`.
>
> Last reviewed: 30 September 2026
>
> Repository: https://github.com/ItzVirAj/ItzVirAj-SketchItUpOSOurERP

## 1. System Overview

SketchItUp Owner OS is an integrated business operating platform.

Current stack:

- **Frontend:** React + Vite
- **Backend:** Python + FastAPI
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL on Neon
- **Realtime/background infrastructure:** Redis
- **Object storage:** S3-compatible storage
- **API:** REST under `/api/v1`
- **Backend architecture:** modular monolith

Core principle:

**one business data model → multiple connected operational views → shared authorization, audit, notifications and integrations**

The application should evolve as one connected operating system, not as a collection of isolated CRUD modules.

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     React + Vite                        │
│                                                         │
│ Dashboard / CRM / Projects / Calendar / Sales /        │
│ Finance / Documents / Communications / Marketing       │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS REST / WebSocket
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI API                           │
│                                                         │
│ Core/Auth/RBAC                                          │
│ Projects & Tasks                                        │
│ Calendar                                                │
│ CRM                                                     │
│ Sales                                                   │
│ Finance                                                 │
│ Dashboard                                               │
│ Documents                                               │
│ Notifications                                           │
│ Communications + WebSocket                              │
│ Marketing                                               │
└───────────────┬───────────────────────────┬─────────────┘
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌─────────────────┐
        │ PostgreSQL    │          │ Redis           │
        │ Neon          │          │ pub/sub,        │
        │ business data │          │ realtime,       │
        │ audit data    │          │ background use  │
        └───────────────┘          └─────────────────┘
                │
                ▼
        ┌─────────────────┐
        │ S3-compatible   │
        │ object storage  │
        │ documents/files │
        └─────────────────┘
```

## 3. Frontend Layer

The frontend is responsible for:

- rendering business workflows and data views
- collecting user input
- calling backend APIs
- handling authentication state
- handling UI-level permission visibility
- showing loading, empty, success and error states
- maintaining appropriate local UI state
- opening WebSocket/realtime connections where supported

### Frontend rule

The frontend is **not** the source of truth for business rules.

Business validation, authorization, organization scoping, status transitions, ownership checks and audit requirements belong to the backend/database layer.

The frontend can mirror these rules for UX, but never for security.

## 4. Backend Layer

The backend is a **FastAPI modular monolith**.

The current entrypoint is:

`backend/app/main.py`

Registered API areas include:

- `/api/v1` — core/auth
- `/api/v1/projects`
- `/api/v1/calendar`
- `/api/v1/crm`
- `/api/v1/sales`
- `/api/v1/finance`
- `/api/v1/dashboard`
- `/api/v1/documents`
- `/api/v1/notifications`
- `/api/v1/communications`
- `/api/v1/marketing`

Communications also exposes a WebSocket router.

### Backend module pattern

Each module should own its:

- models
- request/response schemas
- routes
- module-specific services
- module-specific validation

Cross-cutting concerns should remain shared rather than duplicated.

## 5. Core / Platform Layer

The core module provides identity and authorization.

Current core entities include:

- `organizations`
- `users`
- `roles`
- `permissions`
- `user_roles`
- `role_permissions`
- `audit_logs`
- `auth_sessions`
- `login_attempts`

Current authentication flow:

```
Request
  ↓
Bearer access token
  ↓
JWT validation
  ↓
Current user lookup
  ↓
Permission / role check
  ↓
Organization-scoped application query
  ↓
Business operation
  ↓
Audit event
```

Current security foundations include:

- JWT access tokens
- refresh sessions using hashed tokens
- Argon2 password hashing
- permission dependencies
- organization-aware object lookups

## 6. Data Layer

PostgreSQL on Neon is the primary application datastore.

SQLAlchemy is the application ORM.

Current business models generally use:

- UUID identifiers
- `organization_id`
- foreign keys
- `created_at`
- `updated_at`

Where the base/platform model provides soft-delete support, it must be respected.

### Tenant isolation

Every organization-owned query must be scoped to the current user's:

`organization_id`

Any ID supplied by the client must be validated against the same organization before it is used.

Cross-tenant references must never be trusted merely because the UUID exists.

## 7. Canonical Business Relationships

The platform is intentionally relationship-driven.

Primary business chain:

```
Lead
  ↓
Client / Contact
  ↓
Proposal
  ↓
Contract
  ↓
Project
  ↓
Tasks / Calendar / Documents / Communications
  ↓
Milestones
  ↓
Invoices
  ↓
Payments
```

Marketing can feed the acquisition side:

```
Marketing Campaign
       ↓
Lead attribution
       ↓
Sales
       ↓
Revenue attribution
```

Notifications, audit and timeline/activity should observe important transitions in this graph.

## 8. Current Module Boundaries

### Core

Identity, organizations, users, roles, permissions, authentication sessions, login attempts and audit.

### Projects

Current entities:

- `projects`
- `tasks`

Projects can reference CRM clients.

Tasks belong to projects and can be assigned to users.

### Calendar

Current entity:

- `events`

Events can reference projects and are owned by the creating user.

### CRM

Current entities:

- `clients`
- `contacts`
- `crm_pipelines`
- `crm_pipeline_stages`
- `leads`
- `lead_activities`
- `lead_follow_ups`

The current backend contains validation for:

- pipeline/stage consistency
- organization ownership
- lead ownership
- active lead follow-up requirements
- lost-stage reason requirements
- client/contact organization ownership
- campaign organization ownership
- lead temperature values

### Sales

Current entities:

- `proposals`
- `contracts`

Contracts can reference proposals, leads, clients and projects.

### Finance

Current entities include:

- `invoices`
- `invoice_milestones`
- `payments`

The finance module also contains expense functionality.

Finance links invoices to clients, projects and contracts.

### Dashboard

Dashboard is an aggregation/read layer over operational data.

It should not become a second source of truth.

### Documents

Current entities:

- `document_folders`
- `documents`
- `document_versions`

PostgreSQL stores metadata while S3-compatible storage is intended for file objects.

### Notifications

Provides notification retrieval/read functionality and scheduled overdue notifications.

Notifications should be generated through shared backend services rather than recreated separately in every frontend screen.

### Communications

Current entities:

- `communication_channels`
- `communication_channel_members`
- `communication_channel_read_states`
- `communication_messages`

Realtime delivery uses Redis pub/sub plus FastAPI WebSockets.

### Marketing

Current entities:

- `marketing_channels`
- `marketing_campaigns`
- `marketing_campaign_channels`
- `marketing_content_items`
- `marketing_gigs`
- `marketing_bids`
- `marketing_metrics`
- `marketing_brand_assets`
- `marketing_outreach`

Marketing is connected to CRM through `leads.campaign_id` and includes KPI/attribution logic.

## 9. Cross-Cutting Services

### Authentication

One authentication mechanism should serve every module.

### Authorization

Permission checks should be centralized and applied consistently at route and object levels.

### Audit

Meaningful create/update/delete/status operations should create audit events.

### Notifications

Use one shared notification service for consistent delivery and metadata.

### Redis

Redis is infrastructure, not canonical business storage.

Use it for concerns such as:

- pub/sub
- realtime delivery
- rate limiting where implemented
- scheduler/job coordination
- future caching/background work

### Object storage

Binary documents/files belong in object storage.

PostgreSQL stores metadata, ownership and storage references.

## 10. API Architecture

Application endpoints should follow:

`/api/v1/<module>/<resource>`

Examples:

- `GET /api/v1/crm/leads`
- `POST /api/v1/crm/leads`
- `PATCH /api/v1/crm/leads/{lead_id}`
- `GET /api/v1/projects/{project_id}/tasks`
- `GET /api/v1/finance/invoices`

API conventions should be consistent for:

- UUID identifiers
- Pydantic request validation
- Pydantic response schemas
- HTTP status codes
- authentication errors
- authorization errors
- pagination
- filtering
- audit logging

Do not create a second API style inside an individual module without a documented architectural reason.

## 11. Database Migration Architecture

Database changes are migration-driven.

Rules:

1. Production schema changes must be represented in source control.
2. Add a numbered SQL migration for each schema change.
3. Keep migrations deterministic and defensive where practical.
4. Validate changes on a temporary Neon branch before production promotion.
5. Production changes require explicit approval.
6. Verify production after promotion.
7. Never silently rewrite an already-applied historical migration to hide a schema change.

Migration source location:

`db/migrations/`

The migration history is part of the architecture and must remain reproducible.

## 12. Security Architecture

Security is layered:

### Layer 1 — Authentication
Validate access tokens and active users.

### Layer 2 — Permission
Verify the caller can perform the operation.

### Layer 3 — Tenant scope
Verify all referenced objects belong to the caller's organization.

### Layer 4 — Object/business authorization
Verify the specific action is permitted for the target record and its current state.

### Layer 5 — Validation
Reject invalid references, values and state transitions.

### Layer 6 — Audit
Record security-sensitive and business-significant mutations.

UI permission hiding is useful for UX but is never a security boundary.

## 13. Realtime Architecture

Communications currently supports WebSocket delivery.

Flow:

```
Frontend
   ↓
WebSocket
   ↓
FastAPI WebSocket endpoint
   ↓
JWT + permission + channel-access checks
   ↓
Redis pub/sub
   ↓
Connected clients
```

Archived channels must not be treated as active realtime targets.

WebSocket authorization must remain consistent with REST authorization.

## 14. Background Processing

The backend currently starts an overdue-notification loop during application lifespan.

Current scheduled checks include operational records such as:

- CRM follow-ups
- tasks
- invoices

As the product expands, asynchronous work should move toward a centralized job abstraction instead of many independent module loops.

Potential job categories:

- email delivery
- calendar synchronization
- recurring invoice generation
- scheduled notifications
- report generation
- document processing
- meeting/AI processing
- webhook retries

## 15. External Integration Architecture

External systems should be isolated behind adapters/services.

Expected integration families include:

- Google Calendar / Meet / Drive / Gmail
- email providers
- S3-compatible storage
- payment gateways
- e-sign providers
- AI providers
- accounting integrations
- WhatsApp / Telegram
- GitHub / GitLab
- marketing platforms

External credentials must remain server-side.

Never expose provider secrets directly to the browser.

## 16. Frontend ↔ Backend Contract

For every feature, the intended flow is:

```
UI component
  ↓
Feature API client/service
  ↓
/api/v1 endpoint
  ↓
FastAPI request schema
  ↓
Authorization
  ↓
Organization/object validation
  ↓
Business operation
  ↓
PostgreSQL / Redis / storage
  ↓
Typed response
  ↓
Frontend state update
```

Each frontend feature should have an explicit mapping of:

- route/page
- UI component
- API client/service
- endpoint
- request payload
- response model
- permission
- loading state
- empty state
- error handling
- refetch/cache strategy
- realtime subscription, where applicable

Do not duplicate backend business rules inside individual React components.

## 17. Architectural Rules for Future Development

### Rule 1 — Preserve the modular monolith

Do not introduce microservices simply because the feature count grows.

### Rule 2 — One source of truth

Do not duplicate canonical business entities in separate modules.

### Rule 3 — Cross-module links are first-class

Prefer actual foreign keys/service relationships over string-only references.

### Rule 4 — Backend owns business rules

Frontend validation exists for user experience; backend validation is authoritative.

### Rule 5 — Organization scope is mandatory

All organization-owned reads and writes must enforce tenant isolation.

### Rule 6 — Audit important writes

Meaningful business and security state changes should be auditable.

### Rule 7 — Prefer reusable platform services

Auth, permissions, audit, notifications, jobs, timeline/activity, storage and integrations should be reusable infrastructure.

### Rule 8 — Use migrations

Database changes must be reproducible from repository history.

### Rule 9 — Avoid hidden coupling

Do not copy data from one module into another merely to simplify a screen.

### Rule 10 — Keep derived views derived

Dashboard, reports and KPI screens should calculate from canonical operational data.

## 18. Current Architectural Direction

The existing implementation is moving from a set of operational modules toward an integrated Owner OS.

The next architecture-level priorities are:

1. Universal activity/timeline model
2. Centralized automation/job framework
3. Stronger object-level authorization policy
4. Consistent pagination/filtering/query conventions
5. Explicit frontend API service layer
6. Automated test coverage
7. Integration adapters
8. End-to-end golden-path verification
9. Database integrity and tenant-isolation tests
10. Shared domain events for cross-module automation

## 19. Golden Business Flow

The architecture should support the following without unnecessary duplicate records:

```
Marketing / Inbound
        ↓
       Lead
        ↓
   Qualification
        ↓
     Proposal
        ↓
     Contract
        ↓
      Client
        ↓
     Project
        ↓
Tasks / Calendar / Communication / Documents
        ↓
     Milestones
        ↓
      Invoice
        ↓
      Payment
        ↓
 Revenue / Reporting / Timeline
```

A feature is architecturally complete when it connects correctly to the relevant parts of this graph.

## 20. Architecture Decision Record

### Baseline architecture

**React + Vite frontend + FastAPI modular monolith + PostgreSQL on Neon**

### Architectural intent

This structure provides:

- clear module boundaries
- shared database transactions
- centralized authorization
- organization/tenant scoping
- auditability
- relatively low operational complexity
- a direct path for future integrations and background jobs

### Do not introduce

- premature microservices
- frontend-only business workflows
- direct unmanaged production schema edits
- cross-tenant shortcuts
- duplicate canonical entities
- module-specific security models that bypass core authorization

## 21. Source-of-Truth Code Locations

When reviewing or implementing architecture, inspect the actual repository first.

Start with:

- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/db.py`
- `backend/app/modules/core/`
- `backend/app/modules/projects/`
- `backend/app/modules/calendar/`
- `backend/app/modules/crm/`
- `backend/app/modules/sales/`
- `backend/app/modules/finance/`
- `backend/app/modules/dashboard/`
- `backend/app/modules/documents/`
- `backend/app/modules/notifications/`
- `backend/app/modules/communications/`
- `backend/app/modules/marketing/`
- `db/migrations/`

The actual repository implementation takes precedence over assumptions.

## 22. Guidance for an AI Developer

Treat this document as the current architectural baseline, not as permission to invent a parallel architecture.

Before making a change:

1. inspect the repository and current implementation
2. identify the affected module and dependencies
3. inspect the database model and migration history
4. inspect current API conventions
5. inspect the current frontend/backend integration
6. preserve existing business workflows unless a requirement explicitly changes them
7. design the data flow before writing the UI
8. implement the smallest coherent change
9. add/update tests
10. verify the result
11. document any new architectural decision

For features touching multiple modules, explicitly design:

**entity → database relationship → API/service → authorization → audit → notification/domain event → frontend API client → UI**

Do not build a disconnected frontend screen and invent its backend linkage afterward.
