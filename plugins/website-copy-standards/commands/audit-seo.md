---
description: Run SEO/GEO audit on existing content
argument-hint: [file-path or URL]
---

# Audit SEO

You are executing the `/audit-seo` command.

@../SKILL.md

Perform the Audit Workflow defined above.

## Input

- `$ARGUMENTS` — File path or URL to audit

If no argument provided, ask the user for the content to audit.

## Process

1. **Technical Check**
   - H1 count and primary entity presence
   - Heading hierarchy (no skipped levels)
   - Semantic HTML elements (article, section, aside)
   - JSON-LD Schema presence

2. **Content Quality**
   - Answer blocks after question H2s
   - Reading level (target: Grade 8)
   - Sentence rhythm variation
   - Specific vs generic claims

3. **Accessibility**
   - Image alt text
   - Descriptive link text
   - Color contrast considerations

4. **AI Optimization**
   - Entity mapping completeness
   - Answer-first structure
   - Citation-worthiness

## Output

Provide a structured audit report with:
- Score per category
- Specific issues found
- Prioritized recommendations
