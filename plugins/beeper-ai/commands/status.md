---
description: Check Beeper and Fabric service connectivity
---

# /beeper-ai:status

Check the status of Beeper Desktop and Fabric server connections.

@../SKILL.md

## Instructions

Run the beeper-ai status command to verify connectivity:

```bash
cd /Users/adnanmueller/projects/code/beeper-ai && uv run beeper-ai status
```

Report the results to the user, including:
- Beeper Desktop connection status
- Number of connected accounts
- Fabric server status
- Number of available patterns
- Style guide availability

If any service is disconnected, provide troubleshooting hints:
- For Beeper: Ensure Beeper Desktop is running with API enabled (Settings > Developers)
- For Fabric: Start with `fabric --serve --address :8080`
- For missing token: Set BEEPER_ACCESS_TOKEN in .env file
