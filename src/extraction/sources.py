from typing import List, Dict, Optional
from src.clients.storage_client import read_file_from_gcs, storage_client
from bs4 import BeautifulSoup
import re
import os

import requests

import logging

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": "RagGroundingBot/1.0 (educational project; BeautifulSoup scraper)"
}


def extract_paragraphs_from_url(url: str, max_paragraphs: int = None) -> List[Dict]:
    """Extracts paragraphs from a Wikipedia page."""
    response = requests.get(url, headers=_HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    docs = []
    for i, p in enumerate(paragraphs):
        if max_paragraphs is not None and i >= max_paragraphs:
            break
        text = p.get_text()  # on garde tous les espaces
        text = text.replace('\xa0', ' ')  # on remplace les espaces insécables par des espaces normaux
        text = ' '.join(text.split())  # on normalise les espaces (supprime les doublons)
        if text:
            docs.append({
                "text": text,
                "metadata" : {
                    "source": "url",
                    "url": url,
                    "chunk_id": i
                }
            })
    return docs

def extract_paragraphs_from_wikipedia(url: str, max_paragraphs: int = None) -> List[Dict]:
    """Extract paragraphs from a Wikipedia page with section titles."""
    response = requests.get(url, headers=_HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", class_="mw-parser-output")
    if not content:
        return []

    current_section = "Introduction"
    docs = []
    count = 0

    # This will walk all content in order: h2, p, h3, p, etc.
    for element in content.find_all(["h2", "h3", "h4", "p"]):
        logger.info(f"Extracting {current_section} from {url}")
        if element.name in ["h2", "h3", "h4"]:
            # Clean up title: remove '[edit]' or span elements
            current_section = element.get_text().replace("[edit]", "").strip()
        elif element.name == "p":
            text = element.get_text().replace('\xa0', ' ')
            text = ' '.join(text.split())
            if text:
                docs.append({
                    "text": text,
                    "metadata" : {
                        "source": "wikipedia",
                        "url": url,
                        "section": current_section,
                        "chunk_id": count
                    }
                })
                count += 1
                if max_paragraphs is not None and count >= max_paragraphs:
                    break

    return docs

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
                            max_docs: Optional[int] = None) -> List[Dict]:
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
                continue

            full_text = "\n".join(paragraphs).strip()
            if not full_text:
                continue

            documents.append({
                "text": full_text,
                "metadata" : {
                    "source": "gcs",
                    "chunk_id": count,
                    "file": os.path.basename(blob.name),
                    "lang": "zh" if suffix == ".html" else "unknown",
                    "type": suffix
                }
            })
            count += 1

        except Exception as e:
            logger.warning(f"Failed to extract {blob.name}: {e}")
            continue

    return documents



def extract_documents(source: str, **kwargs) -> List[Dict]:
    """
    Unified function to extract documents from various sources.
    Currently supports: wikipedia, gcs_html
    """
    if source == "url":
        return extract_paragraphs_from_url(kwargs["url"], kwargs.get("max_paragraphs", None))
    elif source == "wikipedia":
        return extract_paragraphs_from_wikipedia(kwargs["url"], kwargs.get("max_paragraphs", None))
    elif source == "gcs":
        return extract_from_gcs(
            bucket_name=kwargs["bucket_name"],
            prefix=kwargs.get("prefix"),
            suffix=kwargs.get("suffix"),
            max_docs=kwargs.get("max_docs", None)
        )
    else:
        raise ValueError(f"Unsupported source type: {source}")
