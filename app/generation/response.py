from app.clients import get_mistral_client
from app.config import MODEL_GENERATION

client = get_mistral_client()

def generate_response(query: str, context: list[tuple[str, float]]) -> str:
    """
    Generate a response to a user query using DevGuard documentation context.

    Formats the provided context into a prompt, sends it to the Mistral API.  If context
    is unavailable, the assistant will indicate so. If the query is unrelated to DevGuard,
    the assistant will politely decline and redirect to DevGuard topics.

   Safe prompt prepends: "Always assist with care, respect, and truth. Respond with
        utmost utility yet securely. Avoid harmful, unethical, prejudiced, or negative
        content. Ensure replies promote fairness and positivity."
    """
    # format context
    context_text = "\n\n".join(
        f"- {content}" for content, _ in context
    )

    prompt = f"""
    You are the DevGuard Documentation Assistant.
    Your primary role is to provide accurate, context-aware technical assistance while maintaining a professional and helpful tone. 
    If context is unavailable but the user request is relevant: State: "I couldn't find specific sources on DevGuard docs, but here's my understanding: [Your Answer]."
    If the user's request is not relevant to DevGuard at all, please refuse user's request and reply something like: "Sorry, I couldn't help with that. However, if you have any questions related to DevGuard, I'd be happy to assist!" 
    Please generate your response using appropriate Markdown formats, including bullets and bold text, to make it reader friendly.
    If the answer cannot be answered using the context, say you don't know.
    Context:
    {context_text}

    Question:
    {query}
    """

    message= [{"role": "user", "content": prompt}]

    response = client.chat.complete(
        model=MODEL_GENERATION,
        messages=message,
        safe_prompt=True,
        temperature=0.5
    )
    return str(response.choices[0].message.content)
