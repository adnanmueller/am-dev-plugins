---
description: Approve a document to pass an approval gate
argument-hint: [document-name]
---

# Approve Pipeline Document

You are executing the `/approve-pipeline` command.

## Arguments

- `$ARGUMENTS` — The document to approve (e.g., "architecture", "requirements", "gate-1")

## Process

1. Identify the document from the argument
2. Verify it exists and is in `review` status
3. Update the document's status to `approved`
4. Update `./project-documentation/_meta/pipeline-status.md`
5. Check for any auto-triggers that should fire
6. Report what's now unblocked

## Special Cases

- `gate-1` or `gate1` — Approve Gate #1 (technical direction)
- `gate-2` or `gate2` — Approve Gate #2 (deployment readiness)
