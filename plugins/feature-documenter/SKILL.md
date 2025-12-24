---
name: feature-documenter
description: Create clear feature documentation for non-professional developers. Use PROACTIVELY when documenting new features, significant code changes, creating technical specifications, or when a feature isn't covered in the original project spec. Triggers on requests like "document this feature", "create feature docs", "write technical specification", "document these changes", or any request to explain what code does for future reference.
---

# Feature Documenter

Create comprehensive feature documentation that helps non-professional developers understand and maintain code.

## Workflow

1. **Determine template complexity**
   - Quick overview or simple feature? → Use simplified template (see `references/template-simple.md`)
   - Detailed specification or complex feature? → Use comprehensive template (see `references/template-comprehensive.md`)

2. **Gather context before documenting**
   - Check `./docs/system-design/` for existing specifications
   - Search for related GitHub issues or requirements documents
   - Use Grep/Glob to find related components in the codebase
   - Review existing feature documentation for consistency

3. **Create documentation**
   - Start with core sections: Problem Statement, Solution Overview, Core Components
   - Expand progressively as the feature develops
   - Save to project's `/docs` or `.claude/docs` directory

## Template Selection Guide

**Use simplified template when:**
- Documenting a small, self-contained feature
- Creating quick reference documentation
- Time is limited and basic coverage is sufficient
- The feature has minimal dependencies

**Use comprehensive template when:**
- Documenting complex features with multiple components
- Creating specifications for features spanning multiple systems
- Documentation will be referenced by multiple team members
- The feature has significant architectural implications
- Risk assessment and testing strategies are needed

## Key Principles

- Write for developers who may not have context on the codebase
- Focus on the "why" as much as the "what"
- Include concrete examples and test scenarios
- Keep documentation as living documents—update as features evolve
- Use clear, straightforward language without unnecessary jargon
