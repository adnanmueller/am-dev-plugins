# Document Processing Guide

This guide covers advanced usage patterns and integration strategies for the document-processor plugin.

## Understanding PDF Structure

### Text-Based vs Image-Based PDFs

**Text-based PDFs** contain actual text characters that can be selected and copied. These extract quickly and accurately with `pypdf` or `pdftotext`.

**Image-based PDFs** (scanned documents) contain images of text. These require OCR (Optical Character Recognition) to extract text, which is slower and less accurate.

To determine PDF type:
1. Open in a PDF viewer
2. Try to select text
3. If you can't select individual words, it's image-based

### Extraction Quality Hierarchy

1. **pdftotext** (poppler) - Best quality for complex layouts
2. **pypdf** - Good for simple layouts, pure Python
3. **OCR** - Required for scanned documents

## Advanced PDF Extraction

### Handling Multi-Column Layouts

PDFs with columns may extract with jumbled text. Try:

```bash
# pdftotext handles columns better
python scripts/extract_pdf.py --file columned.pdf --use-pdftotext
```

If still problematic, process specific page ranges and manually reorder.

### Extracting Tables from PDFs

The extraction scripts extract table text but don't preserve structure. For structured table extraction:

1. Extract the text
2. Identify table boundaries manually
3. Use Claude to reformat into proper tables

### Password-Protected PDFs

Neither `pypdf` nor `pdftotext` can handle encrypted PDFs without the password. Options:

1. Remove protection using the PDF owner password
2. Use a tool like `qpdf` to decrypt: `qpdf --password=secret --decrypt input.pdf output.pdf`

## Advanced DOCX Processing

### Preserving Complex Formatting

The markdown conversion handles:
- Headings (H1-H6)
- Bold, italic, underline, strikethrough
- Bullet and numbered lists
- Tables with proper alignment
- Block quotes

It does NOT preserve:
- Font faces and sizes
- Colors
- Custom styles
- Complex positioning

### Handling Tracked Changes

The current extraction shows the final document state. Tracked changes (insertions/deletions) are not visible in the output.

### Working with Templates

DOCX templates with form fields extract the field values, not the field definitions. For template analysis, inspect the raw XML:

```bash
unzip document.docx -d extracted/
cat extracted/word/document.xml | xmllint --format -
```

## Integration Patterns

### Obsidian Vault Processing

For batch processing an Obsidian vault's attachments:

```bash
# Find all PDFs in attachments
find ~/obsidian-vault/attachments -name "*.pdf" -size +5M

# Process each large PDF
for pdf in ~/obsidian-vault/attachments/*.pdf; do
  if [ $(stat -f%z "$pdf") -gt 5242880 ]; then
    python scripts/extract_pdf.py --file "$pdf" --json > "${pdf%.pdf}.extracted.json"
  fi
done
```

### Note Link Resolution

When processing notes with wiki-links like `[[Document Name.pdf]]`:

1. Resolve the link to the actual file path
2. Check the attachments folder (commonly `attachments/` or `assets/`)
3. Process the resolved file

### Chunked Processing for Context Limits

For very large documents that need summarization:

```bash
# Extract in 25-page chunks
python scripts/extract_pdf.py --file massive.pdf --split 25 --json > chunks.json
```

Then process each chunk separately:
1. Summarize chunk 1
2. Summarize chunk 2
3. ...
4. Synthesize all chunk summaries into a final summary

## Performance Optimization

### Parallel Processing

For batch jobs, process files in parallel:

```bash
# Using GNU parallel
find . -name "*.pdf" | parallel -j 4 python scripts/extract_pdf.py --file {} --json ">" {.}.json
```

### Caching Extracted Content

Store extracted text alongside originals to avoid re-processing:

```
attachments/
├── document.pdf
├── document.pdf.extracted.txt
├── report.docx
└── report.docx.extracted.md
```

Check modification times before re-extracting:

```bash
# Only extract if PDF is newer than extracted text
if [ document.pdf -nt document.pdf.extracted.txt ]; then
  python scripts/extract_pdf.py --file document.pdf > document.pdf.extracted.txt
fi
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `pypdf not installed` | Missing dependency | `pip install pypdf` |
| `python-docx not installed` | Missing dependency | `pip install python-docx` |
| `tesseract not installed` | Missing OCR engine | `brew install tesseract` |
| `pdf2image.exceptions.PDFInfoNotInstalledError` | Missing poppler | `brew install poppler` |
| `PdfReadError: EOF marker not found` | Corrupted PDF | Try opening in PDF viewer first |
| `BadZipFile: File is not a zip file` | Not a valid DOCX | Verify file format |

### Graceful Degradation

The scripts attempt multiple extraction methods:

1. Try primary method (pypdf for PDF, python-docx for DOCX)
2. If minimal text extracted, suggest alternatives
3. Provide clear error messages with install instructions

## Output Format Reference

### PDF JSON Schema

```json
{
  "success": true,
  "file_path": "/path/to/document.pdf",
  "extraction_method": "pypdf",
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "creation_date": "2024-01-15T10:30:00",
    "page_count": 25,
    "file_size_bytes": 1048576,
    "file_size_human": "1.0 MB"
  },
  "total_chars": 50000,
  "pages": [
    {
      "page_number": 1,
      "text": "Page content here...",
      "char_count": 2000
    }
  ]
}
```

### DOCX JSON Schema

```json
{
  "success": true,
  "file_path": "/path/to/document.docx",
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "created": "2024-01-15T10:30:00",
    "modified": "2024-01-20T14:00:00",
    "paragraph_count": 50,
    "table_count": 3,
    "image_count": 5,
    "word_count": 2500,
    "char_count": 15000
  },
  "content": "Extracted text or markdown here...",
  "images": [
    {
      "filename": "image_1.png",
      "original_name": "image1.png",
      "content_type": "image/png",
      "size_bytes": 50000,
      "saved_path": "./extracted_images/image_1.png"
    }
  ]
}
```

## Security Considerations

### Malicious Documents

PDFs and DOCX files can contain:
- Embedded JavaScript (PDFs)
- Macros (DOCX)
- External links

The extraction scripts only extract text content and do not execute any embedded code. However, be cautious when:
- Opening extracted content in applications that might execute scripts
- Following links extracted from documents

### Sensitive Content

Extracted text may contain sensitive information. Consider:
- Where extraction output is stored
- Who has access to extracted files
- Whether extracted content should be encrypted
