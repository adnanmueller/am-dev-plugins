# AM Claude Plugins

A collection of specialized AI skills and workflows for [Claude Code](https://claude.ai/code). Features a comprehensive development pipeline for solo founders plus writing and documentation tools.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add adnanmueller/am-claude-plugins
```

Then install any plugin:

```
/plugin install development-pipeline@am-claude-plugins
/plugin install ai-text-humaniser@am-claude-plugins
/plugin install website-copy-standards@am-claude-plugins
/plugin install feature-documenter@am-claude-plugins
```

## Available Plugins

| Plugin | Category | Description |
|--------|----------|-------------|
| **development-pipeline** | workflow | Full development workflow with 11 specialized agents |
| **ai-text-humaniser** | writing | Removes AI-sounding patterns from generated text |
| **website-copy-standards** | writing | SEO/GEO optimized website copywriting |
| **feature-documenter** | documentation | Generates feature documentation from code analysis |

---

## Development Pipeline

The flagship plugin — a comprehensive, stack-agnostic development workflow designed for solo founders.

### Pipeline Overview

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

### Specialized Agents

| Agent | Phase | Description |
|-------|-------|-------------|
| Pipeline Coordinator | — | Main entry point, orchestrates workflow |
| Bootstrap | 0 | Project initialization and setup |
| Product Manager | 1 | Requirements and user stories |
| UX/UI Designer (Lite) | 2a | Quick design brief for MVPs |
| UX/UI Designer (Full) | 2a | Complete design system |
| System Architect | 2b | Technical architecture and APIs |
| Backend Engineer | 3a | Server-side implementation |
| Frontend Engineer | 3b | Client-side implementation |
| QA Specs | 3c | Test specifications |
| QA Validation | 4 | Test execution and validation |
| DevOps | 5 | Deployment and infrastructure |
| Security Audit | 6 | Security assessment |

### Key Features

- **Parallel Execution**: Phases 2a/2b and 3a/3b/3c run in parallel
- **Human Approval Gates**: Critical checkpoints before implementation and deployment
- **Universal Handoff Schema**: YAML frontmatter for dependency tracking and versioning
- **Security Embedded**: Security considerations tracked through every phase
- **Stack Agnostic**: Works with any technology stack

### Default Technology Stack

- **Frontend**: Next.js 14 + Tailwind CSS + Zustand
- **Backend**: Python 3.11 + FastAPI
- **Database**: PostgreSQL + Prisma ORM
- **Deployment**: Vercel (frontend) + Railway (backend)
- **CI/CD**: GitHub Actions

### Project Scope Types

| Scope | Documentation | Quality | Speed |
|-------|---------------|---------|-------|
| MVP | Lite | Balanced | Fast |
| Production | Full | Comprehensive | Thorough |
| Prototype | Minimal | Functional | Fastest |

### Quick Start

1. Install the plugin: `/plugin install development-pipeline@am-claude-plugins`
2. Say: "I want to build [your idea]"
3. Claude runs the Bootstrap agent to set up your project
4. Progress through phases with `next` or `phase [N]`
5. Use `status` to see pipeline progress

### Commands

| Command | Description |
|---------|-------------|
| `status` | Show current pipeline status |
| `next` | Proceed to next phase |
| `phase [N]` | Jump to specific phase |
| `approve [doc]` | Approve a document |
| `history` | Show recent activity |

---

## AI Text Humaniser

Transforms AI-generated text into natural, human-sounding prose by removing common AI patterns:

- Filler phrases ("It's worth noting that...", "Let's dive in...")
- Corporate buzzwords (leverage, utilize, synergy)
- Overwrought metaphors and weak intensifiers
- Hedging patterns and mechanical transitions

---

## Website Copy Standards

Professional website copywriting with:

- **SEO Optimization**: Keyword integration, meta descriptions
- **GEO (Generative Engine Optimization)**: AI-friendly structured content
- **Accessibility**: WCAG compliance, screen reader optimization
- **Structured Data**: JSON-LD schema templates (FAQ, Article, Product, Organization)

Includes reference guides for B2B/B2C methodology, landing pages, brand storytelling, and cognitive copywriting.

---

## Feature Documenter

Generates comprehensive feature documentation from code analysis:

- Template-based documentation generation
- Simple and comprehensive output formats
- Code-to-documentation mapping

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-plugin`)
3. Add your plugin to `plugins/` with a `.claude-plugin/plugin.json`
4. Update the marketplace.json to include your plugin
5. Open a Pull Request

### Plugin Structure

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md
└── [additional files]
```

---

## License

MIT License — Use freely in your projects.

---

Built for solo founders who want structure without bureaucracy.
