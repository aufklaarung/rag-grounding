# rag_answer_grounding

## Name
**RAG Question & Answer with Grounding**

## Description
### Proof of Concept

We aim to build a system capable of answering user questions based on a set of documents. These documents may contain redundancy or conflicting information about a given subject (e.g., specific examples that do not generalize well, doubtful statements, etc.). In current business use cases, LLMs are often used to summarize or answer questions about lengthy documents, but users tend to take these answers at face value without verifying their accuracy — which can lead to overconfidence and the propagation of misinformation. Our system is designed to address this issue explicitly by encouraging clarification, avoiding hallucinations, and surfacing ambiguity when needed.

The system should:
- Provide an answer **only when the information is clear and unambiguous**,
- Otherwise, **ask follow-up questions** to help the user refine their query and narrow down the possible interpretations.

To achieve this, the system will leverage:

- **Embeddings** (e.g., via Vertex AI or open-source models) to encode both the documents and user queries into a vector space;
- **RAG (Retrieval-Augmented Generation)** to retrieve the most relevant content and enhance the LLM prompt accordingly;
- **ReAct (Reasoning + Acting)** or **Chain-of-Thought (CoT)** prompting to enable the system to reason about ambiguous queries and guide the user;
- Optionally, **a ranking mechanism or document filtering layer** to prioritize reliable and generalizable content over noisy or anecdotal passages.
