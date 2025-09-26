# app.py
from flask import Flask, request, jsonify

import random

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Dice Game</title></head><body>"
        "<h1>🎲 Simple Dice Game</h1>"
        "<p>Try: <code>/roll?count=2&faces=6</code></p>"
        "<button onclick=\"roll()\">Roll 2d6</button>"
        "<pre id='out'></pre>"
        "<script>"
        "async function roll(){"
        "  const r = await fetch('/roll?count=2&faces=6');"
        "  const j = await r.json();"
        "  document.getElementById('out').textContent = JSON.stringify(j, null, 2);"
        "}"
        "</script>"
        "</body></html>"
    )

@app.route("/roll", methods=["GET"])
def roll():
    try:
        count = int(request.args.get("count", 1))
        faces = int(request.args.get("faces", 6))
    except ValueError:
        return jsonify(error="count and faces must be integers"), 400

    # Optional seed for deterministic rolls (useful for tests/demos)
    seed = request.args.get("seed")
    if seed is not None:
        try:
            random.seed(int(seed))
        except ValueError:
            return jsonify(error="seed must be an integer"), 400

    if not (1 <= count <= 20):
        return jsonify(error="count must be between 1 and 20"), 400
    if not (2 <= faces <= 20):
        return jsonify(error="faces must be between 2 and 20"), 400

    rolls = [random.randint(1, faces) for _ in range(count)]
    total = sum(rolls)
    return jsonify(count=count, faces=faces, rolls=rolls, total=total)

if __name__ == "__main__":
    # Bind to all interfaces so port mapping works in Docker
    app.run(host="0.0.0.0", port=5000)