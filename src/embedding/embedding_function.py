# src/embedding/embedding_function.py

from google.genai import types, errors
from google.api_core import retry
from typing import List, Dict, Any

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

    @staticmethod
    def name() -> str:
        """ChromaDB embedding function protocol: unique name for serialization."""
        return "gemini_embedding"

    def get_config(self) -> Dict[str, Any]:
        """ChromaDB embedding function protocol: serializable config."""
        return {"document_mode": self.document_mode}

    @staticmethod
    def build_from_config(config: Dict[str, Any]) -> "EmbeddingFunction":
        """ChromaDB embedding function protocol: rebuild from saved config."""
        return EmbeddingFunction(document_mode=config.get("document_mode", True))

    def _embed_batch(self, batch: List[str], embedding_task: str) -> List[List[float]]:
        """Embed a single batch with automatic retry on 429/503."""
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=batch,
            config=types.EmbedContentConfig(task_type=embedding_task),
        )
        return [e.values for e in response.embeddings]

    def __call__(self, input: List[str]) -> List[List[float]]:
        import time
        embeddings = []
        batch_size = 100
        embedding_task = "retrieval_document" if self.document_mode else "retrieval_query"

        for i in range(0, len(input), batch_size):
            batch = input[i:i + batch_size]
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    result = self._embed_batch(batch, embedding_task)
                    embeddings.extend(result)
                    break
                except errors.APIError as e:
                    if getattr(e, 'code', None) in {429, 503} and attempt < max_retries - 1:
                        wait = 2 ** attempt * 5
                        logger.warning(f"Rate limited on batch {i}-{i + len(batch)}, retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait)
                    else:
                        logger.error(f"Embedding failed on batch {i}-{i + len(batch)}: {e}")
                        raise
                except Exception as e:
                    logger.error(f"Embedding failed on batch {i}-{i + len(batch)}: {e}")
                    raise

            if i + batch_size < len(input):
                time.sleep(1)

        return embeddings


