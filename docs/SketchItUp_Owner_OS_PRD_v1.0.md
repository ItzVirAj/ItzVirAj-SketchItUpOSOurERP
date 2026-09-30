# SketchItUp Owner OS — Product Requirements Document (PRD) v1.0

> Markdown conversion of the uploaded SketchItUp Owner OS PRD v1.0. Source terminology, requirement IDs, priorities, workflows and section order are preserved.

<PARSED TEXT FOR PAGE: 1 / 42>

---

S K E T C H I T U P S O L U T I O N S
SketchItUp Owner OS
Product Requirements Document (PRD)
One integrated platform to run every activity of Sketchitup Solutions: sales, delivery, marketing, 
people, money and knowledge.
Field Detail
Document version 1.0 (Draft for team review)
Prepared for Founder, Sketchitup Solutions; Development team
Product owner Founder (to be confirmed)
Status Ready for developer review and estimation
Date 29 September 2026
Classification Internal, confidential

---

<PARSED TEXT FOR PAGE: 2 / 42>

---

Table of Contents
# 1. Document Control & How to Use This PRD............................................................................................................. 4
1.1 Version history................................................................................................................................................... 4
1.2 How developers should read this document..................................................................................................... 4
1.3 Conventions....................................................................................................................................................... 4
# 2. Executive Summary ................................................................................................................................................. 5
2.1 Vision ................................................................................................................................................................. 5
2.2 Problem statement............................................................................................................................................ 5
2.3 Goals.................................................................................................................................................................. 5
2.4 Non-goals (Phase 1)........................................................................................................................................... 5
# 3. Scope, Assumptions & Constraints.......................................................................................................................... 6
3.1 In scope.............................................................................................................................................................. 6
3.2 Assumptions ...................................................................................................................................................... 6
3.3 Constraints......................................................................................................................................................... 6
3.4 Dependencies.................................................................................................................................................... 6
# 4. Users, Roles & Permissions...................................................................................................................................... 7
4.1 Roles .................................................................................................................................................................. 7
4.2 Permission matrix (summary)............................................................................................................................ 7
4.3 Key personas...................................................................................................................................................... 7
# 5. Product Principles & Module Map........................................................................................................................... 9
5.1 Design principles................................................................................................................................................ 9
5.2 Module map ...................................................................................................................................................... 9
# 6. Functional Requirements by Module .................................................................................................................... 10
6.1 Command Center (Dashboard & Home).......................................................................................................... 10
6.2 Calendar, Meetings & Meeting Intelligence.................................................................................................... 11
6.3 CRM & Sales Pipeline....................................................................................................................................... 13
6.4 Proposals, Quotations & Contracts ................................................................................................................. 15
6.5 Project & Delivery Management ..................................................................................................................... 16
6.6 Marketing, Brand & Lead-Generation Projects............................................................................................... 18
6.7 Document & Media Library ............................................................................................................................. 20
6.8 Team Communication & Notifications ............................................................................................................ 21
6.9 Client Portal ..................................................................................................................................................... 22
6.10 Finance, Invoicing & Compliance................................................................................................................... 23
6.11 Timesheets & Resource Planning .................................................................................................................. 25
6.12 People Operations (HR Lite) .......................................................................................................................... 26
6.13 Support, Maintenance & AMC....................................................................................................................... 27
6.14 Own Products & Roadmap (SaaS Portfolio)................................................................................................... 28
6.15 Knowledge Base, SOPs & Templates ............................................................................................................. 29
6.16 Assets, Tools & Credential Vault.................................................................................................................... 30

---

<PARSED TEXT FOR PAGE: 3 / 42>

---

6.17 Reporting & Analytics.................................................................................................................................... 31
6.18 Administration, Security & Settings............................................................................................................... 32
# 7. Cross-Module Workflows...................................................................................................................................... 33
End-to-end: Lead to cash....................................................................................................................................... 33
Meeting to action .................................................................................................................................................. 33
Support to product improvement ......................................................................................................................... 33
Marketing to revenue attribution ......................................................................................................................... 33
Standard automation rules to ship in Phase 1....................................................................................................... 33
# 8. Data Model Overview............................................................................................................................................ 34
# 9. Integrations............................................................................................................................................................ 35
9.1 Meeting Intelligence approach........................................................................................................................ 35
# 10. Non-Functional Requirements............................................................................................................................. 36
# 11. Suggested Technical Architecture ....................................................................................................................... 37
11.1 Architecture principles .................................................................................................................................. 37
11.2 Environments and delivery............................................................................................................................ 37
# 12. UX & Design Guidelines....................................................................................................................................... 38
12.1 Principles........................................................................................................................................................ 38
12.2 Primary navigation......................................................................................................................................... 38
12.3 Key screens (minimum) ................................................................................................................................. 38
# 13. Phased Release Plan ............................................................................................................................................ 39
Phase 1: Foundation MVP (about 10 to 12 weeks) ............................................................................................... 39
Phase 2: Scale and Automate (about 10 to 12 weeks) .......................................................................................... 39
Phase 3: Intelligence and Product Leverage (ongoing) ......................................................................................... 39
Suggested Phase 1 sprint sequence ...................................................................................................................... 39
# 14. Risks, Open Questions & Decisions...................................................................................................................... 40
14.1 Risk register ................................................................................................................................................... 40
14.2 Open questions for the founder.................................................................................................................... 40
# 15. Acceptance Criteria & Success Metrics................................................................................................................ 41
15.1 Sample acceptance criteria (format to follow).............................................................................................. 41
# 16. Glossary & Appendices........................................................................................................................................ 42
Appendix A: Requirement count by priority.......................................................................................................... 42
Appendix B: Reusing the master prompt............................................................................................................... 42
If the table of contents appears empty, right-click it in Word and choose Update Field.

---

<PARSED TEXT FOR PAGE: 4 / 42>

---

# 1. Document Control & How to Use This PRD
1.1 Version history
Version Date Author Change
0.1 29 Sep 2026 Founder + AI-assisted drafting Initial brainstorm captured
1.0 29 Sep 2026 Founder + AI-assisted drafting Comprehensive PRD for developer review
1.2 How developers should read this document
• Sections 2 to 5 give context, goals, users and the module map. Read these first so every developer shares 
the same picture.
• Section 6 is the core: one sub-section per module with requirement IDs (for example CRM-04). Use these 
IDs in tickets, commits and test cases.
• Priorities: P0 = must ship in Phase 1 (MVP), P1 = Phase 2, P2 = Phase 3 or later. Priorities can move only 
with the product owner's approval.
• Sections 7 to 12 cover cross-module flows, data, integrations, architecture, non-functional needs and 
design guidance.
• Sections 13 to 16 cover the release plan, risks, open questions and acceptance criteria. Open questions 
must be resolved before the relevant module starts.
1.3 Conventions
Term Meaning
Must / shall Mandatory requirement
Should Strongly recommended; can be deferred with justification
May Optional
Entity A stored business object such as Lead, Project or Invoice
Owner The user accountable for a record (not necessarily the creator)

---

<PARSED TEXT FOR PAGE: 5 / 42>

---

# 2. Executive Summary
2.1 Vision
Owner OS becomes the operating system of Sketchitup Solutions: the one place where the founder and team see 
leads, meetings, projects, deliverables, marketing progress, invoices and conversations, so the firm runs on 
process rather than memory. Sketchitup will use it first for itself (dogfooding). The lessons and reusable modules 
then feed the domain-specific SaaS products it builds for industrial and agribusiness clients.
2.2 Problem statement
• Leads, follow-ups and proposals are tracked manually, so hot leads can go cold unnoticed.
• Tasks, chats, meeting notes and files are spread across several tools; context is lost and status meetings 
take too long.
• Marketing work (social media, marketplace gigs and bids, outreach) has no measured link to revenue.
• Client files, videos and approvals are not organised per client, project and task.
• Finance visibility (receivables, project profitability, cash runway) requires manual consolidation, which is 
risky for a bootstrapped firm.
• Knowledge of how work is done sits in individuals, making onboarding slow and quality inconsistent.
2.3 Goals
# Goal Measure
G1 Single source of truth for all firm activity 90% of tasks, leads and meetings managed in Owner OS 
within 90 days
G2 Never miss a lead follow-up
Follow-up compliance above 90%; zero active leads 
without next action
G3 Predictable delivery On-time milestone rate above 85%; estimate accuracy 
within 20%
G4 Measurable marketing 100% of leads have source and campaign; monthly 
channel ROI report
G5 Faster cash collection Average days-to-collect reduced by 25%; overdue 
reminders automated
G6 Less meeting overhead 30% fewer status meetings; action items captured for 
100% of meetings
G7 Reusable foundation At least 3 modules reusable in client and SaaS products
2.4 Non-goals (Phase 1)
• Full accounting or payroll engine (Owner OS prepares data for the accountant; it does not replace the 
books).
• A full Slack, Zoom or Jira replacement; messaging and meetings stay lightweight and context-linked.
• Automated scraping or posting on marketplaces and social platforms (against their terms).
• Native mobile apps (mobile-responsive web only in Phase 1).

---

<PARSED TEXT FOR PAGE: 6 / 42>

---

# 3. Scope, Assumptions & Constraints
3.1 In scope
The 19 modules described in Section 6, delivered in three phases (Section 13). Scope covers the internal platform 
for Sketchitup Solutions, a limited client portal, and integrations listed in Section 9.
3.2 Assumptions
• Team size is small (roughly 3 to 15 internal users) with occasional freelancers.
• The firm uses Google Workspace (Gmail, Calendar, Meet, Drive).
• Clients are primarily in India (INR, GST), with occasional international clients.
• The in-house developers will build Owner OS part-time alongside client work.
• Budget is bootstrapped: prefer open-source components and pay-as-you-go cloud services.
3.3 Constraints
• No external funding; running cost should stay low at MVP.
• Developer bandwidth is limited; phases must be shippable in small increments.
• Marketplace platforms (Fiverr, Upwork) do not provide open APIs for gig or bid data.
• Meeting transcription depends on Google Workspace edition, consent from participants and privacy law.
3.4 Dependencies
• Google Cloud project with OAuth consent for Calendar, Meet and Drive scopes.
• Email sending domain with SPF, DKIM and DMARC configured.
• Payment gateway merchant account and GST registration details for invoicing.
• Cloud hosting account and object storage.

---

<PARSED TEXT FOR PAGE: 7 / 42>

---

# 4. Users, Roles & Permissions
4.1 Roles
Role Description and primary access
Founder / Owner Full access, all data including finance, HR and settings; approves proposals, discounts, 
change requests
Admin / Operations Operational configuration, users, templates, documents; no salary or restricted finance 
unless granted
Project Manager / Tech Lead Manage assigned projects, boards, sprints, estimates, releases, timesheet approval, 
project-level financial summary
Developer My tasks, boards of assigned projects, time logging, files, messaging, stand-ups, wiki
Designer / QA Same as Developer with design and testing views, bug tracker and approvals
Business Development / Sales CRM, proposals, calendar, marketing tracker; limited project view
Marketing Executive Marketing module, content calendar, asset library, lead source data
Finance / Accounts Invoices, payments, expenses, GST/TDS reports; read access to projects
Freelancer / Contractor Specific projects and folders only, time-boxed access, no company-wide data
Client (portal) Own projects, published files, approvals, invoices, tickets only
4.2 Permission matrix (summary)
Full = create, view, edit, delete. Edit = create, view, edit. View = read only. Assigned = only records assigned to the 
user. * = only projects the user manages. Detailed field-level rules are configured in ADM-02.
Area Founder Admin PM/Lead Dev Sales Mktg Finance Client
CRM & leads Full Full View - Full View View -
Proposals & 
contracts
Full Edit View - Edit - View Own
Projects & tasks Full Full Full* Assigned View Mktg 
only View Published
Calendar & meetings Full Full Full Own+team Full Full Own Invited
Marketing module Full Full View - View Full - -
Documents Full Full Project Project Client Assets Invoices Published
Messaging Full Full Full Full Full Full Full Project 
thread
Finance & invoicing Full Limited Project 
summary
- - - Full Own 
invoices
Timesheets Full Full Approve 
team
Own Own Own View -
HR & people data Full HR only Team basics Own Own Own Payroll 
inputs -
Credential vault Full Full Project Assigned - Channels - -
Settings & audit Full Full - - - - - -
4.3 Key personas

---

<PARSED TEXT FOR PAGE: 8 / 42>

---

Persona Daily goals Owner OS must give them
Nikhil, Founder See the health of the firm, close deals, 
unblock the team, keep cash healthy
Command center, pipeline, project health, 
receivables, approvals, weekly digest
Senior developer / tech 
lead
Plan sprints, review work, keep delivery on 
track
Boards, sprint tools, estimates, release notes, 
capacity view
Junior developer Know what to do today, log time, ask for 
help
My Tasks, stand-up entry, notifications, wiki, 
chat
Business development Never miss a follow-up, send proposals fast CRM, templates, follow-up alerts, proposal 
tracking
Marketing executive Publish consistently, track what converts Content calendar, gig and bid tracker, 
attribution
Client stakeholder Know progress without chasing, approve 
quickly Portal with status, files, approvals, invoices

---

<PARSED TEXT FOR PAGE: 9 / 42>

---

# 5. Product Principles & Module Map
5.1 Design principles
• One data model, many views: a task appears on a Kanban board, the calendar, My Tasks and reports, 
always from the same record.
• Everything links to a client, project or lead so context follows the work.
• Lean first: ship the simplest workflow that removes manual effort, then iterate.
• Follow-up by design: the system nudges people; nothing depends on memory.
• Human in control of AI: AI drafts, humans approve.
• Secure by default: least privilege, explicit client visibility, full audit.
• Configurable, not custom-coded: stages, fields, templates and automations are settings, so new needs do 
not require releases.
5.2 Module map
Group Modules Phase focus
Grow CRM (CRM), Proposals & Contracts (SAL), Marketing & Lead-gen (MKT) Phase 1
Deliver Projects (PRJ), Calendar & Meetings (CAL), Documents (DOC), Client 
Portal (PORT), Support & AMC (SUP) Phase 1 to 2
Collaborate Command Center (DASH), Communication (COMM), Knowledge Base 
(KB) Phase 1 to 2
Money Finance & Compliance (FIN), Timesheets & Resources (TIME) Phase 1 to 2
People & Assets HR Lite (HR), Assets & Vault (VAULT) Phase 2
Products Own Products & Roadmap (PROD) Phase 3
Insight & Control Reporting (RPT), Administration & Security (ADM) Phase 1 onwards

---

<PARSED TEXT FOR PAGE: 10 / 42>

---

# 6. Functional Requirements by Module
Requirement IDs are stable. Priority key: P0 = Phase 1 (MVP), P1 = Phase 2, P2 = Phase 3 or later.
6.1 Command Center (Dashboard & Home)
Purpose
A single landing screen that tells the founder and each team member what needs attention today across sales, 
delivery, money and people.
Features and requirements
ID Requirement Priority
### DASH-01 Role-based home dashboard: Founder view (business health), Developer view (my tasks, today's 
meetings, mentions), Sales view (my leads, follow-ups due) P0
### DASH-02 Today panel: meetings, tasks due, follow-ups due, overdue items, pending approvals P0
### DASH-03 Business snapshot widgets: pipeline value by stage, active projects with RAG status, revenue this 
month, receivables outstanding, cash-in forecast P0
### DASH-04 Team snapshot: who is on leave, workload heat-map, timesheet compliance P1
### DASH-05 Global search across leads, clients, projects, tasks, documents, messages, wiki (permission aware) P0
### DASH-06 Quick-add (+) menu: lead, task, meeting, note, expense, ticket from anywhere; keyboard 
shortcuts P1
### DASH-07 Personal notification centre and unread counters (see COMM module) P0
### DASH-08 Customisable widgets and saved views per user P2
Business rules
• Every widget must respect the viewer's permissions; a developer must never see revenue or salary data 
unless granted.
• Dashboard data refreshes at most every 5 minutes; drill-down opens the underlying filtered list.
Main data entities
Widget, SavedView, GlobalSearchIndex

---

<PARSED TEXT FOR PAGE: 11 / 42>

---

6.2 Calendar, Meetings & Meeting Intelligence
Purpose
One calendar for tasks, meetings, stand-ups, deadlines and follow-ups, with client linkage, Google Meet links and an 
AI assistant that turns meetings into summaries and action items.
Features and requirements
ID Requirement Priority
### CAL-01 Unified calendar with day, week, month and agenda views; colour-coded by type (meeting, 
stand-up, task, deadline, follow-up, leave, milestone) P0
### CAL-02 Create events with title, type, participants (internal users and external emails), linked 
client/lead/project/task, agenda, location or link, reminders P0
### CAL-03 Two-way sync with Google Calendar; auto-generate a Google Meet link when Meet is chosen; 
invites sent to attendees P0
### CAL-04 Recurring events (daily stand-up, weekly review, monthly finance review) with per-occurrence 
exceptions P0
### CAL-05 Availability and conflict detection; suggest free slots for selected participants P1
### CAL-06 Daily stand-up template: each developer records yesterday / today / blockers in the event or 
asynchronously; blockers auto-create flagged tasks P0
### CAL-07 Tasks with due dates appear on the calendar; drag to reschedule; drag from calendar to project 
board P1
### CAL-08 Meeting notes editor attached to each event with agenda, decisions and action-item blocks; 
action items convert to tasks with assignee and due date in one click P0
### CAL-09 Meeting Intelligence Bot (see workflow CAL-W2): joins or ingests the meeting, produces 
transcript, summary, decisions, action items, client commitments and follow-up email draft P1
### CAL-10 Consent controls: bot only records or transcribes when the organiser enables it; participants are 
informed in the invite and at meeting start; per-client opt-out flag P1
### CAL-11 Client-facing booking page (discovery-call scheduler) that creates a lead and a meeting when 
booked P1
### CAL-12 Reminders by in-app, email and optional WhatsApp/push; configurable lead time P0
### CAL-13 Meeting history per client and per project (timeline view) with searchable summaries P1
### CAL-14 Time zone support per user and per event (clients may be outside India) P1
Key workflows
CAL-W1: Schedule a client meeting
# 1. User clicks New Event and selects type Client Meeting.
# 2. Selects client or lead; contacts auto-suggest as attendees.
# 3. Adds agenda, picks slot (system flags conflicts), toggles Google Meet.
# 4. System creates Google Calendar event and Meet link, sends invites, logs an activity on the client timeline.
# 5. Reminders fire before start; on completion the user is prompted to add notes or confirm the AI summary.
CAL-W2: Meeting summarisation
# 1. Organiser enables Meeting Intelligence on the event (default off for clients until consent policy is set).
# 2. Bot obtains the transcript through the chosen capture method (Phase 1: upload of Google Meet 
transcript/recording; Phase 2: automatic ingestion via Workspace APIs or a meeting-bot service).

---

<PARSED TEXT FOR PAGE: 12 / 42>

---

# 3. AI pipeline produces: 5-line summary, key discussion points, decisions, action items with suggested owner and 
due date, open questions, client requirements captured.
# 4. Organiser reviews and edits in a review screen; nothing is shared until approved.
# 5. On approval, action items become tasks, requirements are appended to the linked project or lead, and an 
optional follow-up email draft is created.
Business rules
• Recording or transcription requires explicit consent; store consent status on the event.
• Raw audio/video is retained for a configurable period (default 30 days) after which only the approved 
summary and transcript remain.
• AI output is always a draft until a human approves it.
• Transcript access follows the same permission scope as the linked client or project.
Main data entities
Event, EventAttendee, Reminder, StandupEntry, MeetingNote, Transcript, MeetingSummary, ActionItem, 
ConsentRecord

---

<PARSED TEXT FOR PAGE: 13 / 42>

---

6.3 CRM & Sales Pipeline
Purpose
Capture every lead from every source, move it through a visible pipeline, and never miss a follow-up. Covers 
Kanban boards, activity tracking and conversion to client and project.
Features and requirements
ID Requirement Priority
### CRM-01 Lead capture: manual entry, web form, CSV import, email-to-lead, marketplace inquiry entry 
(Fiverr/Upwork), referral, event/LinkedIn outreach P0
### CRM-02 Lead fields: name, company, industry vertical, contact person(s), phone, email, source, campaign, 
estimated value, expected close date, requirement summary, owner, tags, temperature (Cold / 
Warm / Hot)
P0
### CRM-03 Kanban pipeline with configurable stages. Default: New, Contacted, Qualified, Discovery Done, 
Proposal Sent, Negotiation, Won (Converted), Lost (Closed), On Hold P0
### CRM-04 Temperature tagging (Cold / Warm / Hot) independent of stage, with rule-based suggestions (for 
example Hot when proposal opened twice) P0
### CRM-05 Multiple pipelines (Custom Software, SaaS Subscription, Maintenance/AMC, Marketplace Gigs) 
each with its own stages P1
### CRM-06 Activity log per lead: calls, emails, WhatsApp, meetings, notes; log from calendar and email 
automatically P0
### CRM-07 Follow-up engine: next-action date mandatory on active leads; overdue follow-ups escalate on 
dashboard and notifications P0
### CRM-08 Lost reason capture (price, timing, competitor, no response, scope mismatch, other) with notes; 
win/loss analytics P0
### CRM-09 Convert lead to Client + Contact + Project draft in one action; carries requirements, files and 
history P0
### CRM-10 Account and contact management: multiple contacts per client, roles (decision maker, technical, 
finance), communication preferences, birthdays/anniversaries P0
### CRM-11 Lead scoring (fit and engagement) with configurable rules P2
### CRM-12 Email templates and sequences (intro, follow-up 1/2/3, post-proposal nudge); tracked opens 
where supported P1
### CRM-13 Duplicate detection on email, phone and company name with merge tool P1
### CRM-14 Sales forecast: weighted pipeline by stage probability, monthly and quarterly view P1
### CRM-15 Saved filters and list view alongside Kanban; bulk actions (assign, tag, move stage) P0
### CRM-16 Referral tracking: who referred, referral thanks/commission notes P2
Key workflows
CRM-W1: Lead to Won
# 1. Lead enters via any source and lands in New with owner assigned automatically or manually.
# 2. Owner makes first contact within SLA (default 24 hours); activity logged; stage moves to Contacted.
# 3. Qualification checklist (budget, authority, need, timeline) completed; stage moves to Qualified or Lost with 
reason.
# 4. Discovery call scheduled from the lead card; meeting notes attached; requirements captured.
# 5. Proposal created from template (see SAL module) and sent; stage moves to Proposal Sent.

---

<PARSED TEXT FOR PAGE: 14 / 42>

---

# 6. Follow-ups run on the follow-up engine; negotiation notes recorded.
# 7. On acceptance, mark Won: system creates Client, Project draft, contract task and invoice milestone plan.
Business rules
• A lead cannot leave New without an owner.
• Active leads must always have a next follow-up date.
• Moving to Lost requires a reason.
• Won leads become read-only in the pipeline but remain linked to the client and project.
Main data entities
Lead, Pipeline, Stage, Account/Client, Contact, Activity, FollowUp, LostReason, EmailTemplate, Source, Campaign

---

<PARSED TEXT FOR PAGE: 15 / 42>

---

6.4 Proposals, Quotations & Contracts
Purpose
Turn a qualified lead into a signed engagement quickly and consistently, with reusable templates, pricing, approvals 
and e-signature.
Features and requirements
ID Requirement Priority
### SAL-01 Proposal builder from templates: scope, deliverables, timeline, assumptions, exclusions, team, 
pricing, payment milestones, terms P0
### SAL-02 Pricing models: fixed price, time and material, monthly retainer, SaaS subscription, AMC; INR 
default with multi-currency option P0
### SAL-03 Rate card and effort estimator (roles x days) feeding the quote; margin visibility (internal only) P1
### SAL-04 Versioning of proposals with change history and comparison P1
### SAL-05 Shareable proposal link with view tracking (opened, time spent) and accept/decline action P1
### SAL-06 Contract templates (MSA, SOW, NDA, SaaS agreement) with merge fields; e-signature integration 
or signed-PDF upload P0
### SAL-07 Internal approval for discounts above threshold P2
### SAL-08 Signed documents auto-stored in the client folder and linked to the project P0
### SAL-09 Renewal and expiry reminders for AMC, SaaS subscriptions and NDAs P1
Key workflows
SAL-W1: Proposal to signed contract
# 1. From the lead card choose Create Proposal and pick a template.
# 2. Estimator fills effort and price; system computes totals, taxes and milestone schedule.
# 3. Founder reviews and approves; proposal is shared by link or PDF.
# 4. Client views or accepts; activity is logged and the lead temperature updates.
# 5. Contract generated from template, sent for e-signature, stored on completion.
# 6. Project and invoice schedule are auto-created from the accepted proposal.
Business rules
• Every proposal must reference a lead or client.
• Accepted proposal values lock; changes require a new version or a change request.
• GST is applied per client state and registration status.
Main data entities
Proposal, ProposalVersion, ProposalItem, RateCard, Contract, ContractTemplate, Signature

---

<PARSED TEXT FOR PAGE: 16 / 42>

---

6.5 Project & Delivery Management
Purpose
Plan, assign, track and deliver client projects and internal projects on Kanban boards, with sprints, milestones, bugs, 
releases and client visibility.
Features and requirements
ID Requirement Priority
### PRJ-01 Project record: client, type (Custom build, SaaS product, Maintenance, Internal, Marketing), 
scope reference, start/end, budget (hours and money), PM, team, status, RAG health P0
### PRJ-02 Kanban board per project with configurable columns (default: Backlog, To Do, In Progress, In 
Review, QA/Testing, Blocked, Done) P0
### PRJ-03 Task fields: title, description (rich text), assignee, reporter, priority, type (feature, bug, chore, 
research), estimate, due date, labels, sprint, milestone, dependencies, attachments, checklist, 
watchers
P0
### PRJ-04 Sub-tasks, task templates and duplication P1
### PRJ-05 Board, list, timeline (Gantt) and calendar views; filter by assignee, label, sprint, priority P0
### PRJ-06 Sprints: planning, backlog grooming, burndown, velocity, carry-over rules P1
### PRJ-07 Milestones tied to payment milestones; completion can trigger invoice reminder P0
### PRJ-08 Comments with @mentions, threaded discussion, activity history per task P0
### PRJ-09 Bug tracker with severity, environment, steps to reproduce, attachments, linked build/release P1
### PRJ-10 Release management: release notes, version numbers, deployment checklist, rollback notes, 
environment (dev/staging/prod) P1
### PRJ-11 Change request workflow: request, impact analysis (effort, cost, timeline), approval, task 
creation, billing impact P0
### PRJ-12 Time tracking: start/stop timer or manual entry per task; billable flag P0
### PRJ-13 Project health: planned vs actual hours, budget burn, overdue tasks, blocked tasks, auto RAG P1
### PRJ-14 Project templates (for example SaaS MVP, Website, Mobile app, Data dashboard) with pre-built 
boards and checklists P1
### PRJ-15 Client visibility settings: which boards, milestones and files are visible in the client portal P1
### PRJ-16 Definition-of-done checklist per project and mandatory project closure review (lessons learned, 
final files, handover, feedback request) P1
### PRJ-17 Personal My Tasks view across all projects, grouped by due date P0
### PRJ-18 Git integration: link branches, pull requests and commits to tasks; status auto-update on merge P2
Key workflows
PRJ-W1: Project kickoff
# 1. Won lead auto-creates a project draft; PM assigned.
# 2. PM applies a project template, imports scope from the signed proposal as epics and tasks.
# 3. Team members are added with roles; kickoff meeting scheduled from the project.
# 4. Client folder structure is created automatically; client portal access invited.
# 5. Sprint 1 planned; milestones linked to payment schedule.
PRJ-W2: Task lifecycle

---

<PARSED TEXT FOR PAGE: 17 / 42>

---

# 1. Task created in Backlog or To Do with estimate and assignee.
# 2. Assignee moves to In Progress and logs time.
# 3. On completion moves to In Review; reviewer approves or returns with comments.
# 4. QA verifies; bugs are logged as linked tasks.
# 5. Done triggers milestone progress update and notifications.
PRJ-W3: Change request
# 1. Anyone raises a change request against a project (internal or via client portal).
# 2. PM estimates impact; founder approves, rejects or defers.
# 3. Approved: tasks and additional billing items are created; client is notified.
# 4. Rejected or deferred: reason recorded and shared with the client.
Business rules
• A task in Done requires no open blocking dependencies.
• Billable time can only be logged on projects with an active status.
• Only PM or founder can change project budget or milestone dates.
Main data entities
Project, Board, Column, Task, SubTask, Sprint, Milestone, TimeEntry, Bug, Release, ChangeRequest, 
ProjectTemplate, Label, Dependency

---

<PARSED TEXT FOR PAGE: 18 / 42>

---

6.6 Marketing, Brand & Lead-Generation Projects
Purpose
Manage Sketchitup's own growth as projects: social media presence, content calendar, campaigns, marketplace 
profiles and gigs (Fiverr, Upwork and similar), outreach, and the metrics that show what is working.
Features and requirements
ID Requirement Priority
### MKT-01 Marketing project type using the same Kanban engine, with templates (Social media launch, 
Content calendar, Outreach campaign, Marketplace profile setup, Case-study production) P0
### MKT-02 Channel registry: LinkedIn, Instagram, X, YouTube, website/blog, Fiverr, Upwork, Freelancer, 
Clutch/GoodFirms, directories; profile URL, owner, status, credentials pointer (to vault), goals P0
### MKT-03 Content calendar: post idea, channel, format (post, carousel, video, article), owner, approval 
status, publish date, asset links, caption, hashtags P0
### MKT-04 Content workflow: Idea, Draft, Design, Review, Approved, Scheduled, Published, Repurposed P0
### MKT-05 Campaign records: objective, audience, budget, duration, channels, UTM parameters, owner, 
linked leads generated P0
### MKT-06 Marketplace gig tracker: gig title, category, keywords, price packages, portfolio items, 
impressions, clicks, inquiries, orders, conversion rate, reviews, last optimised date (entered 
manually or via CSV import because marketplaces do not offer open APIs)
P0
### MKT-07 Marketplace proposal tracker (Upwork bids/connects): job link, bid amount, connects used, 
status (sent, viewed, interview, hired, declined), outcome and learning notes P0
### MKT-08 Outreach tracker: prospect list, message sequence step, response status, meeting booked; tie 
into CRM as leads on positive response P1
### MKT-09 Lead attribution: every lead carries source and campaign; funnel from impression to lead to 
proposal to won per channel P0
### MKT-10 Marketing KPIs: followers, impressions, engagement rate, website visits, leads, cost per lead, 
conversion, revenue per channel; monthly manual or CSV entry, optional API pulls later P1
### MKT-11 Weekly marketing checklist (post X times, respond to inquiries, update gigs, outreach quota) with 
streaks and reminders P1
### MKT-12 Asset library for brand kit, logos, templates, case studies, testimonials, demo videos P0
### MKT-13 Testimonial and case-study pipeline: request from client at project closure, approval status, 
publishing status P1
### MKT-14 Email newsletter or campaign integration (Mailchimp/Brevo) and subscriber sync P2
### MKT-15 SEO tracker: target keywords, ranking notes, blog backlog P2
Key workflows
MKT-W1: Launch social media presence
# 1. Create marketing project from the Social media launch template.
# 2. Tasks: define positioning, set up profiles, design brand kit, plan 30-day content calendar, write first 12 posts.
# 3. Content moves through the content workflow; approvals by founder.
# 4. Posts published; metrics logged weekly.
# 5. Monthly review: what worked, adjust calendar; hot engagement converts to CRM leads.
MKT-W2: Marketplace gig lifecycle
# 1. Create gig entry with keywords, packages and portfolio samples.

---

<PARSED TEXT FOR PAGE: 19 / 42>

---

# 2. Publish on the marketplace; record link and launch date.
# 3. Log weekly impressions, clicks and inquiries.
# 4. Inquiry becomes a CRM lead with source set to the marketplace.
# 5. Optimise gig every 2 to 4 weeks based on conversion; keep version notes.
Business rules
• Every marketing activity that can generate a lead must have a source value usable in CRM.
• Platform credentials are never stored in plain text here; only references to the vault.
• Do not automate scraping or posting that violates marketplace or social platform terms.
Main data entities
Channel, ContentItem, Campaign, Gig, MarketplaceBid, OutreachProspect, MarketingMetric, BrandAsset, 
Testimonial

---

<PARSED TEXT FOR PAGE: 20 / 42>

---

6.7 Document & Media Library
Purpose
Structured storage for client files, project deliverables, videos, contracts and internal documents, organised in 
folders that mirror clients, projects and tasks.
Features and requirements
ID Requirement Priority
### DOC-01 Automatic folder tree: Client > Project > (Requirements, Design, Development, QA, Deliverables, 
Contracts, Invoices, Meetings, Media); templates per project type P0
### DOC-02 Upload files and folders by drag and drop; multi-file; progress; resume on failure P0
### DOC-03 Attach files to tasks, leads, meetings, tickets and messages; they appear in the parent folder 
automatically P0
### DOC-04 Video support: upload, in-app player, thumbnail, optional link to YouTube/Drive/Loom instead of 
storing large files P0
### DOC-05 Versioning: new upload with same name creates a version; restore previous P1
### DOC-06 Permissions per folder: internal only, team, client-visible; inherits from project with overrides P0
### DOC-07 Preview for PDF, images, Office documents, video and code snippets P1
### DOC-08 Tags, description, search by name, tag, content (text extraction for PDF/Office) P1
### DOC-09 Shareable expiring links with optional password for external sharing P1
### DOC-10 Storage quotas per client and alerts; archive and retention policy on project closure P1
### DOC-11 Google Drive connector: link or sync selected folders P2
### DOC-12 Virus scan on upload; file type and size limits (configurable, default 2 GB per file) P0
### DOC-13 Audit trail: who viewed, downloaded, shared or deleted P1
Key workflows
DOC-W1: Client deliverable handover
# 1. Developer uploads final build notes and demo video into the Deliverables folder.
# 2. PM marks the folder client-visible and requests approval.
# 3. Client receives notification in the portal, downloads and approves.
# 4. Approval is logged; milestone and invoice reminder trigger.
Business rules
• Deleted files go to a recycle bin for 30 days.
• Client-visible content requires an explicit publish action; nothing is visible by default.
• Storage uses object storage with encryption at rest.
Main data entities
Folder, File, FileVersion, ShareLink, Tag, StorageQuota, AccessLog

---

<PARSED TEXT FOR PAGE: 21 / 42>

---

6.8 Team Communication & Notifications
Purpose
Lightweight messaging and a reliable notification system so the team sees what matters on login without leaving 
Owner OS. Not a Slack replacement; context-linked collaboration.
Features and requirements
ID Requirement Priority
### COMM-01 Channels: general, per-project auto-channels, per-client channels, private groups; direct 
messages
P0
### COMM-02 Text messages with formatting, emoji reactions, file attachments, @mentions, threads P0
### COMM-03 Message links to any object (task, lead, ticket, document) with rich preview P1
### COMM-04 Unread indicators, last-read markers, search history P0
### COMM-05 Announcements: founder posts pinned announcements that require acknowledgement P1
### COMM-06 Notification centre: assigned to me, mentioned, due soon, overdue, approvals needed, meeting 
reminders, client replies, system alerts P0
### COMM-07 Login digest: on first login of the day show summary of unread messages, new assignments and 
today's schedule P0
### COMM-08 Delivery channels: in-app, browser push, email digest, optional WhatsApp/Telegram for critical 
alerts; per-user preferences and quiet hours P1
### COMM-09 Presence status (online, in a meeting, on leave) drawn from calendar P2
### COMM-10 Quick huddle button that creates and posts a Google Meet link P2
### COMM-11 Client-facing messaging thread per project (via portal) with internal-only notes clearly separated P1
### COMM-12 Message retention and export policy; admin can archive channels P1
Business rules
• Notifications are grouped and de-duplicated; a task edited five times in a minute generates one 
notification.
• Mentions always notify regardless of mute settings unless the user has set do-not-disturb.
• Client-visible threads never expose internal channel content.
Main data entities
Channel, Message, Thread, Reaction, Notification, NotificationPreference, Announcement, Acknowledgement

---

<PARSED TEXT FOR PAGE: 22 / 42>

---

6.9 Client Portal
Purpose
A branded, secure window for clients to see progress, approve deliverables, share requirements, raise requests, 
view invoices and communicate, reducing status-update meetings and email chains.
Features and requirements
ID Requirement Priority
### PORT-01 Client login (email + OTP/password), multiple users per client with roles P1
### PORT-02 Project overview: status, milestones, recent updates, upcoming meetings P1
### PORT-03 Approved deliverables and shared folders with download and comment P1
### PORT-04 Approval requests (design, milestone, UAT sign-off) with digital record P1
### PORT-05 Raise requests, bugs and change requests with attachments P1
### PORT-06 Invoices, payment status, pay-online link, statements P1
### PORT-07 Support tickets and SLA status for maintenance clients P1
### PORT-08 Feedback and NPS request at milestones and closure P2
### PORT-09 White-label branding (logo, colours, custom domain) P2
Business rules
• Clients see only what is explicitly published to them.
• All client actions are logged and time-stamped for dispute resolution.
Main data entities
ClientUser, Approval, PortalRequest, FeedbackResponse

---

<PARSED TEXT FOR PAGE: 23 / 42>

---

6.10 Finance, Invoicing & Compliance
Purpose
Invoice clients, track payments and expenses, understand project profitability and stay GST-ready, without 
replacing the accountant's books.
Features and requirements
ID Requirement Priority
### FIN-01 Invoice creation from milestones, time entries, subscriptions or manual; GST-compliant format 
(GSTIN, HSN/SAC, CGST/SGST/IGST), PDF and email P0
### FIN-02 Invoice numbering series, credit notes, proforma invoices, quotes to invoice conversion P0
### FIN-03 Payment recording (bank, UPI, card, gateway), partial payments, reconciliation notes; 
Razorpay/Stripe links P0
### FIN-04 Recurring invoices for retainers, AMC and SaaS subscriptions with auto-reminders P1
### FIN-05 Receivables ageing (0-30, 31-60, 61-90, 90+), automated polite reminders and escalation P0
### FIN-06 Expense tracking: category, project, vendor, receipt upload, reimbursable flag, approval P0
### FIN-07 Vendor and freelancer payments with TDS tracking and payment schedule P1
### FIN-08 Project profitability: revenue, direct cost (time x cost rate, expenses), margin; client profitability P1
### FIN-09 Subscription and tool cost register (cloud, SaaS tools, domains) with renewal alerts and owner P0
### FIN-10 Cash-flow forecast: expected inflow from milestones/invoices, planned outflow, runway view 
(critical for a bootstrapped firm) P1
### FIN-11 Tax helper: GST summary by month, TDS summary, export for accountant (CSV/Tally-compatible) P1
### FIN-12 Multiple entities and currencies (for example Sketchitup Solutions LLP and future entities) P2
### FIN-13 Budget vs actual for the company and per project P2
### FIN-14 Financial data restricted to Founder and Finance roles; field-level audit P0
Key workflows
FIN-W1: Milestone to cash
# 1. Milestone marked complete and approved by client.
# 2. System drafts invoice with correct taxes; founder reviews and sends.
# 3. Payment link and due date sent to client; reminders scheduled.
# 4. Payment recorded; receipt issued; project financials update.
# 5. Overdue invoices escalate through reminder stages and notify the owner.
FIN-W2: Monthly close
# 1. Import or reconcile bank statement entries manually or via CSV.
# 2. Review unmatched receipts and expenses.
# 3. Generate GST and TDS summaries; send to accountant.
# 4. Lock the period to prevent back-dated edits.
Business rules
• Issued invoices cannot be edited, only cancelled by credit note.
• Locked periods reject edits unless the founder unlocks with a reason.

---

<PARSED TEXT FOR PAGE: 24 / 42>

---

Main data entities
Invoice, InvoiceItem, Payment, CreditNote, Expense, Vendor, Subscription, TaxSetting, PeriodLock, CashflowEntry

---

<PARSED TEXT FOR PAGE: 25 / 42>

---

6.11 Timesheets & Resource Planning
Purpose
Know who is working on what, how loaded they are, and whether estimates match reality.
Features and requirements
ID Requirement Priority
### TIME-01 Daily/weekly timesheet view built from task timers and manual entries P0
### TIME-02 Submit and approve weekly timesheets; lock after approval P1
### TIME-03 Capacity planning: allocation per person per project per week; over/under allocation warnings P1
### TIME-04 Cost rate and billing rate per role/person (restricted visibility) P1
### TIME-05 Utilisation report: billable vs non-billable vs bench P1
### TIME-06 Estimate accuracy report per project, task type and person P2
### TIME-07 Freelancer and contractor allocation and cost tracking P1
Business rules
• Working hours, holidays and leaves reduce available capacity automatically.
Main data entities
Timesheet, TimeEntry, Allocation, RateCard, Capacity

---

<PARSED TEXT FOR PAGE: 26 / 42>

---

6.12 People Operations (HR Lite)
Purpose
Keep the essentials of team management in one place: onboarding, leaves, attendance, performance, hiring and 
learning.
Features and requirements
ID Requirement Priority
### HR-01 Employee directory with role, skills, reporting line, joining date, contact, emergency contact P0
### HR-02 Leave management: types, balances, requests, approvals, team calendar P0
### HR-03 Attendance or daily check-in (remote-friendly), work-from-home marking P1
### HR-04 Onboarding checklist (accounts, access, laptop, NDA, policies, first-week plan) and offboarding 
checklist (access revoke, handover, asset return) P0
### HR-05 Hiring pipeline (ATS lite): role openings, candidates Kanban, interview schedule and scorecards, 
offer tracking P1
### HR-06 Performance: goals/OKRs, monthly 1:1 notes, feedback, quarterly review P1
### HR-07 Skill matrix and learning plan; certifications tracker P2
### HR-08 Policy documents with acknowledgement tracking P1
### HR-09 Payroll inputs export (days worked, leaves, reimbursements); payroll itself remains external 
initially P2
### HR-10 Employee documents vault (restricted): offer letters, IDs, contracts P1
Key workflows
HR-W1: New developer onboarding
# 1. Founder creates employee and selects onboarding template.
# 2. System creates tasks: accounts, repo access, tool access, NDA e-sign, intro meetings.
# 3. Buddy assigned; first-week plan and stand-up invites created automatically.
# 4. Day-30 review scheduled automatically.
Business rules
• Sensitive HR data visible only to Founder and HR-designated role.
• Offboarding checklist must complete before the account is disabled, and access revocation is logged.
Main data entities
Employee, LeaveRequest, LeaveBalance, Attendance, OnboardingTemplate, Candidate, Interview, Goal, 
ReviewNote, PolicyAck

---

<PARSED TEXT FOR PAGE: 27 / 42>

---

6.13 Support, Maintenance & AMC
Purpose
Handle post-delivery issues and recurring maintenance contracts with clear SLAs and history.
Features and requirements
ID Requirement Priority
### SUP-01 Ticket intake: portal, email-to-ticket, manual; fields for client, product/project, severity, category P1
### SUP-02 SLA policies by plan (response and resolution targets) with breach warnings P1
### SUP-03 Assignment, status flow (New, Triage, In Progress, Waiting on Client, Resolved, Closed), internal 
notes, canned replies P1
### SUP-04 Convert ticket to bug or change request on a project board P1
### SUP-05 AMC/maintenance contract register: scope, hours included, renewal date, price; usage vs 
entitlement P1
### SUP-06 Customer satisfaction survey on closure P2
### SUP-07 Incident log and post-mortem template for production incidents P2
### SUP-08 Uptime and environment register for deployed client systems (URLs, hosting, backups, owners) P1
Business rules
• Critical severity tickets notify founder and assignee immediately on all channels.
Main data entities
Ticket, SLAPolicy, AMCContract, Incident, EnvironmentRecord

---

<PARSED TEXT FOR PAGE: 28 / 42>

---

6.14 Own Products & Roadmap (SaaS Portfolio)
Purpose
Sketchitup builds its own domain SaaS products; this module manages product roadmaps, releases, feedback and 
pilot customers separately from client work.
Features and requirements
ID Requirement Priority
### PROD-01 Product register (for example agri and industrial vertical products): vision, target customer, 
status, owner, pricing plans P1
### PROD-02 Roadmap board: Ideas, Planned, In Development, Beta, Live, Sunset; quarterly view P1
### PROD-03 Feature request and feedback inbox linked to customers and votes P1
### PROD-04 Pilot and customer tracker for each product: onboarding stage, usage notes, renewal date P1
### PROD-05 Release notes and changelog publisher P2
### PROD-06 Product metrics manual or API entry: signups, active users, MRR, churn P2
### PROD-07 Reusable component library register (modules reused across client projects) to increase delivery 
leverage P2
Business rules
• Internal product work is tracked as projects with type Product and never mixed into client billing.
Main data entities
Product, RoadmapItem, FeatureRequest, PilotCustomer, ReleaseNote, ProductMetric, Component

---

<PARSED TEXT FOR PAGE: 29 / 42>

---

6.15 Knowledge Base, SOPs & Templates
Purpose
Capture how Sketchitup works so quality does not depend on memory: processes, coding standards, checklists, 
templates and learnings.
Features and requirements
ID Requirement Priority
### KB-01 Wiki with nested pages, rich text, code blocks, diagrams, attachments, page history P1
### KB-02 SOP library: lead handling, proposal creation, kickoff, code review, deployment, support handling, 
onboarding P1
### KB-03 Templates library (proposal, SOW, meeting notes, project plans, checklists) usable across 
modules P1
### KB-04 Engineering standards: coding guidelines, branching strategy, security checklist, environment 
setup
P1
### KB-05 Lessons learned repository linked to project closure P2
### KB-06 Search with AI question answering over approved internal content (with source links) P2
### KB-07 Page ownership, review dates and stale content alerts P2
Business rules
• Only approved pages are indexed for AI answers.
Main data entities
WikiPage, PageVersion, SOP, Template, LessonLearned

---

<PARSED TEXT FOR PAGE: 30 / 42>

---

6.16 Assets, Tools & Credential Vault
Purpose
Track company assets, tool subscriptions, domains, hosting and shared credentials securely.
Features and requirements
ID Requirement Priority
### VAULT-01 Asset register: laptops, devices, licences with assignee, purchase date, warranty, condition P1
### VAULT-02 Domain, hosting, SSL and cloud account register with renewal dates and owners P1
### VAULT-03 Encrypted credential vault with role-based sharing, access log and rotation reminders (or 
integration with an existing password manager) P1
### VAULT-04 Client environment credentials stored per project with strict access and expiry P1
### VAULT-05 Access review report: who has access to what, quarterly P2
Business rules
• Credentials are encrypted with per-record keys; viewing is logged; never appear in notifications or search 
snippets.
Main data entities
Asset, DomainRecord, HostingAccount, Credential, AccessGrant

---

<PARSED TEXT FOR PAGE: 31 / 42>

---

6.17 Reporting & Analytics
Purpose
Give the founder decision-ready numbers with minimal manual effort.
Features and requirements
ID Requirement Priority
### RPT-01 Sales reports: pipeline by stage/source/owner, conversion rates, win/loss reasons, sales cycle 
length, forecast P0
### RPT-02 Delivery reports: project status, delays, throughput, bug rates, sprint velocity P1
### RPT-03 Financial reports: revenue, receivables ageing, expenses, project and client profitability, cash￾flow P1
### RPT-04 Team reports: utilisation, workload, timesheet compliance, leave summary P1
### RPT-05 Marketing reports: channel performance, cost per lead, content output, gig and bid conversion P1
### RPT-06 Weekly founder digest (auto-email/PDF) and monthly business review pack P1
### RPT-07 Custom report builder with saved filters, export to CSV/PDF P2
### RPT-08 OKR/goal tracking dashboard for company objectives P2
Business rules
• Reports use a single source of truth; no manual data re-entry across modules.
Main data entities
Report, ReportSchedule, KPI, Objective, KeyResult

---

<PARSED TEXT FOR PAGE: 32 / 42>

---

6.18 Administration, Security & Settings
Purpose
Control who can do what, keep an audit trail, and configure the system for the firm.
Features and requirements
ID Requirement Priority
### ADM-01 User management, invitations, SSO with Google, 2FA, session management P0
### ADM-02 Role-based access control with custom roles and field-level restrictions (see permission matrix) P0
### ADM-03 Audit log: create/update/delete/export/permission changes with user, time and IP; immutable P0
### ADM-04 Configurable pipelines, statuses, custom fields, tags, templates, numbering series, tax settings, 
working days and holidays P0
### ADM-05 Company settings: entities, branding, addresses, GST details, default currency, time zone P0
### ADM-06 Data import and export (CSV) for all major entities; full backup export P0
### ADM-07 Automation rules builder (if this then that): for example when lead becomes Won create project, 
when task overdue notify PM P1
### ADM-08 Webhooks and public API keys for future integrations P2
### ADM-09 Data retention and deletion policies; DPDP-aligned consent and erasure workflow for client 
personal data P1
### ADM-10 System health page, background job monitor and error logs (admin) P1
Business rules
• Least privilege by default: new users have minimal access until roles are assigned.
• All admin actions are audit logged.
Main data entities
User, Role, Permission, AuditLog, Setting, AutomationRule, ApiKey, Webhook

---

<PARSED TEXT FOR PAGE: 33 / 42>

---

# 7. Cross-Module Workflows
These flows show how modules connect. They are the basis for end-to-end tests and demos.
End-to-end: Lead to cash
# 1. Marketing or referral generates a lead (MKT, CRM).
# 2. Discovery meeting scheduled and summarised (CAL).
# 3. Proposal and contract signed (SAL).
# 4. Project created from template, folders and channel auto-provisioned (PRJ, DOC, COMM).
# 5. Delivery through sprints with time tracking (PRJ, TIME).
# 6. Milestone approval via client portal (PORT).
# 7. Invoice issued and payment recorded (FIN).
# 8. Project closed with review, testimonial request and AMC offer (PRJ, MKT, SUP).
Meeting to action
# 1. Meeting held (CAL) and summarised by the bot.
# 2. Action items approved and converted into tasks on the right boards (PRJ).
# 3. Assignees notified (COMM); items due appear on their calendar (CAL).
# 4. Unresolved items roll into the next meeting agenda automatically.
Support to product improvement
# 1. Client raises ticket (SUP, PORT).
# 2. Recurring issue identified; logged as a feature request on the product roadmap (PROD).
# 3. Fix released with notes (PRJ release); client notified with the changelog.
Marketing to revenue attribution
# 1. Campaign or gig creates inquiries (MKT).
# 2. Inquiry becomes lead with source (CRM).
# 3. Won revenue flows back to the channel report (RPT), showing return on effort.
Standard automation rules to ship in Phase 1
Trigger Automatic action
Lead moves to Won Create client, project draft, kickoff task, folder tree and invoice 
schedule
New lead created without owner Assign by round-robin or to founder; notify
Follow-up date passed Notify owner; escalate to founder after 2 days
Task overdue Notify assignee and PM; mark on dashboard
Milestone approved Draft invoice and notify finance/founder
Invoice overdue by 3, 10, 20 days Send staged reminders; flag to founder at 20 days
Meeting summary approved Create tasks from action items and post summary to project channel
Employee added Apply onboarding checklist
Subscription or domain renewal within 30 days Notify owner and founder

---

<PARSED TEXT FOR PAGE: 34 / 42>

---

# 8. Data Model Overview
The following core entities and relationships must be reflected in the schema. Field-level design will be finalised 
by the tech lead during Sprint 0.
Entity Key relationships Notes
Organization / Entity Has Users, Clients, Projects, Settings Supports multiple legal 
entities later
User / Employee Belongs to Role(s); assigned Tasks, Leads, Events One person, one login; HR 
fields restricted
Client / Account Has Contacts, Leads, Projects, Invoices, Contracts, 
Folders
Created from lead conversion 
or manually
Contact Belongs to Client; participates in Meetings and Tickets Roles and communication 
preferences
Lead Belongs to Pipeline and Stage; has Activities, Proposals; 
converts to Client
Source and Campaign 
mandatory
Proposal / Contract Belongs to Lead or Client; creates Project and Invoice 
schedule Versioned
Project Belongs to Client; has Board, Tasks, Milestones, Files, 
Channel, TimeEntries
Type: client, product, 
internal, marketing
Task Belongs to Project/Board/Column; has Assignee, 
SubTasks, Comments, Files, TimeEntries, Dependencies
Also linked from Meetings 
(action items)
Event / Meeting Links to Client, Lead, Project, Task; has Attendees, 
Notes, Transcript, Summary Sync with Google Calendar
Campaign / Channel / 
ContentItem / Gig / Bid
Linked to Leads for attribution; ContentItem belongs to 
Campaign Manual entry and CSV import
Folder / File Belongs to Client/Project/Task; has Versions, 
ShareLinks, AccessLogs
Object storage with 
metadata in database
Channel / Message / 
Notification
Channel linked to Project/Client; Notification targets 
User and any object Preferences per user
Invoice / Payment / Expense / 
Subscription
Invoice belongs to Client/Project/Milestone; Payment 
belongs to Invoice Locked periods

---

