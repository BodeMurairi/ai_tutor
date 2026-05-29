#!/usr/bin/env python3

from haystack.components.preprocessors import DocumentSplitter

from .ingestion import convert_html_documents, convert_markdown_documents

python_document = convert_html_documents()
javascript, dart = convert_markdown_documents()

# HTML-converted text uses single \n, so word-based splitting works better
html_splitter = DocumentSplitter(split_by="word", split_length=200, split_overlap=20)

# Markdown uses blank lines between paragraphs — passage splitting is appropriate
md_splitter = DocumentSplitter(split_by="passage", split_length=5, split_overlap=1)


def py_splitter() -> list:
    """Python splitter"""
    result = html_splitter.run(documents=python_document)
    return result["documents"]


def js_dart_splitter() -> tuple[list, list]:
    """Dart and JS splitter"""
    js_result = md_splitter.run(documents=javascript)
    dart_result = md_splitter.run(documents=dart)
    return js_result["documents"], dart_result["documents"]


if __name__ == "__main__":
    py_docs = py_splitter()

    print(f"Total Python chunks: {len(py_docs)}")

    for doc in py_docs[:3]:
        print(doc.content[:300])
        print(doc.meta)
        print("-" * 50)
