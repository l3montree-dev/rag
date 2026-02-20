from app.clients import get_mistral_client
from app.config import MODEL_GENERATION

client = get_mistral_client()

def generate_response(query: str, context: list[tuple[str, float]]) -> str:
    # format context
    context_text = "\n\n".join(
        f"- {content}" for content, _ in context
    )

    prompt = f"""
    Use ONLY the following context to answer the question.
    If the answer cannot be answered using the context, say you don't know.
    Context:
    {context_text}

    Question:
    {query}
    """

    message= [{"role": "user", "content": prompt}]

    """
        Toggling the safe prompt will prepend your messages with the following system prompt:
        Always assist with care, respect, and truth. Respond with utmost utility yet securely. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity.
    """
    response = client.chat.complete(
        model=MODEL_GENERATION,
        messages=message,
        safe_prompt=True,
        temperature=0.0 # no randomness, since we want the same answer for the same question and context
    )
    return str(response.choices[0].message.content)
