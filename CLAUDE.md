# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Claude Code Plugin Marketplace** (`am-claude-plugins`) containing 4 specialized AI skills:

1. **development-pipeline** — Full development workflow with 11 agents for solo founders
2. **ai-text-humaniser** — Removes AI-sounding patterns from text
3. **website-copy-standards** — SEO/GEO optimized website copywriting
4. **feature-documenter** — Generates feature documentation from code analysis

## Marketplace Structure

```
am-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json           # Marketplace manifest (lists all plugins)
├── plugins/
│   ├── development-pipeline/      # Main development workflow
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json        # Plugin manifest
│   │   ├── SKILL.md               # Pipeline Coordinator
│   │   ├── schema/
│   │   ├── templates/
│   │   └── agents/                # 11 specialized agents
│   ├── ai-text-humaniser/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── SKILL.md
│   ├── website-copy-standards/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── scripts/
│   │   └── assets/
│   └── feature-documenter/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── SKILL.md
│       └── references/
├── README.md
├── CLAUDE.md
└── .gitignore
```

## Development Pipeline Architecture

### Pipeline Phases

7 phases with 2 approval gates:

- **Phase 0 (Bootstrap)**: Project setup, stack selection
- **Phase 1 (Product Manager)**: Requirements, user stories, priorities
- **Phase 2a/2b (Design + Architecture)**: Run in parallel
- **Approval Gate #1**: Human confirms technical direction
- **Phase 3a/3b/3c (Implementation)**: Backend, Frontend, QA Specs in parallel
- **Phase 4 (QA Validation)**: Execute tests
- **Phase 5 (DevOps)**: Infrastructure and CI/CD
- **Phase 6 (Security Audit)**: Security review
- **Approval Gate #2**: Human confirms deployment readiness

### Universal Handoff Schema

All documents use standardized YAML frontmatter (defined in `plugins/development-pipeline/schema/handoff-schema.md`):

```yaml
document_type: [bootstrap | requirements | architecture | ...]
version: "1.0.0"  # MAJOR.MINOR.PATCH
status: [draft | review | approved | superseded]
phase: [0 | 1 | 2a | 2b | 3a | 3b | 3c | 4 | 5 | 6]
depends_on: [{document, version, status}]
security_considerations: [{id, category, consideration, status, mitigation, owner}]
```

### Dependency Matrix

| Phase | Requires |
|-------|----------|
| 1 - Product Manager | Phase 0 approved |
| 2a - UX/UI | Phase 1 approved |
| 2b - Architect | Phase 1 approved |
| 3a - Backend | Phase 2b + Gate #1 approved |
| 3b - Frontend | Phase 2a + 2b + Gate #1 approved |
| 4 - QA | Phase 3a + 3b + 3c complete |
| 5 - DevOps | Phase 4 approved |
| 6 - Security | Phase 5 approved |

## Default Technology Stack

- **Frontend**: Next.js 14 + Tailwind CSS + Zustand
- **Backend**: Python 3.11 + FastAPI
- **Database**: PostgreSQL + Prisma ORM
- **Deployment**: Vercel (frontend) + Railway (backend)
- **CI/CD**: GitHub Actions

## Adding New Plugins

1. Create folder in `plugins/` with `.claude-plugin/plugin.json`
2. Add plugin entry to `.claude-plugin/marketplace.json`
3. Include at minimum a `SKILL.md` defining the plugin's behavior

## Conventions

- Plugins are defined in `SKILL.md` files with YAML frontmatter
- Each plugin has its own `.claude-plugin/plugin.json` manifest
- Marketplace manifest lists all available plugins with sources
- Security considerations tracked throughout development-pipeline phases
- Agent files in development-pipeline follow naming: `00-bootstrap.md` through `06-security.md`

## Available Scripts

### Content Validation (website-copy-standards)

```bash
# Validate HTML for GEO/SEO standards
python plugins/website-copy-standards/scripts/validate_content.py --file page.html
python plugins/website-copy-standards/scripts/validate_content.py --url https://example.com --json
```

Checks: H1 tags, heading hierarchy, semantic HTML, schema markup, readability (Grade 8 target), scannability, link text, image alt text, answer-first structure.

### Schema Generation (website-copy-standards)

```bash
# Generate JSON-LD schema (faqpage, article, organization, product)
python plugins/website-copy-standards/scripts/generate_schema.py --type faqpage --interactive
python plugins/website-copy-standards/scripts/generate_schema.py --type article --input data.json --output schema.json
```

Templates available in `plugins/website-copy-standards/assets/schema-templates/`.

## Quick Reference

```bash
# Add marketplace
/plugin marketplace add adnanmueller/am-claude-plugins

# Install plugins
/plugin install development-pipeline@am-claude-plugins
/plugin install ai-text-humaniser@am-claude-plugins
/plugin install website-copy-standards@am-claude-plugins
/plugin install feature-documenter@am-claude-plugins
```
