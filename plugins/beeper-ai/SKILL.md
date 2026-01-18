---
name: beeper-ai
description: |
  AI-powered chat assistant for Beeper Desktop. Use when user asks about:
  - Searching messages across platforms (/beeper-ai:search)
  - Summarizing conversations (/beeper-ai:summarize)
  - Generating replies (/beeper-ai:reply)
  - Analyzing communication style (/beeper-ai:analyze-style)
  - Checking Beeper/Fabric connectivity (/beeper-ai:status)
version: 1.0.0
---

# Beeper Desktop API Knowledge

This skill provides knowledge about the Beeper Desktop API and the beeper-ai integration.

## Beeper Desktop API Overview

Beeper Desktop provides a local REST API for accessing messages across all connected platforms.

### Base URL
```
http://localhost:23373
```

### Authentication
Requires an access token set in the `BEEPER_ACCESS_TOKEN` environment variable.
Get the token from: Beeper Desktop > Settings > Developers

### Key Endpoints

#### Status
```
GET /api/v1/status
```
Check if the API is running.

#### Accounts
```
GET /api/v1/accounts
```
List all connected messaging accounts (bridges).

#### Chats
```
GET /api/v1/accounts/{account_id}/chats
GET /api/v1/chats/{chat_id}
```
List chats for an account or get a specific chat.

#### Messages
```
GET /api/v1/chats/{chat_id}/messages
POST /api/v1/chats/{chat_id}/messages
```
Get or send messages.

## Fabric Integration

beeper-ai uses Fabric for AI features instead of direct Anthropic API calls.

### Fabric Server
```
http://localhost:8080
```

Start with: `fabric --serve --address :8080`

### Key Patterns Used

| Pattern | Use Case |
|---------|----------|
| `summarize` | Conversation summaries |
| `analyze_personality` | Style guide generation |
| `write_essay` | Reply generation |
| `extract_wisdom` | Key insights extraction |
| `improve_writing` | Reply refinement |

### Fabric API
```
POST /chat
{
  "prompts": [{
    "userInput": "...",
    "patternName": "summarize",
    "model": "claude-sonnet-4-20250514"
  }]
}
```

## beeper-ai Package Structure

```
src/beeper_ai/
├── core/
│   ├── config.py          # Settings (pydantic-settings)
│   └── exceptions.py      # Custom exceptions
├── api/
│   ├── client.py          # BeeperClient wrapper
│   └── models.py          # Data models (Account, Chat, Message)
├── fabric/
│   ├── client.py          # FabricClient for AI calls
│   ├── patterns.py        # Pattern definitions
│   └── sessions.py        # Session management
├── ai/
│   ├── assistant.py       # Main ChatAssistant facade
│   ├── style_analyzer.py  # StyleGuide generation
│   ├── summarizer.py      # Conversation summarization
│   └── smart_reply.py     # Reply generation
├── search/
│   ├── engine.py          # SearchEngine
│   └── filters.py         # SearchFilters
└── cli/
    └── main.py            # Click CLI commands
```

## Configuration

Environment variables (set in `.env`):

```bash
BEEPER_ACCESS_TOKEN=xxx
BEEPER_BASE_URL=http://localhost:23373
FABRIC_BASE_URL=http://localhost:8080
FABRIC_DEFAULT_MODEL=claude-sonnet-4-20250514
STYLE_GUIDE_PATH=./data/style_guide.json
MIN_MESSAGES_FOR_ANALYSIS=100
```

## CLI Commands

```bash
beeper-ai status                    # Check connectivity
beeper-ai search "query"            # Search messages
beeper-ai summarize <chat_id>       # Summarize conversation
beeper-ai reply <chat_id>           # Generate reply
beeper-ai analyze-style             # Create style guide
```

## Common Tasks

### Find a Chat ID
1. Search for messages from the person/conversation
2. The chat_id appears in search results

### Generate a Style-Matched Reply
1. Ensure style guide exists (`analyze-style` if needed)
2. Run `reply <chat_id>` - style is applied automatically

### Troubleshooting
- "Connection refused" on Beeper: Ensure Desktop app is running
- "Connection refused" on Fabric: Start with `fabric --serve`
- "Insufficient data": Need more messages for style analysis
