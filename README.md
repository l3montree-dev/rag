# RAG Demo
This project implements a minimal Retrieval-Augmented Generation (RAG) pipeline using Mistral AI, PostgreSQL with pgvector, and Flask.

## Architecture

The system follows a simple RAG pipeline:

1. Markdown documents are loaded and chunked.
2. Chunks are embedded using Mistral embeddings.
3. Embeddings are stored in PostgreSQL with pgvector.
4. At query time:
   - The query is embedded.
   - Top-k similar chunks are retrieved.
   - The LLM generates an answer using the retrieved context.


## Environment Variables

Create a `.env` file in the project root:

```env
API_KEY=your_api_key
DOCS_PATH=/path/to/your/markdown/files
DB_USER=user
DB_PASSWORD=password
```

## Virtual Environment Setup
Set up the venv and load the necessary requirements to run the project:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
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

## Index Documents

Before running queries, you must index your documents:

```bash
python scripts/index_documents.py
``` 

## Run the API Server

From the project root to start the API Server:

```bash
python run.py
```

# A/B Testing Evaluation
This project includes an A/B evaluation interface to compare different RAG configurations (e.g. chunk size, temperature, top-k retrieval).

The system:

- Generates answers for multiple configurations
- Creates all unique pairwise comparisons per question
- Stores comparisons in PostgreSQL
- Allows human evaluators to vote
- Stores votes for later Bradley–Terry / Gaussian Process analysis

## Database Setup for A/B Testing
Run the following commands after connecting to PostgreSQL.
```sql
CREATE TABLE IF NOT EXISTS ab_pairs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    config_a TEXT NOT NULL,
    config_b TEXT NOT NULL,
    answered BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ab_results (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    config_a TEXT NOT NULL,
    config_b TEXT NOT NULL,
    winner TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Generate Evaluation Data
You must first generate responses for all configurations. This can be done with ```generate_data.ipynb```

Example expected format (data.json):
```json
[
  {
    "config": "config_1",
    "results": [
      {
        "question": "How can I search for license risks?",
        "answer": "..."
      }
    ]
  }
]
```

Place this file in the project root.

## Start the A/B Testing Server
Run:
```bash
python3 -m app.api.testing_server
```
Then open:
```
http://127.0.0.1:5000/
```

## How the A/B System works
- All unique config pairs are generated per question
- Each comparison is shown exactly once
- Votes are stored in ```ab_results```
- Pairs are marked as answered in ```ab_pairs```
- When all comparisons are complete, the interface stops

For 5 configs and 5 questions:
- 10 comparisons per question
- 50 total comparisons
