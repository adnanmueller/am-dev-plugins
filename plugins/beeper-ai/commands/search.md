---
description: Search messages across all connected platforms
argument-hint: <query> [--platform <platform>] [--limit <n>]
---

# /beeper-ai:search

Search messages across all your connected messaging platforms via Beeper.

@../SKILL.md

## Usage

```
/beeper-ai:search <query> [--platform <platform>] [--limit <n>]
```

## Instructions

Run the beeper-ai search command:

```bash
cd /Users/adnanmueller/projects/code/beeper-ai && uv run beeper-ai search "$QUERY" $PLATFORM_FLAG $LIMIT_FLAG
```

Where:
- `$QUERY` is the search text (required)
- `$PLATFORM_FLAG` is `--platform <platform>` if specified
- `$LIMIT_FLAG` is `--limit <n>` if specified

## Example Commands

```bash
# Basic search
uv run beeper-ai search "meeting tomorrow"

# Search WhatsApp only
uv run beeper-ai search "dinner plans" --platform whatsapp

# Get more results
uv run beeper-ai search "project update" --limit 50
```

## Output

Present the search results in a readable format showing:
- Platform name
- Chat/conversation name
- Sender
- Message snippet with highlighted matches
- Date
