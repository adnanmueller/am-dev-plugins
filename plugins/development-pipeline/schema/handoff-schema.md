# Universal Handoff Schema Specification

Version: 1.0.0

This schema defines the standard format for all documents produced by agents in the development pipeline. Every document MUST include this frontmatter to enable proper pipeline coordination, dependency tracking, and approval workflows.

## Schema Definition

```yaml
---
# =============================================================================
# METADATA — Required for all documents
# =============================================================================
document_type: [bootstrap | requirements | design_brief | design_system | architecture | api_contract | data_model | implementation | test_spec | test_results | deployment | security_audit]
version: "1.0.0"  # Semantic versioning: MAJOR.MINOR.PATCH
status: [draft | review | approved | superseded]
created_by: [bootstrap | product_manager | ux_ui_designer | architect | backend_engineer | frontend_engineer | qa_engineer | devops_engineer | security_analyst]
created_at: "YYYY-MM-DDTHH:MM:SSZ"  # ISO 8601 format
last_updated: "YYYY-MM-DDTHH:MM:SSZ"
project: "project-slug"  # Lowercase, hyphenated

# =============================================================================
# PIPELINE POSITION — Required for dependency tracking
# =============================================================================
phase: [0 | 1 | 2a | 2b | 3a | 3b | 3c | 4 | 5 | 6]
# Phase mapping:
#   0  = Bootstrap
#   1  = Product Manager
#   2a = UX/UI Designer
#   2b = System Architect
#   3a = Backend Engineer
#   3b = Frontend Engineer
#   3c = QA Specs (parallel with 3a/3b)
#   4  = QA Validation
#   5  = DevOps
#   6  = Security Audit

depends_on:
  - document: "filename.md"
    version: ">=1.0.0"  # Semver range
    status: approved    # Required status: approved | any
    
blocks:  # Documents that cannot proceed until this is approved
  - "downstream-document.md"

# =============================================================================
# APPROVAL GATES — Required for gate documents
# =============================================================================
requires_human_approval: [true | false]
approval_status: [pending | approved | rejected | not_required]
approval_notes: ""
approved_at: "YYYY-MM-DDTHH:MM:SSZ"  # Only if approved

# =============================================================================
# STACK CONTEXT — Inherited from bootstrap, included in all documents
# =============================================================================
stack:
  frontend: [nextjs | react | vue | svelte | other]
  backend: [python | node | go | rust | other]
  database: [postgresql | mongodb | sqlite | mysql | other]
  deployment: [vercel | aws | railway | fly | other]
  
# =============================================================================
# SECURITY CONSIDERATIONS — Required for all documents
# =============================================================================
security_considerations:
  - id: "SEC-001"
    category: [authentication | authorisation | data_protection | input_validation | infrastructure | dependencies | other]
    consideration: "Description of security consideration"
    status: [identified | mitigated | accepted_risk | not_applicable]
    mitigation: "How this is addressed (if mitigated)"
    owner: [product_manager | architect | backend_engineer | frontend_engineer | devops_engineer | security_analyst]
    
# =============================================================================
# CHANGE TRACKING — For iterations and amendments
# =============================================================================
supersedes: "previous-version-filename.md"  # If this replaces another doc
amendments:
  - version: "1.1.0"
    date: "YYYY-MM-DDTHH:MM:SSZ"
    summary: "What changed"
    breaking: [true | false]  # Does this require downstream regeneration?
---
```

## Version Semantics

Following semver principles adapted for documentation:

- **MAJOR**: Breaking changes requiring downstream document regeneration
  - Example: Changing authentication from session-based to JWT
  - Example: Removing a core feature
  - Example: Restructuring the data model fundamentally

- **MINOR**: Additions or enhancements that are backwards-compatible
  - Example: Adding a new optional feature
  - Example: Adding new API endpoints
  - Example: Expanding acceptance criteria

- **PATCH**: Clarifications, typo fixes, formatting improvements
  - Example: Fixing typos
  - Example: Adding examples for clarity
  - Example: Reformatting for readability

## Dependency Resolution Rules

### Version Matching

Dependencies use semver ranges:
- `">=1.0.0"` — Any version 1.0.0 or higher
- `"^1.2.0"` — Any version >=1.2.0 and <2.0.0
- `"~1.2.0"` — Any version >=1.2.0 and <1.3.0
- `"1.2.0"` — Exactly version 1.2.0 (strict mode for production)

### Status Requirements

- `approved` — Dependency must be approved before this document can proceed
- `any` — Dependency can be draft (useful during rapid iteration)

### Cascade Rules

When a document is updated with `breaking: true`:

1. All documents that depend on it are marked `status: review`
2. Pipeline Coordinator alerts user to review downstream impacts
3. User decides: regenerate downstream docs or mark amendment as non-breaking

## Security Consideration Categories

Each phase has expected security categories:

| Phase | Expected Categories |
|-------|---------------------|
| 0 - Bootstrap | infrastructure, dependencies |
| 1 - Product Manager | data_protection, authentication |
| 2a - UX/UI | input_validation, data_protection |
| 2b - Architect | authentication, authorisation, infrastructure, data_protection |
| 3a - Backend | authentication, authorisation, input_validation, data_protection |
| 3b - Frontend | input_validation, data_protection |
| 3c - QA Specs | authentication, input_validation |
| 4 - QA Validation | all (validation of prior considerations) |
| 5 - DevOps | infrastructure, dependencies |
| 6 - Security | all (comprehensive audit) |

## Document Lifecycle

```
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌────────────┐
│  draft  │ ──► │ review  │ ──► │ approved │ ──► │ superseded │
└─────────┘     └─────────┘     └──────────┘     └────────────┘
                    │                                   ▲
                    │ (rejected)                        │
                    ▼                                   │
               ┌─────────┐                              │
               │  draft  │ (revision) ──────────────────┘
               └─────────┘
```

## Example Document Header

```yaml
---
document_type: architecture
version: "1.2.0"
status: approved
created_by: architect
created_at: "2025-01-15T10:30:00Z"
last_updated: "2025-01-16T14:22:00Z"
project: "task-management-app"

phase: 2b
depends_on:
  - document: "product-requirements.md"
    version: ">=1.0.0"
    status: approved
blocks:
  - "backend-implementation.md"
  - "frontend-implementation.md"
  - "test-strategy.md"

requires_human_approval: true
approval_status: approved
approval_notes: "Approved with note: revisit caching strategy after MVP"
approved_at: "2025-01-16T15:00:00Z"

stack:
  frontend: nextjs
  backend: python
  database: postgresql
  deployment: vercel

security_considerations:
  - id: "SEC-001"
    category: authentication
    consideration: "JWT tokens must be short-lived with refresh token rotation"
    status: mitigated
    mitigation: "15-minute access tokens, 7-day refresh tokens with rotation on use"
    owner: backend_engineer
  - id: "SEC-002"
    category: data_protection
    consideration: "User passwords must be hashed with modern algorithm"
    status: identified
    mitigation: "Use argon2id with recommended parameters"
    owner: backend_engineer

amendments:
  - version: "1.1.0"
    date: "2025-01-15T16:00:00Z"
    summary: "Added caching layer specification"
    breaking: false
  - version: "1.2.0"
    date: "2025-01-16T14:22:00Z"
    summary: "Revised API rate limiting approach"
    breaking: false
---
```
