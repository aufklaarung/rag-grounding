from src.extraction.sources import extract_documents
from src.embedding.ingestion import  safe_add_to_chromadb
from src.embedding.retriever import  get_best_matches
from src.clients.chromadb_client import reset_chromadb

import logging
from src.clients.chromadb_client import client

if __name__ == "__main__":
    collection_name = "test"
    # 1. Extract documents from various sources
    documents = extract_documents(source="gcs", bucket_name="mwm-cb-workspace",
                                  prefix="tiktok/html/generated/original/", suffix=".html", max_docs=10)
    # 2. Add these documents (embedded) to our vector database
    safe_add_to_chromadb(documents, collection_name)
    # 3 . RAG time
    print(client.get_collection(collection_name).count())
    # results = get_best_matches("Qui est Albert Einstein?", collection_name)