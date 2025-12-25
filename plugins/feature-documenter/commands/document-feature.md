---
description: Document a feature with automatic template selection
argument-hint: [feature-name or file-path]
---

# Document Feature

You are executing the `/document-feature` command.

@../SKILL.md

Follow the workflow above to create feature documentation.

## Arguments

- `$ARGUMENTS` — Feature name or file path to document

If no argument, ask the user what feature they want to document.

## Process

1. **Gather Context**
   - Check `./docs/system-design/` for existing specifications
   - Search for related issues or requirements
   - Explore the codebase for related components

2. **Determine Template**
   - Assess complexity based on:
     - Number of components involved
     - Dependencies on other systems
     - Architectural implications
   - Auto-select simplified or comprehensive template

3. **Create Documentation**
   - Apply selected template
   - Fill in all relevant sections
   - Save to appropriate docs directory

## Output

Feature documentation saved to the project's docs folder, with a summary of what was documented.
