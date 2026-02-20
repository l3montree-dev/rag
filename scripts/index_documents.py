from app.ingestion.reader import read_docs
from app.ingestion.chunking import chunking
from app.ingestion.embedding import get_embeddings
from app.clients import get_db_connection

# read, chunk and embed the docs
docs = read_docs()
chunks = chunking(docs)
embeddings = get_embeddings(chunks)

conn = get_db_connection()
cur = conn.cursor()

# put embeddings into db
for chunk, embedding in zip(chunks, embeddings):
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (chunk, embedding)
    )

conn.commit()
cur.close()
conn.close()
