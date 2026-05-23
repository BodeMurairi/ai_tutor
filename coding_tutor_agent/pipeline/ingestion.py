#!/usr/bin/env python3

from pathlib import Path
from haystack import Pipeline
from haystack.components.converters import HTMLToDocument, MarkdownToDocument

DOCS_PATH = Path(__file__).parent.parent / "documents"


def convert_html_documents() -> list:
    """Load and convert Python HTML docs to Haystack Documents with metadata."""
    html_converter = HTMLToDocument()
    python_path = DOCS_PATH / "python"

    all_docs = []
    for subfolder in ["tutorial", "reference", "library"]:
        sources = list((python_path / subfolder).glob("**/*.html"))
        if not sources:
            continue
        result = html_converter.run(sources=sources)
        for doc in result["documents"]:
            doc.meta["language"] = "python"
            doc.meta["source"] = "python-official-documentation"
            doc.meta["topic"] = Path(doc.meta.get("file_path", "")).stem
        all_docs.extend(result["documents"])

    return all_docs


def convert_markdown_documents() -> tuple[list, list]:
    """Load and convert JavaScript and Dart markdown docs to Haystack Documents with metadata."""
    converter = MarkdownToDocument()

    js_sources = list((DOCS_PATH / "javascript").glob("**/*.md"))
    dart_sources = list((DOCS_PATH / "dart").glob("**/*.md"))

    js_result = converter.run(sources=js_sources)
    for doc in js_result["documents"]:
        doc.meta["language"] = "javascript"
        doc.meta["source"] = "mdn-official-documentation"
        doc.meta["topic"] = Path(doc.meta.get("file_path", "")).stem

    dart_result = converter.run(sources=dart_sources)
    for doc in dart_result["documents"]:
        doc.meta["language"] = "dart"
        doc.meta["source"] = "dart-official-documentation"
        doc.meta["topic"] = Path(doc.meta.get("file_path", "")).stem

    return js_result["documents"], dart_result["documents"]

if __name__ == "__main__":
    print(convert_html_documents())
    print("____________________________________________")
    print(convert_markdown_documents())
