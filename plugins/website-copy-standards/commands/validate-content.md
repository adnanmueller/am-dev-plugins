---
description: Run content validation against GEO/SEO standards
argument-hint: [--file path | --url URL]
allowed-tools: Bash(python:*)
---

# Validate Content

You are executing the `/validate-content` command.

Run the content validator script to check HTML against GEO/copywriting standards.

## Usage

```bash
# Validate local file
python plugins/website-copy-standards/scripts/validate_content.py --file page.html

# Validate URL
python plugins/website-copy-standards/scripts/validate_content.py --url https://example.com

# JSON output
python plugins/website-copy-standards/scripts/validate_content.py --url https://example.com --json
```

## Checks Performed

| Category | Check |
|----------|-------|
| Structure | Single H1 tag with primary entity |
| Structure | Heading hierarchy (no skipped levels) |
| Structure | Semantic HTML elements present |
| SEO | Schema markup (JSON-LD) present |
| Readability | Target Grade 8 reading level |
| Scannability | Short paragraphs, bullet points, bold |
| Accessibility | Descriptive link text (no "click here") |
| Accessibility | Image alt text present |
| GEO | Answer-first structure after question H2s |

## Output

Returns pass/fail for each check with specific recommendations for failures.
