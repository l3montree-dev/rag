import random
from itertools import combinations
from flask import Flask, render_template, request, redirect
from app.clients import get_db_connection
import json
import os

app = Flask(__name__)

# load the data from the json file
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# flatten into question/config/answer structure
pairs : list[dict]= []
for config_block in raw_data:
    config_id = config_block["config"]
    for result in config_block["results"]:
        pairs.append({
            "question": result["question"],
            "config": config_id,
            "answer": result["answer"]
        })

# get unique questions and configs for preparing the pairs in the db
questions : list[str] = list(set(p["question"] for p in pairs))
configs : list[str] = list(set(p["config"] for p in pairs))

# prepare all unique pairs of configs for each question and insert into db if not already there
def prepare_pairs():
    conn = get_db_connection()
    cur = conn.cursor()
    # insert unique pairs of configs for each question into the ab_pairs table (if they don't already exist)
    for question in questions:
        # filter pairs for the current question
        configs_for_question = [p for p in pairs if p["question"] == question]
        for a, b in combinations(configs_for_question, 2):
            cur.execute("""
                INSERT INTO ab_pairs (question, config_a, config_b)
                SELECT %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM ab_pairs
                    WHERE question=%s AND config_a=%s AND config_b=%s
                )
            """, (
                question, a["config"], b["config"],
                question, a["config"], b["config"]
            ))
    conn.commit()
    cur.close()
    conn.close()


# get the next unanswered pair from the db, along with the corresponding answers, and randomize left/right
def get_next_pair() -> tuple[int, str, dict, dict] | None:
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, question, config_a, config_b
        FROM ab_pairs
        WHERE answered = FALSE
        ORDER BY RANDOM()
        LIMIT 1
    """)

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    pair_id, question, config_a, config_b = row

    # get answers
    answer_a = next(p["answer"] for p in pairs
                    if p["question"] == question and p["config"] == config_a)

    answer_b = next(p["answer"] for p in pairs
                    if p["question"] == question and p["config"] == config_b)

    # randomize left/right
    if random.random() > 0.5:
        left = {"config": config_a, "answer": answer_a}
        right = {"config": config_b, "answer": answer_b}
    else:
        left = {"config": config_b, "answer": answer_b}
        right = {"config": config_a, "answer": answer_a}

    return pair_id, question, left, right


@app.route("/")
def index():
    pair = get_next_pair()

    if not pair:
        return "<h2>All comparisons completed! Thank you :)</h2>"

    pair_id, question, a, b = pair

    return render_template(
        "ab_evaluation.html",
        pair_id=pair_id,
        question=question,
        a=a,
        b=b
    )


@app.route("/vote", methods=["POST"])
def vote():
    pair_id = request.form["pair_id"]
    winner = request.form["winner"]

    conn = get_db_connection()
    cur = conn.cursor()

    # get original pair info
    cur.execute("""
        SELECT question, config_a, config_b
        FROM ab_pairs
        WHERE id = %s
    """, (pair_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return redirect("/")
    question, config_a, config_b = row

    # save vote
    cur.execute("""
        INSERT INTO ab_results (question, config_a, config_b, winner)
        VALUES (%s, %s, %s, %s)
    """, (question, config_a, config_b, winner))

    # mark pair as answered
    cur.execute("""
        UPDATE ab_pairs
        SET answered = TRUE
        WHERE id = %s
    """, (pair_id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    prepare_pairs()
    app.run(host="0.0.0.0", port=5000, debug=True)