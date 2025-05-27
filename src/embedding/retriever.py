# src/embedding/retriever.py
from typing import List, Tuple
from src.db.collections import get_query_collection

from logging import getLogger

logger = getLogger(__name__)

def get_best_matches(
    query: str,
    collection_name: str,
    threshold: float = 0.60,
    max_results: int = 100
) -> Tuple[List[str], List[str]]:
    """
    Query ChromaDB using a similarity search and filter results above a threshold.
    """
    db = get_query_collection(collection_name)

    result = db.query(query_texts=[query], n_results=max_results)
    documents = result["documents"][0]
    scores = result["distances"][0]
    metadatas = result.get("metadatas", [[]])[0]  # may be empty list if missing

    filtered_docs = []
    filtered_meta = []
    for doc, score, meta in zip(documents, scores, metadatas):
        if score <= (1 - threshold):
            filtered_docs.append(doc)
            filtered_meta.append(meta)
    logger.info(f"🔍 Retrieved {len(filtered_docs)} matches (threshold={threshold})")
    return filtered_docs, filtered_meta