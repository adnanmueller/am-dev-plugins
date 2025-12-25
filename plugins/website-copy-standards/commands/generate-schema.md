---
description: Generate JSON-LD Schema markup for structured data
argument-hint: [type: faqpage|article|organization|product]
allowed-tools: Bash(python:*)
---

# Generate Schema

You are executing the `/generate-schema` command.

Generate JSON-LD Schema markup using the available templates and scripts.

## Arguments

- `$1` — Schema type: faqpage, article, organization, product

## Methods

### Interactive Mode
```bash
python plugins/website-copy-standards/scripts/generate_schema.py --type $1 --interactive
```

### From Data File
```bash
python plugins/website-copy-standards/scripts/generate_schema.py --type $1 --input data.json --output schema.json
```

### Manual Template
Copy and customize from `plugins/website-copy-standards/assets/schema-templates/`

## Supported Types

| Type | Use Case |
|------|----------|
| `faqpage` | FAQ sections, Q&A content |
| `article` | Blog posts, news, how-to guides |
| `organization` | Company info, contact details |
| `product` | E-commerce product pages |

## Output

Valid JSON-LD that can be embedded in the page `<head>` or `<body>`.
