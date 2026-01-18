---
description: Summarize a conversation
argument-hint: <chat_id> [--limit <n>]
---

# /beeper-ai:summarize

Generate an AI summary of a Beeper conversation.

@../SKILL.md

## Usage

```
/beeper-ai:summarize <chat_id> [--limit <n>]
```

## Instructions

Run the beeper-ai summarize command:

```bash
cd /Users/adnanmueller/projects/code/beeper-ai && uv run beeper-ai summarize "$CHAT_ID" $LIMIT_FLAG
```

Where:
- `$CHAT_ID` is the conversation ID (required)
- `$LIMIT_FLAG` is `--limit <n>` if specified

## Finding Chat IDs

If the user doesn't know the chat ID, help them find it:

1. Search for messages from that conversation:
   ```bash
   uv run beeper-ai search "<person or keyword>" --limit 5
   ```

2. The search results include chat IDs in the output

## Output

Present the summary clearly, including:
- Brief overview of the conversation
- Key topics discussed
- Any decisions or action items mentioned
- The time period covered
