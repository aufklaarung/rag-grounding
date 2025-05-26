# src/embedding/embedding_function.py

from google.genai import types, errors
from google.api_core import retry
from typing import List

from src.clients.gemini_client import client

import logging

logger = logging.getLogger(__name__)

class EmbeddingFunction:
    """
    Wrapper class for generating text embeddings using the Gemini embedding model.

    This class allows switching between two modes:
    - 'retrieval_document': optimized for embedding reference documents.
    - 'retrieval_query': optimized for embedding user queries.

    The mode can be toggled using the `document_mode` flag.

    Attributes:
        document_mode (bool): If True, sets the embedding task to 'retrieval_document'.
                              If False, sets it to 'retrieval_query'.

    Methods:
        __call__(input: List[str]) -> List[List[float]]:
            Generates embeddings for a list of input strings using the specified mode.
            Automatically retries on transient errors using the configured retry decorator.
    """
    def __init__(self, document_mode=True):
        self.document_mode = document_mode
        self.client = client

    @retry.Retry(predicate=lambda e: isinstance(e, errors.APIError) and getattr(e, 'code', None) in {429, 503}) #function that identifies error codes
    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = []
        batch_size = 100
        embedding_task = "retrieval_document" if self.document_mode else "retrieval_query"

        for i in range(0, len(input), batch_size):
            try:
                response = self.client.models.embed_content(
                    model="models/embedding-001",
                    contents=input[i:i + batch_size],
                    config=types.EmbedContentConfig(task_type=embedding_task),
                )
                embeddings.extend([e.values for e in response.embeddings])
            except Exception as e:
                logger.warning(f"Embedding failed on batch {i}-{i + len(batch)}: {e}")

        return embeddings


