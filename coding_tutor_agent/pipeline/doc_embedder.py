#!/usr/bin/env python3

import dataclasses
import os
from dotenv import load_dotenv
from typing import Any

from google import genai
from google.genai import types
from haystack import Document, component

from .splitter_doc import py_splitter, js_dart_splitter

load_dotenv()


@component
class GeminiDocumentEmbedder:
    """Haystack component that embeds documents using Google gemini-embedding-2."""

    def __init__(self, model: str = "models/gemini-embedding-2", task_type: str = "RETRIEVAL_DOCUMENT"):
        self.model = model
        self.task_type = task_type
        self.client = None

    def warm_up(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    @component.output_types(documents=list[Document])
    def run(self, documents: list[Document]) -> dict[str, Any]:
        if self.client is None:
            self.warm_up()

        config = types.EmbedContentConfig(task_type=self.task_type)

        embedded: list[Document] = []
        for doc in documents:
            response = self.client.models.embed_content(
                model=self.model,
                contents=doc.content or "",
                config=config,
            )
            embedded.append(dataclasses.replace(doc, embedding=response.embeddings[0].values))

        return {"documents": embedded}


embedder = GeminiDocumentEmbedder()


def py_embedding() -> list:
    """Embed Python doc chunks into dense vectors"""
    result = embedder.run(documents=py_splitter())
    return result["documents"]


def js_dart_embedding() -> tuple[list, list]:
    """Embed JS and Dart doc chunks into dense vectors"""
    js_chunks, dart_chunks = js_dart_splitter()
    js_result = embedder.run(documents=js_chunks)
    dart_result = embedder.run(documents=dart_chunks)
    return js_result["documents"], dart_result["documents"]


if __name__ == "__main__":
    py_docs = py_embedding()
    print(f"Total Python embedded chunks: {len(py_docs)}")
    print(f"Embedding dimension: {len(py_docs[0].embedding)}")
    for doc in py_docs[:2]:
        print(doc.meta)
        print(f"  embedding[:5] = {doc.embedding[:5]}")
        print("-" * 50)
