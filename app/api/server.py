from flask import Flask, request, jsonify
from app.retrieval.vector_store import retrieve_top_k
from app.generation.response import generate_response

app = Flask(__name__)

@app.post("/query")
def query():
    q = request.json["query"]
    context = retrieve_top_k(q, k=5)
    answer = generate_response(q, context)
    return jsonify({"answer": answer})
