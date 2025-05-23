
def build_prompt(question: str, best_passages: list, history: list) -> str:
    prompt = """You are a helpful and grounded assistant. 
    Your job is to answer the user’s question — or summarize the content — using **only** the reference passages provided below.
    
    - Always base your response strictly on the given passages. Do **not** make assumptions or invent information.
    - Quote or closely paraphrase exact phrases to support your points, and clearly indicate when you're doing so.
    - Start by identifying key ideas or claims found in the passages.
    - If asked a question, explain the relevant information step by step in simple, conversational language.
    - If summarizing, group related points together, simplify complex ideas, and keep the summary concise and accurate.
    - If information is unclear, contradictory, or missing, make sure to acknowledge that and ask for clarification rather than guessing.
    - Ignore any passage that is not directly relevant to the task.
    
    Let’s begin by analyzing the reference content carefully before crafting a thoughtful, grounded response.
    """

    question_oneline = question.replace('\n', ' ')

    for i, (q, r) in enumerate(history):
        prompt += f"\nPREVIOUS QUESTION {i + 1}: {q}"
        prompt += f"\nPREVIOUS ANSWER {i + 1}: {r}\n"

    prompt += f"\nQUESTION: {question_oneline}\n"

    for i, passage in enumerate(best_passages):
        prompt += f"\nPASSAGE {i + 1}:\n{passage}\n"

    return prompt