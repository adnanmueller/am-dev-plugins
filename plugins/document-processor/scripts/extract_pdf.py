#!/usr/bin/env python3
"""
Extract text and metadata from PDF files.

Usage:
    python extract_pdf.py --file document.pdf
    python extract_pdf.py --file scanned.pdf --ocr
    python extract_pdf.py --file large.pdf --split 50
    python extract_pdf.py --file document.pdf --metadata-only
    python extract_pdf.py --file document.pdf --json

Features:
- Text extraction using pypdf (pure Python) or pdftotext (if available)
- OCR fallback for scanned/image PDFs (requires pytesseract)
- Page-by-page extraction with page numbers
- Metadata extraction (title, author, creation date, page count)
- Split large PDFs into chunks by page range
- JSON output mode for programmatic use
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class PDFMetadata:
    """PDF document metadata."""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    page_count: int = 0
    file_size_bytes: int = 0
    file_size_human: str = ""


@dataclass
class PageContent:
    """Content from a single PDF page."""
    page_number: int
    text: str
    char_count: int


@dataclass
class ExtractionResult:
    """Complete extraction result."""
    success: bool
    file_path: str
    metadata: PDFMetadata
    pages: list
    total_chars: int
    extraction_method: str
    error: Optional[str] = None


def format_file_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def format_pdf_date(date_str: str) -> Optional[str]:
    """Parse PDF date format (D:YYYYMMDDHHmmSS) to ISO format."""
    if not date_str:
        return None
    try:
        # Remove D: prefix if present
        if date_str.startswith("D:"):
            date_str = date_str[2:]
        # Parse basic format YYYYMMDDHHMMSS
        if len(date_str) >= 14:
            dt = datetime.strptime(date_str[:14], "%Y%m%d%H%M%S")
            return dt.isoformat()
        elif len(date_str) >= 8:
            dt = datetime.strptime(date_str[:8], "%Y%m%d")
            return dt.isoformat()
    except (ValueError, TypeError):
        pass
    return date_str


def check_pdftotext() -> bool:
    """Check if pdftotext is available."""
    return shutil.which("pdftotext") is not None


def check_tesseract() -> bool:
    """Check if tesseract OCR is available."""
    return shutil.which("tesseract") is not None


def extract_with_pypdf(file_path: str) -> ExtractionResult:
    """Extract PDF content using pypdf library."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="pypdf",
            error="pypdf not installed. Run: pip install pypdf"
        )

    try:
        reader = PdfReader(file_path)
        file_stat = os.stat(file_path)

        # Extract metadata
        info = reader.metadata or {}
        metadata = PDFMetadata(
            title=info.get("/Title") or info.get("Title"),
            author=info.get("/Author") or info.get("Author"),
            subject=info.get("/Subject") or info.get("Subject"),
            creator=info.get("/Creator") or info.get("Creator"),
            producer=info.get("/Producer") or info.get("Producer"),
            creation_date=format_pdf_date(str(info.get("/CreationDate", ""))),
            modification_date=format_pdf_date(str(info.get("/ModDate", ""))),
            page_count=len(reader.pages),
            file_size_bytes=file_stat.st_size,
            file_size_human=format_file_size(file_stat.st_size)
        )

        # Extract text page by page
        pages = []
        total_chars = 0
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            char_count = len(text)
            total_chars += char_count
            pages.append(PageContent(
                page_number=i,
                text=text.strip(),
                char_count=char_count
            ))

        return ExtractionResult(
            success=True,
            file_path=file_path,
            metadata=metadata,
            pages=pages,
            total_chars=total_chars,
            extraction_method="pypdf"
        )

    except Exception as e:
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="pypdf",
            error=str(e)
        )


def extract_with_pdftotext(file_path: str) -> ExtractionResult:
    """Extract PDF content using pdftotext command."""
    if not check_pdftotext():
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="pdftotext",
            error="pdftotext not installed. Run: brew install poppler"
        )

    try:
        # Get page count first
        result = subprocess.run(
            ["pdfinfo", file_path],
            capture_output=True,
            text=True
        )
        page_count = 0
        for line in result.stdout.split("\n"):
            if line.startswith("Pages:"):
                page_count = int(line.split(":")[1].strip())
                break

        file_stat = os.stat(file_path)
        metadata = PDFMetadata(
            page_count=page_count,
            file_size_bytes=file_stat.st_size,
            file_size_human=format_file_size(file_stat.st_size)
        )

        # Extract text page by page
        pages = []
        total_chars = 0
        for page_num in range(1, page_count + 1):
            result = subprocess.run(
                ["pdftotext", "-f", str(page_num), "-l", str(page_num), file_path, "-"],
                capture_output=True,
                text=True
            )
            text = result.stdout.strip()
            char_count = len(text)
            total_chars += char_count
            pages.append(PageContent(
                page_number=page_num,
                text=text,
                char_count=char_count
            ))

        return ExtractionResult(
            success=True,
            file_path=file_path,
            metadata=metadata,
            pages=pages,
            total_chars=total_chars,
            extraction_method="pdftotext"
        )

    except Exception as e:
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="pdftotext",
            error=str(e)
        )


def extract_with_ocr(file_path: str) -> ExtractionResult:
    """Extract PDF content using OCR (for scanned documents)."""
    if not check_tesseract():
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="ocr",
            error="tesseract not installed. Run: brew install tesseract"
        )

    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError as e:
        missing = str(e).split("'")[1] if "'" in str(e) else "pdf2image/pytesseract"
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="ocr",
            error=f"{missing} not installed. Run: pip install pdf2image pytesseract Pillow"
        )

    try:
        # Convert PDF to images
        images = convert_from_path(file_path)
        file_stat = os.stat(file_path)

        metadata = PDFMetadata(
            page_count=len(images),
            file_size_bytes=file_stat.st_size,
            file_size_human=format_file_size(file_stat.st_size)
        )

        # OCR each page
        pages = []
        total_chars = 0
        for i, image in enumerate(images, 1):
            text = pytesseract.image_to_string(image)
            char_count = len(text)
            total_chars += char_count
            pages.append(PageContent(
                page_number=i,
                text=text.strip(),
                char_count=char_count
            ))

        return ExtractionResult(
            success=True,
            file_path=file_path,
            metadata=metadata,
            pages=pages,
            total_chars=total_chars,
            extraction_method="ocr"
        )

    except Exception as e:
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="ocr",
            error=str(e)
        )


def extract_metadata_only(file_path: str) -> ExtractionResult:
    """Extract only metadata without page content."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        file_stat = os.stat(file_path)

        info = reader.metadata or {}
        metadata = PDFMetadata(
            title=info.get("/Title") or info.get("Title"),
            author=info.get("/Author") or info.get("Author"),
            subject=info.get("/Subject") or info.get("Subject"),
            creator=info.get("/Creator") or info.get("Creator"),
            producer=info.get("/Producer") or info.get("Producer"),
            creation_date=format_pdf_date(str(info.get("/CreationDate", ""))),
            modification_date=format_pdf_date(str(info.get("/ModDate", ""))),
            page_count=len(reader.pages),
            file_size_bytes=file_stat.st_size,
            file_size_human=format_file_size(file_stat.st_size)
        )

        return ExtractionResult(
            success=True,
            file_path=file_path,
            metadata=metadata,
            pages=[],
            total_chars=0,
            extraction_method="metadata-only"
        )

    except ImportError:
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="metadata-only",
            error="pypdf not installed. Run: pip install pypdf"
        )
    except Exception as e:
        return ExtractionResult(
            success=False,
            file_path=file_path,
            metadata=PDFMetadata(),
            pages=[],
            total_chars=0,
            extraction_method="metadata-only",
            error=str(e)
        )


def split_pages(result: ExtractionResult, chunk_size: int) -> list:
    """Split extraction result into chunks of pages."""
    chunks = []
    for i in range(0, len(result.pages), chunk_size):
        chunk_pages = result.pages[i:i + chunk_size]
        start_page = chunk_pages[0].page_number
        end_page = chunk_pages[-1].page_number
        chunk_chars = sum(p.char_count for p in chunk_pages)

        chunks.append({
            "chunk_number": len(chunks) + 1,
            "page_range": f"{start_page}-{end_page}",
            "start_page": start_page,
            "end_page": end_page,
            "page_count": len(chunk_pages),
            "char_count": chunk_chars,
            "pages": [asdict(p) for p in chunk_pages]
        })

    return chunks


def format_human_output(result: ExtractionResult, split_size: Optional[int] = None) -> str:
    """Format extraction result for human reading."""
    lines = [
        "=" * 60,
        "PDF EXTRACTION REPORT",
        "=" * 60,
        "",
        f"File: {result.file_path}",
        f"Status: {'SUCCESS' if result.success else 'FAILED'}",
        f"Method: {result.extraction_method}",
    ]

    if result.error:
        lines.append(f"Error: {result.error}")
        return "\n".join(lines)

    # Metadata section
    lines.extend([
        "",
        "METADATA",
        "-" * 40
    ])

    meta = result.metadata
    if meta.title:
        lines.append(f"Title: {meta.title}")
    if meta.author:
        lines.append(f"Author: {meta.author}")
    if meta.subject:
        lines.append(f"Subject: {meta.subject}")
    if meta.creation_date:
        lines.append(f"Created: {meta.creation_date}")
    lines.extend([
        f"Pages: {meta.page_count}",
        f"Size: {meta.file_size_human}",
        f"Total Characters: {result.total_chars:,}"
    ])

    # Content section
    if result.pages:
        lines.extend([
            "",
            "CONTENT",
            "-" * 40
        ])

        if split_size:
            chunks = split_pages(result, split_size)
            for chunk in chunks:
                lines.extend([
                    "",
                    f"=== CHUNK {chunk['chunk_number']}: Pages {chunk['page_range']} ({chunk['char_count']:,} chars) ===",
                    ""
                ])
                for page in chunk["pages"]:
                    lines.extend([
                        f"--- Page {page['page_number']} ---",
                        page["text"],
                        ""
                    ])
        else:
            for page in result.pages:
                lines.extend([
                    f"--- Page {page.page_number} ({page.char_count:,} chars) ---",
                    page.text,
                    ""
                ])

    lines.append("=" * 60)
    return "\n".join(lines)


def format_json_output(result: ExtractionResult, split_size: Optional[int] = None) -> str:
    """Format extraction result as JSON."""
    output = {
        "success": result.success,
        "file_path": result.file_path,
        "extraction_method": result.extraction_method,
        "metadata": asdict(result.metadata),
        "total_chars": result.total_chars
    }

    if result.error:
        output["error"] = result.error
    elif result.pages:
        if split_size:
            output["chunks"] = split_pages(result, split_size)
        else:
            output["pages"] = [asdict(p) for p in result.pages]

    return json.dumps(output, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Extract text and metadata from PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_pdf.py --file document.pdf
  python extract_pdf.py --file scanned.pdf --ocr
  python extract_pdf.py --file large.pdf --split 50
  python extract_pdf.py --file document.pdf --metadata-only
  python extract_pdf.py --file document.pdf --json

Extraction Methods:
  Default: Uses pypdf (pure Python, always available)
  --use-pdftotext: Uses pdftotext (better quality, requires poppler)
  --ocr: Uses tesseract OCR (for scanned documents)
        """
    )

    parser.add_argument("--file", "-f", required=True, help="PDF file to extract")
    parser.add_argument("--ocr", action="store_true", help="Use OCR for scanned documents")
    parser.add_argument("--use-pdftotext", action="store_true", help="Use pdftotext instead of pypdf")
    parser.add_argument("--split", "-s", type=int, metavar="N", help="Split output into chunks of N pages")
    parser.add_argument("--metadata-only", "-m", action="store_true", help="Extract only metadata")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--page", "-p", type=int, help="Extract only specific page number")
    parser.add_argument("--pages", type=str, help="Extract page range (e.g., 1-10 or 1,3,5)")

    args = parser.parse_args()

    # Validate file exists
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Choose extraction method
    if args.metadata_only:
        result = extract_metadata_only(args.file)
    elif args.ocr:
        result = extract_with_ocr(args.file)
    elif args.use_pdftotext:
        result = extract_with_pdftotext(args.file)
    else:
        # Default: try pypdf first
        result = extract_with_pypdf(args.file)
        # If pypdf extracted very little text, suggest OCR
        if result.success and result.total_chars < 100 and result.metadata.page_count > 0:
            avg_chars = result.total_chars / result.metadata.page_count
            if avg_chars < 50:
                print("Note: Very little text extracted. This may be a scanned PDF.", file=sys.stderr)
                print("Try: python extract_pdf.py --file {} --ocr".format(args.file), file=sys.stderr)

    # Filter to specific pages if requested
    if result.success and result.pages:
        if args.page:
            result.pages = [p for p in result.pages if p.page_number == args.page]
            result.total_chars = sum(p.char_count for p in result.pages)
        elif args.pages:
            # Parse page range (e.g., "1-10" or "1,3,5")
            page_nums = set()
            for part in args.pages.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    page_nums.update(range(start, end + 1))
                else:
                    page_nums.add(int(part))
            result.pages = [p for p in result.pages if p.page_number in page_nums]
            result.total_chars = sum(p.char_count for p in result.pages)

    # Format and output
    if args.json:
        print(format_json_output(result, args.split))
    else:
        print(format_human_output(result, args.split))

    # Exit code
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
