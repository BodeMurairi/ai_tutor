#!/usr/bin/env python3

import dataclasses
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from haystack import component

load_dotenv()


@component
class GeminiTextEmbedder:
    """Haystack component that embeds a query string using Google gemini-embedding-2."""

    def __init__(self, model: str = "models/gemini-embedding-2", task_type: str = "RETRIEVAL_QUERY"):
        self.model = model
        self.task_type = task_type
        self.client = None

    def warm_up(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    @component.output_types(embedding=list[float])
    def run(self, text: str) -> dict[str, Any]:
        if self.client is None:
            self.warm_up()

        config = types.EmbedContentConfig(task_type=self.task_type)
        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=config,
        )
        return {"embedding": response.embeddings[0].values}


query_embedder = GeminiTextEmbedder()


def embed_query(text: str) -> list[float]:
    """Embed a user query into a dense vector."""
    result = query_embedder.run(text=text)
    return result["embedding"]
