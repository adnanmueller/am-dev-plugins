# Development Pipeline Skills

A comprehensive, stack-agnostic development pipeline for solo founders. This skill package provides 9 specialised agents that guide you from idea to deployment.

## Installation

Copy the `development-pipeline` folder to your Claude skills directory:
- User skills: `/mnt/skills/user/development-pipeline/`
- Or reference directly in your project

## Pipeline Overview

```
Phase 0  │ BOOTSTRAP         │ Project setup, stack selection
         │                   │
Phase 1  │ PRODUCT MANAGER   │ Requirements, user stories, priorities
         │                   │
Phase 2a │ UX/UI DESIGNER    │ Design brief (lite) or design system (full)
Phase 2b │ ARCHITECT         │ Technical architecture, API contracts, ADRs
         │                   │ [Parallel execution]
         │                   │
         │ ══ APPROVAL GATE #1 ══
         │                   │
Phase 3a │ BACKEND           │ API implementation, business logic
Phase 3b │ FRONTEND          │ UI components, state management
Phase 3c │ QA SPECS          │ Test specifications [Auto-triggered]
         │                   │ [Parallel execution]
         │                   │
Phase 4  │ QA VALIDATION     │ Execute tests, validate quality
         │                   │
Phase 5  │ DEVOPS            │ Local setup → Infrastructure → CI/CD
         │                   │
Phase 6  │ SECURITY AUDIT    │ Comprehensive security review
         │                   │
         │ ══ APPROVAL GATE #2 ══
```

## Agents

| Agent | File | Description |
|-------|------|-------------|
| Pipeline Coordinator | `SKILL.md` | Main entry point, orchestrates workflow |
| Bootstrap | `agents/00-bootstrap/SKILL.md` | Project initialisation |
| Product Manager | `agents/01-product-manager/SKILL.md` | Requirements & user stories |
| UX/UI Designer (Lite) | `agents/02a-ux-ui-lite/SKILL.md` | Quick design brief for MVPs |
| UX/UI Designer (Full) | `agents/02a-ux-ui-full/SKILL.md` | Complete design system |
| System Architect | `agents/02b-architect/SKILL.md` | Technical architecture & APIs |
| Backend Engineer | `agents/03a-backend/SKILL.md` | Server-side implementation |
| Frontend Engineer | `agents/03b-frontend/SKILL.md` | Client-side implementation |
| QA Specs | `agents/03c-qa-specs/SKILL.md` | Test specifications |
| QA Validation | `agents/04-qa-validation/SKILL.md` | Test execution & validation |
| DevOps | `agents/05-devops/SKILL.md` | Deployment & infrastructure |
| Security Audit | `agents/06-security/SKILL.md` | Security assessment |

## Key Features

### Handoff Schema
All documents use a universal YAML frontmatter schema (`schema/handoff-schema.md`) for:
- Version tracking (semver)
- Dependency management
- Approval gate enforcement
- Security consideration tracking

### Design System
- **OKLCH colour space** for perceptually uniform colours
- Accessibility-first (WCAG AA minimum)
- Responsive breakpoints
- Component specifications

### Technology Stack Defaults
- **Frontend**: Next.js 14 + Tailwind + Zustand
- **Backend**: Python 3.11 + FastAPI
- **Database**: PostgreSQL + Prisma
- **Deployment**: Vercel + Railway

### Security Embedded
Security considerations are tracked through every phase, not just the final audit:
- Data classification (Phase 1)
- Input validation (Phase 2a)
- Threat modelling (Phase 2b)
- OWASP compliance (Phase 3)
- Infrastructure security (Phase 5)
- Comprehensive audit (Phase 6)

## Quick Start

1. Start a new chat with Claude
2. Say: "I want to build [your idea]"
3. Claude will run the Bootstrap agent to set up your project
4. Progress through phases with "next" or "phase [N]"
5. Use "status" to see pipeline progress

## Commands

| Command | Description |
|---------|-------------|
| `status` | Show current pipeline status |
| `next` | Proceed to next phase |
| `phase [N]` | Jump to specific phase |
| `approve [doc]` | Approve a document |
| `history` | Show recent activity |

## Configuration

### Project Scope Types
- **MVP**: Fast iteration, lite documentation
- **Production**: Full quality, comprehensive docs
- **Prototype**: Speed above all, minimal docs

### Design System Modes
- **Lite**: Single design brief (default for MVP)
- **Full**: Complete design system with components

## File Structure Generated

```
your-project/
├── project-documentation/
│   ├── _meta/
│   │   ├── project-config.yaml
│   │   ├── pipeline-status.md
│   │   └── decision-log.md
│   ├── 00-bootstrap/
│   ├── 01-requirements/
│   ├── 02-design/
│   ├── 03-architecture/
│   │   ├── api-contracts/
│   │   └── data-models/
│   ├── 04-implementation/
│   │   ├── backend/
│   │   └── frontend/
│   ├── 05-testing/
│   ├── 06-deployment/
│   └── 07-security/
├── src/
│   ├── backend/
│   └── frontend/
└── tests/
```

## Customisation

### Adding Custom Agents
1. Create a new folder in `agents/`
2. Add `SKILL.md` with the agent definition
3. Update `depends_on` and `blocks` in related agents

### Modifying Stack Defaults
Edit `templates/project-config.yaml` to change default technology choices.

## License

MIT — Use freely in your projects.

---

Built for solo founders who want structure without bureaucracy.
