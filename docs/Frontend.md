# SketchItUp Owner OS — Frontend

> Frontend implementation and integration contract for ItzVirAj/ItzVirAj-SketchItUpOSOurERP.
>
> Last reviewed: 30 September 2026
>
> This document is the frontend source-of-truth for how the React application must connect to the existing FastAPI backend.
>
> Repository: https://github.com/ItzVirAj/ItzVirAj-SketchItUpOSOurERP

# 1. Current Frontend State

The current frontend is a minimal React/Vite shell.

Current tracked frontend files:

~~~
src/
├── App.tsx
├── main.tsx
└── styles.css
~~~

Current dependencies include:

- React
- React DOM
- Vite
- TypeScript
- TanStack React Query
- lucide-react
- Vitest

The current App.tsx provides the visual application shell, sidebar navigation, topbar, Home placeholder and a backend health check.

The navigation currently changes local state rather than routing to real module pages.

The current health integration is:

~~~
GET /api/v1/health
~~~

Vite currently proxies:

~~~
/api → http://localhost:8000
~~~

Frontend business requests should therefore use relative URLs such as:

~~~
/api/v1/crm/leads
/api/v1/projects
/api/v1/finance/invoices
~~~

Do not hard-code http://localhost:8000 throughout React components.

# 2. Frontend Architecture Target

The frontend should move from the current single-file shell to a feature-oriented application without duplicating backend business logic.

Recommended structure:

~~~
src/
├── app/
│   ├── AppRouter.tsx
│   ├── providers/
│   └── auth/
├── api/
│   ├── client.ts
│   ├── auth.ts
│   ├── dashboard.ts
│   ├── crm.ts
│   ├── projects.ts
│   ├── calendar.ts
│   ├── sales.ts
│   ├── finance.ts
│   ├── documents.ts
│   ├── notifications.ts
│   ├── communications.ts
│   └── marketing.ts
├── components/
│   ├── ui/
│   ├── data-table/
│   ├── kanban/
│   ├── drawers/
│   ├── forms/
│   └── feedback/
├── features/
│   ├── home/
│   ├── crm/
│   ├── projects/
│   ├── calendar/
│   ├── sales/
│   ├── finance/
│   ├── documents/
│   ├── communications/
│   ├── marketing/
│   └── people/
├── layouts/
│   ├── AppLayout.tsx
│   └── AuthLayout.tsx
├── lib/
│   ├── queryClient.ts
│   ├── permissions.ts
│   ├── formatters.ts
│   └── errors.ts
├── types/
└── styles/
~~~

This is a target structure, not a requirement to move every file in one change.

# 3. Core Rule: Backend Is the Source of Truth

The frontend must never become a second business backend.

React may:

- validate obvious form input
- show disabled actions
- format dates/currency
- optimistically update safe UI state
- cache API results
- provide loading/error UX

React must not be trusted for:

- permissions
- organization/tenant isolation
- financial rules
- state transitions
- ownership
- duplicate prevention
- contract/invoice lifecycle
- audit requirements

Every protected mutation must reach FastAPI, which performs the authoritative validation.

# 4. Frontend ↔ Backend Request Flow

Every feature should follow:

~~~
User action
   ↓
React component
   ↓
feature hook
   ↓
api/<module>.ts
   ↓
shared api/client.ts
   ↓
Bearer access token
   ↓
FastAPI /api/v1/...
   ↓
authentication
   ↓
permission
   ↓
organization/object validation
   ↓
business logic
   ↓
PostgreSQL / Redis / storage
   ↓
JSON response
   ↓
React Query cache
   ↓
UI
~~~

For mutations:

~~~
Form submit
   ↓
API mutation
   ↓
success → invalidate/refetch affected queries
failure → map backend error → show actionable message
~~~

Do not put raw fetch calls for business endpoints directly into page components.

# 5. Shared API Client

Create one shared API client such as src/api/client.ts.

Responsibilities:

- base URL handling
- JSON serialization
- Authorization header
- common headers
- response parsing
- consistent error object
- 401 handling
- refresh-token flow
- retry of the original request after successful refresh where safe
- avoid infinite refresh loops
- logout when refresh is invalid
- correlation/request ID support if later introduced

Preferred frontend usage:

~~~
api.get("/api/v1/crm/leads")
api.post("/api/v1/crm/leads", payload)
api.patch("/api/v1/crm/leads/{id}", payload)
~~~

Avoid multiple authentication implementations across components.

# 6. Authentication Integration

The backend currently provides:

~~~
POST /api/v1/auth/bootstrap
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
~~~

## Login

Use:

~~~
POST /api/v1/auth/login
~~~

The frontend must handle the returned access and refresh session using the application's chosen secure browser strategy.

Never expose token values in the UI, URL or logs.

## App bootstrap

After application startup:

~~~
GET /api/v1/auth/me
~~~

Use the response to establish:

- authenticated user
- organization
- role context
- permission-driven UI

## Refresh

When an access token expires:

1. attempt refresh
2. replace the access session
3. retry the original request once
4. prevent refresh loops
5. logout when refresh fails

## Logout

Use:

~~~
POST /api/v1/auth/logout
~~~

Clear frontend authentication state after the request.

# 7. Route Protection

The application should have public auth routes and protected application routes.

Target public routes:

~~~
/login
/auth/...
~~~

Target protected routes:

~~~
/
/calendar
/crm
/projects
/marketing
/files
/messages
/finance
/people
/knowledge
/reports
/admin
~~~

Unauthenticated users must not access protected pages.

The current local-state navigation pattern must be replaced by actual route navigation.

# 8. Permission-Aware Frontend

The backend already has permission concepts such as:

- users.read
- users.create
- roles.read
- audit.read
- dashboard.read
- projects.read
- projects.create
- tasks.read
- tasks.create
- calendar.read
- calendar.create
- crm.read
- crm.create
- sales.read
- sales.create
- finance.read
- finance.create
- finance.expenses.read
- finance.expenses.create
- notifications.read
- notifications.create
- communications.read
- communications.create
- marketing.read
- marketing.create

The frontend should use permission context to control:

- sidebar visibility
- page access
- action buttons
- edit controls
- delete controls
- approval actions

UI permission checks are UX only. Backend authorization remains mandatory.

# 9. Query / Cache Rules

TanStack React Query is already installed and should become the standard server-state layer.

Use stable query keys.

Examples:

~~~
["dashboard", "overview"]
["crm", "leads", filters]
["crm", "lead", leadId]
["projects"]
["projects", projectId]
["projects", projectId, "tasks"]
["calendar", "events", filters]
["sales", "proposals"]
["finance", "invoices"]
["finance", "summary"]
["documents", "folders"]
["communications", "channels"]
["communications", "messages", channelId]
["marketing", "campaigns"]
~~~

Mutation behavior should invalidate only affected queries.

Example:

~~~
Create task
  ↓
invalidate ["projects", projectId, "tasks"]
  ↓
invalidate dashboard queries if required
~~~

Do not refetch the entire application after every mutation.

# 10. Error Handling Contract

Convert backend errors into one consistent frontend error shape.

At minimum track:

- HTTP status
- backend detail/message
- field-level validation details when available
- retryability
- authentication state

Recommended behavior:

| Status | Frontend behavior |
|---|---|
| 400 | Show validation/business-rule error |
| 401 | Attempt refresh, otherwise logout |
| 403 | Show access denied / hide unavailable action |
| 404 | Show not found state |
| 409 | Show conflict and refresh relevant resource |
| 422 | Show field/form validation |
| 429 | Show rate-limit message |
| 500+ | Show server error + retry |

Do not replace actionable backend messages with an unhelpful generic message.

# 11. Loading / Empty / Error States

Every real page must have:

- initial loading state
- skeleton where appropriate
- empty state
- API error state
- retry action
- mutation pending state
- success feedback
- permission-denied state where relevant

Do not show fake zero values before a request succeeds.

# 12. HOME / DASHBOARD

Backend area:

backend/app/modules/dashboard/router.py

The dashboard backend provides aggregation endpoints covering areas such as:

- activity
- pipeline
- projects
- finance aging
- attention
- upcoming items
- overview-style data

Create:

src/api/dashboard.ts

Build components for:

- business snapshot
- pipeline summary
- active projects
- receivables
- overdue attention
- upcoming meetings
- activity
- notifications
- quick actions

Dashboard cards should navigate to canonical module routes.

Examples:

~~~
Pipeline → /crm
Projects → /projects
Receivables → /finance
Meeting → /calendar
Attention → exact source record
~~~

Dashboard must never create or store duplicate business records.

# 13. CRM FRONTEND

Backend base:

/api/v1/crm

Current backend resources include:

~~~
GET    /api/v1/crm/clients
POST   /api/v1/crm/clients
PATCH  /api/v1/crm/clients/{client_id}

GET    /api/v1/crm/clients/{client_id}/contacts
POST   /api/v1/crm/contacts

GET    /api/v1/crm/pipelines
GET    /api/v1/crm/pipelines/{pipeline_id}/stages

GET    /api/v1/crm/leads
POST   /api/v1/crm/leads
PATCH  /api/v1/crm/leads/{lead_id}

GET    /api/v1/crm/leads/{lead_id}/activities
POST   /api/v1/crm/leads/{lead_id}/activities

GET    /api/v1/crm/leads/{lead_id}/follow-ups
POST   /api/v1/crm/leads/{lead_id}/follow-ups
POST   /api/v1/crm/leads/{lead_id}/follow-ups/{follow_up_id}/complete

POST   /api/v1/crm/leads/bulk-stage
~~~

Target routes:

~~~
/crm
/crm/leads/:leadId
/crm/clients/:clientId
~~~

## CRM Kanban

Load:

~~~
pipelines
stages
leads
~~~

Use POST /api/v1/crm/leads/bulk-stage for bulk stage movement.

Do not update stage only in local state.

## Lead detail

Load:

- lead
- activities
- follow-ups
- client/contact
- campaign context

Use the existing API for create/update actions.

Respect backend rules for:

- active lead follow-up
- lost reason
- owner organization
- client/contact organization
- campaign organization
- pipeline/stage relationship
- temperature values

Surface backend validation errors directly.

# 14. PROJECTS FRONTEND

Backend base:

/api/v1/projects

Current endpoints:

~~~
GET    /api/v1/projects
POST   /api/v1/projects
PATCH  /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}

GET    /api/v1/projects/{project_id}/tasks
POST   /api/v1/projects/{project_id}/tasks

PATCH  /api/v1/projects/{project_id}/tasks/{task_id}
DELETE /api/v1/projects/{project_id}/tasks/{task_id}
~~~

Target routes:

~~~
/projects
/projects/:projectId
/projects/:projectId/tasks/:taskId
/tasks
~~~

Project detail should load the canonical project and its task list.

Task mutations use:

~~~
POST /api/v1/projects/{project_id}/tasks
PATCH /api/v1/projects/{project_id}/tasks/{task_id}
~~~

On success:

- invalidate task list
- refresh affected project summary
- refresh dashboard queries where relevant

When linking clients/projects, always persist UUIDs.

# 15. CALENDAR FRONTEND

Backend base:

/api/v1/calendar

Current endpoints:

~~~
GET    /api/v1/calendar
POST   /api/v1/calendar
PATCH  /api/v1/calendar/{event_id}
DELETE /api/v1/calendar/{event_id}
~~~

Target route:

~~~
/calendar
~~~

Use:

~~~
GET /api/v1/calendar
POST /api/v1/calendar
PATCH /api/v1/calendar/{event_id}
DELETE /api/v1/calendar/{event_id}
~~~

Backend validates event times.

The UI should prevent:

~~~
ends_at <= starts_at
~~~

Events can link to projects through project_id.

Populate project selectors from the real project API and submit the project UUID.

# 16. SALES FRONTEND

Backend base:

/api/v1/sales

Current resources:

~~~
GET    /api/v1/sales/proposals
POST   /api/v1/sales/proposals
PATCH  /api/v1/sales/proposals/{proposal_id}
POST   /api/v1/sales/proposals/{proposal_id}/send
POST   /api/v1/sales/proposals/{proposal_id}/accept

GET    /api/v1/sales/contracts
POST   /api/v1/sales/contracts
PATCH  /api/v1/sales/contracts/{contract_id}
POST   /api/v1/sales/contracts/{contract_id}/status
~~~

Target routes:

~~~
/sales
/sales/proposals
/sales/proposals/:proposalId
/sales/contracts
/sales/contracts/:contractId
~~~

Proposal forms should select canonical:

- lead
- client
- project

Sending uses:

~~~
POST /api/v1/sales/proposals/{proposal_id}/send
~~~

Accepting uses:

~~~
POST /api/v1/sales/proposals/{proposal_id}/accept
~~~

The accept response contains the created contract. Use that returned contract ID.

Do not assume acceptance succeeded before the API response arrives.

# 17. FINANCE FRONTEND

Backend base:

/api/v1/finance

Current endpoints include:

~~~
GET    /api/v1/finance/invoices
POST   /api/v1/finance/invoices
POST   /api/v1/finance/invoices/{invoice_id}/status
GET    /api/v1/finance/invoices/{invoice_id}/balance

POST   /api/v1/finance/invoices/{invoice_id}/milestones
GET    /api/v1/finance/invoices/{invoice_id}/milestones

POST   /api/v1/finance/invoices/{invoice_id}/payments

GET    /api/v1/finance/contracts/{contract_id}/invoice

GET    /api/v1/finance/expenses
POST   /api/v1/finance/expenses

GET    /api/v1/finance/summary
~~~

Target routes:

~~~
/finance
/finance/invoices
/finance/invoices/:invoiceId
/finance/expenses
~~~

Invoice detail loads:

~~~
invoice
balance
milestones
~~~

Payments use:

~~~
POST /api/v1/finance/invoices/{invoice_id}/payments
~~~

Never mark an invoice paid only in local state.

The backend controls payment balance and lifecycle.

# 18. DOCUMENTS / FILES FRONTEND

Backend area:

/api/v1/documents

Current infrastructure includes:

- folders
- documents
- document versions
- storage URL generation

Target routes:

~~~
/files
/files/folders/:folderId
/files/:documentId
~~~

Build:

- folder tree
- file grid/list
- upload
- preview
- download
- versions
- metadata
- client/project linking

Documents may reference:

- client_id
- project_id
- folder_id

Always persist real IDs.

For presigned upload/download:

~~~
Frontend requests URL
  ↓
Backend checks permission
  ↓
Backend creates short-lived URL
  ↓
Frontend transfers file
~~~

The frontend must never receive storage credentials.

# 19. COMMUNICATIONS FRONTEND

Backend base:

/api/v1/communications

Current REST resources include:

~~~
GET    /api/v1/communications/channels
POST   /api/v1/communications/channels

POST   /api/v1/communications/channels/{channel_id}/archive
POST   /api/v1/communications/channels/{channel_id}/unarchive

POST   /api/v1/communications/channels/{channel_id}/members
DELETE /api/v1/communications/channels/{channel_id}/members/{member_user_id}

GET    /api/v1/communications/channels/unread
POST   /api/v1/communications/channels/{channel_id}/read

GET    /api/v1/communications/channels/{channel_id}/messages
POST   /api/v1/communications/channels/{channel_id}/messages

PATCH  /api/v1/communications/messages/{message_id}
~~~

Target routes:

~~~
/messages
/messages/:channelId
~~~

Initial load:

1. load channels
2. load unread counts
3. select active channel
4. load messages
5. mark channel read

## Realtime

The backend WebSocket endpoint is:

~~~
/api/v1/communications/ws?token=<access_token>
~~~

The frontend should implement a dedicated WebSocket service.

Lifecycle:

~~~
login
  ↓
open socket
  ↓
authenticate
  ↓
receive message.created / message.updated
  ↓
update/invalidate message query
  ↓
update unread state
  ↓
reconnect after disconnect
~~~

Close the socket on logout.

Do not create duplicate sockets for the same authenticated session.

# 20. NOTIFICATIONS FRONTEND

Backend area:

/api/v1/notifications

Current capabilities include:

- list notifications
- unread filtering
- mark one read
- mark all read
- generate overdue notifications

Build:

- notification bell
- dropdown
- notification center
- unread count
- read state
- deep links

Where a notification provides a source entity/path, navigate to the canonical source rather than hard-coding unrelated pages.

# 21. MARKETING FRONTEND

Backend base:

/api/v1/marketing

Current resources:

~~~
/channels
/campaigns
/campaigns/{campaign_id}/channels
/content
/gigs
/bids
/metrics
/assets
/attribution
/kpi
/outreach
~~~

Target pages:

~~~
/marketing
/marketing/channels
/marketing/campaigns
/marketing/content
/marketing/gigs
/marketing/bids
/marketing/metrics
/marketing/assets
/marketing/outreach
~~~

Connect dashboard data from:

~~~
GET /api/v1/marketing/kpi
GET /api/v1/marketing/attribution
~~~

Campaign selectors must use real campaign UUIDs.

For CRM lead creation/update, campaign_id must reference a real marketing campaign.

For CSV import, show:

- uploading
- processing
- imported rows
- rejected rows
- errors
- final result

Do not show success until the backend confirms it.

# 22. PEOPLE / HR FRONTEND

People exists in the navigation, but the current repository has only a limited backend placeholder for this area.

Do not create a fake employee database in React.

For Employee Master, the eventual relationship is:

~~~
User
  ↓
Employee profile
  ↓
Department / designation / joining date / manager
  ↓
Documents / emergency contact / employment status
~~~

The backend contract must exist before the final HR UI is connected.

Use the canonical authenticated user IDs.

# 23. KNOWLEDGE / REPORTS / ADMIN

Do not invent permanent frontend data structures for backend modules that do not yet have a confirmed API contract.

Admin already has backend support for:

~~~
GET /api/v1/users
POST /api/v1/users
GET /api/v1/roles
GET /api/v1/permissions
GET /api/v1/audit
~~~

Connect these to:

- user list
- user creation
- role/permission display
- audit log

Knowledge and Reports should be connected only after their backend contracts are confirmed.

# 24. Global Search

The current shell search field is visual only.

Implement one authenticated search API rather than searching each module independently in the browser.

Conceptual flow:

~~~
search term
   ↓
GET /api/v1/search?q=...
   ↓
backend applies organization/object visibility
   ↓
typed result groups
   ↓
frontend result palette
   ↓
navigate to canonical record
~~~

Search results must contain real entity IDs.

# 25. Cross-Module Linking Rules

This is a core requirement.

Never use human-readable names as the primary relationship key.

Use UUIDs:

~~~
Lead.id
Client.id
Project.id
Proposal.id
Contract.id
Invoice.id
Task.id
Event.id
Document.id
~~~

Examples:

~~~
project.client_id
    ↓
/crm/clients/{client_id}
~~~

~~~
invoice.project_id
    ↓
/projects/{project_id}
~~~

~~~
proposal.lead_id
    ↓
/crm/leads/{lead_id}
~~~

The frontend should navigate through the same canonical records used by the backend.

# 26. Form Design Rules

Separate:

### Display value

What the user sees.

### Submitted value

What the backend receives.

Example:

~~~
Client selector
label = "Acme Industries"
value = client UUID
~~~

Do not submit a display name where the API expects client_id.

The same rule applies to:

- project selectors
- owner/assignee selectors
- campaign selectors
- pipeline/stage selectors
- proposal/contract links
- invoice references

# 27. Date / Time Handling

Backend uses timezone-aware datetimes.

Frontend should:

- keep API dates in ISO format
- parse explicitly
- display in user locale
- preserve timezone information
- submit ISO timestamps
- distinguish all-day and timed events

Do not use browser-local display formatting as the API storage format.

# 28. Currency / Finance Display

The server is authoritative for finance calculations.

Frontend should:

- format currency
- show currency code
- show tax/balance breakdown
- protect locked financial states
- submit numeric values matching backend schemas

Do not calculate important accounting totals only in React.

# 29. React Query Mutation Pattern

Use:

~~~
useQuery
  ↓
render data

useMutation
  ↓
submit API request
  ↓
onSuccess:
    invalidate targeted query keys
  ↓
onError:
    show backend error
~~~

Avoid global refresh behavior.

Avoid maintaining permanent copies of server entities in ad-hoc React context.

# 30. Realtime / Query Synchronization

Realtime events should update canonical React Query data.

Example:

~~~
message.created
  ↓
identify channelId
  ↓
update/invalidate ["communications","messages",channelId]
  ↓
increment unread state if channel inactive
~~~

Do not build a second message database in React state.

# 31. Frontend Security Rules

Never:

- put API secrets in frontend code
- put database credentials in frontend code
- put S3 secret keys in frontend code
- trust route hiding as authorization
- trust disabled buttons
- log access/refresh tokens
- persist provider secrets
- construct sensitive storage paths by guesswork

The current WebSocket token-in-query-string design should be reviewed before production deployment.

# 32. API Contract Types

Create TypeScript types matching backend schemas.

Recommended files:

~~~
src/types/api.ts
src/types/crm.ts
src/types/projects.ts
src/types/calendar.ts
src/types/sales.ts
src/types/finance.ts
src/types/documents.ts
src/types/communications.ts
src/types/marketing.ts
~~~

When an API schema changes:

1. update TypeScript type
2. update API client
3. update affected hooks/components
4. run typecheck
5. test the flow

Do not duplicate backend field definitions manually across many components.

# 33. Routing Map

Target application routing:

~~~
/                         Home
/calendar                 Calendar
/crm                      CRM
/crm/leads/:leadId        Lead detail
/crm/clients/:clientId    Client detail

/projects                 Projects
/projects/:projectId      Project detail
/tasks                    My Tasks

/marketing                Marketing
/marketing/campaigns      Campaigns
/marketing/content        Content
/marketing/outreach       Outreach

/files                    Files
/files/:documentId        Document detail

/messages                 Communications
/messages/:channelId      Channel

/finance                  Finance
/finance/invoices         Invoices
/finance/invoices/:id     Invoice detail
/finance/expenses         Expenses

/people                   People
/knowledge                Knowledge
/reports                  Reports
/admin                    Admin
~~~

The exact routing library may be selected during implementation, but routes must replace local active-state navigation.

# 34. Navigation → API Mapping

| Frontend module | Primary backend |
|---|---|
| Home | /api/v1/dashboard/* |
| Calendar | /api/v1/calendar/* |
| CRM | /api/v1/crm/* |
| Projects | /api/v1/projects/* |
| Marketing | /api/v1/marketing/* |
| Files | /api/v1/documents/* |
| Messages | /api/v1/communications/* + WebSocket |
| Finance | /api/v1/finance/* |
| People | backend contract to be completed |
| Knowledge | backend contract to be completed |
| Reports | backend/report contract to be completed |
| Admin | /api/v1/users, /roles, /permissions, /audit |

# 35. Frontend Implementation Order

## Step 1 — Application infrastructure

Create:

- router
- auth provider/state
- shared API client
- React Query configuration
- permission helper
- error handling
- protected routes

## Step 2 — Home

Connect the existing dashboard backend.

Replace every placeholder metric with real API data.

## Step 3 — CRM

Build:

- lead list
- Kanban
- lead detail
- clients
- contacts
- activities
- follow-ups

## Step 4 — Projects

Build:

- project list
- project detail
- task list
- task drawer
- task creation/update

## Step 5 — Calendar

Build:

- calendar view
- event CRUD
- project linking

## Step 6 — Sales

Build:

- proposals
- proposal builder
- send
- accept
- contracts
- status transitions

## Step 7 — Finance

Build:

- invoice list
- invoice detail
- balance
- payments
- milestones
- expenses
- summary

## Step 8 — Files

Build document/folder interface and storage integration.

## Step 9 — Communications

Build REST + WebSocket chat.

## Step 10 — Marketing

Connect all implemented marketing endpoints.

## Step 11 — Admin

Connect users, roles, permissions and audit.

## Step 12 — Remaining modules

Implement Knowledge, Reports, People and Client Portal only after their backend contracts are established.

# 36. Backend-First Integration Rule

When a UI control has no backend support:

~~~
DO NOT:
UI → local fake state

DO:
UI requirement
  ↓
check backend
  ↓
if missing:
    design backend contract
    ↓
    migration if needed
    ↓
    API
    ↓
    tests
    ↓
    frontend client
    ↓
    UI
~~~

This prevents the frontend from becoming a disconnected second system.

# 37. What Not To Do

Do not:

- create mock records as permanent product data
- hard-code dashboard values
- hard-code users/clients/projects
- keep fake arrays as permanent module data
- duplicate backend calculations
- create a second client model in React
- create a second task system in React
- bypass API calls for CRUD
- swallow backend errors
- use display names where UUIDs are required
- show success before the API confirms success
- silently ignore 401/403/409 responses
- make every component responsible for token handling

# 38. Frontend Testing Requirements

Test at minimum:

## Authentication

- login success
- login failure
- expired access token
- refresh success
- refresh failure
- logout
- protected route

## CRM

- lead loading
- filtering
- create
- stage update
- lost-stage validation
- follow-up completion

## Projects

- project loading
- task create/update
- invalid assignee response
- task deletion

## Finance

- invoice loading
- status transition errors
- payment over balance
- balance display

## Communications

- channel loading
- unread count
- message send
- edit
- reconnect
- archive behavior

## Forms

- backend validation display
- pending state
- success state
- retry state

# 39. End-to-End Frontend Regression Flow

The frontend must eventually pass this complete user journey:

~~~
Login
  ↓
Home loads live dashboard
  ↓
Open CRM
  ↓
Open Lead
  ↓
Create follow-up
  ↓
Move lead
  ↓
Open Client
  ↓
Open/Create Proposal
  ↓
Send Proposal
  ↓
Accept Proposal
  ↓
Open generated Contract
  ↓
Create/activate Project
  ↓
Create Task
  ↓
Create Calendar Event
  ↓
Open Files
  ↓
Upload/attach Document
  ↓
Open Communications
  ↓
Send Realtime Message
  ↓
Open Finance
  ↓
Create/issue Invoice
  ↓
Record Payment
  ↓
Return Home
  ↓
Verify dashboard/activity reflects changes
~~~

At each step verify:

- real API request
- correct UUID relationships
- authorization
- error handling
- cache invalidation
- UI state
- backend persistence

# 40. Definition of Frontend Complete

A frontend module is COMPLETE only when:

- route exists
- page exists
- API client exists
- authenticated request works
- response is mapped to typed UI data
- loading state works
- empty state works
- error state works
- mutations work
- cache invalidation works
- permissions are respected
- linked records navigate correctly
- backend validation is surfaced
- no permanent mock data remains
- tests cover critical behavior

For realtime modules, also require:

- connection
- authorization
- event handling
- reconnect
- cleanup on logout

# 41. AI Frontend Developer Instructions

Use this document together with:

- Architecture.md
- docs/CurrentState.md
- docs/FeaturesTobeAdded.md
- docs/Bugs&Fixes.md
- Owner OS PRD

Before touching frontend code:

1. inspect current React files
2. inspect backend router
3. inspect backend schemas
4. inspect relevant models/migrations
5. identify exact endpoint and permission
6. determine which fields are IDs versus display values
7. build/update API client
8. build query/mutation hook
9. build UI
10. connect real backend data
11. handle loading/error/empty states
12. test permission behavior
13. test cross-module links
14. update this document if the API contract changes

### Critical rule

DO NOT create a frontend implementation that bypasses the real backend.

For every feature, the AI must be able to answer:

~~~
What page?
What API?
What HTTP method?
What request body?
What response?
What permission?
What UUID relationships?
What mutation side effect?
What query gets invalidated?
What error states?
What route does the user navigate to?
~~~

If those answers are unknown, inspect the repository before coding.

# 42. Final Frontend Principle

The Owner OS frontend should feel like one connected application.

A user should be able to move naturally:

~~~
Lead
 → Client
 → Proposal
 → Contract
 → Project
 → Task
 → Meeting
 → Document
 → Communication
 → Invoice
 → Payment
 → Dashboard / Timeline
~~~

Every arrow must be backed by a real relationship and a real API contract.

The frontend is the operational interface.

The backend remains the source of truth.
