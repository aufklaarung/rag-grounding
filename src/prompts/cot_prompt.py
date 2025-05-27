
def build_prompt(question: str, passages_with_metadata: list, history: list) -> str:
    prompt = """You are a helpful and grounded assistant. 
    Your job is to answer the user’s question — or summarize the content — using **only** the reference passages provided below.
    
    - Always base your response strictly on the given passages. Do **not** make assumptions or invent information.
    - Quote or paraphrase exact phrases when possible, and always reference the section or file it came from.
    - At the end of your response, list the source and the reference where each piece of information was sourced.
    - If the same idea appears in multiple sections, mention all of them.
    - If information is unclear, contradictory, or missing, make sure to acknowledge that and ask for clarification rather than guessing.

    Let’s begin by analyzing the reference content carefully before crafting a thoughtful, grounded response.
    """

    question_oneline = question.replace('\n', ' ')

    for i, (q, r) in enumerate(history):
        prompt += f"\nPREVIOUS QUESTION {i + 1}: {q}"
        prompt += f"\nPREVIOUS ANSWER {i + 1}: {r}\n"

    prompt += f"\nQUESTION: {question_oneline}\n"

    for passage in passages_with_metadata:
        meta = passage.get("metadata", {})
        source = meta.get("source", "Unknown Source")
        if source == "gcs":
            ref = meta.get("file", "Unknown File")
        elif source == "wikipedia":
            source = meta.get("url")
            ref = meta.get("section", "Unknown Section")
        prompt += f"\nPassage from source {source} and reference: {ref}):\n{passage['text']}\n"

    return prompt