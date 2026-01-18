---
description: Analyze your sent messages to create a personal style guide
argument-hint: [--platform <platform>] [--export <path>]
---

# /beeper-ai:analyze-style

Analyze your sent messages across all platforms to create a personal communication style guide. This style guide is then used to generate replies that match your natural voice.

@../SKILL.md

## Usage

```
/beeper-ai:analyze-style [--platform <platform>] [--export <path>]
```

## Instructions

Run the beeper-ai analyze-style command:

```bash
cd /Users/adnanmueller/projects/code/beeper-ai && uv run beeper-ai analyze-style $PLATFORM_FLAG $EXPORT_FLAG
```

Where:
- `$PLATFORM_FLAG` is `--platform <platform>` if specified (e.g., whatsapp, telegram)
- `$EXPORT_FLAG` is `--export <path>` if specified

## Requirements

- At least 100 sent messages are needed for accurate analysis
- Beeper Desktop must be running with API enabled
- Fabric server must be running

## Output

Present the analysis results including:

### Style Characteristics
- **Formality Level**: casual, semi-formal, or formal
- **Emoji Usage**: none, minimal, moderate, or frequent
- **Punctuation Style**: minimal, standard, or expressive
- **Average Message Length**: typical character count
- **Question Style**: direct, rhetorical, or leading

### Patterns Detected
- Common phrases you use
- Greeting patterns (how you start messages)
- Sign-off patterns (how you end messages)
- Filler words

### Platform Variations
If analyzing multiple platforms, show differences in style per platform.

## Storage

The style guide is automatically saved to `data/style_guide.json` and will be used by `/beeper-ai:reply` for generating style-matched responses.
