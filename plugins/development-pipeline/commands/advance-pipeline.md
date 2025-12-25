---
description: Move to the next phase with dependency validation
---

# Advance Pipeline

You are executing the `/advance-pipeline` command.

@../SKILL.md

1. Determine the current phase from pipeline status
2. Identify the next logical phase(s) that can proceed
3. Validate all dependencies are met (see Dependency Matrix in skill)
4. If blocked, explain what's missing
5. If ready, invoke the appropriate agent

## Dependency Check

Before advancing, verify:
- Required upstream documents are `approved`
- Approval gates (if applicable) are passed
- No blocking items exist
