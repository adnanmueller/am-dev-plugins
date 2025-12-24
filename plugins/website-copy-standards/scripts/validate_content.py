#!/usr/bin/env python3
"""
Validate HTML content for GEO and copywriting standards.

Usage:
    python validate_content.py --file page.html
    python validate_content.py --url https://example.com/page
    python validate_content.py --file page.html --json

Checks:
- Single H1 tag with primary keyword/entity
- Proper H1-H6 hierarchy
- Semantic HTML5 elements
- Schema markup presence
- Answer-first structure
- Readability score (target Grade 8)
- Scannable formatting
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Optional
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.error import URLError


@dataclass
class ValidationResult:
    """Container for validation results."""
    passed: bool
    message: str
    severity: str = "info"  # info, warning, error
    recommendation: str = ""


@dataclass
class ContentReport:
    """Full validation report."""
    overall_score: int = 0
    results: list = field(default_factory=list)

    def add(self, category: str, result: ValidationResult):
        self.results.append({"category": category, **result.__dict__})

    def calculate_score(self):
        """Calculate overall score based on results."""
        total = len(self.results)
        if total == 0:
            return 0
        passed = sum(1 for r in self.results if r["passed"])
        # Weight errors more heavily
        errors = sum(1 for r in self.results if r["severity"] == "error" and not r["passed"])
        self.overall_score = max(0, int((passed / total) * 100) - (errors * 10))
        return self.overall_score


class HTMLContentParser(HTMLParser):
    """Parse HTML to extract structure and content."""

    def __init__(self):
        super().__init__()
        self.headings = []
        self.current_heading = None
        self.heading_text = ""
        self.paragraphs = []
        self.current_paragraph = ""
        self.in_paragraph = False
        self.lists = {"ul": 0, "ol": 0}
        self.semantic_elements = {"article": 0, "section": 0, "aside": 0, "nav": 0, "header": 0, "footer": 0}
        self.bold_count = 0
        self.link_texts = []
        self.current_link_text = ""
        self.in_link = False
        self.has_schema = False
        self.schema_types = []
        self.images_without_alt = 0
        self.images_with_alt = 0
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Check headings
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_heading = tag
            self.heading_text = ""
            if tag == 'h1':
                self.h1_count += 1

        # Check paragraphs
        if tag == 'p':
            self.in_paragraph = True
            self.current_paragraph = ""

        # Check lists
        if tag in ['ul', 'ol']:
            self.lists[tag] += 1

        # Check semantic elements
        if tag in self.semantic_elements:
            self.semantic_elements[tag] += 1

        # Check bold/strong
        if tag in ['strong', 'b']:
            self.bold_count += 1

        # Check links
        if tag == 'a':
            self.in_link = True
            self.current_link_text = ""

        # Check images
        if tag == 'img':
            if attrs_dict.get('alt', '').strip():
                self.images_with_alt += 1
            else:
                self.images_without_alt += 1

        # Check for Schema markup
        if tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            self.has_schema = True

    def handle_endtag(self, tag):
        if tag == self.current_heading:
            self.headings.append((tag, self.heading_text.strip()))
            self.current_heading = None

        if tag == 'p':
            if self.current_paragraph.strip():
                self.paragraphs.append(self.current_paragraph.strip())
            self.in_paragraph = False

        if tag == 'a':
            if self.current_link_text.strip():
                self.link_texts.append(self.current_link_text.strip())
            self.in_link = False

    def handle_data(self, data):
        if self.current_heading:
            self.heading_text += data
        if self.in_paragraph:
            self.current_paragraph += data
        if self.in_link:
            self.current_link_text += data


def calculate_readability(text: str) -> float:
    """Calculate Flesch-Kincaid Grade Level."""
    # Simple implementation
    sentences = len(re.findall(r'[.!?]+', text)) or 1
    words = len(text.split())
    syllables = sum(count_syllables(word) for word in text.split())

    if words == 0:
        return 0

    # Flesch-Kincaid Grade Level
    grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
    return max(0, round(grade, 1))


def count_syllables(word: str) -> int:
    """Count syllables in a word (approximate)."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1

    vowels = "aeiouy"
    count = 0
    prev_is_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel

    # Adjust for silent e
    if word.endswith('e'):
        count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1

    return max(1, count)


def validate_heading_hierarchy(headings: list) -> ValidationResult:
    """Check for proper H1-H6 hierarchy."""
    if not headings:
        return ValidationResult(
            passed=False,
            message="No headings found",
            severity="error",
            recommendation="Add H1 heading with primary keyword/entity"
        )

    levels = [int(h[0][1]) for h in headings]

    # Check for skipped levels
    issues = []
    for i in range(1, len(levels)):
        if levels[i] > levels[i-1] + 1:
            issues.append(f"Skipped from H{levels[i-1]} to H{levels[i]}")

    if issues:
        return ValidationResult(
            passed=False,
            message=f"Heading hierarchy issues: {'; '.join(issues)}",
            severity="warning",
            recommendation="Maintain sequential heading levels (H1 -> H2 -> H3)"
        )

    return ValidationResult(
        passed=True,
        message=f"Heading hierarchy is valid ({len(headings)} headings)"
    )


def validate_h1(parser: HTMLContentParser) -> ValidationResult:
    """Validate single H1 tag."""
    if parser.h1_count == 0:
        return ValidationResult(
            passed=False,
            message="No H1 tag found",
            severity="error",
            recommendation="Add exactly one H1 tag with primary keyword/entity"
        )
    elif parser.h1_count > 1:
        return ValidationResult(
            passed=False,
            message=f"Multiple H1 tags found ({parser.h1_count})",
            severity="error",
            recommendation="Use only one H1 tag per page"
        )
    return ValidationResult(
        passed=True,
        message="Single H1 tag present"
    )


def validate_semantic_html(parser: HTMLContentParser) -> ValidationResult:
    """Check for semantic HTML5 elements."""
    total = sum(parser.semantic_elements.values())
    if total == 0:
        return ValidationResult(
            passed=False,
            message="No semantic HTML5 elements found",
            severity="warning",
            recommendation="Use <article>, <section>, <aside> for better AI parsing"
        )

    present = [k for k, v in parser.semantic_elements.items() if v > 0]
    return ValidationResult(
        passed=True,
        message=f"Semantic elements present: {', '.join(present)}"
    )


def validate_schema(parser: HTMLContentParser) -> ValidationResult:
    """Check for Schema markup."""
    if not parser.has_schema:
        return ValidationResult(
            passed=False,
            message="No JSON-LD Schema markup found",
            severity="warning",
            recommendation="Add FAQPage, Article, or Organization schema for AI visibility"
        )
    return ValidationResult(
        passed=True,
        message="JSON-LD Schema markup present"
    )


def validate_readability(paragraphs: list) -> ValidationResult:
    """Check readability score (target Grade 8)."""
    if not paragraphs:
        return ValidationResult(
            passed=True,
            message="No paragraph text to analyse"
        )

    text = " ".join(paragraphs)
    grade = calculate_readability(text)

    if grade > 12:
        return ValidationResult(
            passed=False,
            message=f"Reading level too high: Grade {grade}",
            severity="warning",
            recommendation="Simplify sentences for Grade 8 target. Use shorter sentences and simpler words."
        )
    elif grade > 8:
        return ValidationResult(
            passed=True,
            message=f"Reading level acceptable: Grade {grade} (target: 8)",
            severity="info",
            recommendation="Consider simplifying for broader accessibility"
        )

    return ValidationResult(
        passed=True,
        message=f"Reading level excellent: Grade {grade}"
    )


def validate_scannable(parser: HTMLContentParser, paragraphs: list) -> ValidationResult:
    """Check for scannable formatting."""
    issues = []

    # Check for lists
    total_lists = parser.lists['ul'] + parser.lists['ol']
    if total_lists == 0:
        issues.append("No bullet/numbered lists")

    # Check for bold text
    if parser.bold_count < 3:
        issues.append("Limited use of bold text for emphasis")

    # Check paragraph length
    long_paragraphs = sum(1 for p in paragraphs if len(p.split()) > 60)
    if long_paragraphs > 0:
        issues.append(f"{long_paragraphs} paragraphs exceed 60 words")

    if issues:
        return ValidationResult(
            passed=len(issues) < 2,
            message=f"Scannability issues: {'; '.join(issues)}",
            severity="warning" if len(issues) < 2 else "error",
            recommendation="Use bullet points, bold key phrases, and shorter paragraphs (73% of users skim)"
        )

    return ValidationResult(
        passed=True,
        message="Content is well-formatted for skimming"
    )


def validate_link_text(parser: HTMLContentParser) -> ValidationResult:
    """Check for descriptive link text."""
    bad_links = ["click here", "read more", "here", "link", "more"]
    found_bad = [lt for lt in parser.link_texts if lt.lower() in bad_links]

    if found_bad:
        return ValidationResult(
            passed=False,
            message=f"Generic link text found: {', '.join(set(found_bad))}",
            severity="warning",
            recommendation="Use descriptive link text for accessibility and SEO (e.g., 'Read our SEO guide')"
        )

    return ValidationResult(
        passed=True,
        message=f"Link text is descriptive ({len(parser.link_texts)} links checked)"
    )


def validate_images(parser: HTMLContentParser) -> ValidationResult:
    """Check for alt text on images."""
    total = parser.images_with_alt + parser.images_without_alt
    if total == 0:
        return ValidationResult(
            passed=True,
            message="No images found"
        )

    if parser.images_without_alt > 0:
        return ValidationResult(
            passed=False,
            message=f"{parser.images_without_alt} of {total} images missing alt text",
            severity="error",
            recommendation="Add descriptive alt text for all images (accessibility + visual search)"
        )

    return ValidationResult(
        passed=True,
        message=f"All {total} images have alt text"
    )


def validate_answer_first(headings: list, paragraphs: list) -> ValidationResult:
    """Check for answer-first structure (question H2 followed by concise answer)."""
    question_headings = [h for h in headings if h[1].strip().endswith('?')]

    if not question_headings:
        return ValidationResult(
            passed=True,
            message="No question-format headings found",
            severity="info",
            recommendation="Consider using question H2s for voice search (e.g., 'What is Entity SEO?')"
        )

    return ValidationResult(
        passed=True,
        message=f"{len(question_headings)} question-format headings found (good for voice search)"
    )


def validate_content(html: str) -> ContentReport:
    """Run all validations on HTML content."""
    report = ContentReport()

    # Parse HTML
    parser = HTMLContentParser()
    try:
        parser.feed(html)
    except Exception as e:
        report.add("Parsing", ValidationResult(
            passed=False,
            message=f"HTML parsing error: {e}",
            severity="error"
        ))
        return report

    # Run validations
    report.add("H1 Tag", validate_h1(parser))
    report.add("Heading Hierarchy", validate_heading_hierarchy(parser.headings))
    report.add("Semantic HTML", validate_semantic_html(parser))
    report.add("Schema Markup", validate_schema(parser))
    report.add("Readability", validate_readability(parser.paragraphs))
    report.add("Scannability", validate_scannable(parser, parser.paragraphs))
    report.add("Link Text", validate_link_text(parser))
    report.add("Image Alt Text", validate_images(parser))
    report.add("Answer-First", validate_answer_first(parser.headings, parser.paragraphs))

    report.calculate_score()
    return report


def format_report(report: ContentReport, as_json: bool = False) -> str:
    """Format validation report for output."""
    if as_json:
        return json.dumps({
            "overall_score": report.overall_score,
            "results": report.results
        }, indent=2)

    lines = [
        "=" * 60,
        f"CONTENT VALIDATION REPORT",
        f"Overall Score: {report.overall_score}/100",
        "=" * 60,
        ""
    ]

    # Group by severity
    errors = [r for r in report.results if r["severity"] == "error" and not r["passed"]]
    warnings = [r for r in report.results if r["severity"] == "warning" and not r["passed"]]
    passed = [r for r in report.results if r["passed"]]

    if errors:
        lines.append("ERRORS (must fix):")
        for r in errors:
            lines.append(f"  [X] {r['category']}: {r['message']}")
            if r.get('recommendation'):
                lines.append(f"      -> {r['recommendation']}")
        lines.append("")

    if warnings:
        lines.append("WARNINGS (should fix):")
        for r in warnings:
            lines.append(f"  [!] {r['category']}: {r['message']}")
            if r.get('recommendation'):
                lines.append(f"      -> {r['recommendation']}")
        lines.append("")

    if passed:
        lines.append("PASSED:")
        for r in passed:
            lines.append(f"  [+] {r['category']}: {r['message']}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate HTML content for GEO and copywriting standards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_content.py --file index.html
  python validate_content.py --url https://example.com/page
  python validate_content.py --file page.html --json > report.json
        """
    )
    parser.add_argument("--file", "-f", help="HTML file to validate")
    parser.add_argument("--url", "-u", help="URL to fetch and validate")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.file and not args.url:
        print("Error: Provide --file or --url", file=sys.stderr)
        sys.exit(1)

    # Get HTML content
    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                html = f.read()
        else:
            with urlopen(args.url, timeout=30) as response:
                html = response.read().decode('utf-8')
    except (FileNotFoundError, URLError) as e:
        print(f"Error loading content: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate
    report = validate_content(html)

    # Output
    print(format_report(report, as_json=args.json))

    # Exit code based on errors
    has_errors = any(r["severity"] == "error" and not r["passed"] for r in report.results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
