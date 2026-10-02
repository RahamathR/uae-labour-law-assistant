"""Health check for source PDFs: page count, text layer, and a text sample."""
from pathlib import Path

import pymupdf

RAW_DIR = Path("data/raw")
MIN_CHARS = 50  # pages with fewer characters are probably scanned or blank

for pdf_path in sorted(RAW_DIR.glob("*.pdf")):
    with pymupdf.open(pdf_path) as doc:
        chars_per_page = [len(page.get_text().strip()) for page in doc]
        low_text_pages = [i + 1 for i, n in enumerate(chars_per_page) if n < MIN_CHARS]

        print(f"\n=== {pdf_path.name} ===")
        print(f"Pages: {doc.page_count}")
        print(f"Total characters: {sum(chars_per_page):,}")
        print(f"Pages with little/no text: {low_text_pages or 'none'}")
        print("Sample from page 2:")
        print(doc[1].get_text()[:300] if doc.page_count > 1 else "(single page)")