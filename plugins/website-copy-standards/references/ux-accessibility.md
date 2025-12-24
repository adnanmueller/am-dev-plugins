# UX Writing & Accessibility Reference

Microcopy, accessibility standards, voice search, and Zero UI.

## Table of Contents
1. [Microcopy Principles](#microcopy)
2. [Error Messages](#error-messages)
3. [POUR Framework](#pour-framework)
4. [Alt Text Guidelines](#alt-text)
5. [Link Text](#link-text)
6. [Heading Hierarchy](#headings)
7. [Dark Mode](#dark-mode)
8. [Zero UI & Voice](#zero-ui)
9. [Voice Search Optimisation](#voice-search)
10. [Local Intent](#local-intent)

---

## Microcopy

Microcopy guides users through digital products. Buttons, labels, tooltips.

### Action-Oriented Language

| Weak | Strong |
|------|--------|
| "Submit" | "Get My Free Guide" |
| "Click Here" | "Start Your Free Trial" |
| "OK" | "Save Changes" |
| "Next" | "Continue to Payment" |

### Principles

1. **Clarity over cleverness:** Describe the action outcome
2. **Conciseness:** Mobile-first demands brevity
3. **Specificity:** "Download 2025 Report" not "Download"
4. **Reduce hesitation:** Button text should eliminate uncertainty

### Agentic AI Compatibility

Clear labels help AI agents navigate interfaces:
- Bad: "Let's Go!" (ambiguous)
- Good: "Complete Purchase" (explicit action)

---

## Error Messages

Error messages should explain what went wrong AND how to fix it.

### Structure

```
[What happened] + [How to fix it] + [Optional: empathy]
```

### Examples

| Bad | Good |
|-----|------|
| "Error 404" | "We couldn't find that page. Check the URL or head back to the homepage." |
| "Invalid input" | "We couldn't quite catch that. Please check the format and try again." |
| "Failed" | "The file was too large. Try one under 10MB." |

### Tone

- Acknowledge frustration
- Avoid blaming user
- Offer clear next step
- Brand personality can diffuse tension

---

## POUR Framework

WCAG 2.2 accessibility: Perceivable, Operable, Understandable, Robust.

### Perceivable
- All content available to screen readers
- Alt text for images
- Captions for video
- Sufficient colour contrast

### Operable
- Keyboard navigable
- Skip links for main content
- No time limits (or adjustable)
- Focus indicators visible

### Understandable
- Clear language (Grade 8 reading level)
- Consistent navigation
- Predictable interactions
- Error prevention and recovery

### Robust
- Valid HTML
- ARIA labels where needed
- Works across assistive technologies

---

## Alt Text

Describe content AND function for screen readers.

### Guidelines

1. **Be specific:** Not "image" but "Photo of product dashboard"
2. **Include function:** "Submit button with arrow icon"
3. **Context matters:** What would user miss without it?
4. **Skip decorative:** Use empty alt="" for decorative images
5. **No "image of":** Screen readers already announce it's an image

### Examples

| Bad | Good |
|-----|------|
| "logo.png" | "Acme Corp logo" |
| "Chart" | "Bar chart showing 40% revenue increase Q3 2024" |
| "Man" | "Customer using mobile app to track delivery" |

---

## Link Text

Screen reader users navigate by jumping between links. Generic text loses context.

### Rules

- Links must describe destination
- Never: "Click here", "Read more", "Here", "Link"
- Always: "Read our 2025 SEO Guide", "Download the pricing PDF"

### Examples

| Bad | Good |
|-----|------|
| "For more information, click here" | "Read our complete accessibility guide" |
| "Learn more" | "Learn more about pricing plans" |
| "See details" | "See service package details" |

---

## Headings

Proper H1-H6 hierarchy enables assistive technology navigation.

### Rules

1. Single H1 per page
2. Sequential levels (H1 → H2 → H3, never skip)
3. Headings describe content below
4. Don't use headings for styling (use CSS)

### Document Outline

```
H1: Page Title
  H2: First Major Section
    H3: Subsection
    H3: Subsection
  H2: Second Major Section
    H3: Subsection
```

---

## Dark Mode

Dark mode affects text perception and user state.

### Halation Effect

White text on black appears to "bleed" or look bolder.

**Fix:** Use off-white (#F5F5F5) on dark grey (#1A1A1A), not pure white on black.

### Tone Considerations

Dark mode often used in low-light/evening environments.
- Consider "quieter" microcopy
- Avoid aggressive ALL CAPS
- Softer urgency language

---

## Zero UI

Interfaces controlled by voice, gesture, or ambient sensors. No screen.

### Writing for Zero UI

Without visual cues, copy IS the interaction.

**Visual UI:** Green checkmark = success
**Zero UI:** "Okay, I've added that to your list."

### Principles

1. Confirm actions verbally
2. Anticipate user intent precisely
3. Provide feedback through audio/haptic
4. Keep responses concise but complete

---

## Voice Search

Voice queries are longer and more conversational than text.

### Query Differences

| Text Search | Voice Search |
|-------------|--------------|
| "weather NY" | "What is the weather like in New York today?" |
| "best pizza near me" | "Where can I find the best pizza near me?" |

### Optimisation

1. **Use question H2s:** Match spoken queries
2. **Concise answers:** ~30 words immediately after heading
3. **FAQ sections:** Natural Q&A format
4. **Simple grammar:** Subject-verb-object
5. **Grade 8 reading level:** TTS clarity

### TTS Readability

For text-to-speech:
- Avoid complex sentences with multiple clauses
- No parentheses in core answers
- No semicolons in answer sentences
- Clear pronunciation (spell out acronyms first use)

---

## Local Intent

Large portion of voice searches are local ("near me").

### Google Business Profile

Your GBP description = as important as website copy.

**Optimise for:**
- Clear service + location: "Emergency Plumber in Sydney"
- Not vague: "Premier Plumbing Solutions"

### Local Signals

- City/suburb in key content
- Local phone number
- Address in footer
- LocalBusiness schema markup
