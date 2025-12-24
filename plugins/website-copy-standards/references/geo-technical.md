# GEO Technical Reference

Generative Engine Optimisation (GEO) for AI Answer Engines and search visibility.

## Table of Contents
1. [Information Synthesis vs Retrieval](#information-synthesis)
2. [RAG Implications](#rag-implications)
3. [Information Gain](#information-gain)
4. [Entity-Based SEO](#entity-based-seo)
5. [Semantic HTML5](#semantic-html5)
6. [Answer-First Structure](#answer-first-structure)
7. [Schema Markup](#schema-markup)
8. [Visual Search Optimisation](#visual-search)

---

## Information Synthesis

**Old Model (IR):** User searches → Engine returns URLs → User reads multiple sources
**New Model (GEO):** User asks → Engine reads sources → Engine synthesises answer

**Implication:** Goal is not ranking but *citation*. Content must contribute facts the AI uses.

---

## RAG Implications

Retrieval-Augmented Generation (RAG) process:
1. AI receives query
2. Retrieves relevant "context chunks" from web
3. Generates answer from chunks

**Writing for RAG:**
- Structure content in discrete, standalone blocks
- Use clear definitions that can be extracted
- Provide direct answers to questions
- Use structured lists for easy "grabbing"

---

## Information Gain

AI models calculate probabilistic value of text. Repeated information = low value.

**High-value content includes:**
- Original statistics ("Our 2025 tests show 14% increase...")
- Proprietary case studies
- Expert quotes with attribution
- Unique data points not found elsewhere
- First-hand experience markers ("In our testing...")

**Avoid:** Rehashing top-ranking results (copycat content is penalised)

---

## Entity-Based SEO

Search engines use Knowledge Graph: entities (things) with attributes and relationships.

### From Keywords to Entities

| Keyword SEO | Entity SEO |
|-------------|-----------|
| Exact match strings | Concepts, things, places |
| Keyword density | Contextual richness |
| Target phrases | Topic clusters |
| Bot-focused | LLM + human focused |

### Implementation

1. **Disambiguation:** Define primary entity in opening paragraphs
   - Bad: "Learn about Java" (coffee? island? language?)
   - Good: "Java is a compiled programming language..."

2. **Attribute Enrichment:** Explicitly state entity attributes
   - Dimensions, materials, origins, compatibility
   - Enables AI comparison tables

3. **Consistency:** Maintain identical naming across domain
   - Same brand/product name on About page, blogs, footer
   - Creates single authoritative Knowledge Graph node

4. **Topic Clusters:** Pillar pages linked to cluster pages
   - Pillar: "Retirement Planning" (broad entity)
   - Clusters: "401(k) Limits", "Roth IRA Rules", "Social Security"
   - Use contextual link text defining relationships

---

## Semantic HTML5

HTML structure signals content hierarchy to AI parsers.

### Required Elements

```html
<article>    <!-- Main content container -->
<section>    <!-- Thematic grouping -->
<aside>      <!-- Tangential content (tells AI: context, not main answer) -->
<header>     <!-- Demarcates boilerplate from content -->
<footer>     <!-- Demarcates boilerplate from content -->
<nav>        <!-- Navigation (excluded from main content parsing) -->
```

### Heading Hierarchy

- **H1:** Exactly one per page. Contains primary keyword/entity.
- **H2/H3:** Act as retrieval hooks. Use questions for voice search.
  - Bad: "Introduction"
  - Good: "What is Entity SEO?"
- **Never skip levels:** H1 → H2 → H3 (not H1 → H3)

### Tables for Data

Data in HTML tables is significantly easier for LLMs to parse than prose.
Use `<table>` for: pricing, features, specs, comparisons.

---

## Answer-First Structure

Inverted Pyramid: Most important information at top.

### The Answer Block Method

```html
<h2>How does Schema Markup affect SEO?</h2>  <!-- Trigger -->
<p>Schema markup increases visibility by 40% by...</p>  <!-- Answer: 40-60 words -->
<p>This works because AI models...</p>  <!-- Context/nuance -->
```

**Rules:**
- Question in H2 tag
- Concise direct answer immediately following (40-60 words)
- Definitional, fact-dense first paragraph
- Supporting detail after

---

## Schema Markup

JSON-LD structured data in `<head>` provides explicit machine-readable labels.

### EnvokeAI 8 Priority Fields

Fields prioritised by LLMs for entity understanding:

1. `name` - Clear entity denomination
2. `description` - Concise summary
3. `url` - Canonical location
4. `image` - Visual representation
5. `sameAs` - Authority links (Wikipedia, Wikidata, socials)
6. `datePublished` / `dateModified` - Freshness
7. `author` / `creator` - E-E-A-T signal
8. `mainEntityOfPage` - Primary topic signal

### Critical Schema Types

**FAQPage** - Most potent for GEO. Hand-feeds Q&A pairs to AI.
```json
{"@type": "FAQPage", "mainEntity": [{"@type": "Question"...}]}
```

**Article/BlogPosting** - Links content to Author (Person) and Publisher (Organization)

**Organization** - Controls brand understanding: logo, socials, founders, contact

**Speakable** - Identifies sections for text-to-speech (voice assistants)

### Knowledge Graph Connection

Use properties to map content to known entities:
- `mentions` - Links to other entities discussed
- `about` - Defines subject matter
- Link to Wikidata entries for disambiguation

---

## Visual Search

Multimodal search requires optimised images.

### Image Optimisation

1. **Descriptive filenames:** `nike-air-max-2025-red-side-view.jpg`
2. **Alt text:** Describe content AND function
3. **Contextual placement:** Image near relevant text
4. **High resolution:** Clear subject for object recognition

### Image Schema

```json
{
  "@type": "ImageObject",
  "contentUrl": "...",
  "license": "...",
  "acquireLicensePage": "...",
  "creditText": "..."
}
```

### Video Optimisation

- Always provide full text transcript
- Define chapters with timestamps (Key Moments)
- Use VideoObject schema
