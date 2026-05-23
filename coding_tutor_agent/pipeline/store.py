#!/usr/bin/env python3

import logging
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore

from .doc_embedder import py_embedding, js_dart_embedding

logger = logging.getLogger(__name__)

document_store = QdrantDocumentStore(
    url="http://localhost:6333",
    index="coding_tutor",
    embedding_dim=3072,
    recreate_index=False,
)


def populate_store() -> None:
    """Embed all documents and write them into Qdrant. Skips if already populated."""
    if document_store.count_documents() > 0:
        logger.info(f"Qdrant already has {document_store.count_documents()} docs — skipping embedding.")
        return

    logger.info("Embedding Python docs...")
    py_docs = py_embedding()
    document_store.write_documents(documents=py_docs)

    logger.info("Embedding JavaScript and Dart docs...")
    js_docs, dart_docs = js_dart_embedding()
    document_store.write_documents(documents=js_docs)
    document_store.write_documents(documents=dart_docs)

    logger.info(f"Done — {document_store.count_documents()} chunks written to Qdrant.")


if __name__ == "__main__":
    populate_store()
    print(f"Store populated — total documents: {document_store.count_documents()}")
