---
description: Generate a smart reply for a conversation
argument-hint: <chat_id> [--no-style]
---

# /beeper-ai:reply

Generate a contextual reply for a Beeper conversation that matches your communication style.

@../SKILL.md

## Usage

```
/beeper-ai:reply <chat_id> [--no-style]
```

## Instructions

Run the beeper-ai reply command:

```bash
cd /Users/adnanmueller/projects/code/beeper-ai && uv run beeper-ai reply "$CHAT_ID" $STYLE_FLAG
```

Where:
- `$CHAT_ID` is the conversation ID (required)
- `$STYLE_FLAG` is `--no-style` if user wants to skip style matching

## Style Matching

By default, replies are generated to match the user's personal communication style as defined in their style guide. The style guide is created by running `/beeper-ai:analyze-style`.

If no style guide exists, the command will still work but won't apply style matching.

## Output

Present the generated reply and:
1. Show the suggested reply text
2. Ask if the user wants to:
   - Send the reply as-is
   - Refine it (make shorter, friendlier, more formal, etc.)
   - Generate alternative options
   - Cancel

## Sending the Reply

If the user approves, use the Beeper API to send:
```bash
# This is handled by the CLI command with user confirmation
```

**Important**: Always confirm with the user before actually sending any message.
