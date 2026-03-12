from app import conversation
from src.extraction.sources import extract_documents
from src.embedding.ingestion import safe_add_to_chromadb
from src.clients.chromadb_client import reset_chromadb
from src.services.conversation import ConversationService
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    collection_name = "relativitydb"

    # Extracting documents
    urls=["https://en.wikipedia.org/wiki/Special_relativity",
          "https://en.wikipedia.org/wiki/Spacetime",
          "https://en.wikipedia.org/wiki/Classical_mechanics",
          "https://en.wikipedia.org/wiki/Annus_mirabilis_papers",
          "https://en.wikipedia.org/wiki/Michelson%E2%80%93Morley_experiment",
          "https://en.wikipedia.org/wiki/Aether_theories",
          "https://en.wikipedia.org/wiki/Lorentz_ether_theory",
          "https://en.wikipedia.org/wiki/Hermann_Minkowski",
          "https://en.wikipedia.org/wiki/Galileo_Galilei",
          "https://en.wikipedia.org/wiki/Principle_of_relativity",
          "https://en.wikipedia.org/wiki/General_relativity",
          "https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation",
          "https://en.wikipedia.org/wiki/Philosophi%C3%A6_Naturalis_Principia_Mathematica",
          "https://en.wikipedia.org/wiki/Gravity",
          "https://en.wikipedia.org/wiki/Albert_Einstein",
          "https://en.wikipedia.org/wiki/Time_dilation",
          "https://en.wikipedia.org/wiki/Length_contraction",
          "https://en.wikipedia.org/wiki/Mass%E2%80%93energy_equivalence",
          "https://en.wikipedia.org/wiki/Equivalence_principle",
          "https://en.wikipedia.org/wiki/Einstein_field_equations",
          "https://en.wikipedia.org/wiki/Schwarzschild_metric",
          "https://en.wikipedia.org/wiki/Gravitational_lens",
          "https://en.wikipedia.org/wiki/Black_hole",
          "https://en.wikipedia.org/wiki/Gravitational_wave",
          "https://en.wikipedia.org/wiki/Lorentz_transformation",
          "https://en.wikipedia.org/wiki/Minkowski_space"
          ]

    documents = []
    for url in urls:
        document = extract_documents(source='wikipedia', url=url)
        documents.extend(document)
    safe_add_to_chromadb(documents, collection_name)


