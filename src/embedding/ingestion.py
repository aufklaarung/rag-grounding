# src/embedding/ingestion.py
from typing import List, Dict
from src.db.collections import get_document_collection

def safe_add_to_chromadb(
        documents: List[Dict],
        collection_name: str):
    """
    Adds documents to ChromaDB safely, assigning unique IDs and using the correct embedding function.
    """
    #We retrieve the collection and associated embedding function
    db = get_document_collection(collection_name)

    #Compute the offset depending on current db size
    offset = len(db.get()["ids"])
    ids = [str(i + offset) for i in range(len(documents))]

    try:
        db.add(
            documents=[doc["text"] for doc in documents],
            ids=ids,
            metadatas=[doc.get("metadata", {}) for doc in documents]
        )
        print(f"Added {len(documents)} documents to collection '{collection_name}' (offset={offset})")
    except Exception as e:
        print(f"Failed to add documents: {e}")
