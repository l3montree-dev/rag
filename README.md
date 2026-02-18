# RAG Demo
This project is a minimal Retrieval-Augmented Generation (RAG) setup using
Mistral AI, PostgreSQL with pgvector, and Jupyter Notebooks.

## Database Initialization

Run the following SQL commands **in order** after connecting to your PostgreSQL database.

---

### 1. Enable the pgvector Extension

This must be done **once per database** before using vector types.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Create the documents table
The embedding dimension must match your embedding model output. 
In this project, embeddings have 1024 dimensions.


```sql
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(1024) NOT NULL
);
```

### 3. Verify Setup
Confirm that the table and vector dimension are correct.

```sql
\d documents;
```
```sql
SELECT vector_dims(embedding) FROM documents LIMIT 1;
```