from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.retrieval.vector_store import retrieve_top_k
from app.generation.response import generate_response

app = Flask(__name__)

# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day"]  #global limit
)

@app.get("/")
def home():
    return render_template("index.html")


@app.post("/query")
@limiter.limit("60 per minute")  # limit LLM calls
def query():
    q = request.json["query"]
    context = retrieve_top_k(q, k=10)
    answer = generate_response(q, context)
    return jsonify({"answer": answer})


# rate limit error response
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded. Please slow down."
    }), 429
