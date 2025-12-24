#!/usr/bin/env python3
"""
Generate JSON-LD Schema markup for common types.

Usage:
    python generate_schema.py --type faqpage --input data.json
    python generate_schema.py --type article --interactive
    python generate_schema.py --type organization --output schema.json

Supports: faqpage, article, organization, product
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Any


def get_faqpage_schema(data: dict) -> dict:
    """Generate FAQPage schema from Q&A pairs."""
    questions = data.get("questions", [])
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q.get("question", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": q.get("answer", "")
                }
            }
            for q in questions
        ]
    }


def get_article_schema(data: dict) -> dict:
    """Generate Article schema with EnvokeAI 8 priority fields."""
    return {
        "@context": "https://schema.org",
        "@type": data.get("articleType", "Article"),
        "headline": data.get("headline", ""),
        "name": data.get("name", data.get("headline", "")),
        "description": data.get("description", ""),
        "url": data.get("url", ""),
        "image": data.get("image", ""),
        "datePublished": data.get("datePublished", datetime.now().isoformat()),
        "dateModified": data.get("dateModified", datetime.now().isoformat()),
        "author": {
            "@type": data.get("authorType", "Person"),
            "name": data.get("authorName", ""),
            "url": data.get("authorUrl", "")
        },
        "publisher": {
            "@type": "Organization",
            "name": data.get("publisherName", ""),
            "logo": {
                "@type": "ImageObject",
                "url": data.get("publisherLogo", "")
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": data.get("url", "")
        }
    }


def get_organization_schema(data: dict) -> dict:
    """Generate Organization schema for brand entity."""
    schema = {
        "@context": "https://schema.org",
        "@type": data.get("orgType", "Organization"),
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "url": data.get("url", ""),
        "logo": data.get("logo", ""),
        "image": data.get("image", data.get("logo", "")),
        "sameAs": data.get("sameAs", []),
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": data.get("telephone", ""),
            "contactType": data.get("contactType", "customer service"),
            "email": data.get("email", "")
        }
    }
    if data.get("founders"):
        schema["founder"] = [
            {"@type": "Person", "name": f} for f in data["founders"]
        ]
    if data.get("address"):
        schema["address"] = {
            "@type": "PostalAddress",
            **data["address"]
        }
    return schema


def get_product_schema(data: dict) -> dict:
    """Generate Product schema for e-commerce."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "image": data.get("image", ""),
        "url": data.get("url", ""),
        "sku": data.get("sku", ""),
        "brand": {
            "@type": "Brand",
            "name": data.get("brandName", "")
        },
        "offers": {
            "@type": "Offer",
            "price": data.get("price", ""),
            "priceCurrency": data.get("currency", "AUD"),
            "availability": data.get("availability", "https://schema.org/InStock"),
            "url": data.get("url", "")
        }
    }
    if data.get("aggregateRating"):
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": data["aggregateRating"].get("ratingValue", ""),
            "reviewCount": data["aggregateRating"].get("reviewCount", "")
        }
    return schema


SCHEMA_GENERATORS = {
    "faqpage": get_faqpage_schema,
    "article": get_article_schema,
    "organization": get_organization_schema,
    "product": get_product_schema
}


def interactive_faqpage() -> dict:
    """Collect FAQ data interactively."""
    print("\n=== FAQPage Schema Generator ===")
    questions = []
    while True:
        q = input("\nEnter question (or 'done' to finish): ").strip()
        if q.lower() == 'done':
            break
        a = input("Enter answer: ").strip()
        questions.append({"question": q, "answer": a})
    return {"questions": questions}


def interactive_article() -> dict:
    """Collect Article data interactively."""
    print("\n=== Article Schema Generator ===")
    return {
        "headline": input("Headline: ").strip(),
        "description": input("Description (1-2 sentences): ").strip(),
        "url": input("Article URL: ").strip(),
        "image": input("Featured image URL: ").strip(),
        "authorName": input("Author name: ").strip(),
        "authorUrl": input("Author profile URL: ").strip(),
        "publisherName": input("Publisher/Site name: ").strip(),
        "publisherLogo": input("Publisher logo URL: ").strip(),
        "articleType": input("Article type [Article/BlogPosting/NewsArticle]: ").strip() or "Article"
    }


def interactive_organization() -> dict:
    """Collect Organization data interactively."""
    print("\n=== Organization Schema Generator ===")
    data = {
        "name": input("Organization name: ").strip(),
        "description": input("Description: ").strip(),
        "url": input("Website URL: ").strip(),
        "logo": input("Logo URL: ").strip(),
        "telephone": input("Phone number: ").strip(),
        "email": input("Contact email: ").strip(),
        "orgType": input("Type [Organization/LocalBusiness/Corporation]: ").strip() or "Organization"
    }
    social = input("Social profile URLs (comma-separated): ").strip()
    if social:
        data["sameAs"] = [s.strip() for s in social.split(",")]
    return data


def interactive_product() -> dict:
    """Collect Product data interactively."""
    print("\n=== Product Schema Generator ===")
    return {
        "name": input("Product name: ").strip(),
        "description": input("Description: ").strip(),
        "url": input("Product URL: ").strip(),
        "image": input("Product image URL: ").strip(),
        "sku": input("SKU: ").strip(),
        "brandName": input("Brand name: ").strip(),
        "price": input("Price (number only): ").strip(),
        "currency": input("Currency [AUD]: ").strip() or "AUD"
    }


INTERACTIVE_COLLECTORS = {
    "faqpage": interactive_faqpage,
    "article": interactive_article,
    "organization": interactive_organization,
    "product": interactive_product
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate JSON-LD Schema markup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_schema.py --type faqpage --interactive
  python generate_schema.py --type article --input article_data.json
  python generate_schema.py --type organization --input org.json --output schema.json
        """
    )
    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["faqpage", "article", "organization", "product"],
        help="Schema type to generate"
    )
    parser.add_argument(
        "--input", "-i",
        help="JSON file with input data"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Collect data interactively"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--minify",
        action="store_true",
        help="Output minified JSON"
    )

    args = parser.parse_args()

    # Get input data
    if args.interactive:
        data = INTERACTIVE_COLLECTORS[args.type]()
    elif args.input:
        with open(args.input, 'r') as f:
            data = json.load(f)
    else:
        print("Error: Provide --input file or use --interactive mode", file=sys.stderr)
        sys.exit(1)

    # Generate schema
    schema = SCHEMA_GENERATORS[args.type](data)

    # Output
    indent = None if args.minify else 2
    output = json.dumps(schema, indent=indent, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Schema written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
