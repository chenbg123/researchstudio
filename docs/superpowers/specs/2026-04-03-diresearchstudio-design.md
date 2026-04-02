# DiResearchStudio Design Spec

Date: 2026-04-03
Status: Approved in conversation, pending final user review

## 1. Overview

This project is a secondary development of the existing DeerFlow codebase into a new enterprise-facing product named **DiResearchStudio**.

The first release of DiResearchStudio should transform the current general-purpose AI workspace into a multi-user, enterprise-oriented research and report-generation platform with:

- PostgreSQL-backed persistence
- Multi-user login and session management
- Full chat message persistence
- Per-user chat history isolation
- Admin-managed local accounts
- Future-compatible trusted header SSO
- Persistent uploaded/generated file management
- OBS/object-storage-ready artifact architecture
- Enterprise-style login and workspace UI
- Test-stage admin control over mode/profile, skills, MCP visibility, and conversation review
- A unified agent platform that can evolve from one main agent into multiple domain-specific agents over time

The user-visible product name should be **DiResearchStudio** rather than DeerFlow.

## 2. Product Goals

### 2.1 Functional goals

The first release must support:

1. Connect the system to PostgreSQL.
2. Support multi-user login with account + password.
3. Persist complete chat message content to the database.
4. Replace the current landing page with a login page.
5. After login, users go directly into the chat workspace.
6. Users see only their own history in the left sidebar.
7. Admins can create and disable users.
8. Future production deployments can use a trusted OA/SSO header login flow.
9. If an SSO/header user does not exist locally, the system auto-creates the local user.
10. Uploaded and generated files should be modeled and persisted in a production-friendly way.
11. Production deployments may store uploaded/generated files in OBS or compatible object storage.
12. The workspace UI should be upgraded from a simple demo-style chat page into a more professional enterprise workspace.
13. During the current testing phase, admins must also be able to manage mode/profile, skills visibility, MCP visibility, and review conversations.

### 2.2 Non-goals for phase 1

The first release should not overreach into a full no-code agent platform. The following are explicitly deferred or only minimally pre-structured:

- Full multi-agent orchestration UI
- Full tenant/workspace hierarchy
- Fine-grained audit role separation
- Visual prompt/workflow builder
- Full policy engine for tool/data permissions
- Rich self-service end-user skill/MCP installation

## 3. Current System Context

DiResearchStudio is being built on top of the existing DeerFlow architecture:

- **Frontend**: Next.js 16, React 19, TypeScript
- **Gateway API**: FastAPI
- **Agent runtime**: LangGraph-based backend
- **Sandbox**: per-thread runtime workspace
- **Extensions**: skills + MCP support via shared configuration

Existing structure confirms that the current system is already close to a reusable AI workspace platform, not only a single chatbot. This makes it a suitable foundation for enterprise productization.

## 4. Authentication and Identity Strategy

### 4.1 Dual-mode authentication

DiResearchStudio should support two identity sources under one unified local user model:

1. **Local account login**
   - Administrator pre-creates accounts.
   - Users log in with username/email + password.
   - No self-registration in phase 1.

2. **Trusted header SSO login**
   - In production, an OA/SSO portal or reverse proxy may authenticate the user externally.
   - It passes trusted headers such as user ID or username to DiResearchStudio.
   - DiResearchStudio reads the trusted header, maps it to a local user, establishes a local session, and redirects directly to the workspace.
   - If the user does not yet exist locally, the system auto-creates the local user.

### 4.2 Unified local user model

Instead of introducing a separate `auth_accounts` table in phase 1, the user requested a simplified model inspired by Chainlit’s `User` table style.

Recommended `users` structure:

- `id` — internal primary key (UUID recommended; do not overload external identifiers as the primary key)
- `provider` — e.g. `local`, `oa-header`, future `ldap`, `oauth`, etc.
- `identifier` — unique identifier within a provider, e.g. username or external user ID
- `password_hash` — nullable, used for local accounts only
- `role` — e.g. `admin`, `user`
- `status` — e.g. `active`, `disabled`
- `display_name`
- `email` — nullable
- `metadata` — JSONB for flexible extra attributes
- `last_login_at`
- `created_at`
- `updated_at`

Constraints:

- `UNIQUE(provider, identifier)`

This keeps the model simple while allowing multiple identity providers later.

### 4.3 Session strategy

Regardless of how a user logs in, the system should normalize them into the same local user/session model:

- `local` users authenticate by password
- `oa-header` users authenticate through trusted headers
- after successful mapping, both get the same application session treatment

This keeps chat history, settings, permissions, and file ownership unified.

## 5. Authorization Model

### 5.1 Roles

Phase 1 uses a simple RBAC model:

#### `user`
Can:
- log in
- view and use their own conversations
- upload files into their own conversation context
- access their own generated artifacts
- use modes/profiles and capabilities made visible by admin

Cannot:
- view other users’ data
- manage platform configuration

#### `admin`
For the current testing stage, admin needs enhanced powers.

Can:
- create users
- disable/enable users
- reset local account passwords
- manage mode/profile visibility
- manage skills visibility
- manage MCP visibility
- review all conversations
- manage platform-level settings later as needed

This is intentionally broader than a minimal production admin role because the current stage requires testing and validation of different business modes and integrations.

### 5.2 Conversation visibility

- Normal users can only access their own threads, messages, and file artifacts.
- Admins can review all conversations during the current testing stage.
- The spec should note that long-term production may later separate `admin`, `auditor`, and `super_admin`, but phase 1 does not require that split.

## 6. Data Model Design

The solution should borrow ideas from Chainlit’s persistence model, especially around user/thread/step/element concepts, but adapt them to DiResearchStudio’s existing architecture and requirements.

### 6.1 Core tables

#### `users`
Stores application users and identity provider info.

Important fields:
- `id`
- `provider`
- `identifier`
- `password_hash`
- `role`
- `status`
- `display_name`
- `email`
- `metadata` JSONB
- timestamps

#### `chat_threads`
Stores conversation/session metadata.

Important fields:
- `id`
- `user_id`
- `title`
- `mode` or `profile_key`
- optional `agent_key`
- `metadata` JSONB
- `created_at`
- `updated_at`
- optional soft-delete fields if desired

Notes:
- `mode/profile_key` is important even if phase 1 only exposes one default mode initially.
- This field reserves the path toward future domain-specific workflows.

#### `chat_messages`
Stores complete chat message content, not only thread metadata.

Important fields:
- `id`
- `thread_id`
- `user_id` (optional if strictly derivable from thread, but useful for security queries/audit)
- `role` (`user`, `assistant`, `tool`, `system` as needed)
- `content` JSONB (to preserve structured content, rich blocks, and future extensibility)
- `text_content` or summary/indexable field if useful
- `message_index` or ordering field
- `metadata` JSONB
- `created_at`

This table must preserve **full message content**.

#### `chat_elements`
This replaces a narrower “artifact-only” idea with a more general Chainlit-Element-inspired model.

It should cover:
- uploaded files
- generated files
- images
- code artifacts
- report files
- ppt files
- references to external object storage

Important fields:
- `id`
- `thread_id`
- `message_id` or run linkage where applicable
- `user_id` (optional but recommended for auditing and access control)
- `type`
- `name`
- `mime`
- `size`
- `storage_provider` (e.g. `local`, `obs`)
- `object_key` or storage key
- `url` if applicable
- `source` (`upload`, `generated`, etc.)
- `metadata` JSONB
- `props` JSONB if useful
- timestamps

### 6.2 Optional phase 1 or phase 1.5 tables

Depending on implementation detail, the system may later introduce tables like:

- `agent_runs`
- `mode_profiles`
- `mode_profile_skill_bindings`
- `mode_profile_mcp_bindings`
- `user_settings`

These do not all need to be fully implemented in phase 1, but the design should not block them.

## 7. File and Artifact Architecture

### 7.1 Current runtime sandbox model

The current DeerFlow runtime already creates per-thread user-data directories such as:

- workspace
- uploads
- outputs

This should remain the **runtime execution layer**.

It is useful for:
- temporary tool execution
- file transformations
- local run context
- agent-generated outputs before persistence or publishing

### 7.2 Production file design

In production, uploaded and generated files should not rely only on thread-local filesystem storage.

Recommended separation:

1. **Runtime sandbox layer**
   - Per-thread working files
   - Temporary execution area
   - Internal agent/tool operations

2. **Durable asset layer**
   - OBS / object storage for uploaded/generated files
   - `chat_elements` records as the persistent metadata index
   - download/preview routed through secure backend endpoints

This means the sandbox remains valuable, but persistent business assets should move to object storage.

### 7.3 Why `chat_elements` is the right abstraction

The user explicitly asked whether Chainlit’s `Element` pattern should be referenced. The answer is yes.

A generalized `chat_elements` table is better than a narrow `chat_artifacts` table because the platform must support:

- user uploads
- generated reports
- ppt outputs
- code files
- screenshots/images
- future rich elements

This is closer to the business needs of DiResearchStudio.

### 7.4 Access and security

The existing safe path resolution and active-content download protection should be preserved.

Requirements:
- prevent path traversal
- protect access by thread ownership/authorization
- force safe download behavior for dangerous active content types where needed
- preserve backend mediation instead of exposing raw internal paths

## 8. MCP, Skills, and Settings Model

### 8.1 Current state

From the current implementation:

- **MCP configuration** is stored in shared `extensions_config.json` and managed through backend APIs.
- **Skills configuration** is also deployment-level/shared and managed through shared configuration plus installed skill directories.
- **Frontend settings** are stored in browser `localStorage`, which isolates by browser context, not by backend user account.

### 8.2 Production interpretation

For production, these concerns should be separated into three layers:

#### Platform-level configuration
Managed by deployer/admin:
- MCP server registration and enablement
- skills installation and enablement
- object storage and external system connections
- trusted header SSO config

#### User-level preferences
Managed per user:
- UI preferences
- default model/profile preference
- local layout behavior
- optional mode/profile defaults

#### Thread-level state
Managed per conversation:
- active mode/profile
- files attached to the thread
- generated outputs
- execution metadata

### 8.3 Phase 1 decision

The user explicitly accepted browser-local isolation for basic UI settings in office environments, so local browser storage is acceptable in phase 1 for ordinary UI preferences.

However:
- platform-level MCP and skills should remain admin-controlled
- user settings should be designed so they can be moved server-side later if strict account-level preference isolation becomes necessary

### 8.4 Test-stage admin capabilities

For the current test phase, admin must also manage:
- mode/profile visibility
- skills visibility
- MCP visibility
- conversation review

This does not mean all these capabilities need full polished admin platforms in phase 1, but they must exist in some practical form.

## 9. Agent Platform Strategy

### 9.1 Current backend role

The existing backend should be understood as:

- Frontend = unified AI workbench
- Gateway API = platform access/control layer
- LangGraph runtime = agent execution and orchestration base
- MCP/tools/skills = external ability layer
- Sandbox + storage = file execution and persistence layer

This is a strong fit for building DiResearchStudio as an **enterprise agent workspace**.

### 9.2 Recommended phase 1 approach

The user raised an important architecture question: whether domain requirements should become separate agents, or whether one unified agent can satisfy multiple needs through skills and MCP.

The agreed design direction is:

**Phase 1: one main agent + multiple skills + multiple MCP integrations + mode/profile abstraction**

This means:
- keep one primary workspace agent for initial delivery
- attach multiple data-access and document/report capabilities through tools/MCP
- represent domain differences through `mode/profile`
- use skill-like capability templates and MCP-backed connectors rather than building many separate agents immediately

### 9.3 Why not start with many separate agents

The user specifically asked why domain requirements should not be implemented only via skills/MCP. The conclusion is:

- skills and MCP can cover a lot of variation early on
- one unified agent is valid for phase 1
- but the architecture must leave room for future separation when workflows, permissions, outputs, or monitoring needs diverge significantly

So phase 1 should **not** overbuild a multi-agent system, but should **reserve the option** to evolve into one later.

### 9.4 Long-term evolution path

Recommended evolution:

- **Phase 1**: single main agent + multi-skill + multi-MCP + mode/profile
- **Phase 2**: split mature domain workflows into dedicated agents/graphs if needed
- **Long-term**: multi-agent enterprise platform under one DiResearchStudio workspace

Examples of future specialized agents if needed:
- competitor analysis
- public opinion analysis
- internal document report generation
- ppt generation
- weekly report generation

The key is that phase 1 remains simple while preserving forward compatibility.

## 10. Frontend Design

### 10.1 Product naming

The product name should be changed from **DeerFlow** to **DiResearchStudio** in user-visible surfaces.

Phase 1 should prioritize replacing user-visible branding:
- login page title
- page titles
- workspace branding
- empty states and copy
- admin page copy

Internal package/module renaming can be evaluated later and does not need to be mandatory in phase 1.

### 10.2 Login page replaces landing page

Current `/` should stop being the marketing/landing page and become the login entry for DiResearchStudio.

Recommended design:
- enterprise-oriented login page
- product description on one side
- login card on the other side
- supports local login form
- supports trusted-header auto-login flow
- if SSO is detected, auto-validate and redirect into workspace
- if SSO fails, fallback to standard login page with a clear but safe error state

### 10.3 Workspace redesign

The current workspace is considered too simple for enterprise use.

Approved design direction:

**Keep the existing core information architecture but redesign it into a more professional enterprise workspace.**

Recommended structure:

#### Left sidebar
- new conversation
- search history
- thread list
- time grouping (today / last 7 days / older)
- clear session titles and update time
- future profile/mode indicators

#### Center chat area
- top bar with conversation title, current user info, active mode/profile, settings entry, admin entry where applicable
- improved chat message presentation for text, code, citations, tool output, and structured content
- bottom input bar fixed for professional daily use
- upload button and future mode/profile switch affordance

#### Right-side collapsible panel
Recommended for phase 1 or close follow-up:
- uploaded files in the thread
- generated outputs (reports, PPTs, code, images)
- execution status summary
- referenced documents list
- visible tool/MCP context summary if useful

This structure is important because the product needs to support more than plain chat.

### 10.4 File and artifact presentation

Uploaded and generated files should be displayed as card-like elements rather than raw attachments only.

The UI should support:
- uploads with filename/type/size/source metadata
- generated reports, PPTs, and code files with preview/download affordances where possible
- richer image and document previews in future

### 10.5 Admin pages

At minimum, phase 1 should provide admin pages for:

- `/admin/users`
- `/admin/modes` or equivalent mode/profile management view
- `/admin/skills`
- `/admin/mcp`
- `/admin/conversations`

They do not need to be overly complex at first, but must satisfy testing-stage admin needs.

## 11. Backend/API Change Points

The following areas are expected to change or expand:

### 11.1 Authentication/session layer
- activate and extend Better Auth or equivalent local session flow
- add trusted-header bootstrap flow
- connect auth to PostgreSQL-backed user records

### 11.2 Thread/message persistence
- persist thread records to PostgreSQL
- persist full message content to PostgreSQL
- load per-user history into workspace sidebar

### 11.3 File persistence and retrieval
- persist `chat_elements` metadata
- support OBS/object storage for durable files
- preserve secure backend-mediated downloads

### 11.4 Admin control endpoints
Need backend support for:
- user management
- mode/profile visibility management
- skill visibility/enabled state management
- MCP visibility/enabled state management
- cross-user conversation review for admins

### 11.5 Mode/profile support
Even if initially static in code or config, APIs and models should reserve a place for:
- thread-level `mode/profile`
- visible mode/profile lists
- per-mode/profile capability binding later

## 12. Error Handling

### 12.1 Local login errors
Show user-friendly but safe messages for:
- invalid credentials
- disabled account
- unavailable login method

### 12.2 Header SSO errors
Handle cases such as:
- missing trusted headers
- incomplete header values
- untrusted source
- auto-create failure

Behavior:
- log full backend details
- present safe frontend message
- fallback to login page when possible

### 12.3 Authorization errors
- unauthorized access to another user’s conversation or files returns `403`
- missing resources return `404`
- all access decisions should be auditable in logs

### 12.4 File/storage errors
Examples:
- upload rejection
- unsupported file type
- object storage write failure
- sandbox sync failure
- generated artifact failure

Behavior:
- frontend should show understandable failure states
- backend should keep diagnosable logs
- failed artifact generation should not poison future conversation use

## 13. Testing Strategy

The repo currently has backend tests but no frontend test framework configured. The phase 1 implementation should still include structured verification.

### 13.1 Auth and user-flow tests
Cover:
- local login success/failure
- disabled account rejection
- header SSO success
- header SSO auto-create user
- user isolation of history visibility

### 13.2 Persistence tests
Cover:
- create thread
- save full chat messages
- load thread history
- ensure ownership constraints
- ensure admin review access where enabled

### 13.3 File and artifact tests
Cover:
- upload persistence
- generated file metadata persistence in `chat_elements`
- OBS/object storage read/write flow
- secure artifact access checks
- path safety behavior remains intact

### 13.4 Frontend workflow validation
Cover:
- `/` is login page
- post-login redirect to workspace
- sidebar shows current user history
- improved workspace components render correctly
- admin pages satisfy basic management needs

## 14. Phase 1 Implementation Boundary

### 14.1 Must be included in phase 1
- PostgreSQL integration
- multi-user local accounts
- admin-created users
- header SSO compatible flow
- auto-create user on trusted header login
- full chat message persistence
- per-user thread isolation
- `chat_elements` design and implementation path
- OBS/object-storage-ready artifact path
- login page replacing landing page
- enterprise workspace redesign
- minimal admin pages
- DiResearchStudio branding replacement
- single main agent + skills/MCP + mode/profile structure

### 14.2 Reserve but do not fully implement in phase 1
- fully separate dedicated business agents
- advanced policy engine
- complete multi-tenant hierarchy
- advanced audit center
- visual workflow/prompt builder
- deeply granular per-role access matrix for every extension

## 15. Final Design Summary

DiResearchStudio phase 1 should deliver an enterprise-ready foundation built on the current DeerFlow architecture with the following shape:

- unified **DiResearchStudio** branding
- PostgreSQL-backed multi-user product
- local login + future-ready trusted header SSO
- admin-managed users
- full conversation persistence
- user-isolated history
- admin review and admin-controlled visibility of modes/profiles, skills, and MCP during testing
- generalized `chat_elements` model for uploaded/generated files
- sandbox runtime plus OBS/object-storage durable storage strategy
- one main agent with mode/profile differentiation and shared skills/MCP integrations
- enterprise-style login and chat workspace UI

This gives the project a practical first release while preserving a clean path toward future domain specialization and platform growth.
