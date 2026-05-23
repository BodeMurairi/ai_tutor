#!/usr/bin/env python3

from google.adk.tools.tool_context import ToolContext

from ..pipeline.retrieval import search_docs as retrieval_search
from ..pipeline.store import document_store


async def search_docs(query: str, tool_context: ToolContext) -> str:
    """
    Search the official programming documentation for content relevant to the user's question.
    Call this tool before answering any technical question so your response is grounded in
    accurate documentation. Pass the core concept or topic as the query.

    Args:
        query: The programming concept, function, or topic to look up (e.g. "list comprehensions",
               "async await", "class inheritance")
        tool_context: ADK tool context (injected automatically — do not pass this)

    Returns:
        Relevant documentation excerpts to use as context in your answer.
    """
    if document_store.count_documents() == 0:
        return "Documentation is still loading in the background. Please ask again in a moment."

    language = tool_context.state.get("current_language")
    results = retrieval_search(query=query, language=language)

    if not results:
        return "No relevant documentation found for this query."

    parts = []
    for i, doc in enumerate(results, 1):
        topic = doc["meta"].get("topic", "unknown")
        snippet = (doc["content"] or "")[:600].strip()
        parts.append(f"[{i}] {topic}\n{snippet}")

    return "\n\n---\n\n".join(parts)
