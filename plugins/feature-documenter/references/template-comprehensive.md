# Comprehensive Feature Documentation Template

Use this template for detailed feature specifications and complex features.

---

# Feature Documentation: [Feature Name]

## Status
[Planning | In Progress | Testing | Complete | Deprecated]

## Links & References
**Feature Requirements:** [Link to requirements doc/issue if available]  
**Task/Ticket:** [Link to GitHub issue, Trello card, etc. if available]  
**Related Files:**
- [List key files this feature touches]
- [Configuration files]
- [Test files]

## Problem Statement
[What specific problem does this solve? What wasn't working before? Keep this focused and clear.]

## Solution Overview
[Describe what you're building in straightforward terms. What does the user see/experience? What happens behind the scenes?]

## Architecture Integration

**Where this fits in the overall app:**
[How does this connect to existing systems? What layer of the app does this live in? Frontend, backend, database, API, etc.]

**Data flow:**
[How information moves through this feature—from user input to final output]

## Core Components

### [Component/Function Name 1]
**Purpose:** [What this piece does]  
**Input:** [What it receives]  
**Output:** [What it produces]  
**Location:** [File path or module name]

### [Component/Function Name 2]
**Purpose:** [What this piece does]  
**Input:** [What it receives]  
**Output:** [What it produces]  
**Location:** [File path or module name]

### [Additional components as needed]

## Implementation Details

**Dependencies:**
- [External libraries/packages needed]
- [Internal modules this depends on]
- [APIs or services required]

**Key Configuration:**
- [Environment variables]
- [Config file settings]
- [Feature flags or toggles]

**Database Changes:**
[New tables, columns, migrations needed—or "None" if not applicable]

## Testing Approach

**How to test this feature:**
- [Manual testing steps]
- [Automated tests to write]
- [Edge cases to verify]

**Test data needed:**
[What kind of data/scenarios to test with]

## Known Issues & Future Improvements

**Current limitations:**
- [What doesn't work perfectly yet]
- [Performance bottlenecks]
- [Incomplete functionality]

**Edge cases to handle:**
- [Unusual inputs or scenarios]
- [Error conditions]
- [Boundary conditions]

**Planned improvements:**
- [Features to add later]
- [Optimisations to make]
- [Technical debt to address]

## Risks & Considerations

**Technical risks:**
- [What could break]
- [Dependencies that might cause issues]
- [Performance concerns]

**User impact:**
- [How this affects existing users]
- [Breaking changes]
- [Learning curve]

## Documentation & Resources

**Related documentation:**
- [Links to API docs]
- [User guides]
- [Other feature docs that connect to this]

**External references:**
- [Tutorials or examples used]
- [Stack Overflow solutions]
- [Library documentation]

---
**Created:** [Date] by [Name]  
**Last Updated:** [Date] by [Name]  
**Review Date:** [When to revisit this]
