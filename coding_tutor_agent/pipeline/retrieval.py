#!/usr/bin/env python3

from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever

from .store import document_store
from .text_embedder import embed_query

embedding_retriever = QdrantEmbeddingRetriever(document_store=document_store, top_k=5)


def search_docs(query: str, language: str | None = None) -> list[dict]:
    """
    Dense retrieval from Qdrant. Filters by language when provided.
    Returns a list of dicts with 'content' and 'meta' keys.
    """
    filters = {"field": "meta.language", "operator": "==", "value": language} if language else None

    query_embedding = embed_query(query)

    results = embedding_retriever.run(
        query_embedding=query_embedding,
        filters=filters,
    )

    return [
        {"content": doc.content, "meta": doc.meta}
        for doc in results["documents"]
    ]


if __name__ == "__main__":
    from .store import populate_store
    populate_store()

    results = search_docs("how do list comprehensions work", language="python")
    print(f"Retrieved {len(results)} documents\n")
    for r in results:
        print(f"[{r['meta']['topic']}] {r['content'][:200]}")
        print("-" * 60)
