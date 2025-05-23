from typing import List, Optional
from src.clients.storage_client import read_file_from_gcs, storage_client
from bs4 import BeautifulSoup
import re

import requests

import logging

logger = logging.getLogger(__name__)


def extract_paragraphs_from_url(url: str, max_paragraphs: int = 100) -> List[str]:
    """Extracts paragraphs from a Wikipedia page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    docs = []
    for p in paragraphs:
        text = p.get_text()  # on garde tous les espaces
        text = text.replace('\xa0', ' ')  # on remplace les espaces insécables par des espaces normaux
        text = ' '.join(text.split())  # on normalise les espaces (supprime les doublons)
        if text:
            docs.append(text)

    return docs[:max_paragraphs]


def extract_chinese_paragraphs_from_html(html_content: str) -> List[str]:
    """Extracts Chinese paragraphs from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text_elements = soup.find_all(string=True)

    paragraphs = []
    for text in text_elements:
        clean_text = text.strip()
        if clean_text and re.search(r'[\u4e00-\u9fff]', clean_text):
            paragraphs.append(clean_text)
    return paragraphs


def extract_from_gcs(bucket_name: str, suffix: str, prefix: Optional[str] = None,
                            max_docs: Optional[int] = None) -> List[str]:
    """
    Extracts documents from GCS and returns a list of full-text documents.
    Each document is a joined string of paragraphs.
    """
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    documents = []
    count = 0

    for blob in blobs:
        logger.info(f"Extracting {blob.name}")
        if not blob.name.endswith(suffix):
            continue
        if max_docs is not None and count >= max_docs:
            break

        try:
            content = read_file_from_gcs(bucket, blob.name)

            if suffix == ".html":
                paragraphs = extract_chinese_paragraphs_from_html(content)
            elif suffix == ".txt":
                paragraphs = content.splitlines()
            else:
                continue  # skip unsupported

            if paragraphs:
                full_text = "\n".join(paragraphs)
                documents.append(full_text)
                count += 1

        except Exception as e:
            print(f"Erreur avec {blob.name} : {e}")

    return documents


def extract_documents(source: str, **kwargs) -> List[str]:
    """
    Unified function to extract documents from various sources.
    Currently supports: wikipedia, gcs_html
    """
    if source == "url":
        return extract_paragraphs_from_url(kwargs["url"], kwargs.get("max_paragraphs", 100))
    elif source == "gcs":
        return extract_from_gcs(
            bucket_name=kwargs["bucket_name"],
            prefix=kwargs.get("prefix"),
            suffix=kwargs.get("suffix"),
            max_docs=kwargs.get("max_docs")
        )
    else:
        raise ValueError(f"Unsupported source type: {source}")
