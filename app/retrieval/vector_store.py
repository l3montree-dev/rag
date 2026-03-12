from app.clients import get_db_connection
from app.ingestion.embedding import text_embedding

def retrieve_top_k(query: str, k: int = 5):
    """Retrieve the top k most similar documents to the given query.

    This function computes the embedding for the query, queries the vector database
    for documents ordered by cosine similarity, and returns the top k results."""
    embedding = text_embedding(query)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT content,
               1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """, (embedding, embedding, k))

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
